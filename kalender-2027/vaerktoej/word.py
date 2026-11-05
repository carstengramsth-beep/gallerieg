"""Laver Word-fil med alle tekster til kunstkalender 2027 - til print og rettelse i hånden."""
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_LINE_SPACING

LILLA = RGBColor(0x8E, 0x6A, 0xA5)
doc = Document()
sec = doc.sections[0]
sec.page_width, sec.page_height = Cm(21), Cm(29.7)
sec.left_margin = sec.right_margin = Cm(2.5)
sec.top_margin = sec.bottom_margin = Cm(2)

st = doc.styles["Normal"]
st.font.name = "Calibri"
st.font.size = Pt(12)
st.paragraph_format.line_spacing = 1.5
st.paragraph_format.space_after = Pt(4)


def overskrift(tekst, niveau=1):
    h = doc.add_heading(tekst, level=niveau)
    for r in h.runs:
        r.font.color.rgb = LILLA
    return h


def felt(label, tekst):
    p = doc.add_paragraph()
    p.add_run(label + " ").bold = True
    p.add_run(tekst)
    return p


def skrivelinjer(n=2):
    for _ in range(n):
        p = doc.add_paragraph("_" * 62)
        p.runs[0].font.color.rgb = RGBColor(0xBB, 0xBB, 0xBB)


doc.add_heading("Kunstkalender 2027 – alle tekster til rettelse", 0)
doc.add_paragraph("Udkast 2 · 28. oktober 2026 · Sidetallene passer til det printede A3-udkast.")
p = doc.add_paragraph()
p.add_run("Sådan retter du: ").bold = True
p.add_run("Streg over og skriv det rigtige ved siden af, eller på stregerne. "
          "Tekst i [firkantede parenteser] mangler eller er et forslag.")

overskrift("Side 1 – Forside")
felt("Billedtekst:", "Fra serien “Damer for sjov”. Akryl 40 x 60 cm.")
skrivelinjer(1)

overskrift("Side 2 – Omslag")
felt("Stor tekst på billedet:", "2027")
skrivelinjer(1)

overskrift("Side 3 – Tekstsiden")
felt("Overskrift:", "Kunstkalender 2027")
felt("Elisabeths tekst om 2027:", "[Elisabeths tekst om kalender 2027 kommer her. Fx: hvilke motiver og "
     "serier der er valgt i år, udstillinger i 2026 og planer for 2027.]")
skrivelinjer(6)
felt("Henvisning:", "Følg mig på instagram: galleri.eg og min hjemmeside: www.elisabeth.minisite.dk "
     "og hold dig opdateret om mine udstillinger i 2027.")
felt("Mellemoverskrift:", "Og lidt om mig selv.")
doc.add_paragraph().add_run("Om mig selv:").bold = True
for afsnit in [
    "Jeg maler fortrinsvis landskaber, himmel/hav ekspressivt og med abstraktioner, men også huse, ansigter, "
    "mennesker, blomster – også med abstraktioner. Jeg maler abstrakte malerier, hvor motivet ikke er figurativt.",
    "Jeg har gennem de sidste 13 år deltaget i flere kurser – både i ind- og udlandet. Jeg har bl.a. været på "
    "”Kunsthøjskolen på Ærø”, ”Kunstskolen Sønderbygaard”, Vinderup, ”Kragekær Kunstskole”, Tåsinge, flere gange. "
    "Jeg har været på kursus i Sydfrankrig og Sydafrika. Jeg er tilknyttet et par kunstskoler og et par malehold, "
    "hvor jeg henter inspiration og får udvidet mit kendskab til forskellige maleteknikker.",
    "Jeg har udstillet mine malerier forskellige steder – både fælles udstillinger og alene. Jeg har udstillet "
    "gennem Stevns Kunstforening nogle gange, bl.a. på ”Kulturloftet” i Store Heddinge. Derudover har jeg udstillet "
    "flere steder på Stevns, i Køge, i Greve, i Herlev, i Brøndby, på CPH Art Space på Docken i København, Byens hus "
    "i Gentofte, Galleri Pialeh Frederiksberg, Sognegården i Stenløse.",
    "Jeg er i 2019 igen begyndt at lave stentøj, som ellers har været lagt på hylden i nogle år p g a en "
    "skulderskade. Jeg laver små skulpturer, blomster og fugle i stentøj.",
]:
    doc.add_paragraph(afsnit)
felt("Bundlinje:", "Elisabeth Gram • Store Heddinge • 20604377 • eg@paritas.dk • elisabeth.minisite.dk • "
     "instagram: galleri.eg")
felt("De tre små billeder:", "Vinterstemning (januar), Himmel og hav (november), Himmel og hav (december).")
skrivelinjer(2)

MDR = [
    ("Januar", "“Vinterstemning”. Akryl 50 x 40 cm.",
     ["1 Nytårsdag", "6 Hellig tre konger", "8 Prins Vincent og Prinsesse Josephine", "24 Komtesse Athena"]),
    ("Februar", "Inspiration “Birketræer i vinterdragt”. Akryl 50 x 40 cm.",
     ["5 Dronning Mary", "6 Prinsesse Marie", "7 Fastelavn"]),
    ("Marts", "“Japansk Sumi-e kalligrafi”. Sort tusch og akvarel. [størrelse]",
     ["20 Forårsjævndøgn", "21 Palmesøndag", "25 Skærtorsdag", "26 Langfredag",
      "28 Påskedag / Sommertid begynder", "29 2. påskedag"]),
    ("April", "“Dame i forventningsstemning”. Akryl 40 x 50 cm.",
     ["9 Danmarks besættelse 1940", "16 Dronning Margrethe", "21 Prinsesse Isabella", "29 Prinsesse Benedikte"]),
    ("Maj", "“Vilde, vidunderlige valmuer og markblomster”. Akryl 40 x 50 cm.",
     ["4 Grev Henrik", "5 Danmarks befrielse 1945", "6 Kr. himmelfartsdag", "16 Pinsedag", "17 2. pinsedag",
      "26 Kong Frederik X"]),
    ("Juni", "“Valmueabstraktion”. Akryl 50 x 60 cm.",
     ["5 Grundlovsdag", "7 Prins Joachim", "15 Valdemarsdag", "21 Længste dag", "24 Sankt Hans dag"]),
    ("Juli", "“Aftenstemning”. Softpastel. [størrelse]", ["22 Grev Felix"]),
    ("August", "“Solnedgang”. Akvarel. [størrelse]", ["28 Grev Nikolai"]),
    ("September", "“Den første efterårsbuket”. Akvarel. [størrelse]",
     ["5 Danmarks udsendte", "23 Efterårsjævndøgn"]),
    ("Oktober", "“Efterårsstemning”. Akvarel. [størrelse]", ["15 Kronprins Christian", "31 Sommertid slutter"]),
    ("November", "“Himmel og hav”. Akryl 50 x 40 cm.", ["11 Morten Bisp", "28 1. søndag i advent"]),
    ("December", "“Himmel og hav”. Akryl 50 x 60 cm.",
     ["5 2. søndag i advent", "12 3. søndag i advent", "19 4. søndag i advent", "24 Juleaften", "25 Juledag",
      "26 2. juledag", "31 Nytårsaften"]),
]

doc.add_page_break()
overskrift("Side 4 til 15 – Månederne")
doc.add_paragraph("Mangler der en mærkedag, fx en fødselsdag i familien? Så skriv den ind i den rigtige måned.")
for i, (navn, tekst, dage) in enumerate(MDR):
    overskrift(f"Side {i + 4} – {navn}", 2)
    felt("Billedtekst:", tekst)
    felt("Mærkedage:", " · ".join(dage))
    skrivelinjer(1)

ud = "/tmp/claude-0/-home-user-lubnan-ordreflow/259446df-a932-552e-a062-1f4173d942b6/scratchpad/Kunstkalender-2027-alle-tekster.docx"
doc.save(ud)
print(ud)
