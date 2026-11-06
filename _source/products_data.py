# -*- coding: utf-8 -*-
"""Product catalogue data: 12 categories x 6 systems.

Each category carries the copy for its landing page plus a base spec block;
each product adds two variant specs, a size range and a one-line claim.
Images are intentionally left as placeholders (see build_products.py).
"""

# Products scraped from the existing Weinas site (title, specs, price, images).
# Regenerate with _source/scrape_sliding.py; the file is optional.
import io
import json as _json
import os as _os

_SRC = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "source_products.json")
SOURCE = _json.load(io.open(_SRC, encoding="utf-8")) if _os.path.exists(_SRC) else []

GROUPS = [
    ("sliding", "Sliding systems", "Sliding on tracks that disappear into the frame."),
    ("casement", "Casement & swing", "Side-hung leaves, opened by hand and sealed by compression."),
    ("thermal", "Thermal & tilt", "Polyamide-broken frames for cold, heat and noise."),
    ("entrance", "Entrance & folding", "The opening that has to close, lock and last."),
]

CATEGORIES = [
    dict(
        slug="aluminium-sliding-doors", no="01", group="sliding",
        name="Aluminium Sliding Doors", short="Sliding doors",
        tagline="Large panels, flush tracks, hidden drainage.",
        lead=("Sixteen sliding systems, from a 1.8 mm windproof exterior door to a broken-bridge double-glazed "
              "door built for typhoon zones. Prices run USD85–135 per square metre, MOQ 4–6 m², delivery "
              "25–35 days ex-works Foshan."),
        chips=["16 models", "USD85–135 / m²", "MOQ 4–6 m²"],
        base=[("Profile alloy", "6063-T5, 3.0–5.0 mm wall"), ("Thermal break", "24 mm polyamide"),
              ("Glazing", "5 + 15A + 5, up to 32 mm"), ("Hardware", "German tandem rollers, 304 track")],
        products=[
            ("WS-90", "Heavy-Duty Sliding Door", "Our standard for coastal villas and hotel terraces.",
             [("Leaf weight", "up to 400 kg"), ("Track", "2 or 3 rail, flush")], "3.0 × 3.4 m"),
            ("WS-70", "Slim Sliding Door", "Narrower sightline for glazed walls that read as glass.",
             [("Sightline", "18 mm"), ("Track", "2 rail, low profile")], "2.8 × 3.0 m"),
            ("WS-120", "Lift-and-Slide Door", "Raises before it glides, so a six-metre leaf moves with one hand.",
             [("Max span", "6.0 m clear"), ("Operation", "lift, slide, lower")], "6.0 × 3.2 m"),
            ("WS-60", "Two-Track Sliding Door", "Apartment-scale sliding door for balconies and loggias.",
             [("Sightline", "26 mm"), ("Track", "2 rail, surface fixed")], "2.4 × 2.4 m"),
            ("WS-100", "Corner Sliding Door", "Two leaves meet at a 90° corner with no fixed post.",
             [("Corner", "90°, post-free"), ("Leaves", "2–4")], "4.2 × 3.0 m"),
            ("WS-90P", "Pocket Sliding Door", "The leaf slides into a wall pocket and disappears completely.",
             [("Pocket depth", "120 mm"), ("Leaf weight", "up to 250 kg")], "2.0 × 2.6 m"),
        ]),
    dict(
        slug="aluminium-casement-windows", no="02", group="casement",
        name="Aluminium Casement Windows", short="Casement windows",
        tagline="Side-hung leaves, compression seals, wide sightlines.",
        lead=("A casement closes onto a gasket rather than sliding past it, which is why it seals better "
              "than any other opening. We machine the drainage and the hardware ports in-house on the same "
              "CNC line that cuts the frames, so the sash sits square in its rebate."),
        chips=["Sightline 55 mm", "Uw 1.4 W/m²K", "Rw 40 dB option"],
        base=[("Profile alloy", "6063-T5, 1.8–2.0 mm wall"), ("Sealing", "EPDM compression gasket"),
              ("Glazing", "5 + 12A + 5, up to 44 mm"), ("Hardware", "German friction stays, multi-point lock")],
        products=[
            ("WC-75", "Casement Window", "The standard outward-opening window for villas and apartments.",
             [("Opening", "outward, single sash"), ("Sash weight", "up to 90 kg")], "0.6 × 0.6 to 1.4 × 2.4 m"),
            ("WC-65", "Slim Casement Window", "A 48 mm frame for renovation work where the reveal is tight.",
             [("Frame width", "48 mm"), ("Opening", "inward or outward")], "0.5 × 0.5 to 1.2 × 2.2 m"),
            ("WC-85", "Acoustic Casement Window", "Laminated glass and a double gasket line for airports and arterials.",
             [("Acoustic", "Rw 40 dB"), ("Glazing", "8 + 12A + 8.8 laminated")], "0.8 × 0.8 to 1.6 × 2.4 m"),
            ("WC-55", "Trade Casement Window", "The volume model: same profile, simpler hardware set.",
             [("Opening", "outward, single sash"), ("Hardware", "two-point lock")], "0.6 × 0.6 to 1.2 × 1.8 m"),
            ("WC-95", "Panoramic Casement Window", "One floor-to-head sash with no transom in the view.",
             [("Max sash", "1.6 × 2.8 m"), ("Sightline", "55 mm")], "1.0 × 2.4 to 1.6 × 2.8 m"),
            ("WC-75D", "Double Casement Window", "Two sashes meeting at a central mullion, both operable.",
             [("Sashes", "2, both opening"), ("Mullion", "60 mm")], "1.2 × 1.0 to 3.0 × 2.4 m"),
        ]),
    dict(
        slug="aluminium-sliding-windows", no="03", group="sliding",
        name="Aluminium Sliding Windows", short="Sliding windows",
        tagline="Two or three tracks, no swing clearance needed.",
        lead=("Where a casement would foul a balcony rail or a kitchen worktop, a slider keeps the opening "
              "in the plane of the wall. We build two- and three-track versions on the same profile family "
              "as the sliding doors, so the sightlines match across a facade."),
        chips=["2–3 track", "Span to 4.2 m", "Uw 1.5 W/m²K"],
        base=[("Profile alloy", "6063-T5, 1.6–2.0 mm wall"), ("Tracks", "2 or 3, stainless capped"),
              ("Glazing", "5 + 9A + 5, up to 24 mm"), ("Hardware", "nylon rollers, brush seal")],
        products=[
            ("WSW-70", "Sliding Window", "Two-track slider for bedrooms and kitchens.",
             [("Tracks", "2"), ("Sash weight", "up to 60 kg")], "0.8 × 0.8 to 2.4 × 1.8 m"),
            ("WSW-55", "Slim Sliding Window", "A 45 mm frame that keeps more glass in a small opening.",
             [("Frame width", "45 mm"), ("Tracks", "2")], "0.6 × 0.6 to 2.0 × 1.6 m"),
            ("WSW-90", "Heavy Sliding Window", "Three tracks and wider sashes, still one-finger operation.",
             [("Tracks", "3"), ("Sash weight", "up to 120 kg")], "1.2 × 1.0 to 3.6 × 2.2 m"),
            ("WSW-110", "Panoramic Slider", "Two large panes with a single 35 mm meeting stile.",
             [("Meeting stile", "35 mm"), ("Span", "up to 4.2 m")], "2.4 × 1.4 to 4.2 × 2.6 m"),
            ("WSW-70S", "Sliding Window with Flyscreen", "A third track carries the insect screen, not the glass.",
             [("Tracks", "3 incl. screen"), ("Screen", "304 mesh")], "0.8 × 0.8 to 2.4 × 1.8 m"),
            ("WSW-80", "Bay Sliding Window", "Angled bay assembled from slider sections on a 45° post.",
             [("Bay angle", "45°"), ("Tracks", "2 per section")], "project specific"),
        ]),
    dict(
        slug="interior-sliding-partition-doors", no="04", group="sliding",
        name="Interior Sliding Partition Doors", short="Interior partitions",
        tagline="Soft-close tracks, acoustic leaves, pocket options.",
        lead=("Interior partitions take the same extrusion as the exterior systems and add a soft-close "
              "carriage, a brush seal at the head and an acoustic gasket at the meeting stile. The result "
              "is a moving wall that closes quietly and stays closed."),
        chips=["40 dB acoustic", "Soft-close", "Pocket or surface"],
        base=[("Profile alloy", "6063-T5, 1.4–1.8 mm wall"), ("Sealing", "brush + acoustic gasket"),
              ("Glazing", "6 mm toughened, single"), ("Hardware", "soft-close carriage, 304 track")],
        products=[
            ("IP-40", "Single-Glazed Partition", "One glass leaf on a surface-mounted track.",
             [("Glazing", "6 mm toughened"), ("Track", "surface, 40 mm")], "0.8 × 2.1 to 1.2 × 2.6 m"),
            ("IP-60", "Acoustic Partition", "Double glazing and a gasket line for meeting rooms.",
             [("Acoustic", "40 dB"), ("Glazing", "6 + 8A + 6")], "0.9 × 2.1 to 1.6 × 2.6 m"),
            ("IP-80", "Library Partition", "Soft-close and a full-height brush seal, for reading rooms.",
             [("Operation", "soft-close"), ("Seal", "full-height brush")], "1.0 × 2.1 to 1.8 × 2.8 m"),
            ("IP-100", "Full-Height Partition", "Floor-to-slab leaf with a concealed head track.",
             [("Height", "up to 3.2 m"), ("Track", "concealed")], "1.0 × 2.6 to 2.0 × 3.2 m"),
            ("IP-120", "Corner Return Partition", "Two leaves that meet at a corner and continue around it.",
             [("Corner", "90°"), ("Leaves", "2–3")], "project specific"),
            ("IP-70", "Sliding-Folding Partition", "Panels fold as they slide, so the stack stays shallow.",
             [("Panels", "3–6"), ("Stack", "180 mm per panel")], "1.8 × 2.1 to 4.2 × 2.8 m"),
        ]),
    dict(
        slug="aluminium-casement-doors", no="05", group="casement",
        name="Aluminium Casement Doors", short="Casement doors",
        tagline="French leaves, terrace thresholds, multi-point locks.",
        lead=("A casement door is a window you walk through, which changes the hardware: the lock has to "
              "reach the floor, the threshold has to drain, and the leaf has to carry its own weight on "
              "three hinges. We build single and double leaves up to 120 kg each."),
        chips=["Leaf to 120 kg", "Multi-point lock", "Flush threshold"],
        base=[("Profile alloy", "6063-T5, 1.8–2.2 mm wall"), ("Hinges", "3 × stainless, adjustable"),
              ("Glazing", "5 + 12A + 5, up to 32 mm"), ("Locking", "3-point, lever handle")],
        products=[
            ("WCD-75", "Single Casement Door", "One outward leaf with a flush aluminium threshold.",
             [("Leaf", "up to 100 kg"), ("Threshold", "flush, drained")], "0.8 × 2.1 to 1.2 × 2.6 m"),
            ("WCD-85", "Double Casement Door", "French pair with a rebated meeting stile and espagnolette.",
             [("Leaves", "2, rebated"), ("Lock", "espagnolette")], "1.4 × 2.1 to 2.6 × 2.8 m"),
            ("WCD-65", "Slim Casement Door", "Narrow stiles for a full-height glazed leaf.",
             [("Stile", "60 mm"), ("Leaf", "up to 80 kg")], "0.8 × 2.1 to 1.1 × 2.8 m"),
            ("WCD-95", "Pivot-Hung Casement Door", "Hangs on a top and bottom pivot, no visible hinge line.",
             [("Hinge", "concealed pivot"), ("Leaf", "up to 120 kg")], "0.9 × 2.1 to 1.4 × 2.8 m"),
            ("WCD-75S", "Casement Door with Sidelight", "One operable leaf plus a fixed glazed panel.",
             [("Configuration", "leaf + fixed"), ("Mullion", "60 mm")], "1.4 × 2.1 to 2.4 × 2.6 m"),
            ("WCD-105", "Terrace Casement Door", "Triple-glazed leaf on a drained terrace threshold.",
             [("Glazing", "triple, 44 mm"), ("Uw", "1.1 W/m²K")], "1.0 × 2.1 to 1.6 × 2.8 m"),
        ]),
    dict(
        slug="aluminium-tilt-and-turn-windows", no="06", group="thermal",
        name="Aluminium Tilt And Turn Windows", short="Tilt & turn",
        tagline="Turn for air, tilt for safety, lock for the night.",
        lead=("A tilt-and-turn sash turns inward on a vertical axis and tilts on a horizontal one from the "
              "same handle. It is the default window in central Europe for a reason: it ventilates without "
              "a draught at head height and it cleans from inside."),
        chips=["Dual action", "Uw 1.1 W/m²K", "Rw 38 dB"],
        base=[("Profile alloy", "6063-T5, 1.8–2.0 mm wall"), ("Fittings", "tilt-and-turn gear, 180° turn"),
              ("Glazing", "5 + 14A + 5, up to 40 mm"), ("Sealing", "dual EPDM, corner welded")],
        products=[
            ("WT-75", "Tilt & Turn Window", "The standard inward-opening dual-action sash.",
             [("Turn", "180° inwards"), ("Sash", "up to 80 kg")], "0.6 × 0.6 to 1.4 × 2.4 m"),
            ("WT-65", "Slim Tilt & Turn Window", "A 52 mm frame for deep reveals and stone facades.",
             [("Frame", "52 mm"), ("Opening", "inward, tilt or turn")], "0.5 × 0.5 to 1.2 × 2.2 m"),
            ("WT-85", "Acoustic Tilt & Turn", "Laminated build with an offset gasket for Rw 38 dB.",
             [("Acoustic", "Rw 38 dB"), ("Glazing", "8 + 14A + 8.8")], "0.8 × 0.8 to 1.6 × 2.4 m"),
            ("WT-55", "Trade Tilt & Turn", "Volume model with a two-point lock and standard gear.",
             [("Lock", "2-point"), ("Sash", "up to 60 kg")], "0.6 × 0.6 to 1.2 × 1.8 m"),
            ("WT-95", "Panoramic Tilt & Turn", "A single wide sash that tilts across its full width.",
             [("Max sash", "1.8 × 2.6 m"), ("Gear", "heavy-duty tilt")], "1.0 × 2.2 to 1.8 × 2.6 m"),
            ("WT-75F", "Tilt & Turn French Door", "Two sashes, both operable, with a low threshold.",
             [("Leaves", "2"), ("Threshold", "20 mm, drained")], "1.4 × 2.1 to 2.8 × 2.6 m"),
        ]),
    dict(
        slug="thermal-insulation-windows", no="07", group="thermal",
        name="Thermal Insulation Windows", short="Thermal windows",
        tagline="Polyamide-broken frames for cold and hot climates alike.",
        lead=("The thermal break is the difference between a window that condenses and one that does not. "
              "Our thermal line uses a 24–34 mm polyamide bridge, warm-edge spacer and triple glazing, "
              "tested to Uw 0.8 W/m²K on the passive model."),
        chips=["Uw 0.8–1.0", "Triple glazing", "Warm-edge spacer"],
        base=[("Thermal break", "24–34 mm polyamide"), ("Spacer", "warm-edge, stainless"),
              ("Glazing", "triple, up to 52 mm"), ("Certification", "EN 14351-1, CE marked")],
        products=[
            ("WTH-90", "Thermal Window", "The baseline thermal window for cold-climate housing.",
             [("Uw", "0.9 W/m²K"), ("Glazing", "triple 48 mm")], "0.8 × 0.8 to 1.6 × 2.4 m"),
            ("WTH-100", "Passive Thermal Window", "Passive-house certified build with 34 mm break.",
             [("Uw", "0.8 W/m²K"), ("Break", "34 mm")], "0.8 × 0.8 to 1.4 × 2.4 m"),
            ("WTH-75", "Thermal Casement", "Thermal frame in a side-hung configuration.",
             [("Uw", "1.0 W/m²K"), ("Opening", "outward")], "0.6 × 0.6 to 1.4 × 2.2 m"),
            ("WTH-110", "Thermal Slider", "A broken-frame slider for balconies in cold climates.",
             [("Uw", "1.1 W/m²K"), ("Tracks", "2, thermally separated")], "1.2 × 1.0 to 3.0 × 2.2 m"),
            ("WTH-90T", "Thermal Tilt & Turn", "Thermal frame with tilt-and-turn gear.",
             [("Uw", "0.9 W/m²K"), ("Turn", "180° inwards")], "0.6 × 0.6 to 1.4 × 2.4 m"),
            ("WTH-105", "Thermal Picture Window", "Fixed frame, maximum glass, minimum U-value.",
             [("Uw", "0.7 W/m²K"), ("Opening", "fixed")], "1.2 × 1.2 to 3.0 × 2.8 m"),
        ]),
    dict(
        slug="aluminium-swing-doors", no="08", group="casement",
        name="Aluminium Swing Doors", short="Swing doors",
        tagline="Concealed hinges, heavy leaves, quiet closers.",
        lead=("Swing doors carry the most weight and take the most abuse. We build them on 2.2 mm walls "
              "with three adjustable hinges, a concealed closer option and a rebated frame that closes "
              "onto a gasket rather than a stop."),
        chips=["Concealed hinge", "RC2 option", "Leaf to 140 kg"],
        base=[("Profile alloy", "6063-T5, 2.0–2.2 mm wall"), ("Hinges", "3 × adjustable, stainless"),
              ("Glazing", "6 mm toughened or solid panel"), ("Closer", "concealed, adjustable")],
        products=[
            ("WD-70", "Swing Door", "The general-purpose single leaf for commercial interiors.",
             [("Leaf", "up to 100 kg"), ("Closer", "concealed")], "0.9 × 2.1 to 1.1 × 2.4 m"),
            ("WD-80", "Double Swing Door", "A rebated pair with flush bolts on the inactive leaf.",
             [("Leaves", "2"), ("Lock", "flush bolt + lever")], "1.6 × 2.1 to 2.4 × 2.4 m"),
            ("WD-90", "Concealed-Hinge Door", "No visible hinge line; the leaf closes onto a hidden gasket.",
             [("Hinge", "concealed"), ("Leaf", "up to 120 kg")], "0.9 × 2.1 to 1.2 × 2.8 m"),
            ("WD-60", "Slim Swing Door", "Narrow stiles for a full-height glass leaf.",
             [("Stile", "55 mm"), ("Leaf", "up to 80 kg")], "0.8 × 2.1 to 1.0 × 2.8 m"),
            ("WD-100", "Security Swing Door", "RC2-rated build with a reinforced lock stile.",
             [("Rating", "RC2"), ("Lock", "multi-point")], "0.9 × 2.1 to 1.2 × 2.4 m"),
            ("WD-85", "Glass Swing Door", "Barely-there frame for shopfronts and offices.",
             [("Stile", "45 mm"), ("Glass", "10 mm toughened")], "0.9 × 2.1 to 1.2 × 2.6 m"),
        ]),
    dict(
        slug="aluminium-bathroom-doors", no="09", group="entrance",
        name="Aluminium Bathroom Doors", short="Bathroom doors",
        tagline="Frosted glass, sealed edges, condensation-proof.",
        lead=("A bathroom door fails at the bottom edge first. Ours uses an anodised bottom rail, a sealed "
              "glazing bead and frosted toughened glass, so the leaf survives steam and a mop without "
              "swelling or delaminating."),
        chips=["Frosted toughened", "Sealed bead", "Slim stile"],
        base=[("Profile alloy", "6063-T5, 1.6 mm wall"), ("Glass", "6 mm frosted toughened"),
              ("Sealing", "sealed bead, bottom rail anodised"), ("Hardware", "privacy lock, 2 hinges")],
        products=[
            ("WB-45", "Frosted Bathroom Door", "The standard frosted single leaf.",
             [("Glass", "6 mm frosted"), ("Lock", "privacy turn")], "0.7 × 2.0 to 0.9 × 2.2 m"),
            ("WB-55", "Narrow-Stile Bathroom Door", "More glass, less frame, for small bathrooms.",
             [("Stile", "50 mm"), ("Glass", "frosted 6 mm")], "0.6 × 2.0 to 0.9 × 2.2 m"),
            ("WB-65", "Pivot Bathroom Door", "No swing clearance needed: the leaf pivots in place.",
             [("Hinge", "pivot"), ("Swing", "in or out")], "0.6 × 2.0 to 0.8 × 2.2 m"),
            ("WB-50", "Sliding Bathroom Door", "A top-hung slider for tight ensuites.",
             [("Track", "top-hung"), ("Leaf", "up to 40 kg")], "0.6 × 2.0 to 0.9 × 2.2 m"),
            ("WB-70", "Double Bathroom Door", "A pair for master ensuites and hotel bathrooms.",
             [("Leaves", "2"), ("Glass", "frosted 6 mm")], "1.2 × 2.0 to 1.8 × 2.2 m"),
            ("WB-40", "Compact Bathroom Door", "The smallest leaf we build, for powder rooms.",
             [("Leaf", "600 mm"), ("Glass", "frosted 5 mm")], "0.55 × 1.9 to 0.7 × 2.1 m"),
        ]),
    dict(
        slug="aluminium-front-doors", no="10", group="entrance",
        name="Aluminium Front Doors", short="Front doors",
        tagline="Security core, thermal leaf, one-hand locking.",
        lead=("The front door is a thermal and security assembly, not a panel. We build a 68 mm leaf on a "
              "thermal break, with a steel security core, a nine-point lock and a drained threshold that "
              "keeps the weather outside the seal."),
        chips=["RC2 / RC3 option", "68 mm leaf", "9-point lock"],
        base=[("Leaf depth", "68 mm, thermal break"), ("Core", "steel security insert"),
              ("Locking", "9-point, anti-pick cylinder"), ("Threshold", "drained, thermally broken")],
        products=[
            ("WE-70", "Entrance Door", "The standard single entrance leaf with a glazed panel.",
             [("Leaf", "up to 120 kg"), ("Lock", "6-point")], "0.9 × 2.1 to 1.1 × 2.4 m"),
            ("WE-80", "Security Entrance Door", "RC2 build with a reinforced frame and anti-lift bolts.",
             [("Rating", "RC2"), ("Lock", "9-point")], "0.9 × 2.1 to 1.1 × 2.4 m"),
            ("WE-90", "Double Entrance Door", "A rebated pair for villas, with a fixed inactive leaf.",
             [("Leaves", "2"), ("Lock", "9-point + flush bolts")], "1.6 × 2.1 to 2.2 × 2.6 m"),
            ("WE-100", "Pivot Entrance Door", "Oversize entrance leaf on a concealed pivot.",
             [("Leaf", "up to 160 kg"), ("Hinge", "concealed pivot")], "1.0 × 2.2 to 1.4 × 2.8 m"),
            ("WE-75", "Entrance Door with Sidelight", "One leaf plus a fixed glazed sidelight.",
             [("Configuration", "leaf + sidelight"), ("Lock", "6-point")], "1.3 × 2.1 to 2.0 × 2.4 m"),
            ("WE-110", "Grand Entrance Door", "Double leaf with transom for hotels and showrooms.",
             [("Leaves", "2 + transom"), ("Height", "up to 3.0 m")], "1.8 × 2.4 to 2.8 × 3.0 m"),
        ]),
    dict(
        slug="aluminium-pivot-doors", no="11", group="entrance",
        name="Aluminium Pivot Doors", short="Pivot doors",
        tagline="Offset axis, oversize leaves, no visible hinge.",
        lead=("A pivot door turns on an axis set back from the stile, so a 1.4 m leaf opens with a fraction "
              "of the clearance a hinged door needs. We set the pivot into a floor plate and a head "
              "bearing rated for 200 kg."),
        chips=["Leaf to 200 kg", "Offset axis", "Floor plate"],
        base=[("Profile alloy", "6063-T5, 2.2 mm wall"), ("Pivot", "floor plate + head bearing"),
              ("Leaf weight", "up to 200 kg"), ("Sealing", "brush + gasket line")],
        products=[
            ("WP-100", "Pivot Door", "The standard single pivot leaf for entrances.",
             [("Leaf", "up to 120 kg"), ("Axis", "centred")], "0.9 × 2.1 to 1.2 × 2.8 m"),
            ("WP-120", "Oversize Pivot Door", "A leaf wide enough to park a car through.",
             [("Leaf width", "up to 1.8 m"), ("Weight", "up to 200 kg")], "1.2 × 2.4 to 1.8 × 3.0 m"),
            ("WP-90", "Slim Pivot Door", "Narrow frame, glazed leaf, almost no visible metal.",
             [("Stile", "50 mm"), ("Glass", "10 mm toughened")], "0.9 × 2.1 to 1.2 × 2.8 m"),
            ("WP-110", "Offset Pivot Door", "Axis set back from the stile so the leaf sweeps clear of a wall.",
             [("Axis", "offset 150 mm"), ("Clearance", "reduced")], "1.0 × 2.2 to 1.4 × 2.8 m"),
            ("WP-130", "Monumental Pivot Door", "Double-height entrance for lobbies and hotels.",
             [("Height", "up to 4.0 m"), ("Weight", "up to 200 kg per leaf")], "1.2 × 2.8 to 2.0 × 4.0 m"),
            ("WP-95", "Glass Pivot Door", "Full-height glass leaf on a floor pivot.",
             [("Glass", "12 mm toughened"), ("Axis", "centred")], "1.0 × 2.2 to 1.4 × 2.8 m"),
        ]),
    dict(
        slug="aluminium-folding-doors", no="12", group="entrance",
        name="Aluminium Folding Doors", short="Folding doors",
        tagline="Panels that stack, openings that vanish.",
        lead=("A folding door turns a wall into a stack of panels. We build them on a top-hung carriage "
              "so the floor track can stay flush, with a floating mullion between pairs and a choice of "
              "inward or outward stacking."),
        chips=["Up to 12 panels", "6.0 m clear", "Top-hung"],
        base=[("Profile alloy", "6063-T5, 2.0 mm wall"), ("Carriage", "top-hung, stainless"),
              ("Glazing", "5 + 12A + 5, up to 32 mm"), ("Track", "flush floor, drained")],
        products=[
            ("WF-85", "Folding Door", "The standard four-panel folding door.",
             [("Panels", "3–6"), ("Stacking", "inward or outward")], "2.4 × 2.1 to 4.8 × 2.6 m"),
            ("WF-70", "Slim Folding Door", "Narrow panels so the stack is only 140 mm deep.",
             [("Panel width", "700 mm"), ("Stack", "140 mm/panel")], "1.8 × 2.1 to 3.6 × 2.4 m"),
            ("WF-100", "Thermal Folding Door", "Broken frame for cold-climate terraces.",
             [("Uw", "1.1 W/m²K"), ("Glazing", "triple, 40 mm")], "2.4 × 2.1 to 5.0 × 2.6 m"),
            ("WF-60", "Two-Panel Folding Door", "A small folding pair for courtyards and bars.",
             [("Panels", "2"), ("Opening", "up to 1.8 m")], "1.2 × 2.1 to 1.8 × 2.4 m"),
            ("WF-120", "Corner Folding Door", "Panels fold around a 90° corner with no fixed post.",
             [("Corner", "90°"), ("Panels", "4–8")], "3.0 × 2.1 to 6.0 × 2.6 m"),
            ("WF-90F", "Folding Door with Flyscreen", "A screen panel travels with the stack.",
             [("Screen", "304 mesh"), ("Panels", "3–6")], "2.4 × 2.1 to 4.8 × 2.6 m"),
        ]),
]
