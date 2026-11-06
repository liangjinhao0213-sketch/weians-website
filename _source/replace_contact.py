# -*- coding: utf-8 -*-
"""Replace every placeholder contact detail with the real Weinas details."""
import io
import os

ROOT = r"C:\Users\LJHRMXS\Documents\deepseek-harness\default-workspace\weinas-site"

EMAIL = "liangjinhao0213@gmail.com"
PHONE_DISPLAY = "+86 178 1881 9386"
PHONE_TEL = "+8617818819386"
WA_LINK = "https://wa.me/8617818819386"
ADDRESS_INLINE = ("No. 7, Dalingdi, Zhongxiu Second Village Group, Tangbian Village, "
                  "Shishan Town, Foshan, Guangdong, China")
ADDRESS_FOOTER = ("No. 7, Dalingdi, Zhongxiu Second Village Group,<br>"
                  "Tangbian Village, Shishan Town,<br>Foshan, Guangdong, China")
STREET = "No. 7, Dalingdi, Zhongxiu Second Village Group, Tangbian Village, Shishan Town"

COMMON = [
    # footer address block first (more specific than the inline form)
    ("Nanhai District, Foshan,<br>Guangdong, China", ADDRESS_FOOTER),
    ("Nanhai District, Foshan, Guangdong, China", ADDRESS_INLINE),
    ("<dt>Factory</dt>", "<dt>Address</dt>"),
    ("sales@weinas.com", EMAIL),
    ("tel:+8613800000000", "tel:" + PHONE_TEL),
    ("tel:+8675700000000", "tel:" + PHONE_TEL),
    ("https://wa.me/8613800000000", WA_LINK),
    ("+86 138 0000 0000", PHONE_DISPLAY),
    ("+86 757 0000 0000", PHONE_DISPLAY),
    ('"+86-757-0000-0000"', '"+86-178-1881-9386"'),
]

for rel in ("index.html", r"_source\build_site.py"):
    p = os.path.join(ROOT, rel)
    s = io.open(p, encoding="utf-8").read()
    before = s

    # JSON-LD street address needs different handling per file (builder is python source)
    if rel == "index.html":
        s = s.replace('"addressLocality": "Foshan",',
                      '"streetAddress": "%s",\n    "addressLocality": "Foshan",' % STREET)
    else:
        s = s.replace("""a('    "addressLocality": "Foshan",')""",
                      """a('    "streetAddress": "%s",')
    a('    "addressLocality": "Foshan",')""" % STREET)

    for old, new in COMMON:
        s = s.replace(old, new)

    io.open(p, "w", encoding="utf-8").write(s)
    print(rel, "changed" if s != before else "UNCHANGED")

# quick verification
checks = ["sales@weinas.com", "138 0000", "757 0000", "8613800000000", "8675700000000", "Nanhai"]
for rel in ("index.html", r"_source\build_site.py"):
    s = io.open(os.path.join(ROOT, rel), encoding="utf-8").read()
    left = [c for c in checks if c in s]
    print(rel, "leftovers:", left or "none")
