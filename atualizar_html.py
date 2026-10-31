#!/usr/bin/env python3
"""Atualiza apenas os cartões de matérias e o acervo estático usando data/publicacoes.json.
Não usa rede, dependências externas ou bibliotecas de template."""
import json,html,re,datetime
from pathlib import Path
BASE=Path(__file__).resolve().parent
D=json.loads((BASE/'data/publicacoes.json').read_text(encoding='utf-8'))
PAGE=BASE/'index.html'
assert len(D)==len({x['ID'] for x in D}), 'IDs duplicados'
assert all(str(x['URL']).startswith('https://opopular.com.br/') for x in D), 'URL fora do domínio original'
assert len({x['URL'] for x in D})==len(D), 'URLs duplicadas'
H=lambda s:html.escape(str(s),quote=True)

def dbr(x):return datetime.date.fromisoformat(x['Data']).strftime('%d/%m/%Y')
def card(x,first=False):
 css='story story--lead' if first else 'story'
 return f'''<article class="{css}"><div class="story__meta"><span>{H(x['Categoria'])}</span><time datetime="{H(x['Data'])}">{dbr(x)}</time></div><h3><a href="{H(x['URL'])}" target="_blank" rel="noopener noreferrer">{H(x['Título'])}</a></h3><p>{H(x['Resumo editorial V2'])}</p><div class="story__link"><a href="{H(x['URL'])}" target="_blank" rel="noopener noreferrer">Ler no O Popular <span aria-hidden="true">↗</span></a></div></article>'''

def entry(x):
 q=H(' '.join([x['Título'],x['Categoria'],x['Gênero'],x['Resumo editorial V2']]))
 return f'''<li class="archive-row" data-year="{H(x['Data'][:4])}" data-group="{H(x['grupo'])}" data-search="{q}"><time datetime="{H(x['Data'])}">{dbr(x)}</time><div><a href="{H(x['URL'])}" rel="noopener noreferrer" target="_blank">{H(x['Título'])}</a><span class="archive-category">{H(x['Categoria'])}</span></div><span class="archive-arrow" aria-hidden="true">↗</span></li>'''

sel=[x for x in D if x['Destaque']=='Sim'];sel.sort(key=lambda x:x['ordem_selecao'])
assert len(sel)>=2, 'São esperados dois destaques principais'
content=PAGE.read_text(encoding='utf-8')
def swap(s,a,b,t):
 pattern=r'(<!-- '+re.escape(a)+r' -->)(.*?)(<!-- '+re.escape(b)+r' -->)'
 result,n=re.subn(pattern,lambda m:m[1]+'\n'+t+'\n'+m[3],s,flags=re.S)
 assert n==1,(a,b,n)
 return result
content=swap(content,'INICIO_DESTAQUES_PRINCIPAIS','FIM_DESTAQUES_PRINCIPAIS','\n'.join(card(x,i==0) for i,x in enumerate(sel[:2])))
content=swap(content,'INICIO_OUTROS_DESTAQUES','FIM_OUTROS_DESTAQUES','\n'.join(card(x) for x in sel[2:]))
content=swap(content,'INICIO_ACERVO','FIM_ACERVO','\n'.join(entry(x) for x in D))
content=re.sub(r'<p class="results-label" id="resultado-contagem" role="status" aria-live="polite">.*?</p>',f'<p class="results-label" id="resultado-contagem" role="status" aria-live="polite">{len(D)} publicações encontradas</p>',content)
content=re.sub(r'<h2 id="archive-heading">.*?</h2>',f'<h2 id="archive-heading">{len(D)} publicações.<br>Uma busca só.</h2>',content)
PAGE.write_text(content,encoding='utf-8')
print(f'{len(D)} publicações, {len(sel)} destaques, index.html atualizado')
