(function(){
  var nav=document.getElementById('nav');
  if(nav){var onScroll=function(){nav.classList.toggle('solid',window.scrollY>40)};window.addEventListener('scroll',onScroll,{passive:true});onScroll();}

  var mb=document.getElementById('menuBtn'),links=document.getElementById('links');
  if(mb&&links){
    mb.addEventListener('click',function(){var o=links.classList.toggle('open');mb.setAttribute('aria-expanded',o?'true':'false')});
    links.querySelectorAll('a').forEach(function(a){a.addEventListener('click',function(){links.classList.remove('open');mb.setAttribute('aria-expanded','false')})});
  }

  var els=document.querySelectorAll('.rv');
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{threshold:.12,rootMargin:'0px 0px -40px 0px'});
    els.forEach(function(el){io.observe(el)});
  } else { els.forEach(function(el){el.classList.add('in')}); }

  var hero=document.getElementById('hero');
  if(hero){hero.addEventListener('pointermove',function(e){var r=hero.getBoundingClientRect();hero.style.setProperty('--mx',(e.clientX-r.left)+'px');hero.style.setProperty('--my',(e.clientY-r.top)+'px')});}

  var ba=document.getElementById('ba');
  if(ba){var range=ba.querySelector('input');range.addEventListener('input',function(){ba.style.setProperty('--pos',range.value+'%')});}

  var form=document.getElementById('qform');
  if(form){
    var steps=form.querySelectorAll('.qstep'),bar=document.getElementById('progBar'),cur=1;
    var show=function(n){cur=n;steps.forEach(function(s){s.classList.toggle('on',+s.dataset.step===n)});if(bar)bar.style.width=Math.min(n,3)/3*100+'%';var f=form.querySelector('.qstep.on input, .qstep.on button');if(n>1&&f)f.focus({preventScroll:true})};
    form.addEventListener('click',function(e){var t=e.target.closest('[data-next],[data-back]');if(!t)return;show(cur+(t.hasAttribute('data-next')?1:-1))});
    form.addEventListener('submit',function(e){
      if(form.dataset.demo){e.preventDefault();show(4);return;}
      e.preventDefault();
      var data=new URLSearchParams(new FormData(form)).toString();
      fetch('/',{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded'},body:data})
        .then(function(){show(4)}).catch(function(){form.submit()});
    });
  }

  // Hosting badges (e.g. "Powered by Netlify" on free plans) sit fixed in the bottom-right corner.
  // When one appears, lift the phone call bar and pad the footer so nothing is covered.
  (function(){
    var mark=function(){ if(document.getElementById('nl-badge-frame')){ document.body.classList.add('has-badge'); return true; } return false; };
    if(mark()) return;
    if('MutationObserver' in window){
      var mo=new MutationObserver(function(){ if(mark()) mo.disconnect(); });
      mo.observe(document.body,{childList:true});
      setTimeout(function(){ mo.disconnect(); },15000);
    }
  })();

  var yr=document.getElementById('yr'); if(yr) yr.textContent=new Date().getFullYear();
})();
