"""Generate the seven translated public portfolio resumes (or selected locales).

Requires ReportLab, DejaVu Sans, and an embeddable Chinese TrueType font.
On Windows, Microsoft YaHei is embedded as subsets, not copied to the site.
Korean uses Malgun Gothic; Hindi uses Nirmala UI with HarfBuzz shaping.
Japanese uses Yu Gothic.
Example: python scripts/create_translated_resumes.py es fr ko hi
"""
import argparse
import html
import json
import os
import re
import sys
import tempfile
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, KeepTogether

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT/'scripts/resume_translations.json').read_text(encoding='utf-8'))
DATA.update(json.loads((ROOT/'scripts/resume_extra_translations.json').read_text(encoding='utf-8')))
parser=argparse.ArgumentParser()
parser.add_argument('languages',nargs='*',choices=list(DATA))
args=parser.parse_args()
languages=args.languages or list(DATA)
FONTS = [ROOT/'fonts', Path(sys.prefix)/'Lib/site-packages/matplotlib/mpl-data/fonts/ttf', Path('/usr/share/fonts/truetype/dejavu')]
LATIN = next(p for p in FONTS if (p/'DejaVuSans.ttf').exists())
pdfmetrics.registerFont(TTFont('ResumeLatin', str(LATIN/'DejaVuSans.ttf')))
pdfmetrics.registerFont(TTFont('ResumeLatinBold', str(LATIN/'DejaVuSans-Bold.ttf')))
pdfmetrics.registerFontFamily('ResumeLatin', normal='ResumeLatin', bold='ResumeLatinBold', italic='ResumeLatin', boldItalic='ResumeLatinBold')
if 'zh' in languages:
    cjk=Path(os.environ.get('PORTFOLIO_CJK_FONT','C:/Windows/Fonts/msyh.ttc'))
    cjk_bold=Path(os.environ.get('PORTFOLIO_CJK_BOLD','C:/Windows/Fonts/msyhbd.ttc'))
    pdfmetrics.registerFont(TTFont('ResumeCJK',str(cjk),subfontIndex=0))
    pdfmetrics.registerFont(TTFont('ResumeCJKBold',str(cjk_bold),subfontIndex=0))
    pdfmetrics.registerFontFamily('ResumeCJK',normal='ResumeCJK',bold='ResumeCJKBold',italic='ResumeCJK',boldItalic='ResumeCJKBold')
if 'ko' in languages:
    pdfmetrics.registerFont(TTFont('ResumeKorean','C:/Windows/Fonts/malgun.ttf'))
    pdfmetrics.registerFont(TTFont('ResumeKoreanBold','C:/Windows/Fonts/malgunbd.ttf'))
    pdfmetrics.registerFontFamily('ResumeKorean',normal='ResumeKorean',bold='ResumeKoreanBold',italic='ResumeKorean',boldItalic='ResumeKoreanBold')
if 'ja' in languages:
    pdfmetrics.registerFont(TTFont('ResumeJapanese','C:/Windows/Fonts/YuGothR.ttc',subfontIndex=0))
    pdfmetrics.registerFont(TTFont('ResumeJapaneseBold','C:/Windows/Fonts/YuGothB.ttc',subfontIndex=0))
    pdfmetrics.registerFontFamily('ResumeJapanese',normal='ResumeJapanese',bold='ResumeJapaneseBold',italic='ResumeJapanese',boldItalic='ResumeJapaneseBold')
if 'hi' in languages:
    from fontTools.ttLib import TTCollection
    # Extract the selected faces so the shaper and PDF subsetter use the same face.
    hindi_temp=tempfile.TemporaryDirectory(prefix='portfolio-hindi-fonts-')
    collection=TTCollection('C:/Windows/Fonts/Nirmala.ttc')
    for index,name in [(0,'ResumeHindi'),(1,'ResumeHindiBold')]:
        font_path=Path(hindi_temp.name)/(name+'.ttf')
        collection.fonts[index].save(font_path)
        pdfmetrics.registerFont(TTFont(name,str(font_path),shapable=True))
        assert pdfmetrics.getFont(name).shapable,'Install uharfbuzz for Hindi shaping'
    pdfmetrics.registerFontFamily('ResumeHindi',normal='ResumeHindi',bold='ResumeHindiBold',italic='ResumeHindi',boldItalic='ResumeHindiBold')
INK = colors.HexColor('#20271e')
GREEN = colors.HexColor('#324830')
MUTED = colors.HexColor('#60685a')

def actual_text_start(canvas,text):
    value=(b'\xfe\xff'+text.encode('utf-16-be')).hex()
    canvas._code.append(f'/Span << /ActualText <{value}> /Lang (hi) >> BDC')

class ShapedParagraph(Paragraph):
    """Preserve logical Unicode alongside visually shaped Devanagari glyphs."""
    def __init__(self,text,style):
        super().__init__(text,style)
        logical=re.sub(r'<br\s*/?>','\n',text,flags=re.I)
        self.logical_text=html.unescape(re.sub(r'<[^>]*>','',logical))

    def draw(self):
        actual_text_start(self.canv,self.logical_text+'\n')
        try:
            super().draw()
        finally:
            self.canv._code.append('EMC')

for language in languages:
    data=DATA[language]
    chinese = language in ('zh','ja')
    asian=language in ('zh','ja','ko','hi')
    regular,bold={'zh':('ResumeCJK','ResumeCJKBold'),'ja':('ResumeJapanese','ResumeJapaneseBold'),'ko':('ResumeKorean','ResumeKoreanBold'),'hi':('ResumeHindi','ResumeHindiBold')}.get(language,('ResumeLatin','ResumeLatinBold'))
    styles = {
      'name': ParagraphStyle('name', fontName='ResumeLatinBold', fontSize=25, leading=31, textColor=INK, spaceAfter=6),
      'role': ParagraphStyle('role', fontName=regular, fontSize=11 if asian else 10, leading=17 if asian else 15, textColor=GREEN, spaceAfter=6),
      'contact': ParagraphStyle('contact', fontName=regular, fontSize=8.5 if asian else 8.1, leading=13, textColor=MUTED, spaceAfter=3),
      'body': ParagraphStyle('body', fontName=regular, fontSize=10 if asian else 9, leading=16 if asian else 13.5, wordWrap='CJK' if chinese else None, textColor=INK, spaceAfter=7),
      'section': ParagraphStyle('section', fontName=bold, fontSize=10 if asian else 9, leading=15 if asian else 14, textColor=GREEN, spaceBefore=12, spaceAfter=7),
      'project': ParagraphStyle('project', fontName=bold, fontSize=10.5 if asian else 9.5, leading=15 if asian else 14, textColor=INK, spaceAfter=3),
      'meta': ParagraphStyle('meta', fontName=regular, fontSize=8.5 if asian else 8, leading=13 if asian else 12, wordWrap='CJK' if chinese else None, textColor=MUTED, spaceAfter=5),
    }
    if language=='hi':
        for name,style in styles.items():
            if name!='name': style.shaping=1
    def p(text, style='body'):
        return (ShapedParagraph if language=='hi' else Paragraph)(text,styles[style])
    def a(url, label): return f'<link href="{url}" color="#324830"><u>{escape(label)}</u></link>'
    headings = data['headings']
    story = [p('VINICIUS RODRIGUES','name'),p(escape(data['role']),'role'),
      p(escape(data['location'])+' · '+a('mailto:viniciusmangueira04@gmail.com','viniciusmangueira04@gmail.com'),'contact'),
      p(a('https://viniciusrodriguesai.github.io/?lang='+language,data['portfolio'])+' · '+a('https://github.com/viniciusrodriguesai','GitHub')+' · '+a('https://www.linkedin.com/in/viniciusrodriguesai/','LinkedIn'),'contact'),
      Spacer(1,9),HRFlowable(width='100%',thickness=.6,color=colors.HexColor('#bfcbb2')),
      p(headings[0],'section'),p(escape(data['profile'])),p(headings[1],'section')]
    for project in data['projects']:
        story.append(KeepTogether([p(escape(project['title'])+' · '+a(project['url'],data['code']),'project'),p(escape(project['stack']),'meta'),p(escape(project['description']))]))
    technologies=escape(data['technologies'])
    if chinese: technologies=technologies.replace('英语：','<br/>英语：')
    if language=='ko': technologies=technologies.replace('영어:','<br/>영어:')
    if language=='hi': technologies=technologies.replace('अंग्रेज़ी:','<br/>अंग्रेज़ी:')
    story += [p(headings[2],'section'),p(escape(data['experience_title']),'project'),p(escape(data['experience_meta']),'meta'),p(escape(data['experience'])),
      p(headings[3],'section'),p('<b>'+escape(data['degree'])+'</b><br/>'+escape(data['education'])),p(headings[4],'section'),p(technologies)]
    def footer(canvas, doc):
        canvas.saveState()
        canvas.setFont(regular,7.2 if asian else 7)
        canvas.setFillColor(MUTED)
        if language=='hi': actual_text_start(canvas,data['footer']+'\n')
        canvas.drawString(42,26,data['footer'],shaping=language=='hi')
        if language=='hi': canvas._code.append('EMC')
        canvas.restoreState()
    target=ROOT/'assets'/data['filename']
    SimpleDocTemplate(str(target),pagesize=A4,rightMargin=42,leftMargin=42,topMargin=35,bottomMargin=40,title=data['pdf_title'],author='Vinicius Rodrigues').build(story,onFirstPage=footer,onLaterPages=footer)
    print(target.name)
