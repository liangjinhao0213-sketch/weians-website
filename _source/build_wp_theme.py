# -*- coding: utf-8 -*-
"""Generate a WordPress theme that reproduces the static site 1:1.

Phase 1 output (weinas-wp/wp-content/themes/weinas/):
  style.css        theme header + pointer to assets/css/style.css
  functions.php    enqueue assets, menus, theme supports
  header.php       doctype + wp_head + site header + mobile nav + search
  footer.php       footer + toast + quote triggers + wp_footer
  front-page.php   the whole homepage, section by section
  index.php        fallback loop
  page.php         generic page
  assets/          full copy of css / js / fonts / img

Asset URLs are rewritten to get_template_directory_uri(); internal links are
kept as permalink-style paths so phase 2 can map them to CPT archives.

Run:  python build_wp_theme.py
"""
import io
import os
import re
import shutil
import sys

ROOT = r"C:\Users\LJHRMXS\Documents\deepseek-harness\default-workspace"
SITE = os.path.join(ROOT, "weinas-site")
THEME = os.path.join(ROOT, "weinas-wp", "wp-content", "themes", "weinas")

ASSET = "<?php echo esc_url(get_template_directory_uri()); ?>/assets/"


def read_index():
    return io.open(os.path.join(SITE, "index.html"), encoding="utf-8").read()


def rewrite_assets(html):
    """assets/... -> <?php echo ... ?>/assets/... for every URL-bearing attribute."""
    html = re.sub(r'(src|href)="(?:\.\./)*(assets/)',
                  r'\1="' + ASSET.replace("\\", "\\\\") + r"", html)
    # responsive images: srcset / imagesrcset hold a comma separated list
    for attr in ("srcset", "imagesrcset"):
        html = re.sub(r'(%s)="(?:\.\./)*(assets/)' % attr,
                      r'\1="' + ASSET.replace("\\", "\\\\") + r"", html)
        html = html.replace('", assets/', '", ' + ASSET)
        html = html.replace(', assets/', ', ' + ASSET)
    # inline background images
    html = html.replace("url(assets/", "url(" + ASSET)
    return html


def rewrite_links(html):
    """index.html|products/index.html|about-us/... -> permalink style paths."""
    mapping = [
        ('href="index.html"', 'href="<?php echo esc_url(home_url(\'/\')); ?>"'),
        ('href="products/index.html"', 'href="<?php echo esc_url(home_url(\'/products/\')); ?>"'),
        ('href="about-us/index.html"', 'href="<?php echo esc_url(home_url(\'/about-us/\')); ?>"'),
        ('href="contact-us/index.html"', 'href="<?php echo esc_url(home_url(\'/contact-us/\')); ?>"'),
        ('href="blog/index.html"', 'href="<?php echo esc_url(home_url(\'/blog/\')); ?>"'),
        ('href="cases/index.html"', 'href="<?php echo esc_url(home_url(\'/cases/\')); ?>"'),
        ("href='index.html'", "href='<?php echo esc_url(home_url(\"/\")); ?>'"),
    ]
    for a, b in mapping:
        html = html.replace(a, b)
    # any leftover relative .html link, whatever the folder prefix
    html = re.sub(r'href="(?:\.\./)*products/([a-z0-9-]+)/index\.html"',
                  'href="<?php echo esc_url(home_url("/products/\\1/")); ?>"', html)
    html = re.sub(r'href="(?:\.\./)*products/([a-z0-9-]+)/([a-z0-9-]+)\.html"',
                  'href="<?php echo esc_url(home_url("/products/\\1/\\2/")); ?>"', html)
    html = re.sub(r'href="(?:\.\./)*about-us/([a-z0-9-]+)\.html"',
                  'href="<?php echo esc_url(home_url("/about-us/\\1/")); ?>"', html)
    html = re.sub(r'href="(?:\.\./)*blog/([a-z0-9-]+)\.html"',
                  'href="<?php echo esc_url(home_url("/blog/\\1/")); ?>"', html)
    html = re.sub(r'href="(?:\.\./)*cases/([a-z0-9-]+)\.html"',
                  'href="<?php echo esc_url(home_url("/cases/\\1/")); ?>"', html)
    return html


def phpify(html):
    html = rewrite_links(rewrite_assets(html))
    html = html.replace('href="#top"', 'href="<?php echo esc_url(home_url(\'/\')); ?>"')
    return html


FOOTER_CATS = [
    ("Aluminium Sliding Doors", "aluminium-sliding-doors"),
    ("Aluminium Casement Windows", "aluminium-casement-windows"),
    ("Aluminium Sliding Windows", "aluminium-sliding-windows"),
    ("Interior Sliding Partition Doors", "interior-sliding-partition-doors"),
    ("Aluminium Casement Doors", "aluminium-casement-doors"),
    ("Aluminium Tilt And Turn Windows", "aluminium-tilt-and-turn-windows"),
    ("Thermal Insulation Windows", "thermal-insulation-windows"),
    ("Aluminium Swing Doors", "aluminium-swing-doors"),
    ("Aluminium Bathroom Doors", "aluminium-bathroom-doors"),
    ("Aluminium Front Doors", "aluminium-front-doors"),
    ("Aluminium Pivot Doors", "aluminium-pivot-doors"),
    ("Aluminium Folding Doors", "aluminium-folding-doors"),
]


def footer_links(html):
    """The static footer uses in-page anchors; on WordPress they must be real URLs."""
    php = "<?php echo esc_url(home_url('%s')); ?>"
    for label, slug in FOOTER_CATS:
        for old in ('<a href="#catalogue">%s</a>' % label, '<a href="#">%s</a>' % label):
            html = html.replace(old, '<a href="%s">%s</a>' % (php % ("/products/%s/" % slug), label))
    html = html.replace('href="#catalogue">Browse systems', 'href="%s">Browse systems' % (php % "/products/"))
    html = html.replace('href="#quote">Get A Quote', 'href="%s">Get A Quote' % (php % "/contact-us/"))
    html = html.replace('href="#quote">Get a quote', 'href="%s">Get a quote' % (php % "/contact-us/"))
    return html


def slice_between(s, start_marker, end_marker):
    i = s.find(start_marker)
    j = s.find(end_marker, i) + len(end_marker)
    return s[i:j]


def main():
    raw = read_index()
    body_tag = raw.find("<body")
    head_part = raw[:body_tag]
    body = raw[body_tag:]

    header = slice_between(body, '<header class="site-header', "</header>")
    main_html = slice_between(body, '<main id="main">', "</main>")
    footer = slice_between(body, '<footer class="site-footer', "</footer>")
    toast = body[body.find('<div class="toast"'):]
    toast = toast[:toast.find("</div>") + 6]

    # mobile nav + search live between </header> and <main>
    between = body[body.find("</header>"):body.find('<main id="main">')]

    os.makedirs(THEME, exist_ok=True)
    for sub in ("assets",):
        dst = os.path.join(THEME, sub)
        if os.path.isdir(dst):
            shutil.rmtree(dst)
        shutil.copytree(os.path.join(SITE, sub), dst)

    # ---------------------------------------------------------------- style.css
    io.open(os.path.join(THEME, "style.css"), "w", encoding="utf-8").write("""/*
Theme Name: Weinas
Theme URI: https://www.weinas.com/
Description: Aluminium doors and windows manufacturer theme. One-to-one port of the
             static site: Swiss grid, navy #0B2B5B, no gradients, no shadows.
Author: Weinas
Version: 1.0.0
Requires at least: 6.0
Requires PHP: 7.4
Text Domain: weinas
*/

/* The full stylesheet is enqueued from assets/css/style.css in functions.php. */
""")

    # ---------------------------------------------------------------- functions.php
    # Hand-maintained (CPTs, enquiries, helpers) - only write it if missing.
    fphp = os.path.join(THEME, "functions.php")
    if not os.path.exists(fphp):
        io.open(fphp, "w", encoding="utf-8").write("""<?php
/**
 * Weinas theme bootstrap.
 */

if (!defined('ABSPATH')) {
    exit;
}

define('WEINAS_VERSION', '1.0.0');

add_action('after_setup_theme', function () {
    add_theme_support('title-tag');
    add_theme_support('post-thumbnails');
    add_theme_support('html5', array('search-form', 'gallery', 'caption', 'style', 'script'));

    register_nav_menus(array(
        'primary' => __('Primary menu', 'weinas'),
        'footer_products' => __('Footer: products', 'weinas'),
        'footer_company' => __('Footer: company', 'weinas'),
    ));
});

add_action('wp_enqueue_scripts', function () {
    $uri = get_template_directory_uri();

    wp_enqueue_style('weinas-style', $uri . '/assets/css/style.css', array(), WEINAS_VERSION);

    wp_enqueue_script('weinas-main', $uri . '/assets/js/main.js', array(), WEINAS_VERSION, true);
});

/**
 * The static markup uses .html links; on WordPress those become permalinks.
 */
add_filter('body_class', function ($classes) {
    $classes[] = 'weinas';
    return $classes;
});
""")

    # ---------------------------------------------------------------- header.php
    header_php = """<!doctype html>
<html <?php language_attributes(); ?>>
<head>
<meta charset="<?php bloginfo('charset'); ?>">
<meta name="viewport" content="width=device-width, initial-scale=1">
<?php wp_head(); ?>
</head>
<body <?php body_class(); ?>>
<?php wp_body_open(); ?>
""" + phpify(header) + "\n" + phpify(between) + "\n"
    io.open(os.path.join(THEME, "header.php"), "w", encoding="utf-8").write(header_php)

    # ---------------------------------------------------------------- footer.php
    footer_php = footer_links(phpify(footer)) + "\n" + phpify(toast) + """
<script src="<?php echo esc_url(get_template_directory_uri()); ?>/assets/js/main.js" defer></script>
<?php wp_footer(); ?>
</body>
</html>
"""
    io.open(os.path.join(THEME, "footer.php"), "w", encoding="utf-8").write(footer_php)

    # ---------------------------------------------------------------- front-page.php
    front = """<?php get_header(); ?>
""" + phpify(main_html) + """
<?php get_footer(); ?>
"""
    io.open(os.path.join(THEME, "front-page.php"), "w", encoding="utf-8").write(front)

    # ---------------------------------------------------------------- index.php
    io.open(os.path.join(THEME, "index.php"), "w", encoding="utf-8").write("""<?php get_header(); ?>
<main id="main">
  <section class="section">
    <div class="container">
      <?php if (have_posts()) : ?>
        <?php while (have_posts()) : the_post(); ?>
          <article <?php post_class('card'); ?>>
            <h2 class="h3"><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h2>
            <div class="entry"><?php the_excerpt(); ?></div>
          </article>
        <?php endwhile; ?>
      <?php else : ?>
        <p class="lead">Nothing published yet.</p>
      <?php endif; ?>
    </div>
  </section>
</main>
<?php get_footer(); ?>
""")

    # ---------------------------------------------------------------- page.php
    io.open(os.path.join(THEME, "page.php"), "w", encoding="utf-8").write("""<?php get_header(); ?>
<main id="main">
  <?php while (have_posts()) : the_post(); ?>
    <section class="page-hero">
      <div class="container">
        <h1 class="page-hero__title"><?php the_title(); ?></h1>
      </div>
    </section>
    <section class="section">
      <div class="container entry">
        <?php the_content(); ?>
      </div>
    </section>
  <?php endwhile; ?>
</main>
<?php get_footer(); ?>
""")

    files = sorted(os.listdir(THEME))
    print("theme:", THEME)
    for f in files:
        p = os.path.join(THEME, f)
        print("  %-16s %s" % (f, ("dir" if os.path.isdir(p) else "%d KB" % (os.path.getsize(p) / 1024))))
    print("\nfront-page.php %.0f KB | header.php %.0f KB | footer.php %.0f KB"
          % (os.path.getsize(os.path.join(THEME, "front-page.php")) / 1024,
             os.path.getsize(os.path.join(THEME, "header.php")) / 1024,
             os.path.getsize(os.path.join(THEME, "footer.php")) / 1024))


if __name__ == "__main__":
    main()
