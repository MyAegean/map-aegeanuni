#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build-datajs.py — παράγει το map-data.js από το map-data.json.

ΓΙΑΤΙ ΥΠΑΡΧΕΙ:
Το index.html διαβάζει κανονικά το map-data.json με fetch(). Όταν όμως η
σελίδα ανοίγει με διπλό κλικ (file://), οι browsers μπλοκάρουν το fetch()
λόγω CORS. Γι' αυτό υπάρχει και το map-data.js, που είναι ΤΟ ΙΔΙΟ JSON
τυλιγμένο σε μία γραμμή ανάθεσης και φορτώνεται με <script>.

ΜΙΑ ΠΗΓΗ ΑΛΗΘΕΙΑΣ: επεξεργάζεσαι ΜΟΝΟ το map-data.json.
Μετά από κάθε αλλαγή:      python3 build-datajs.py

Αν ο χάρτης σερβίρεται πάντα από http(s):// (static server), το map-data.js
δεν χρησιμοποιείται ποτέ και το script αυτό δεν χρειάζεται να τρέξει.
"""

import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
SRC = HERE / "map-data.json"
DST = HERE / "map-data.js"

BANNER = (
    "/* ΠΑΡΑΓΟΜΕΝΟ ΑΡΧΕΙΟ — ΜΗΝ ΤΟ ΕΠΕΞΕΡΓΑΖΕΣΑΙ.\n"
    "   Πηγή: map-data.json | Αναπαραγωγή: python3 build-datajs.py\n"
    "   Χρησιμεύει μόνο για άνοιγμα από file:// (CORS fallback). */\n"
)


def main() -> int:
    if not SRC.exists():
        print("ΣΦΑΛΜΑ: δεν βρέθηκε το %s" % SRC, file=sys.stderr)
        return 1
    try:
        data = json.loads(SRC.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print("ΣΦΑΛΜΑ: το map-data.json δεν είναι έγκυρο JSON -> %s" % exc, file=sys.stderr)
        return 1

    body = json.dumps(data, ensure_ascii=False, indent=2)
    DST.write_text(BANNER + "window.MAP_DATA = " + body + ";\n", encoding="utf-8")

    units = data.get("units", [])
    depts = sum(len(u.get("departments", [])) for u in units)
    print("OK -> %s (%d σημεία, %d τμήματα)" % (DST.name, len(units), depts))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
