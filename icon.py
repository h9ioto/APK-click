"""Рисует иконку-клавишу и раскладывает по папкам Android. Запуск: python3 icon.py <папка res> | --preview <файл.png>"""
import sys, os
from PIL import Image, ImageDraw

BG=(5,6,10)
TOP=(43,47,56); LEFT=(23,26,32); RIGHT=(10,11,14)
def draw_key(size, fill_frac, with_bg, round_mask=False):
    k=4; N=size*k
    img=Image.new("RGBA",(N,N),BG+(255,) if with_bg else (0,0,0,0))
    d=ImageDraw.Draw(img)
    # key bbox in source coords: x 60..260, y 63..234
    sc=N*fill_frac/200.0
    ox=N/2-160*sc; oy=N/2-148.5*sc
    T=lambda p:(ox+p[0]*sc, oy+p[1]*sc)
    d.polygon([T(p) for p in [(82,105),(160,147),(160,234),(60,180)]],fill=LEFT)
    d.polygon([T(p) for p in [(160,147),(238,105),(260,180),(160,234)]],fill=RIGHT)
    d.polygon([T(p) for p in [(160,63),(238,105),(160,147),(82,105)]],fill=TOP)
    d.polygon([T(p) for p in [(160,76),(218,105),(160,134),(102,105)]],fill=(30,33,40))
    E=[(30,24),(74,24),(74,38),(45,38),(45,45),(68,45),(68,57),(45,57),(45,64),(74,64),(74,76),(30,76)]
    tr=lambda x,y:(.78*x+.78*y+82, -.42*x+.42*y+105)
    d.polygon([T(tr(x,y)) for x,y in E],fill=(255,255,255))
    crack=[(73,142),(86,147),(94,143),(108,158),(118,156),(131,171),(142,176),(154,190),(160,188),(171,181),(182,185),(193,172),(206,174),(218,160),(231,157),(248,144)]
    lw=max(2,int(3.2*sc))
    d.line([T(p) for p in crack],fill=(120,190,255),width=lw*2+2,joint="curve")
    d.line([T(p) for p in crack],fill=(255,255,255),width=lw,joint="curve")
    img=img.resize((size,size),Image.LANCZOS)
    if round_mask:
        m=Image.new("L",(size,size),0); ImageDraw.Draw(m).ellipse((0,0,size-1,size-1),fill=255)
        out=Image.new("RGBA",(size,size),(0,0,0,0)); out.paste(img,(0,0),m); img=out
    return img

if sys.argv[1]=="--preview":
    draw_key(512,.78,True).save(sys.argv[2]); sys.exit()
res=sys.argv[1]
legacy={"mdpi":48,"hdpi":72,"xhdpi":96,"xxhdpi":144,"xxxhdpi":192}
for dens,px in legacy.items():
    dr=os.path.join(res,"mipmap-"+dens)
    os.makedirs(dr,exist_ok=True)
    draw_key(px,.76,True).save(os.path.join(dr,"ic_launcher.png"))
    draw_key(px,.70,True,True).save(os.path.join(dr,"ic_launcher_round.png"))
    fg=round(px*108/48)
    draw_key(fg,.40,False).save(os.path.join(dr,"ic_launcher_foreground.png"))
vals=os.path.join(res,"values"); os.makedirs(vals,exist_ok=True)
open(os.path.join(vals,"ic_launcher_background.xml"),"w").write('<?xml version="1.0" encoding="utf-8"?>\n<resources>\n    <color name="ic_launcher_background">#05060A</color>\n</resources>\n')
print("icons written to",res)
