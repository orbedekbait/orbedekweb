const menu=document.querySelector('.site-menu'),backdrop=document.querySelector('.menu-backdrop'),toggle=document.querySelector('.menu-toggle'),close=document.querySelector('.menu-close');
function setMenu(open){menu.classList.toggle('is-open',open);backdrop.classList.toggle('is-visible',open);menu.setAttribute('aria-hidden',String(!open));toggle.setAttribute('aria-expanded',String(open));document.body.style.overflow=open?'hidden':''}
toggle.addEventListener('click',()=>setMenu(true));close.addEventListener('click',()=>setMenu(false));backdrop.addEventListener('click',()=>setMenu(false));menu.querySelectorAll('a').forEach(link=>link.addEventListener('click',()=>setMenu(false)));
document.getElementById('year').textContent=new Date().getFullYear();
