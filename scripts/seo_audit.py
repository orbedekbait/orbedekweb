#!/usr/bin/env python3
"""Dependency-free technical SEO regression audit for this static site."""

from __future__ import annotations

import json
import re
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse


ROOT = Path(__file__).resolve().parent.parent
BASE_URL = "https://orbedek.co.il/"
NOT_FOUND = "404.html"


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.attrs: dict[str, list[dict[str, str]]] = {}
        self.links: list[str] = []
        self.images: list[dict[str, str]] = []
        self.ids: set[str] = set()
        self.json_ld: list[str] = []
        self._capture: str | None = None
        self._capture_parts: list[str] = []
        self.text: dict[str, list[str]] = {"title": [], "h1": []}

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key: value or "" for key, value in attrs}
        self.attrs.setdefault(tag, []).append(values)
        if values.get("id"):
            self.ids.add(values["id"])
        if tag in {"a", "link"} and values.get("href"):
            self.links.append(values["href"])
        if tag == "img":
            self.images.append(values)
        if tag in {"title", "h1"}:
            self._capture = tag
            self._capture_parts = []
        if tag == "script" and values.get("type", "").lower() == "application/ld+json":
            self._capture = "json_ld"
            self._capture_parts = []

    def handle_endtag(self, tag: str) -> None:
        if self._capture == tag:
            self.text[tag].append(" ".join("".join(self._capture_parts).split()))
            self._capture = None
            self._capture_parts = []
        elif tag == "script" and self._capture == "json_ld":
            self.json_ld.append("".join(self._capture_parts).strip())
            self._capture = None
            self._capture_parts = []

    def handle_data(self, data: str) -> None:
        if self._capture:
            self._capture_parts.append(data)


def parse_page(path: Path) -> PageParser:
    parser = PageParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser


def meta_values(page: PageParser, key: str, value: str) -> list[str]:
    return [
        attrs.get("content", "")
        for attrs in page.attrs.get("meta", [])
        if attrs.get(key, "").lower() == value.lower()
    ]


def link_values(page: PageParser, rel: str) -> list[str]:
    return [
        attrs.get("href", "")
        for attrs in page.attrs.get("link", [])
        if rel in attrs.get("rel", "").lower().split()
    ]


def local_target(raw_url: str) -> tuple[str, str] | None:
    if raw_url.startswith(("mailto:", "tel:", "javascript:", "data:")):
        return None
    parsed = urlparse(raw_url)
    if parsed.scheme and not raw_url.startswith(BASE_URL):
        return None
    if raw_url.startswith(BASE_URL):
        path = unquote(parsed.path.lstrip("/"))
    else:
        path = unquote(parsed.path)
    if path in {"", ".", "./"}:
        path = "index.html"
    return path, unquote(parsed.fragment)


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    html_files = sorted(ROOT.glob("*.html"))
    indexable_files = [path for path in html_files if path.name != NOT_FOUND]
    pages = {path.name: parse_page(path) for path in html_files}

    titles: list[str] = []
    descriptions: list[str] = []
    for path in indexable_files:
        page = pages[path.name]
        title = page.text["title"]
        description = meta_values(page, "name", "description")
        robots = meta_values(page, "name", "robots")
        canonical = link_values(page, "canonical")
        expected_canonical = BASE_URL if path.name == "index.html" else BASE_URL + path.name

        if len(title) != 1 or not title[0]:
            errors.append(f"{path.name}: expected exactly one non-empty title")
        else:
            titles.append(title[0])
        if len(description) != 1 or not description[0]:
            errors.append(f"{path.name}: expected exactly one meta description")
        else:
            descriptions.append(description[0])
        if len(page.text["h1"]) != 1 or not page.text["h1"][0]:
            errors.append(f"{path.name}: expected exactly one non-empty H1")
        if not robots or "noindex" in robots[0].lower() or "index" not in robots[0].lower():
            errors.append(f"{path.name}: page is not explicitly indexable")
        if canonical != [expected_canonical]:
            errors.append(f"{path.name}: canonical must be {expected_canonical}")
        if link_values(page, "describedby") != [BASE_URL + "llms.txt"]:
            errors.append(f"{path.name}: llms.txt discovery link is missing or incorrect")
        html_attrs = page.attrs.get("html", [{}])[0]
        if html_attrs.get("lang") != "he-IL" or html_attrs.get("dir") != "rtl":
            errors.append(f"{path.name}: expected lang=he-IL and dir=rtl")
        for required_property in ("og:title", "og:description", "og:url", "og:image"):
            if not meta_values(page, "property", required_property):
                errors.append(f"{path.name}: missing {required_property}")
        for block_number, block in enumerate(page.json_ld, start=1):
            try:
                json.loads(block)
            except json.JSONDecodeError as exc:
                errors.append(f"{path.name}: invalid JSON-LD block {block_number}: {exc}")

    duplicate_titles = [value for value, count in Counter(titles).items() if count > 1]
    duplicate_descriptions = [value for value, count in Counter(descriptions).items() if count > 1]
    if duplicate_titles:
        errors.append(f"duplicate titles: {duplicate_titles}")
    if duplicate_descriptions:
        errors.append(f"duplicate descriptions: {duplicate_descriptions}")

    not_found = pages[NOT_FOUND]
    not_found_robots = meta_values(not_found, "name", "robots")
    if not not_found_robots or "noindex" not in not_found_robots[0].lower():
        errors.append("404.html: must contain a noindex robots directive")
    if link_values(not_found, "canonical"):
        errors.append("404.html: must not declare a canonical URL")

    for source_name, page in pages.items():
        for image in page.images:
            if "alt" not in image:
                errors.append(f"{source_name}: image is missing an alt attribute")
            for attribute in ("src", "data-src"):
                if image.get(attribute):
                    target = local_target(image[attribute])
                    if target and not (ROOT / target[0]).is_file():
                        errors.append(f"{source_name}: broken image target {image[attribute]}")
        for href in page.links:
            target = local_target(href)
            if not target:
                continue
            target_path, fragment = target
            file_path = ROOT / target_path
            if not file_path.is_file():
                errors.append(f"{source_name}: broken local target {href}")
                continue
            if fragment and file_path.suffix == ".html":
                target_page = pages.get(file_path.name) or parse_page(file_path)
                if fragment not in target_page.ids:
                    errors.append(f"{source_name}: missing fragment target {href}")

    sitemap_root = ET.parse(ROOT / "sitemap.xml").getroot()
    sitemap_namespace = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    sitemap_urls = {node.text or "" for node in sitemap_root.findall("sm:url/sm:loc", sitemap_namespace)}
    expected_urls = {BASE_URL if path.name == "index.html" else BASE_URL + path.name for path in indexable_files}
    if sitemap_urls != expected_urls:
        missing = sorted(expected_urls - sitemap_urls)
        extra = sorted(sitemap_urls - expected_urls)
        errors.append(f"sitemap mismatch; missing={missing}, extra={extra}")
    if BASE_URL + NOT_FOUND in sitemap_urls:
        errors.append("sitemap.xml: 404.html must not be included")

    robots_text = (ROOT / "robots.txt").read_text(encoding="utf-8")
    if "User-agent: *" not in robots_text or "Allow: /" not in robots_text:
        errors.append("robots.txt: expected a global allow rule")
    if f"Sitemap: {BASE_URL}sitemap.xml" not in robots_text:
        errors.append("robots.txt: sitemap directive does not match BASE_URL")

    llms_text = (ROOT / "llms.txt").read_text(encoding="utf-8")
    if not llms_text.startswith("# ") or BASE_URL not in llms_text:
        errors.append("llms.txt: expected a title and canonical site URL")

    if not errors:
        print(f"PASS: {len(indexable_files)} indexable pages match sitemap.xml")
        print("PASS: unique titles, descriptions, canonicals, H1s, robots directives and OG metadata")
        print("PASS: 404 is noindex and excluded from the sitemap")
        print("PASS: internal links, fragments, images and JSON-LD are valid")
        print("PASS: robots.txt and llms.txt are present and internally consistent")
    for warning in warnings:
        print(f"WARN: {warning}")
    for error in errors:
        print(f"FAIL: {error}", file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
