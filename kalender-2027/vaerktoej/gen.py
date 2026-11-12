"""Bygger HTML-sider til kunstkalender 2027 (30 x 60 cm, 1181 x 2362 px)."""
import calendar, datetime, os

OUT = os.path.join(os.path.dirname(__file__), "pages")
os.makedirs(OUT, exist_ok=True)

MDR = ["JANUAR", "FEBRUAR", "MARTS", "APRIL", "MAJ", "JUNI", "JULI",
       "AUGUST", "SEPTEMBER", "OKTOBER", "NOVEMBER", "DECEMBER"]
UGEDAG = ["M", "T", "O", "T", "F", "L", "S"]

# (måned, dag): (tekst, helligdag)
DAGE = {
    (1, 1): ("Nytårsdag", True), (1, 6): ("Hellig tre konger", False),
    (1, 8): ("Prins Vincent og Prinsesse Josephine", False), (1, 24): ("Komtesse Athena", False),
    (2, 5): ("Dronning Mary", False), (2, 6): ("Prinsesse Marie", False), (2, 7): ("Fastelavn", False),
    (3, 20): ("Forårsjævndøgn", False), (3, 21): ("Palmesøndag", False),
    (3, 25): ("Skærtorsdag", True), (3, 26): ("Langfredag", True),
    (3, 28): ("Påskedag / Sommertid begynder", True), (3, 29): ("2. påskedag", True),
    (4, 9): ("Danmarks besættelse 1940", False), (4, 16): ("Dronning Margrethe", False),
    (4, 21): ("Prinsesse Isabella", False), (4, 29): ("Prinsesse Benedikte", False),
    (5, 4): ("Grev Henrik", False), (5, 5): ("Danmarks befrielse 1945", False),
    (5, 6): ("Kr. himmelfartsdag", True), (5, 16): ("Pinsedag", True),
    (5, 17): ("2. pinsedag", True), (5, 26): ("Kong Frederik X", False),
    (6, 5): ("Grundlovsdag", True), (6, 7): ("Prins Joachim", False),
    (6, 15): ("Valdemarsdag", False), (6, 21): ("Længste dag", False), (6, 24): ("Sankt Hans dag", False),
    (7, 22): ("Grev Felix", False), (8, 28): ("Grev Nikolai", False),
    (9, 5): ("Danmarks udsendte", False), (9, 23): ("Efterårsjævndøgn", False),
    (10, 15): ("Kronprins Christian", False), (10, 31): ("Sommertid slutter", False),
    (11, 11): ("Morten Bisp", False), (11, 28): ("1. søndag i advent", False),
    (12, 5): ("2. søndag i advent", False), (12, 12): ("3. søndag i advent", False),
    (12, 19): ("4. søndag i advent", False), (12, 24): ("Juleaften", False),
    (12, 25): ("Juledag", True), (12, 26): ("2. juledag", True), (12, 31): ("Nytårsaften", False),
}

# måned: (billedfil, billedtekst, beskæring)
MALERIER = {
    1: ("01.jpg", "“Vinterstemning”. Akryl 50 x 40 cm.", "50% 50%"),
    2: ("02.jpg", "Inspiration “Birketræer i vinterdragt”. Akryl 50 x 40 cm.", "62% 50%"),
    3: ("03.jpg", "“Japansk Sumi-e kalligrafi”. Sort tusch og akvarel.", "helt:rgb(223,237,252)"),
    4: ("04.jpg", "“Dame i forventningsstemning”. Akryl 40 x 50 cm.", "50% 50%"),
    5: ("05.jpg", "“Vilde, vidunderlige valmuer og markblomster”. Akryl 40 x 50 cm.", "50% 50%"),
    6: ("06.jpg", "“Valmueabstraktion”. Akryl 50 x 60 cm.", "50% 50%"),
    7: ("07.jpg", "“Aftenstemning”. Softpastel.", "58% 50%"),
    8: ("08.jpg", "“Solnedgang”. Akvarel.", "52% 50%"),
    9: ("09.jpg", "“Den første efterårsbuket”. Akvarel.", "50% 50%"),
    10: ("10.jpg", "“Efterårsstemning”. Akvarel.", "35% 50%"),
    11: ("11.jpg", "“Himmel og hav”. Akryl 50 x 40 cm.", "20% 50%"),
    12: ("12.jpg", "“Himmel og hav”. Akryl 50 x 60 cm.", "50% 50%"),
}

FONTS = """
@font-face{font-family:RC;src:url(../fonts/rc-regular.ttf);font-weight:400}
@font-face{font-family:RC;src:url(../fonts/rc-bold.ttf);font-weight:700}
@font-face{font-family:RC;src:url(../fonts/rc-italic.ttf);font-style:italic}
*{box-sizing:border-box;margin:0;padding:0}
body{background:#fff;-webkit-font-smoothing:antialiased}
"""


def side(navn, w, h, css, body):
    html = (f"<!doctype html><html><head><meta charset=utf-8><style>{FONTS}"
            f"html,body{{width:{w}px;height:{h}px;overflow:hidden}}{css}</style></head>"
            f"<body>{body}</body></html>")
    with open(os.path.join(OUT, navn), "w", encoding="utf-8") as f:
        f.write(html)


MDR_CSS = """
.billede{position:absolute;left:0;top:0;width:1181px;height:1575px;overflow:hidden;background:#eee}
.billede img{width:100%;height:100%;object-fit:cover;display:block}
.tom{display:flex;align-items:center;justify-content:center;flex-direction:column;gap:18px;
  font:700 54px RC;color:#9a9a9a;background:repeating-linear-gradient(45deg,#f1f1f1 0 30px,#e9e9e9 30px 60px)}
.tom small{font:400 34px RC}
.tekst{position:absolute;left:98px;top:1587px;font:italic 400 13px RC;color:#555}
.titel{position:absolute;left:98px;right:102px;top:1612px;display:flex;justify-content:space-between;
  font:700 58px RC;color:#a2a2a2;letter-spacing:.5px}
.kol{position:absolute;top:1708px;width:466px;border-top:2px solid #333}
.k1{left:98px}.k2{left:613px}
.r{height:32px;border-bottom:2px solid #333;display:flex;align-items:center;font:700 17px RC;color:#222;padding:0 2px}
.r.l{background:#ececec}.r.s{background:#d2d2d2}
.r .u{width:22px}.r .d{width:26px;text-align:right;margin-right:12px}
.r .n{flex:1}.r .w{width:30px;text-align:right}
.logo{position:absolute;left:1030px;top:2215px;width:105px}
"""


def maaned(m):
    fil, tekst, pos = MALERIER[m]
    dage = calendar.monthrange(2027, m)[1]
    rows = []
    for d in range(1, dage + 1):
        dt = datetime.date(2027, m, d)
        wd = dt.weekday()
        navn, hellig = DAGE.get((m, d), ("", False))
        klasse = "s" if (wd == 6 or hellig) else ("l" if wd == 5 else "")
        uge = str(dt.isocalendar()[1]) if wd == 0 else ""
        rows.append(f'<div class="r {klasse}"><span class=u>{UGEDAG[wd]}</span>'
                    f'<span class=d>{d}</span><span class=n>{navn}</span><span class=w>{uge}</span></div>')
    if fil:
        if pos.startswith("helt:"):
            billede = f'<div class=billede style="background:#fff;display:flex;align-items:center;justify-content:center"><img src="../img/{fil}" style="width:90%;height:auto;box-shadow:0 3px 14px rgba(0,0,0,.28)"></div>'
        else:
            billede = f'<div class=billede><img src="../img/{fil}" style="object-position:{pos}"></div>'
    else:
        billede = '<div class="billede tom">Billede til juli kommer<small>Maleriet fotograferes igen</small></div>'
    body = (billede + f'<div class=tekst>{tekst}</div>'
            f'<div class=titel><span>{MDR[m-1]}</span><span>2027</span></div>'
            f'<div class="kol k1">{"".join(rows[:17])}</div><div class="kol k2">{"".join(rows[17:])}</div>'
            '<img class=logo src="../img/logo.png">')
    side(f"s-{m+3:02d}.html", 1181, 2362, MDR_CSS, body)


def forside():
    css = """
.b{position:absolute;inset:0}.b img{width:100%;height:100%;object-fit:cover;object-position:50% 45%}
.t{position:absolute;left:70px;bottom:44px;font:italic 400 15px RC;color:#fff;text-shadow:0 0 6px rgba(0,0,0,.4)}
.logo{position:absolute;right:60px;bottom:40px;width:140px}"""
    side("s-01.html", 1181, 1575, css,
         '<div class=b><img src="../img/forside.jpg"></div>'
         '<div class=t>Fra serien “Damer for sjov”. Akryl 40 x 60 cm.</div>'
         '<img class=logo src="../img/logo.png">')


def omslag():
    css = """
.b{position:absolute;inset:0}.b img{width:100%;height:100%;object-fit:cover;object-position:50% 50%}
.y{position:absolute;left:0;right:0;bottom:250px;text-align:center;font:400 330px Inter,sans-serif;
  color:rgba(238,236,248,.9);letter-spacing:-6px}"""
    side("s-02.html", 1181, 2362, css,
         '<div class=b><img src="../img/forside.jpg"></div><div class=y>2027</div>')


def tekstside():
    css = """
body{font-family:Inter,sans-serif;color:#222}
.p{position:absolute;inset:70px 80px}
h1{font:800 70px Inter;color:#8e6aa5;letter-spacing:-1px}
.intro{margin-top:18px;font:400 15px Inter;line-height:1.45;columns:2;column-gap:36px}
.intro p{margin-bottom:7px}
.f{margin-top:6px;font:italic 400 14px Inter;color:#8e6aa5;line-height:1.4}
.tre{margin-top:22px;display:grid;grid-template-columns:repeat(3,1fr);gap:12px;grid-template-rows:290px}
.tre img{min-height:0;display:block}
.tre img{width:100%;height:100%;object-fit:cover}
h2{margin-top:26px;font:700 21px Inter;color:#8e6aa5}
.cols{margin-top:6px;columns:2;column-gap:36px;font:400 13.5px Inter;line-height:1.42}
.cols p{margin-bottom:9px}
.fod{position:absolute;bottom:0;font:400 15px Inter;color:#999}"""
    body = """<div class=p>
<h1>Kunstkalender 2027</h1>
<div class=intro>
<p>I dette års kalender har jeg valgt billeder, hvor motiverne er ret forskellige – både i motiver og brug af farver/malemåder/teknikker.</p>
<p>Der er motiver malet med akryl, softpastel, akvarel, japansk SUMI-E kalligrafi. Mine motiver spreder sig over en bred palet. Jeg maler landskaber, himmel/hav, blomster på forskellige måder, ”Damer for sjov”. Jeg maler ofte i serier.</p>
<p>Billederne i kalenderen er et udsnit af nogle af mine malerier. Målene på selve malerierne står under billedet, hvis det er malet på lærred.</p>
<p>Jeg henter inspiration i mine omgivelser, steder jeg har været – og fri fantasi.</p>
</div>
<div class=f>Følg mig på instagram: galleri.eg og min hjemmeside: www.gallerieg.dk og hold dig opdateret om mine udstillinger i 2027.</div>
<div class=tre><img src="../img/02.jpg" style="object-position:62% 50%"><img src="../img/11.jpg" style="object-position:30% 50%"><img src="../img/12.jpg"></div>
<h2>Og lidt om mig selv.</h2>
<div class=cols>
<p>Jeg maler fortrinsvis landskaber, himmel/hav ekspressivt og med abstraktioner, men også huse, ansigter, mennesker, blomster – også med abstraktioner. Jeg har i løbet af det sidste års tid malet en del akvarel og med pastelkridt – har også været på kursus i det.</p>
<p>Jeg har gennem de sidste 17 år deltaget i flere kurser – både i ind- og udlandet. Jeg har bl.a. været på ”Kunsthøjskolen på Ærø”, ”Kunstskolen Sønderbygaard”, Vinderup, ”Kragekær Kunstskole”, Tåsinge, flere gange. Jeg har deltaget i malekurser på Gram Højskole flere gange, en enkelt gang på Ryslinge Højskole. Jeg har været på kursus i Sydfrankrig og Sydafrika. Jeg er tilknyttet en kunstskole og et par malehold, hvor jeg henter inspiration og får udvidet mit kendskab til forskellige maleteknikker.</p>
<p>Jeg har udstillet mine malerier forskellige steder – både fælles udstillinger og alene. Jeg har udstillet gennem Stevns Kunstforening nogle gange, bl.a. på ”Kulturloftet” i Store Heddinge. Derudover har jeg udstillet flere steder på Stevns, i Køge, i Greve, i Herlev, i Brøndby, på CPH Art Space på Docken i København, Byens hus i Gentofte, Galleri Pialeh Frederiksberg, Sognegården i Stenløse, Sjællands Universitets Hospital i Køge, X-Porten i Hundested, Galleri Lowlands, Rørholmsgade København.</p>
<p>Jeg laver små skulpturer, blomster og fugle i stentøj.</p>
</div>
<div class=fod>Elisabeth Gram • Store Heddinge • 20604377 • eg@gallerieg.dk • www.gallerieg.dk • instagram: galleri.eg</div>
</div>"""
    side("s-03.html", 1181, 1181, css, body)


forside(); omslag(); tekstside()
for m in range(1, 13):
    maaned(m)
print("ok", sorted(os.listdir(OUT)))
