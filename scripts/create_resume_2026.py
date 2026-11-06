"""Generate manually translated versions of the supplied 2026 résumé.

The English original is maintained separately. Requires ReportLab, fontTools,
uharfbuzz and Windows fonts Yu Gothic, Microsoft YaHei, Malgun and Nirmala UI.
"""
import html
import json
import re
import tempfile
from pathlib import Path
from xml.sax.saxutils import escape

import fitz
from fontTools.ttLib import TTCollection
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / 'scripts/resume_2026_manual.json').read_text(encoding='utf-8'))
DATA.update(json.loads((ROOT / 'scripts/resume_2026_european.json').read_text(encoding='utf-8')))
LATIN = Path(__import__('sys').prefix) / 'Lib/site-packages/matplotlib/mpl-data/fonts/ttf'
pdfmetrics.registerFont(TTFont('Latin', str(LATIN / 'DejaVuSans.ttf')))
pdfmetrics.registerFont(TTFont('LatinBold', str(LATIN / 'DejaVuSans-Bold.ttf')))
pdfmetrics.registerFontFamily('Latin', normal='Latin', bold='LatinBold', italic='Latin', boldItalic='LatinBold')
for name, reg, bold in [('Chinese','msyh.ttc','msyhbd.ttc'),('Japanese','YuGothR.ttc','YuGothB.ttc'),('Korean','malgun.ttf','malgunbd.ttf')]:
    pdfmetrics.registerFont(TTFont(name, 'C:/Windows/Fonts/' + reg, subfontIndex=0))
    pdfmetrics.registerFont(TTFont(name+'Bold', 'C:/Windows/Fonts/' + bold, subfontIndex=0))
    pdfmetrics.registerFontFamily(name, normal=name, bold=name+'Bold', italic=name, boldItalic=name+'Bold')
temporary = tempfile.TemporaryDirectory(prefix='resume-2026-font-')
collection = TTCollection('C:/Windows/Fonts/Nirmala.ttc')
for idx, name in [(0,'Hindi'),(1,'HindiBold')]:
    path = Path(temporary.name) / (name + '.ttf')
    collection.fonts[idx].save(path)
    pdfmetrics.registerFont(TTFont(name, str(path), shapable=True))
    assert pdfmetrics.getFont(name).shapable
pdfmetrics.registerFontFamily('Hindi',normal='Hindi',bold='HindiBold',italic='Hindi',boldItalic='HindiBold')

class HindiParagraph(Paragraph):
    def __init__(self, text, style):
        super().__init__(text, style)
        self.logical = html.unescape(re.sub(r'<[^>]*>', '', text))
    def draw(self):
        value = (b'\xfe\xff' + (self.logical+'\n').encode('utf-16-be')).hex()
        self.canv._code.append(f'/Span << /ActualText <{value}> /Lang (hi) >> BDC')
        try:
            super().draw()
        finally:
            self.canv._code.append('EMC')

outputs = {'de':'Vinicius-Rodrigues-Resume-DE.pdf','it':'Vinicius-Rodrigues-Resume-IT.pdf','ru':'Vinicius-Rodrigues-Resume-RU.pdf','pt':'Vinicius-Rodrigues-Curriculo.pdf','es':'Vinicius-Rodrigues-Resume-ES.pdf','fr':'Vinicius-Rodrigues-Resume-FR.pdf','zh':'Vinicius-Rodrigues-Resume-ZH.pdf','ja':'Vinicius-Rodrigues-Resume-JA.pdf','ko':'Vinicius-Rodrigues-Resume-KO.pdf','hi':'Vinicius-Rodrigues-Resume-HI.pdf'}
fontmap = {'zh':'Chinese','ja':'Japanese','ko':'Korean','hi':'Hindi'}
project_urls = [
 ('Creator Growth Feedback Loop','creator-growth-feedback-loop.onrender.com','https://github.com/viniciusrodriguesai/creator-growth-feedback-loop','2026'),
 ('Church Roster Bot','github.com/viniciusrodriguesai/church-roster-bot','https://github.com/viniciusrodriguesai/church-roster-bot',None),
 ('World Bank Dashboard','github.com/viniciusrodriguesai/worldbank-economic-dashboard','https://github.com/viniciusrodriguesai/worldbank-economic-dashboard','2024'),
 ('Resume Match AI','github.com/viniciusrodriguesai/resume-agent-system','https://github.com/viniciusrodriguesai/resume-agent-system','2026')]

def make(lang, scale, filename):
    data = DATA[lang]
    font = fontmap.get(lang, 'Latin')
    shaped = lang == 'hi'
    wrap = 'CJK' if lang in ('ja','zh') else None
    size = 8.35 * scale
    def style(name, size_, leading, **kwargs):
        return ParagraphStyle(name, fontName=font, fontSize=size_, leading=leading, wordWrap=wrap, alignment=TA_LEFT, shaping=int(shaped), **kwargs)
    body = style('body',size,size*1.25,spaceAfter=1.5*scale)
    title = style('title',19*scale,23*scale,textColor=colors.HexColor('#203149'),spaceAfter=1)
    role = style('role',8.6*scale,10.3*scale,spaceAfter=2)
    section = style('section',10*scale,12*scale,textColor=colors.HexColor('#176184'),spaceBefore=5*scale,spaceAfter=1)
    project = style('project',9*scale,11*scale,spaceBefore=2*scale,spaceAfter=0)
    def p(value, st=body): return (HindiParagraph if shaped else Paragraph)(value,st)
    def link(url,label): return '<link href="'+escape(url)+'" color="#000000"><u>'+escape(label)+'</u></link>'
    def bullet(text): return p('• '+escape(text))
    def heading(text):
        return [p('<b>'+escape(text)+'</b>',section), HRFlowable(width='100%', thickness=.35, color=colors.HexColor('#777777'), spaceAfter=2)]
    story = [p('VINICIUS RODRIGUES',title), p(escape(data['role']),role),
      p(escape(data['location'])+' | '+link('mailto:viniciusmangueira04@gmail.com','viniciusmangueira04@gmail.com')+' |'),
      p(escape(data['availability'])+' | '+link('https://www.linkedin.com/in/viniciusrodriguesai/','LinkedIn')+' | '+link('https://github.com/viniciusrodriguesai','github.com/viniciusrodriguesai')+' | '+link('https://viniciusrodriguesai.github.io/?lang='+lang,'Portfolio'))]
    story += heading(data['headings'][0]) + [p(escape(data['profile']))]
    story += heading(data['headings'][1]) + [p('<b>'+escape(data['university'])+'</b> | 2028'),p(escape(data['degree'])+' | '+escape(data['location']))]
    labels=data['skill_labels']
    story += heading(data['headings'][2]) + [
      p('<b>'+escape(labels[0])+':</b> Python, TypeScript, JavaScript, SQL, C++, '+escape(data['skill_extra'])),
      p('<b>'+escape(labels[1])+':</b> FastAPI, React, Pydantic, REST APIs, PostgreSQL, MySQL, SQLAlchemy, SQLite'),
      p('<b>'+escape(labels[2])+':</b> Docker, GitHub Actions, Pytest, Vitest, nginx, HMAC, '+escape({'pt':'idempotência','es':'idempotencia','fr':'idempotence','zh':'幂等性','ja':'冪等性','ko':'멱등성','hi':'आइडेम्पोटेंसी','de':'Idempotenz','it':'idempotenza','ru':'идемпотентность'}[lang])+', CI/CD')]
    story += heading(data['headings'][3]) + [p('<b>PET-Saúde Digital, UFPB / SES-PB | '+escape(data['experience_role'])+' | 2025 - '+escape(data['present'])+'</b>',project),p(escape(data['experience_org']))]
    story += [bullet(x) for x in data['experience']]
    story += heading(data['headings'][4])
    stacks = ['FastAPI, React, TypeScript, PostgreSQL, YouTube Data API', 'Python, FastAPI, PostgreSQL, Meta Cloud API ('+data['mock']+')', 'FastAPI, React, TypeScript, Docker, nginx', 'Python, FastAPI, Streamlit, SQLite, NLP, TF-IDF, RapidFuzz, Sentence Transformers, Pytest, Docker, GitHub Actions']
    for i,key in enumerate(['creator','church','world','resume']):
        name,label,url,date=project_urls[i]
        date=date or '2026 - '+data['present']
        story += [p('<b>'+escape(name)+'</b>  '+link(url,label)+' | '+escape(date),project),bullet(stacks[i])]
        story += [bullet(x) for x in data[key]]
    SimpleDocTemplate(str(filename),pagesize=letter,leftMargin=36,rightMargin=36,topMargin=26,bottomMargin=26,title='Vinicius Rodrigues - Resume',author='Vinicius Rodrigues').build(story)

import sys
requested = set(sys.argv[1:]) or set(outputs)
assert requested <= set(outputs), 'Unknown language'
for lang, name in outputs.items():
    if lang not in requested: continue
    path = ROOT/'assets'/name
    for scale in [1.20, 1.15, 1.10, 1.05, 1, .95, .90, .85, .80]:
        make(lang,scale,path)
        with fitz.open(path) as doc:
            if len(doc)==1: break
    print(lang, 'pages',len(fitz.open(path)), 'scale',scale)
