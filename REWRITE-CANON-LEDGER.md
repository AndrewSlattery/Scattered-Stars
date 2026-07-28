# Canon Ledger — the `rewrites/` pass

*Every number, date, name or structural fact that **changed** while rewriting, and every conflict found and resolved. Everything not listed here was carried over unaltered.*

---

## Conflicts found and resolved

**Jump shell radius.** `setting/technology/ftl/index.md` (your rewrite) sets the Sol jump shell at **~30 AU**. The old `appendices/navigation-data.md` still carried the pre-rewrite figure of **~300 AU**, with a matching **~1.7 day** radio lag. The appendix now reads **~30 AU / ~4 hours**, which also agrees with your `communication.md` rewrite ("lag … at least on the order of hours").

**Express-dispatch timings.** The old navigation appendix tabulated Arrhenos↔Tiamming express dispatch at 4–6 days. Your `communication.md` rewrite deliberately replaced all such worked timings with "hours to weeks". The table row is gone; the 180 ly distance and the 180-year radio figure are kept.

**The emperor's style.** Your `government.md` and `mandate/index.md` use **17 Xuanzong**. The timeline still said *Xuanzong XVII*; it now matches.

**Kepler-442 vs Kepler-422.** Your `mandate/index.md` rewrite reads **Kepler-422**. `appendices/mysteries.md`, `appendices/timeline.md` and all pre-rewrite files read **Kepler-442**. I used **442** throughout the files I wrote, on the assumption 422 is a transposition. *If 422 was deliberate, one line in `mandate/index.md` is right and four files need changing — your call.*

**Kepler-442 deployment date.** Added to the timeline at **3858 C**, matching the Yansieve entry and the "four years" in `mandate/military.md`. It had no timeline entry before.

---

## Names changed

**Roughneck's "Covenant Basin" → "the Basin."** One of the four *Covenant* collisions flagged in §5.1. The other three are load-bearing (Dustmote's Rootbound Covenant and its city Covenant; the Drift's Covenant Station), and Roughneck's agricultural region was the only incidental use. No other name was altered.

**Left as they are, deliberately:** *Tam* ×3 (Tam Orel on Osthavn; Tam Essien on the Manufactories; Oriol Tam in the Shambles) — three different powers, no shared scene. *Vex* ×2 (Captain Vex Orien at Korsen's; Vex Calder on Stellavista) — likewise. *Meridian* (the Vega house and its broadcaster) vs *Meridine* (Lyra's equatorial continent) — related by design, and distinguishable.

---

## Editorial rules applied (deduced from your finished files)

- Compress to roughly a quarter to a third of the original.
- No essayistic framing: no rhetorical openers, no "a note on vantage", no "the honest caveat", no closing meditation.
- No didactic narrative — state the contradiction, don't gloss it for the reader.
- No totalising claims: "every", "always", "the organising fact of", "there is no exception".
- No markdown links, no bold, no blockquotes, no "Topics" / "Further Reading" / "See also" apparatus.
- Attribute stat-blocks folded into the opening prose; tables kept only where genuinely tabular, in the headerless pipe form.
- Named people, dates, institutions and concrete texture preserved; adjective piles around them cut.
- Redundancy removed across files, not just within them (see below).

## Redundancy removed across files

Each of these facts now lives in exactly one place, with at most a clause elsewhere:

- Wen Daoshi's full portrait → `hiveholm.md` only (was duplicated in `parvati.md`).
- Misrule in Hiveholm → `mandate/culture.md` only.
- Parvatan cuisine and music → `mandate/culture.md` only.
- The military road to citizenship → `mandate/military.md`; one clause in `parvati.md`.
- The Sefkir Reach expulsion → `sefkir-reach.md`; one line each in the Freeholds index, economy and locations index.
- The Charter's articles → `union-freeholds/governance.md`; summary only in the index.
- Vega's noble hierarchy table → `vega-throne/government.md`; the houses index carries the archducal roster instead.
- The Thirteen and the Veil → `sable-cartel/structure.md`; summary only in the index.
- The three-phase FTL journey → once, in the merged `ftl.md` (it appeared verbatim in both `ftl/index.md` and `ftl/travel.md`).
- The court calendar → `vega-throne/culture.md`; `radiant-court.md` keeps precedence only.

---

## Files merged (134 → 116)

| `setting/technology/ftl/` (6 files) | → `setting/technology/ftl.md` — index and travel duplicated each other outright; travel duplicated communication |
| `setting/geography.md`, `setting/culture.md` (54 + 69 words) | → sections of `setting/overview.md` |
| `neo-solar-republic/locations/index.md` | → `neo-solar-republic/synthesis.md` (folder flattened) |
| `elysian-collective/locations/index.md` | → `elysian-collective/the-garden.md` (folder flattened) |
| `arrhenos/locations/verenstad-gamma/` (4 files) | → `verenstad-gamma.md` — one place, one file |
| `arrhenos/locations/landwick/` (2 files) | → `landwick.md` |
| `arrhenos/locations/nemora-zespol/` (2 files) | → `nemora-zespol.md` |
| `arrhenos/locations/other.md` | → `arrhenos/locations/index.md` (it duplicated the index tables entirely) |
| `brovdingonai/fountain-plazas.md` | → deleted; it was a verbatim copy of the index's fountain section |
| `brovdingonai/{university, transit-hub, industrial-district}.md` | → one paragraph in `brovdingonai/index.md`; each was a 45-word "to be expanded" stub |

`rewrites/README.md` was added (the corpus had none of its own).

---

# Arrhenos de-escalation pass

*Brief: Arrhenos is one of several thousand single-system polities, not an eighth great power. Target register: genuinely peripheral. Method preferred by the user — replace references with other one-system or few-system entities that have no full treatment, which also buys a sense of scale.*

Kepler-422 in `mandate/index.md` corrected to **442**, per your call.

## Substitutes used

Almost all reuse existing canon from `powers/minor-powers.md`, so this pass invented nothing new:

| The Reyes Trust | rimward neutral banking and arbitration; the direct Arrhenos analogue |
| The Khivan trade families | coreward Circuit finance, and now the seat of the Banking War tribunal |
| The Veskarn Combine | underwriting, via its published-accounts corporate arm |
| The Chandrasar Weave | spinward routes, catalogue houses, media audiences |
| Ìlú-Oba | the Broadcast Kingdoms, as Vega's real commercial rival |
| The Amaranth League | the Republic's own émigré splinter |

## Changed

**Relations tables (part 1).** Arrhenos removed from all six great-power relations tables. Elysian gained a Vega row, the NSR the Amaranth League, the Cartel a Vega row, the Freeholds the Khiva Ascendancy, Vega Ìlú-Oba; the Drift table simply lost the row.

**Financial scale (part 2).** The Vega reconstruction is no longer "chiefly by Arrhenos": the 3.8 trillion / 2.4 trillion figures survive, now carried by a syndicate of hundreds led by the Khivan families, the Veskarn Combine and the regional banks of the Sol–Vega neighbourhood. Cassiline's 200 billion is "syndicated" rather than Arrhene. Vega no longer "contended with Arrhenos in interstellar finance" — Kraeven's paper was simply first-rank and its collapse scattered the business. "Quadrillions of quid pass through the planet daily" is gone, replaced by a qualitative description that ends "a rounding error against what the corridors move in a day."

**Universal reach (part 3).** The two sentences that made Arrhenos untouchable — every great power keeping reserves there — are gone. `military.md`'s strategic position is now an explicitly *commercial* argument the Defence ministry does not confuse for a military one, and states it has never been tested. `economy.md` no longer claims the great powers reach for Arrhenos first; it names the Reyes Trust and the Khivan families as working the same seam with no reason to route through Mas. Arrhenos is out of the appendix's list of galactic neutral grounds and is now one contract lineage among six.

**Salience tics.** The Banking War settlement is now arbitrated before a mixed tribunal seated at Khiva, with Arrhene arbiters a third of the bench doing the unglamorous work. Meridian's audience list, Haven Ascendant's academic partners, the Void Reapers' contract ban, Lyra's Exchange comparison, the Freeholds' "discipline without coercion" phrase, and Campottonì's "disputes from half of human space" all now point elsewhere or at nobody in particular. The canonical reference distance in `navigation-data.md` was Arrhenos–Tiamming; it is now Sol–Vega and Tiamming–Vega. Four Arrhene constitutional dates were dropped from the galactic timeline and planetfall merged with the first generation.

External mentions outside `worlds/arrhenos/`: **50 → 36**. Vega 9 → 1; Drift 4 → 2; Mandate, NSR and Elysian now 0.

## Deliberately kept

`minor-powers.md` (both mentions actively deflate — the Reyes Trust as a peer, Resheph as the elder cousin), `lesser-havens.md` ("the Arrhene houses … have no branch on the rimward spokes"), the Freehold bar-room opinion and the loan officer families name their children after, the Arrhene visitor type in `vega-throne/culture.md`, and the Merchant Fleet's neutral-carrier role at Port Lophore.

Untouched because they are your own rewritten files: `setting/calendar.md` (Foundation Day among four Gap traditions) and `setting/technology/fez.md` (the Arrhene merchant fleets as one of three named fez players — arguably still a salience tic).

## Parts 4 and 5 — the Cartel and the Freeholds

**The design decision.** The Cartel material needed an answer to "what constrains Capital if not one gatekeeper", and the answer that fits the setting is: *nothing single does*. Respectability is retail. The Cartel needs ten thousand clerks in ten thousand offices to go on clearing its paper without asking, and it loses that the way it is earned, a little at a time and in a thousand places. Capital's stated want is now "counterparties that will still clear its paper."

That let `relations.md`'s `## Arrhenos` section become **`## The neutral houses`** — a *category* rather than a polity, which removes the eighth-section-for-an-eighth-power structure while keeping the best material. The section names the Reyes Trust, the Khivan families and the Arrhene Consortium as three among a dozen, keeps the monitoring and the intelligence-as-quiet-export, and adds the point that makes the Cartel safe: no house holds enough of its business to threaten it, it could not survive losing them all at once, and they have never once managed to agree on anything — *a problem the Cartel recognises, being built the same way*. The closing "dark and light castings of one trade" line survives, attached to the trade instead of to Arrhenos.

For the Freeholds, the fix was regional. `lesser-havens.md` already established that Arrhene houses have no branch on the rimward spokes, so the frontier's outside credit now comes from whoever is actually there: Khivan families on the coreward runs, the Reyes Trust where the Long Haul thins out, regional banks along the routes, Nexus everywhere, and Arrhene houses "in the handful of systems they have thought it worth opening a branch in." The 3423 C framework keeps its date and its name but is demoted from *the model* to the first of a dozen, "most of them larger, the Khivan one by some margin." The Sefkir Reach now banks with the Reyes Trust.

**Consolidating entries.** Because the Reyes Trust and Khiva now carry real weight, both `minor-powers.md` entries were strengthened to support it — Khiva gains the reconstruction syndicate and the Banking War tribunal seat; the Trust gains the Sefkir Reach, the far Long Haul, and a line establishing that a dozen such houses exist, none large, none able to see what the others are doing. The Trust's old framing measured itself against Arrhenos; it now records a mutual and carefully unstated conviction that the other is the derivative one.

Cross-file agreement checked: the Khiva tribunal appears in `minor-powers.md`, `vega-throne/military.md` and `arrhenos/banking-war.md`; the Reyes/Sefkir relationship in `minor-powers.md` and `sefkir-reach.md`; the syndicate composition in `minor-powers.md` and `vega-throne/economy.md`.

**Final count.** External mentions outside `worlds/arrhenos/`: **50 → 20**. Cartel 12 → 1, Freeholds 9 → 4, Vega 9 → 1, Drift 4 → 2, Mandate / NSR / Elysian 0. Of the twenty that remain, six are timeline and route data, four actively deflate, and the rest are texture — a bar-room opinion, a loan officer, a visitor type, a carrier at Port Lophore.

## Still open

- **§4.9** a Vega agricultural world, **§4.11** the other Nemora cities, **§4.12** Sol expansion — expansions rather than rewrites; left untouched.
- `worlds/arrhenos/vessels/` is a single-file folder. Left as a category you may want to grow.
- The appendices stay lettered A–E and separate, despite A and C being short, because the lettering is a set.
