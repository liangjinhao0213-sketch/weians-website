# -*- coding: utf-8 -*-
"""Case study data: six delivered projects shown in the homepage grid."""

CASES = [
    dict(
        slug="palm-beach", no="01",
        location="Palm Beach, Florida", country="United States",
        type="Residential", system="WS-90 sliding", system_slug="aluminium-sliding-doors",
        image="project-palm-beach.jpg", ratio="4 / 5",
        kicker="COASTAL VILLA · 2024",
        title="A wall of glass that opens to the pool deck.",
        hl="opens to the pool deck.",
        lead=("Twelve WS-90 sliding leaves across three elevations, all with hidden split drainage so the "
              "tracks stay dry through the summer storms that come off the Atlantic."),
        facts=[("System", "WS-90 sliding doors"), ("Panels", "12 leaves, 3 elevations"),
               ("Sightline", "22 mm"), ("Finish", "Matte black, RAL 9005")],
        body=[
            ("The brief", "The house was designed around the pool: the living room, kitchen and main suite each "
             "open onto the deck through a full-height wall of glass. The architect wanted no visible frame "
             "between inside and outside, and no threshold that anyone would trip over."),
            ("What we built", "Twelve WS-90 leaves on three elevations, each on a flush stainless track with a "
             "split drainage rail that carries water out of the cavity rather than across the face of the "
             "profile. The leaves run to 400 kg and still move with one hand."),
            ("Result", "Two hurricane seasons on, the tracks run clean and the gaskets show no staining. The "
             "owner reports the doors are the part of the house guests ask about."),
        ],
    ),
    dict(
        slug="shibuya-tokyo", no="02",
        location="Shibuya, Tokyo", country="Japan",
        type="Commercial", system="IP-60 interior partition", system_slug="interior-sliding-partition-doors",
        image="project-tokyo.jpg", ratio="4 / 3",
        kicker="OFFICE FIT-OUT · 2024",
        title="Meeting rooms that go quiet when the door closes.",
        hl="when the door closes.",
        lead=("Forty-two glass partitions on soft-close carriages, specified to 40 dB so a call in one room "
              "does not travel into the next."),
        facts=[("System", "IP-60 acoustic partition"), ("Units", "42 leaves, 6 floors"),
               ("Acoustic", "Rw 40 dB"), ("Glazing", "6 + 8A + 6 laminated")],
        body=[
            ("The brief", "A technology tenant moving into six floors of a Shibuya tower needed meeting rooms "
             "that read as glass but behave as walls. The fit-out programme allowed four weeks for partitions."),
            ("What we built", "Double-glazed IP-60 leaves on a concealed head track, with a brush seal at the "
             "head and an acoustic gasket at the meeting stile. Carriages are soft-close, so a leaf never lands."),
            ("Result", "Site acoustic testing came back at 39–41 dB across the sample set. The tenant has since "
             "repeated the specification on two more floors."),
        ],
    ),
    dict(
        slug="cottesloe", no="03",
        location="Cottesloe, Western Australia", country="Australia",
        type="Residential", system="WC-75 casement", system_slug="aluminium-casement-windows",
        image="project-cottesloe.jpg", ratio="1 / 1",
        kicker="COASTAL HOUSE · 2023",
        title="Casements that hold a gasket seal against the sea wind.",
        hl="against the sea wind.",
        lead=("Twenty-eight WC-75 casements on a limestone house two streets from the Indian Ocean, tested "
              "to AS 2047 for wind and water."),
        facts=[("System", "WC-75 casement"), ("Units", "28 windows"),
               ("Rating", "AS 2047, N2 / W3"), ("Glazing", "6.38 laminated, low-E")],
        body=[
            ("The brief", "The site takes salt spray and a steady onshore wind. The owners wanted operable "
             "windows rather than fixed glazing, without condensation on the inside face in winter."),
            ("What we built", "WC-75 outward casements with a compression EPDM gasket, laminated low-E glass and "
             "a warm-edge spacer. Frames were finished in a marine-grade powder coat."),
            ("Result", "Three years on, no hardware replacement and no gasket shrinkage. The windows are washed "
             "with fresh water twice a year and nothing else."),
        ],
    ),
    dict(
        slug="byron-bay", no="04",
        location="Byron Bay, New South Wales", country="Australia",
        type="Hospitality", system="WB-45 bathroom doors", system_slug="aluminium-bathroom-doors",
        image="project-byron.jpg", ratio="4 / 5",
        kicker="BOUTIQUE HOTEL · 2023",
        title="Sixty-four bathroom doors that survive steam and a mop.",
        hl="that survive steam and a mop.",
        lead=("Frosted WB-45 leaves with anodised bottom rails, chosen after the previous timber doors swelled "
              "in their first wet season."),
        facts=[("System", "WB-45 bathroom door"), ("Units", "64 doors"),
               ("Glass", "6 mm frosted toughened"), ("Hardware", "Privacy turn, 2 hinges")],
        body=[
            ("The brief", "A 32-key boutique hotel replaced water-damaged timber doors across all rooms. The "
             "replacement had to look softer than a standard commercial door and survive daily wet cleaning."),
            ("What we built", "WB-45 leaves with frosted toughened glass, sealed glazing beads and an anodised "
             "bottom rail — the part that fails first on a bathroom door."),
            ("Result", "Two seasons in, no delamination and no swollen edges. Housekeeping reports the doors are "
             "easier to clean than the timber set they replaced."),
        ],
    ),
    dict(
        slug="al-quoz-dubai", no="05",
        location="Al Quoz, Dubai", country="United Arab Emirates",
        type="Commercial", system="Curtain wall", system_slug="thermal-insulation-windows",
        image="project-dubai.jpg", ratio="16 / 10",
        kicker="MIXED-USE FACADE · 2023",
        title="A facade that keeps 46 °C outside the glass.",
        hl="outside the glass.",
        lead=("2,400 m² of unitised curtain wall with a thermally broken frame and solar-control glazing, "
              "installed across a nine-month programme."),
        facts=[("Scope", "2,400 m² facade"), ("System", "Thermally broken unitised"),
               ("Glazing", "Solar-control, low-E"), ("Uw", "1.4 W/m²K")],
        body=[
            ("The brief", "A mixed-use block in Al Quoz needed a facade that would hold internal temperatures "
             "with the chillers running at part load, in a climate that reaches 46 °C in August."),
            ("What we built", "Unitised panels with a 24 mm polyamide break, warm-edge spacers and solar-control "
             "low-E glass. Units were glazed and sealed in Foshan, then shipped as finished panels."),
            ("Result", "Measured cooling load came in under the design figure. The facade has passed two summer "
             "seasons without a single thermal or water complaint."),
        ],
    ),
    dict(
        slug="kensington-london", no="06",
        location="Kensington, London", country="United Kingdom",
        type="Residential", system="WF-85 folding", system_slug="aluminium-folding-doors",
        image="project-australia.jpg", ratio="16 / 10",
        kicker="GARDEN EXTENSION · 2022",
        title="Four panels that fold the garden into the kitchen.",
        hl="fold the garden into the kitchen.",
        lead=("A WF-85 folding set on a flush track, with a thermal break for a London winter and a stack that "
              "clears the return wall."),
        facts=[("System", "WF-85 folding door"), ("Panels", "4, outward stacking"),
               ("Uw", "1.3 W/m²K"), ("Track", "Flush, drained")],
        body=[
            ("The brief", "A garden extension in a conservation area needed an opening wide enough to blur the "
             "threshold between kitchen and garden, with frames thin enough not to fight the original brickwork."),
            ("What we built", "A four-panel WF-85 set on a flush floor track, thermally broken and triple-sealed, "
             "stacking outward so the internal floor stays clear."),
            ("Result", "The extension is used year-round: the doors stay closed and draught-free in February and "
             "fold flat in July. Planning liked that no frame projects outside the reveal."),
        ],
    ),
]

TYPE_ORDER = ["Residential", "Commercial", "Hospitality"]
