import os, time
from PIL import Image, ImageDraw, ImageFont, ImageShow


def save(sug):
    image(sug).save(os.getcwd() + '/output/'+str(time.time()).replace('.', '')+'.png')

def draw(sug):
    ImageShow.show(image(sug), 'Suguru')

def image(sug):
    background = (255, 255, 255)
    W = 600
    H = 600
    font_path = '/usr/share/fonts/adobe-source-code-pro/SourceCodePro-Black.otf'
    fontsize = 24
    font = ImageFont.truetype(font_path, fontsize)
    text = str(sug)
    location = (55, 40) # hardcoded

    image = Image.new('RGBA', (W, H), background)
    draw = ImageDraw.Draw(image)
    draw.text(location, text, fill='black', font=font)
    return image


def CORNER(r, d, l, u):
    c = (r, d, l, u)
    CORNERS = {(0,0,0,0): '┼',
               (0,0,0,1): '╀',
               (0,0,1,0): '┽',
               (0,0,1,1): '╃',
               (0,1,0,0): '╁',
               (0,1,0,1): '╂',
               (0,1,1,0): '╅',
               (0,1,1,1): '╉',
               (1,0,0,0): '┾',
               (1,0,0,1): '╄',
               (1,0,1,0): '┿',
               (1,0,1,1): '╇',
               (1,1,0,0): '╆',
               (1,1,0,1): '╊',
               (1,1,1,0): '╈',
               (1,1,1,1): '╋'}
    return CORNERS[c]

