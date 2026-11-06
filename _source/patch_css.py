# -*- coding: utf-8 -*-
"""Targeted CSS fixes (UTF-8 safe patcher)."""
import io
import os

ROOT = r"C:\Users\LJHRMXS\Documents\deepseek-harness\default-workspace\weinas-site"
CSS = os.path.join(ROOT, "assets", "css", "style.css")

s = io.open(CSS, encoding="utf-8").read()


def sub(old, new, count=1):
    global s
    if old not in s:
        raise SystemExit("NOT FOUND:\n" + old[:160])
    s = s.replace(old, new, count)


# --- category media: constrain drawings to the 4:3 box -----------------------
sub(""".cat__media {
  display: grid;
  place-items: center;
  aspect-ratio: 4 / 3;
  margin: 4px 0 18px;
}
.cat__media img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  transition: transform 480ms var(--ease);
}""",
""".cat__media {
  position: relative;
  aspect-ratio: 4 / 3;
  margin: 4px 0 18px;
}
.cat__media img {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: contain;
  padding: 4px 2px;
  transition: transform 480ms var(--ease);
}""")

# --- catalogue media: same treatment ---------------------------------------
sub(""".prod__media img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  transition: transform 600ms var(--ease);
}""",
""".prod__media img {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: contain;
  padding: clamp(14px, 1.8vw, 26px);
  transition: transform 600ms var(--ease);
}""")
sub(""".prod__media {
  position: relative;
  display: grid;
  place-items: center;
  aspect-ratio: 4 / 5;
  padding: clamp(16px, 1.8vw, 26px);
  background: var(--offwhite);
  overflow: hidden;
}""",
""".prod__media {
  position: relative;
  aspect-ratio: 4 / 5;
  background: var(--offwhite);
  overflow: hidden;
}""")

# --- cases: true masonry columns -------------------------------------------
sub(""".cases__grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: clamp(20px, 2.4vw, 36px);
  align-items: start;
}
.cases__col { display: grid; gap: clamp(24px, 3vw, 44px); }
.cases__col:nth-child(2) { margin-top: clamp(24px, 4vw, 68px); }
.cases__col:nth-child(3) { margin-top: clamp(8px, 2vw, 36px); }

.case { display: grid; gap: 14px; }""",
""".cases__grid {
  columns: 3;
  column-gap: clamp(18px, 2.2vw, 32px);
}
.case {
  display: grid;
  gap: 14px;
  break-inside: avoid;
  margin-bottom: clamp(20px, 2.6vw, 38px);
}
.case:nth-child(3n + 2) { margin-top: clamp(0px, 2vw, 34px); }""")

# --- collection rail: technical + photo variants ---------------------------
sub(""".rail-card__media img {
  width: 100%;
  aspect-ratio: 4 / 5;
  object-fit: cover;
  transition: transform 700ms var(--ease);
}""",
""".rail-card__media { position: relative; }
.rail-card__media img {
  width: 100%;
  aspect-ratio: 4 / 5;
  object-fit: cover;
  transition: transform 700ms var(--ease);
}
.rail-card--tech .rail-card__media { background: var(--offwhite); border: 1px solid var(--line); }
.rail-card--tech .rail-card__media img {
  object-fit: contain;
  padding: clamp(16px, 2vw, 30px);
}""")

# --- footer columns -------------------------------------------------------
sub(""".footer__grid {
  display: grid;
  grid-template-columns: minmax(0, 3.4fr) minmax(0, 3.2fr) minmax(0, 2fr) minmax(0, 2.6fr);
  gap: clamp(28px, 4vw, 64px);
  padding-bottom: clamp(40px, 4vw, 64px);
}""",
""".footer__grid {
  display: grid;
  grid-template-columns: minmax(0, 3fr) minmax(0, 4fr) minmax(0, 2.1fr) minmax(0, 3.2fr);
  gap: clamp(24px, 3.4vw, 56px);
  padding-bottom: clamp(40px, 4vw, 64px);
}""")
sub(""".footer__links a {
  font-size: 0.8125rem;""",
""".footer__links a {
  font-size: 0.7813rem;""")
sub(""".footer__links--2col { grid-template-columns: 1fr 1fr; column-gap: 20px; }""",
""".footer__links--2col { grid-template-columns: 1fr 1fr; column-gap: 28px; }""")

# --- custom file field ----------------------------------------------------
sub(""".field--file {
  border: 1px dashed var(--line-strong);
  padding: 16px;
  gap: 4px;
}
.field--file label { color: var(--muted-2); }
.field--file input { border: 0; padding: 0; font-size: 0.8125rem; color: var(--muted); }
.field--file input::file-selector-button {
  margin-right: 12px;
  padding: 8px 12px;
  border: 1px solid var(--line-strong);
  background: var(--offwhite);
  color: var(--ink);
  font: inherit;
  font-size: 0.75rem;
  cursor: pointer;
}""",
""".field--file {
  border: 1px dashed var(--line-strong);
  padding: 14px 16px;
  gap: 10px;
}
.file-row { display: flex; align-items: center; gap: 14px; flex-wrap: wrap; }
.file-btn {
  display: inline-flex;
  align-items: center;
  padding: 8px 14px;
  border: 1px solid var(--line-strong);
  background: var(--offwhite);
  font-size: 0.6875rem;
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  cursor: pointer;
  transition: background var(--f-fast), border-color var(--f-fast), color var(--f-fast);
}
.file-btn:hover { background: var(--navy); border-color: var(--navy); color: #fff; }
.file-name { font-size: 0.75rem; color: var(--muted-2); }""")

# --- responsive masonry --------------------------------------------------
sub("""  .cases__grid { grid-template-columns: 1fr 1fr; }
  .cases__col:nth-child(2),
  .cases__col:nth-child(3) { margin-top: 0; }
  .cases__col:nth-child(3) { display: none; }""",
"""  .cases__grid { columns: 2; }""")
sub("""  .cases__grid { grid-template-columns: 1fr; }
  .cases__col:nth-child(3) { display: grid; }""",
"""  .cases__grid { columns: 1; }
  .case:nth-child(3n + 2) { margin-top: 0; }""")

# --- footer responsive ---------------------------------------------------
sub("""  .footer__grid { grid-template-columns: 1fr 1fr; row-gap: 40px; }""",
"""  .footer__grid { grid-template-columns: 1fr 1fr; row-gap: 40px; }
  .footer__brand { grid-column: 1 / -1; }""")

io.open(CSS, "w", encoding="utf-8").write(s)
print("css patched", len(s), "chars")
