const slides=[...document.querySelectorAll('.slide')],deck=document.querySelector('#deck');
let current=0;
function resize(){const v=document.querySelector('#viewport');deck.style.transform=`scale(${Math.min(v.clientWidth/1600,v.clientHeight/900)})`;}
function show(n){
  current=Math.max(0,Math.min(slides.length-1,n));
  slides.forEach((el,i)=>{el.classList.toggle('active',i===current);el.inert=i!==current;el.setAttribute('aria-hidden',String(i!==current));});
  document.querySelector('#counter').textContent=`${String(current+1).padStart(2,'0')} / ${slides.length}`;
  document.querySelector('#prev').disabled=current===0;
  document.querySelector('#next').disabled=current===slides.length-1;
  document.querySelector('.progress').style.width=`${(current+1)/slides.length*100}%`;
  history.replaceState(null,'',`#${current+1}`);
}
document.querySelector('#prev').onclick=()=>show(current-1);
document.querySelector('#next').onclick=()=>show(current+1);
document.querySelector('#toc').onclick=()=>show(1);
document.querySelector('#overview').onclick=()=>{
  const list=document.querySelector('#toc-list');list.replaceChildren();
  titles.forEach((t,i)=>{const b=document.createElement('button');b.textContent=`${String(i+1).padStart(2,'0')}　${t}`;b.dataset.go=i;b.classList.toggle('current',i===current);list.append(b);});
  document.querySelector('#toc-dialog').showModal();
};
document.addEventListener('click',e=>{
  const go=e.target.closest('[data-go]');
  if(go){show(Number(go.dataset.go));document.querySelector('#toc-dialog').close();return;}
  const b=e.target.closest('.image-button');
  if(b){const i=b.querySelector('img'),t=document.querySelector('#lightbox img');t.src=i.src;t.alt=i.alt;document.querySelector('#lightbox').showModal();}
});
document.querySelectorAll('dialog .close').forEach(b=>b.onclick=()=>b.closest('dialog').close());
document.querySelectorAll('dialog').forEach(d=>d.addEventListener('click',e=>{if(e.target!==d)return;const r=d.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)d.close();}));
document.querySelector('#fullscreen').onclick=async()=>{try{if(document.fullscreenElement)await document.exitFullscreen();else await document.documentElement.requestFullscreen();}catch{document.querySelector('#fullscreen').textContent='请按F11';}};
document.querySelector('#print').onclick=async()=>{await document.fonts.ready;window.print();};
document.addEventListener('keydown',e=>{
  if(document.querySelector('dialog[open]')||e.target.closest('input,textarea,select,[contenteditable="true"]'))return;
  if(e.key===' '&&e.target.closest('button,a'))return;
  if(['ArrowRight','ArrowDown','PageDown',' '].includes(e.key)){e.preventDefault();show(current+1);}
  else if(['ArrowLeft','ArrowUp','PageUp'].includes(e.key)){e.preventDefault();show(current-1);}
  else if(e.key==='Home'){e.preventDefault();show(0);}
  else if(e.key==='End'){e.preventDefault();show(slides.length-1);}
  else if(e.key.toLowerCase()==='f')document.querySelector('#fullscreen').click();
  else if(e.key.toLowerCase()==='o')document.querySelector('#overview').click();
});
const viewport=document.querySelector('#viewport');let lastWheel=0,total=0,locked=false,lastFlip=0;
viewport.addEventListener('wheel',e=>{
  if(e.ctrlKey||e.metaKey||document.querySelector('dialog[open]')||Math.abs(e.deltaX)>Math.abs(e.deltaY))return;
  e.preventDefault();const now=performance.now();if(now-lastWheel>220){total=0;locked=false;}lastWheel=now;if(locked)return;
  const delta=e.deltaY*(e.deltaMode===1?16:e.deltaMode===2?viewport.clientHeight:1);
  if(Math.sign(delta)!==Math.sign(total))total=0;total+=delta;
  if(Math.abs(total)>=40){show(current+(total>0?1:-1));locked=true;}
},{passive:false});
viewport.addEventListener('click',e=>{
  if(e.button!==0||e.detail>1||e.ctrlKey||e.metaKey||e.shiftKey||e.altKey||document.querySelector('dialog[open]')||e.target.closest('button,a,input,textarea,select')||window.getSelection()?.toString())return;
  const now=performance.now();if(now-lastFlip<500)return;show(current+1);lastFlip=now;
});
window.addEventListener('resize',resize);
window.addEventListener('hashchange',()=>show((parseInt(location.hash.slice(1))||1)-1));
resize();show((parseInt(location.hash.slice(1))||1)-1);
