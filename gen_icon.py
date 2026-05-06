from PIL import Image, ImageDraw, ImageFont
import os

img = Image.new('RGBA', (256, 256), (255, 255, 255, 0))
draw = ImageDraw.Draw(img)

# White document background with red top
draw.rectangle([30, 20, 226, 236], fill='white', outline='#d0d0d0', width=2)
# Draw a red accent for PDF
draw.rectangle([30, 50, 226, 120], fill='#F40F02')

try:
    font = ImageFont.truetype("arialbd.ttf", 48)
except:
    font = ImageFont.load_default()

# Text "PDF"
draw.text((75, 60), "PDF", fill='white', font=font)

# Some lines to look like a document
draw.rectangle([60, 150, 196, 158], fill='#d0d0d0')
draw.rectangle([60, 175, 196, 183], fill='#d0d0d0')
draw.rectangle([60, 200, 140, 208], fill='#d0d0d0')

img.save('pdf_icon.ico', format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])
print("Icon generated successfully.")
