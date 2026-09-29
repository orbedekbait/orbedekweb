#!/usr/bin/env python3
"""Serve the static site locally with Netlify-style extensionless routes."""

from __future__ import annotations

import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parent.parent
LOCAL_REDIRECTS = {
    "/second-hand-home-inspection": "/badek-home-before-buying",
    "/second-hand-home-inspection/": "/badek-home-before-buying",
    "/second-hand-home-inspection.html": "/badek-home-before-buying",
}


class CleanURLHandler(SimpleHTTPRequestHandler):
    def send_head(self):  # type: ignore[no-untyped-def]
        parsed_url = urlsplit(self.path)
        decoded_path = unquote(parsed_url.path)
        if decoded_path in LOCAL_REDIRECTS:
            target = LOCAL_REDIRECTS[decoded_path]
            if parsed_url.query:
                target += f"?{parsed_url.query}"
            self.send_response(301)
            self.send_header("Location", target)
            self.end_headers()
            return None

        requested_path = decoded_path.lstrip("/")
        candidate = ROOT / f"{requested_path}.html"
        if requested_path and not Path(requested_path).suffix and candidate.is_file():
            original_path = self.path
            self.path = f"/{requested_path}.html"
            try:
                return super().send_head()
            finally:
                self.path = original_path
        return super().send_head()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    handler = partial(CleanURLHandler, directory=ROOT)
    server = ThreadingHTTPServer(("127.0.0.1", args.port), handler)
    print(f"Serving {ROOT} at http://localhost:{args.port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
