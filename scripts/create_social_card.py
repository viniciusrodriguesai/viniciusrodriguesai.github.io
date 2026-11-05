"""Render the portfolio's typographic social preview using installed Windows fonts."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
FONT_DIR = Path('C:/Windows/Fonts')
def font(name, size): return ImageFont.truetype(str(FONT_DIR / name), size)
image = Image.new('RGB', (1200, 630), '#f6f5f0')
draw = ImageDraw.Draw(image)
draw.line((64, 75, 1136, 75), fill='#d7dccc', width=2)
draw.text((64, 29), 'VR.', font=font('arialbd.ttf', 28), fill='#324830')
draw.text((820, 37), 'PORTFÓLIO / 2026', font=font('cour.ttf', 19), fill='#68755c')
draw.text((62, 126), 'Vinicius', font=font('arial.ttf', 100), fill='#20271e')
draw.text((62, 224), 'Rodrigues.', font=font('timesi.ttf', 118), fill='#324830')
draw.text((68, 392), 'Software, dados & inteligência artificial.', font=font('arial.ttf', 29), fill='#324830')
draw.text((68, 449), 'Ciência de Dados e IA · UFPB · João Pessoa, Brasil', font=font('arial.ttf', 20), fill='#68755c')
draw.rounded_rectangle((824, 177, 1136, 414), radius=5, fill='#243623')
for y, number, title in [(204, '01', 'PYTHON / APIs'), (275, '02', 'DADOS / ML'), (346, '03', 'REACT / WEB')]:
    draw.text((846, y + 4), number, font=font('cour.ttf', 18), fill='#c8dda3')
    draw.text((886, y), title, font=font('arial.ttf', 21), fill='#eef2e4')
    if number != '03': draw.line((852, y + 35, 852, y + 63), fill='#728461', width=2)
draw.line((64, 538, 1136, 538), fill='#d7dccc', width=2)
draw.text((68, 567), 'viniciusrodriguesai.github.io', font=font('cour.ttf', 21), fill='#53654a')
draw.ellipse((894, 570, 904, 580), fill='#647c48')
draw.text((918, 564), 'Em busca de estágio', font=font('arial.ttf', 18), fill='#53654a')
image.save(ROOT / 'assets/social-card.png', optimize=True)
