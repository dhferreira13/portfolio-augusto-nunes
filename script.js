"use strict";
(() => {
 document.querySelector('.filters').addEventListener('submit', e => e.preventDefault());
 const menu=document.querySelector('.menu-toggle'); const nav=document.querySelector('#site-nav');
 menu.addEventListener('click', () => { const open=menu.getAttribute('aria-expanded')!=='true';menu.setAttribute('aria-expanded', String(open));menu.setAttribute('aria-label', open?'Fechar navegação':'Abrir navegação');nav.classList.toggle('is-open',open); });
 menu.addEventListener('keydown', e => {if(e.key==='Escape'){nav.classList.remove('is-open');menu.setAttribute('aria-expanded','false');menu.setAttribute('aria-label','Abrir navegação')}});
 nav.querySelectorAll('a').forEach(link=>link.addEventListener('click',()=>{nav.classList.remove('is-open');menu.setAttribute('aria-expanded','false');menu.setAttribute('aria-label','Abrir navegação')}));
 const search=document.querySelector('#busca'), year=document.querySelector('#ano'), topic=document.querySelector('#tema'), clear=document.querySelector('#limpar'), count=document.querySelector('#resultado-contagem'), empty=document.querySelector('#sem-resultados');
 const rows=[...document.querySelectorAll('.archive-row')];
 function normalize(s){return (s||'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLocaleLowerCase('pt-BR')}
 function apply(){let matched=0;const q=normalize(search.value.trim()); for(const row of rows){const ok=(!q||normalize(row.dataset.search).includes(q)) && (!year.value||row.dataset.year===year.value) && (!topic.value||row.dataset.group===topic.value);row.hidden=!ok;if(ok)matched++};count.textContent=matched+' '+(matched===1?'publicação encontrada':'publicações encontradas');empty.hidden=matched!==0}
 [search,year,topic].forEach(el=>el.addEventListener('input',apply));clear.addEventListener('click',()=>{search.value='';year.value='';topic.value='';apply();search.focus()});apply();
})();