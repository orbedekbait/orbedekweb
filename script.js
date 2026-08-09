if(!document.querySelector('.site-header'))document.body.insertAdjacentHTML('afterbegin','<header class="site-header"><a class="logo" href="index.html" aria-label="אור בדק בית - דף הבית"><img src="public/images/or-bedek-logo.png" alt="לוגו אור בדק בית"></a><button class="menu-toggle" type="button" aria-expanded="false" aria-controls="site-menu" aria-label="פתיחת תפריט"><span></span><span></span></button></header><aside class="site-menu" id="site-menu" aria-hidden="true"><div class="menu-top"><img src="public/images/or-bedek-logo.png" alt=""><button class="menu-close" type="button" aria-label="סגירת תפריט">×</button></div><nav aria-label="ניווט ראשי"><a href="index.html">עמוד הבית</a><a href="about.html">קצת עליי</a><a href="services.html">שירותים</a><a href="faq.html">שאלות נפוצות</a><a href="blog.html">בלוג</a><a href="contact.html">צור קשר</a></nav></aside><div class="menu-backdrop" aria-hidden="true"></div>');
const menu=document.querySelector('.site-menu'),backdrop=document.querySelector('.menu-backdrop'),toggle=document.querySelector('.menu-toggle'),close=document.querySelector('.menu-close');
const menuNav=menu.querySelector('nav');
if(!menuNav.querySelector('a[href="sample-report.html"]')){
  const reportLink=document.createElement('a');
  reportLink.href='sample-report.html';
  reportLink.textContent='דוח לדוגמה';
  menuNav.insertBefore(reportLink,menuNav.querySelector('a[href="contact.html"]'));
}
document.querySelectorAll('.footer-links a[href="public/reports/sample-home-inspection-report.pdf"]').forEach(link=>link.href='sample-report.html');
const bookingUrl='https://wa.me/972523199403?text=%D7%A9%D7%9C%D7%95%D7%9D%20%D7%90%D7%95%D7%A8%2C%20%D7%90%D7%A9%D7%9E%D7%97%20%D7%9C%D7%AA%D7%90%D7%9D%20%D7%91%D7%93%D7%99%D7%A7%D7%AA%20%D7%91%D7%93%D7%A7%20%D7%91%D7%99%D7%AA';
document.querySelectorAll('a').forEach(link=>{
  if(!link.textContent.includes('תיאום בדיקה'))return;
  link.href=bookingUrl;
  link.target='_blank';
  link.rel='noopener';
});
document.querySelectorAll('.cards article').forEach(card=>{
  const heading=card.querySelector('h3');
  const copy=card.querySelector('p');
  if(!heading||!copy)return;
  if(heading.textContent==='בדק בית לדירה חדשה'){
    heading.textContent='בדק בית לדירה חדשה מקבלן';
    copy.textContent='בדיקה לאחר הרכישה, לקראת המסירה או אחריה, לאיתור ולתיעוד ליקויים במסגרת תקופות הבדק והאחריות לפי חוק המכר (דירות).';
  }
  if(heading.textContent==='בדק בית לפני קניית יד שנייה'){
    heading.textContent='בדק בית לפני רכישת דירה';
    copy.textContent='בדיקה שמבהירה את מצב הנכס ועלויות התיקון, מספקת בסיס להתמקחות על המחיר ולעיתים מאפשרת לבקש תיקון ליקויים לפני הרכישה.';
  }
});
const desktopMenu=window.matchMedia('(min-width: 781px)');
function setMenu(open){const drawerOpen=open&&!desktopMenu.matches;menu.classList.toggle('is-open',drawerOpen);backdrop.classList.toggle('is-visible',drawerOpen);menu.setAttribute('aria-hidden',String(!desktopMenu.matches&&!drawerOpen));toggle.setAttribute('aria-expanded',String(drawerOpen));document.body.style.overflow=drawerOpen?'hidden':''}
desktopMenu.addEventListener?.('change',()=>setMenu(false));
setMenu(false);
toggle.addEventListener('click',()=>setMenu(true));close.addEventListener('click',()=>setMenu(false));backdrop.addEventListener('click',()=>setMenu(false));menu.querySelectorAll('a').forEach(link=>link.addEventListener('click',()=>setMenu(false)));
document.getElementById('year').textContent=new Date().getFullYear();
document.body.insertAdjacentHTML('beforeend','<div class="floating-contact" aria-label="יצירת קשר מהירה"><a class="float-call" href="tel:0523199403" aria-label="חיוג לטלפון"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.6 10.8a15.1 15.1 0 006.6 6.6l2.2-2.2a1 1 0 011-.24 11.4 11.4 0 003.56.57 1 1 0 011 1V20a1 1 0 01-1 1C10.6 21 3 13.4 3 4a1 1 0 011-1h3.5a1 1 0 011 1 11.4 11.4 0 00.57 3.56 1 1 0 01-.24 1z" /></svg></a><a class="float-whatsapp" href="https://wa.me/972523199403" target="_blank" rel="noopener" aria-label="שליחת הודעת WhatsApp"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20.5 3.5A11.9 11.9 0 0012.05 0C5.45 0 .1 5.32.1 11.9c0 2.1.55 4.15 1.6 5.95L0 24l6.3-1.65a12 12 0 005.74 1.46h.01C18.65 23.81 24 18.48 24 11.9c0-3.18-1.24-6.17-3.5-8.4zM12.05 21.8a9.9 9.9 0 01-5.04-1.38l-.36-.22-3.74.98 1-3.65-.24-.38a9.8 9.8 0 01-1.55-5.25c0-5.47 4.45-9.9 9.93-9.9 2.65 0 5.14 1.03 7.02 2.9a9.82 9.82 0 012.9 7c0 5.46-4.45 9.9-9.92 9.9zm5.44-7.43c-.3-.15-1.76-.87-2.03-.97-.27-.1-.47-.15-.67.15-.2.3-.77.97-.94 1.16-.17.2-.35.22-.65.08-1.77-.88-2.93-1.57-4.1-3.57-.31-.53.31-.49.89-1.63.1-.2.05-.37-.03-.52-.07-.15-.67-1.62-.92-2.22-.24-.58-.49-.5-.67-.5h-.57c-.2 0-.52.08-.8.37-.27.3-1.05 1.03-1.05 2.5s1.08 2.9 1.23 3.1c.15.2 2.13 3.24 5.15 4.55.72.31 1.28.5 1.72.63.72.23 1.37.2 1.88.12.57-.08 1.76-.72 2.01-1.42.25-.7.25-1.3.17-1.42-.07-.12-.27-.2-.57-.35z" /></svg></a></div>');
document.querySelector('.inquiry-form')?.addEventListener('submit',event=>{event.preventDefault();const data=new FormData(event.currentTarget);const text=`פנייה חדשה מאתר אור בדק בית%0Aשם: ${encodeURIComponent(data.get('name'))}%0Aטלפון: ${encodeURIComponent(data.get('phone'))}`;window.open(`https://wa.me/972523199403?text=${text}`,'_blank','noopener')});

const propertyRotator=document.querySelector('[data-property-rotator]');
if(propertyRotator){
  const slides=[...propertyRotator.querySelectorAll('.hero-property-slide')];
  const reduceMotion=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  let activeIndex=0;
  let rotationTimer;
  const showProperty=index=>{
    activeIndex=(index+slides.length)%slides.length;
    slides.forEach((slide,slideIndex)=>{
      const active=slideIndex===activeIndex;
      slide.classList.toggle('is-active',active);
      slide.setAttribute('aria-hidden',String(!active));
    });
  };
  const stopRotation=()=>window.clearInterval(rotationTimer);
  const startRotation=()=>{
    stopRotation();
    if(!reduceMotion)rotationTimer=window.setInterval(()=>showProperty(activeIndex+1),3800);
  };
  document.addEventListener('visibilitychange',()=>document.hidden?stopRotation():startRotation());
  startRotation();
}

const revealSections=document.querySelectorAll('[data-reveal]');
if('IntersectionObserver' in window){
  revealSections.forEach(section=>section.classList.add('reveal-ready'));
  const revealObserver=new IntersectionObserver(entries=>entries.forEach(entry=>{
    if(!entry.isIntersecting)return;
    entry.target.classList.add('is-visible');
    revealObserver.unobserve(entry.target);
  }),{threshold:.2,rootMargin:'0px 0px -10% 0px'});
  revealSections.forEach(section=>revealObserver.observe(section));
}else{
  revealSections.forEach(section=>section.classList.add('is-visible'));
}
