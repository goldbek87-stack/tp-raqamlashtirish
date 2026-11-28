# logo.jpg dan Android ilova belgilari va ochilish (splash) ekranini yasaydi
import os, glob
from PIL import Image, ImageDraw

RES = "android/app/src/main/res"
src = Image.open("logo.jpg").convert("RGB")
W = min(src.size); src = src.crop((0, 0, W, W))

def circle(img):
    s = img.size[0]
    m = Image.new("L", (s*4, s*4), 0); ImageDraw.Draw(m).ellipse((0, 0, s*4-1, s*4-1), fill=255)
    m = m.resize((s, s), Image.LANCZOS)
    out = Image.new("RGBA", (s, s), (0, 0, 0, 0)); out.paste(img, (0, 0), m); return out

for d, k in {"mdpi":1, "hdpi":1.5, "xhdpi":2, "xxhdpi":3, "xxxhdpi":4}.items():
    folder = f"{RES}/mipmap-{d}"; os.makedirs(folder, exist_ok=True)
    # moslashuvchan belgi: 108dp maydon, logotip markazda 84dp doira
    S, D = int(108*k), int(84*k)
    fg = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    fg.paste(circle(src.resize((D, D), Image.LANCZOS)), ((S-D)//2, (S-D)//2))
    fg.save(f"{folder}/ic_launcher_foreground.png")
    c = int(W*0.08); ic = src.crop((c, c, W-c, W-c)).resize((int(48*k),)*2, Image.LANCZOS)
    ic.save(f"{folder}/ic_launcher.png"); circle(ic).save(f"{folder}/ic_launcher_round.png")

# Capacitor'ning standart splash rasmlarini o'chirib, o'rniga oq fonda logotip
for f in glob.glob(f"{RES}/drawable*/splash.png"): os.remove(f)
os.makedirs(f"{RES}/drawable", exist_ok=True)
circle(src.resize((288, 288), Image.LANCZOS)).save(f"{RES}/drawable/splash_logo.png")
open(f"{RES}/drawable/splash.xml", "w").write('''<?xml version="1.0" encoding="utf-8"?>
<layer-list xmlns:android="http://schemas.android.com/apk/res/android">
    <item android:drawable="@android:color/white" />
    <item android:width="144dp" android:height="144dp" android:gravity="center">
        <bitmap android:src="@drawable/splash_logo" android:gravity="fill" />
    </item>
</layer-list>
''')
open(f"{RES}/values/ic_launcher_background.xml", "w").write('''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="ic_launcher_background">#EEF4EE</color>
</resources>
''')
print("Belgilar tayyor")
