"""Generate the English and Simplified Chinese public portfolio resumes.

Requires ReportLab, DejaVu Sans, and an embeddable Chinese TrueType font.
On Windows, Microsoft YaHei is embedded as subsets, not copied to the site.
Set PORTFOLIO_CJK_FONT and PORTFOLIO_CJK_BOLD for alternative font paths.
"""
import json
import os
import sys
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
FONTS = [ROOT/'fonts', Path(sys.prefix)/'Lib/site-packages/matplotlib/mpl-data/fonts/ttf', Path('/usr/share/fonts/truetype/dejavu')]
LATIN = next(p for p in FONTS if (p/'DejaVuSans.ttf').exists())
pdfmetrics.registerFont(TTFont('ResumeLatin', str(LATIN/'DejaVuSans.ttf')))
pdfmetrics.registerFont(TTFont('ResumeLatinBold', str(LATIN/'DejaVuSans-Bold.ttf')))
pdfmetrics.registerFontFamily('ResumeLatin', normal='ResumeLatin', bold='ResumeLatinBold', italic='ResumeLatin', boldItalic='ResumeLatinBold')
cjk = Path(os.environ.get('PORTFOLIO_CJK_FONT', 'C:/Windows/Fonts/msyh.ttc'))
cjk_bold = Path(os.environ.get('PORTFOLIO_CJK_BOLD', 'C:/Windows/Fonts/msyhbd.ttc'))
pdfmetrics.registerFont(TTFont('ResumeCJK', str(cjk), subfontIndex=0))
pdfmetrics.registerFont(TTFont('ResumeCJKBold', str(cjk_bold), subfontIndex=0))
pdfmetrics.registerFontFamily('ResumeCJK', normal='ResumeCJK', bold='ResumeCJKBold', italic='ResumeCJK', boldItalic='ResumeCJKBold')
INK = colors.HexColor('#20271e')
GREEN = colors.HexColor('#324830')
MUTED = colors.HexColor('#60685a')

for language, data in DATA.items():
    chinese = language == 'zh'
    regular, bold = ('ResumeCJK','ResumeCJKBold') if chinese else ('ResumeLatin','ResumeLatinBold')
    styles = {
      'name': ParagraphStyle('name', fontName='ResumeLatinBold', fontSize=25, leading=31, textColor=INK, spaceAfter=6),
      'role': ParagraphStyle('role', fontName=regular, fontSize=11 if chinese else 10, leading=17 if chinese else 15, textColor=GREEN, spaceAfter=6),
      'contact': ParagraphStyle('contact', fontName=regular, fontSize=8.5 if chinese else 8.1, leading=13, textColor=MUTED, spaceAfter=3),
      'body': ParagraphStyle('body', fontName=regular, fontSize=10 if chinese else 9, leading=16 if chinese else 13.5, wordWrap='CJK' if chinese else None, textColor=INK, spaceAfter=7),
      'section': ParagraphStyle('section', fontName=bold, fontSize=10 if chinese else 9, leading=15 if chinese else 14, textColor=GREEN, spaceBefore=12, spaceAfter=7),
      'project': ParagraphStyle('project', fontName=bold, fontSize=10.5 if chinese else 9.5, leading=15 if chinese else 14, textColor=INK, spaceAfter=3),
      'meta': ParagraphStyle('meta', fontName=regular, fontSize=8.5 if chinese else 8, leading=13 if chinese else 12, wordWrap='CJK' if chinese else None, textColor=MUTED, spaceAfter=5),
    }
    def p(text, style='body'): return Paragraph(text, styles[style])
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
    story += [p(headings[2],'section'),p(escape(data['experience_title']),'project'),p(escape(data['experience_meta']),'meta'),p(escape(data['experience'])),
      p(headings[3],'section'),p('<b>'+escape(data['degree'])+'</b><br/>'+escape(data['education'])),p(headings[4],'section'),p(technologies)]
    def footer(canvas, doc):
        canvas.saveState()
        canvas.setFont(regular,7.2 if chinese else 7)
        canvas.setFillColor(MUTED)
        canvas.drawString(42,26,data['footer'])
        canvas.restoreState()
    target=ROOT/'assets'/data['filename']
    SimpleDocTemplate(str(target),pagesize=A4,rightMargin=42,leftMargin=42,topMargin=35,bottomMargin=40,title=data['pdf_title'],author='Vinicius Rodrigues').build(story,onFirstPage=footer,onLaterPages=footer)
    print(target.name)
