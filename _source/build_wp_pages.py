# -*- coding: utf-8 -*-
"""Generate page templates from the static pages (about-us, contact-us, cases).

Emits into the theme:
  page-<slug>.php      for the about / contact pages
  data/pages-import.json   (title, slug, parent, excerpt, template)
  data/cases-import.json   (title, slug, excerpt, image, content html)

Run: python build_wp_pages.py
"""
import io
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
SITE = os.path.join(ROOT, "weinas-site")
THEME = os.path.join(ROOT, "weinas-wp", "wp-content", "themes", "weinas")
ASSET = "<?php echo esc_url(get_template_directory_uri()); ?>/assets/"

PAGES = [
    ("about-us/company-profile.html", "company-profile", "Company Profile", "about-us"),
    ("about-us/factory-tour.html", "factory-tour", "Factory Tour", "about-us"),
    ("about-us/quality-control.html", "quality-control", "Quality Control", "about-us"),
    ("contact-us/index.html", "contact-us", "Contact Us", ""),
    ("cases/index.html", "cases", "Cases", ""),
    ("blog/index.html", "blog", "Journal", ""),
    ("videos/index.html", "videos", "Videos", ""),
]


def read(path):
    return io.open(os.path.join(SITE, path), encoding="utf-8").read()


def phpify(html, depth, plain=False, sib=""):
    """plain=True emits real paths instead of PHP tags (for post_content)."""
    if plain:
        html = re.sub(r'(src|href|srcset|imagesrcset)="(?:\.\./)*assets/',
                      r'\1="/wp-content/themes/weinas/assets/', html)
        html = html.replace('", assets/', '", /wp-content/themes/weinas/assets/')
        html = html.replace(', assets/', ', /wp-content/themes/weinas/assets/')
        html = re.sub(r'href="(?:\.\./)*products/([a-z0-9-]+)/index\.html"', r'href="/products/\1/"', html)
        html = re.sub(r'href="(?:\.\./)*products/([a-z0-9-]+)/([a-z0-9-]+)\.html"', r'href="/products/\1/\2/"', html)
        html = re.sub(r'href="(?:\.\./)*about-us/([a-z0-9-]+)\.html"', r'href="/about-us/\1/"', html)
        html = re.sub(r'href="(?:\.\./)*blog/([a-z0-9-]+)\.html"', r'href="/blog/\1/"', html)
        html = re.sub(r'href="(?:\.\./)*cases/([a-z0-9-]+)\.html"', r'href="/cases/\1/"', html)
        html = re.sub(r'href="(?:\.\./)*cases/index\.html"', 'href="/cases/"', html)
        html = re.sub(r'href="(?:\.\./)*products/index\.html"', 'href="/products/"', html)
        html = re.sub(r'href="(?:\.\./)*blog/index\.html"', 'href="/blog/"', html)
        html = re.sub(r'href="(?:\.\./)*index\.html#quote"', 'href="/contact-us/"', html)
        html = re.sub(r'href="(?:\.\./)*index\.html#catalogue"', 'href="/products/"', html)
        html = re.sub(r'href="(?:\.\./)*index\.html"', 'href="/"', html)
        html = re.sub(r'href="(about-us/[a-z0-9-]+)\.html"', r'href="/\1/"', html)
        html = re.sub(r'href="([a-z0-9-]+)\.html"', r'href="/cases/\1/"', html)
        return html

    pref = "../" * depth
    # assets
    html = re.sub(r'(src|href|srcset|imagesrcset)="(?:\.\./|' + re.escape(pref) + r')*(assets/)',
                  lambda m: '%s="%s' % (m.group(1), ASSET.replace("\\", "\\\\")), html)
    html = html.replace('", assets/', '", ' + ASSET).replace(', assets/', ', ' + ASSET)
    # links (strip the ../ prefix first, then rewrite by hand)
    html = re.sub(r'href="(?:\.\./)+(about-us/[a-z0-9-]+)\.html"',
                  r'href="<?php echo esc_url(home_url(\'/\1/\')); ?>"', html)
    html = re.sub(r'href="(?:\.\./)+(cases/[a-z0-9-]+)\.html"',
                  r'href="<?php echo esc_url(home_url(\'/\1/\')); ?>"', html)
    html = re.sub(r'href="(?:\.\./)+(blog/[a-z0-9-]+)\.html"',
                  r'href="<?php echo esc_url(home_url(\'/\1/\')); ?>"', html)
    html = re.sub(r'href="(?:\.\./)*index\.html#quote"', 'href="<?php echo esc_url(home_url(\'/contact-us/\')); ?>"', html)
    html = re.sub(r'href="(?:\.\./)*index\.html#catalogue"', 'href="<?php echo esc_url(home_url(\'/products/\')); ?>"', html)
    html = html.replace('href="index.html"', 'href="<?php echo esc_url(home_url(\'/\')); ?>"')
    html = html.replace('href="../index.html"', 'href="<?php echo esc_url(home_url(\'/\')); ?>"')
    html = html.replace('href="products/index.html"', 'href="<?php echo esc_url(home_url(\'/products/\')); ?>"')
    html = html.replace('href="../products/index.html"', 'href="<?php echo esc_url(home_url(\'/products/\')); ?>"')
    html = html.replace('href="contact-us/index.html"', 'href="<?php echo esc_url(home_url(\'/contact-us/\')); ?>"')
    html = html.replace('href="../contact-us/index.html"', 'href="<?php echo esc_url(home_url(\'/contact-us/\')); ?>"')
    html = html.replace('href="blog/index.html"', 'href="<?php echo esc_url(home_url(\'/blog/\')); ?>"')
    html = html.replace('href="../blog/index.html"', 'href="<?php echo esc_url(home_url(\'/blog/\')); ?>"')
    html = html.replace('href="cases/index.html"', 'href="<?php echo esc_url(home_url(\'/cases/\')); ?>"')
    html = html.replace('href="../cases/index.html"', 'href="<?php echo esc_url(home_url(\'/cases/\')); ?>"')
    html = html.replace('href="company-profile.html"', 'href="<?php echo esc_url(home_url(\'/about-us/company-profile/\')); ?>"')
    html = html.replace('href="factory-tour.html"', 'href="<?php echo esc_url(home_url(\'/about-us/factory-tour/\')); ?>"')
    html = html.replace('href="quality-control.html"', 'href="<?php echo esc_url(home_url(\'/about-us/quality-control/\')); ?>"')
    html = re.sub(r'href="((?:about-us|cases|blog)/[a-z0-9-]+)\.html"',
                  r'href="<?php echo esc_url(home_url(\'/\1/\')); ?>"', html)
    # products
    html = re.sub(r'href="(?:\.\./)*products/([a-z0-9-]+)/index\.html"',
                  r'href="<?php echo esc_url(home_url(\'/products/\1/\')); ?>"', html)
    html = re.sub(r'href="(?:\.\./)*products/([a-z0-9-]+)/([a-z0-9-]+)\.html"',
                  r'href="<?php echo esc_url(home_url(\'/products/\1/\2/\')); ?>"', html)
    # about / blog / cases, any prefix
    html = re.sub(r'href="(?:\.\./)*about-us/([a-z0-9-]+)\.html"',
                  r'href="<?php echo esc_url(home_url(\'/about-us/\1/\')); ?>"', html)
    html = re.sub(r'href="(?:\.\./)*blog/([a-z0-9-]+)\.html"',
                  r'href="<?php echo esc_url(home_url(\'/blog/\1/\')); ?>"', html)
    html = re.sub(r'href="(?:\.\./)*cases/([a-z0-9-]+)\.html"',
                  r'href="<?php echo esc_url(home_url(\'/cases/\1/\')); ?>"', html)
    # sibling links: blog/x.html inside blog/, cottesloe.html inside cases/
    if sib:
        html = re.sub(r'href="([a-z0-9-]+)\.html"',
                      lambda m: 'href="<?php echo esc_url(home_url(\'/%s/%s/\')); ?>"' % (sib, m.group(1)), html)
    return html


def main_part(html):
    i = html.find('<main id="main">')
    j = html.find('</main>', i)
    return html[i + len('<main id="main">'):j]


def page_title(html):
    m = re.search(r'<title>(.*?)</title>', html, re.S)
    return re.sub(r'\s+', ' ', m.group(1)).split('|')[0].strip() if m else ''


def main():
    os.makedirs(os.path.join(THEME, "data"), exist_ok=True)
    pages = []

    for path, slug, title, parent in PAGES:
        html = read(path)
        depth = 0 if "/" not in path else 1
        sib = "" if not parent else parent
        if slug in ("cases", "blog"):
            sib = slug
        body = phpify(main_part(html), depth, sib=sib)
        tpl = """<?php
/**
 * %s — generated from the static page.
 */
get_header(); ?>
%s
<?php get_footer(); ?>
""" % (title, body)
        io.open(os.path.join(THEME, "page-%s.php" % slug), "w", encoding="utf-8").write(tpl)
        pages.append(dict(slug=slug, title=title, parent=parent, template="page-%s.php" % slug))
        print("page template:", "page-%s.php" % slug)

    # ---------------------------------------------------------------- cases
    cases = []
    case_dir = os.path.join(SITE, "cases")
    for f in sorted(os.listdir(case_dir)):
        if not f.endswith(".html") or f == "index.html":
            continue
        html = read("cases/" + f)
        slug = f[:-5]
        title = page_title(html)
        body = phpify(main_part(html), 1, plain=True)
        img = re.search(r'assets/img/(cases/[^"\s]+\.jpg)', html)
        excerpt = re.search(r'<meta name="description" content="([^"]*)"', html)
        cases.append(dict(
            slug=slug,
            title=title,
            excerpt=(excerpt.group(1) if excerpt else title),
            image=("assets/img/" + img.group(1)) if img else "",
            content=body,
        ))

    io.open(os.path.join(THEME, "data", "pages-import.json"), "w", encoding="utf-8").write(
        json.dumps(pages, ensure_ascii=False))
    io.open(os.path.join(THEME, "data", "cases-import.json"), "w", encoding="utf-8").write(
        json.dumps(cases, ensure_ascii=False))
    print("pages:", len(pages), "| cases:", len(cases))


if __name__ == "__main__":
    main()
