# -*- coding: utf-8 -*-
"""Ids where the answer differs from what a naive/printed key would say.

Single source of truth for the note text in ANSWER_KEY_README.md and for the
lines in review.md.
"""

NOTABLE = [
    ("CHIM-C03-NCOM-137",
     "the ionisation table (578 / 1817 / 2745 → 11577 kJ/mol) is aluminium: "
     "three valence electrons, group 13. A first pass misread the jump as 5→6 (group 15)."),
    ("BIO-C02-NCOM-005",
     "G2 of meiosis means DNA already duplicated (Y = 4C); after meiosis I each cell has "
     "2C, so metaphase II = 0.5 Y, not Y."),
    ("CHIM-C06-NCOM-023",
     "0.1 M = 0.0001 mol per mL, i.e. 0.0001 mol in 1 mL; 0.001 mol in 100 mL would be 0.01 M."),
    ("CHIM-C11-COMM-007",
     "pH 2 → 4 is a 100-fold dilution of [H⁺]; from 1 L the final volume is 100 L."),
    ("CHIM-C11-COMM-027",
     "pH 2 in 10 L = 0.1 mol H⁺ = 0.1 mol NaOH = 4 g; the option 0.4 g uses the wrong volume."),
    ("FIS-C04-NCOM-034",
     "p·A = ρgh·A with A = 10³ cm² = 0.1 m² gives 900 Pa × 0.1 m² = 90 N, the same for cone "
     "and cylinder (hydrostatic paradox)."),
    ("CHIM-C09-NCOM-060",
     "in 2 HBr + I₂ → 2 HI + Br₂ the bromine goes −1 → 0 (oxidised) and iodine 0 → −1 "
     "(reduced); an earlier draft had this letter inverted."),
    ("FIS-C06-NCOM-026",
     "1 F = 1 C/V, so 1 V = 1 coulomb / 1 farad (option E); option D is '1 joule · 1 coulomb', "
     "which is not a volt."),
]
