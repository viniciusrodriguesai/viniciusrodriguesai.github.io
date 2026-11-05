"""Generate the public portfolio resume. Run from the repository root.

Requires ReportLab and DejaVu Sans (Matplotlib or a local fonts directory).
Content comes from the verified portfolio and the owner's recorded education
and PET-Saude contribution. Personal phone number is intentionally excluded.
"""
from pathlib import Path
import sys
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, KeepTogether

ROOT = Path(__file__).resolve().parents[1]
FONT_DIRS = [ROOT / 'fonts', Path(sys.prefix) / 'Lib/site-packages/matplotlib/mpl-data/fonts/ttf', Path('/usr/share/fonts/truetype/dejavu')]
FONT_DIR = next(p for p in FONT_DIRS if (p / 'DejaVuSans.ttf').exists())
pdfmetrics.registerFont(TTFont('DV', str(FONT_DIR / 'DejaVuSans.ttf')))
pdfmetrics.registerFont(TTFont('DV-Bold', str(FONT_DIR / 'DejaVuSans-Bold.ttf')))
pdfmetrics.registerFontFamily('DV', normal='DV', bold='DV-Bold', italic='DV', boldItalic='DV-Bold')
INK, GREEN, MUTED = colors.HexColor('#20271e'), colors.HexColor('#324830'), colors.HexColor('#60685a')
styles = {
 'name': ParagraphStyle('name',fontName='DV-Bold',fontSize=25,leading=31,textColor=INK,spaceAfter=6),
 'role': ParagraphStyle('role',fontName='DV',fontSize=10,leading=15,textColor=GREEN,spaceAfter=6),
 'contact': ParagraphStyle('contact',fontName='DV',fontSize=8.1,leading=13,textColor=MUTED,spaceAfter=3),
 'body': ParagraphStyle('body',fontName='DV',fontSize=9,leading=13.5,textColor=INK,spaceAfter=7,alignment=TA_LEFT),
 'section': ParagraphStyle('section',fontName='DV-Bold',fontSize=9,leading=14,textColor=GREEN,spaceBefore=12,spaceAfter=7),
 'project': ParagraphStyle('project',fontName='DV-Bold',fontSize=9.5,leading=14,textColor=INK,spaceAfter=3),
 'meta': ParagraphStyle('meta',fontName='DV',fontSize=8,leading=12,textColor=MUTED,spaceAfter=5),
}
def p(text, style='body'): return Paragraph(text,styles[style])
def a(url,label): return f'<link href="{url}" color="#324830"><u>{label}</u></link>'
story=[p('VINICIUS RODRIGUES','name'),p('DESENVOLVIMENTO DE SOFTWARE | DADOS E INTELIGÊNCIA ARTIFICIAL','role'),p('João Pessoa, Brasil · '+a('mailto:viniciusmangueira04@gmail.com','viniciusmangueira04@gmail.com'),'contact'),p(a('https://viniciusrodriguesai.github.io/','Portfólio')+' · '+a('https://github.com/viniciusrodriguesai','GitHub')+' · '+a('https://www.linkedin.com/in/viniciusrodriguesai/','LinkedIn'),'contact'),Spacer(1,9),HRFlowable(width='100%',thickness=.6,color=colors.HexColor('#bfcbb2')),p('PERFIL','section'),p('Estudante de Ciência de Dados e Inteligência Artificial na UFPB, em busca de estágio em desenvolvimento, dados ou IA. Desenvolvo aplicações Python e interfaces React, com APIs, persistência e avaliação de modelos. Uso desenvolvimento assistido por IA, com revisão de código e verificações conforme o projeto.')]
story += [p('PROJETOS SELECIONADOS','section')]
projects=[
('Creator Growth Feedback Loop','FastAPI · React / TypeScript · PostgreSQL · YouTube Data API','Aplicação que importa métricas públicas do YouTube, atualiza um dashboard e sugere próximos experimentos de conteúdo. Desenvolvi o fluxo da importação à interface; conferi manualmente métricas e recomendações com 15 vídeos. As sugestões descrevem associações observadas, sem causalidade demonstrada.','https://github.com/viniciusrodriguesai/creator-growth-feedback-loop'),
('Resume Match AI','Python · FastAPI · Streamlit · Recuperação de informação','Workflow de oito etapas que relaciona requisitos de vagas a evidências de currículo. Comparei busca lexical e modelos opcionais em 36 casos sintéticos internos: rótulos idênticos, com maior latência dos modelos em CPU. A busca lexical é o modo padrão; a avaliação não comprova qualidade em seleções reais.','https://github.com/viniciusrodriguesai/resume-agent-system'),
('Classificação de Risco de Crédito','Python · scikit-learn · Redes neurais · Projeto em colaboração','Estudo desenvolvido com Gustavo Pereira. Compara modelos em Home Credit e registra uma replicação separada na base UCI. A MLP selecionada em validação atingiu ROC-AUC de 0,7757 em 4.377 registros de teste, frente a 0,7174 da regressão logística. Probabilidades não calibradas; sem alegação de uso em produção.','https://github.com/viniciusrodriguesai/credit-risk-classification')]
for title,stack,description,url in projects:
 story.append(KeepTogether([p(title+' · '+a(url,'Código'),'project'),p(stack,'meta'),p(description)]))
story += [p('EXPERIÊNCIA EM EXTENSÃO UNIVERSITÁRIA','section'),p('PET-Saúde Digital | UFPB / SES-PB','project'),p('Agosto de 2025 - atual · Atuação voluntária · 4h/semana durante o semestre','meta'),p('Revisão de respostas do assistente de saúde TAÍS frente a protocolos, contribuição à base de conhecimento e revisão de prompts com a equipe. Atuação em avaliação e conteúdo, sem desenvolvimento de código no TAÍS.'),p('FORMAÇÃO','section'),p('<b>Bacharelado em Ciência de Dados e Inteligência Artificial</b><br/>Universidade Federal da Paraíba · conclusão prevista para julho de 2028.'),p('TECNOLOGIAS','section'),p('Python, SQL, JavaScript / TypeScript, FastAPI, React, PostgreSQL, scikit-learn, Git e Docker. Inglês para leitura técnica, mensagens de trabalho e atualizações orais preparadas.')]
def footer(canvas, doc):
 canvas.saveState();canvas.setFont('DV',7);canvas.setFillColor(MUTED)
 canvas.drawString(42,26,'viniciusrodriguesai.github.io · Atualizado em novembro de 2026')
 canvas.restoreState()
target=ROOT/'assets'/'Vinicius-Rodrigues-Curriculo.pdf'
SimpleDocTemplate(str(target),pagesize=A4,rightMargin=42,leftMargin=42,topMargin=35,bottomMargin=40,title='Vinicius Rodrigues - Currículo',author='Vinicius Rodrigues').build(story,onFirstPage=footer,onLaterPages=footer)
print(target)
