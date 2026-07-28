# Rewrite Checklist — full corpus

*Order of work for the `rewrites/` project. Principle: hubs before spokes, event files after the canon they depend on, summaries and appendices last. Covers all 134 lore files; excludes the root working documents (LORE-ROADMAP, HOMOGENEITY-AUDIT, STORY-SEEDS) and the compiled/NotebookLM outputs.*

*Roadmap notes marked §n refer to LORE-ROADMAP.md's still-open items — chances to fold expansion work into the rewrite pass rather than doing it twice.*

---

## Phase 1 — The spine (`setting/`) — ✅ DONE

- [x] `setting/technology/ftl/` — all six files
- [x] `setting/calendar.md`, `geography.md`, `trade-and-currency.md`, `culture.md`, `overview.md`
- [x] `setting/technology/fez.md`, `terraforming.md`, `enhancement.md`

---

## Phase 2 — The powers

Suggested power order: **Mandate → Freeholds** (they share a border and the Grey Incursion / Three Falls / Sefkir canon), then **Vega → Cartel** (both prerequisites for Arrhenos's `banking-war.md`), then **NSR → Elysian → Drift**, then the gazetteer and index. Within each power: index → structure → culture → specialised files → locations → event/voices files.

### The Mandate (18 files) — ✅ DONE — ✅ DONE

- [x] `powers/mandate/index.md`
- [x] `powers/mandate/government.md`
- [x] `powers/mandate/citizen-subject.md`
- [x] `powers/mandate/bureau.md`
- [x] `powers/mandate/culture.md`
- [x] `powers/mandate/military.md`
- [x] `powers/mandate/sapphire-courts.md`
- [x] `powers/mandate/locations/tiamming/index.md`
- [x] `powers/mandate/locations/tiamming/chrysanthemum-court.md`
- [x] `powers/mandate/locations/tiamming/xuan.md`
- [x] `powers/mandate/locations/tiamming/hiveholm.md`
- [x] `powers/mandate/locations/tiamming/osthavn.md`
- [x] `powers/mandate/locations/tiamming/parvati.md`
- [x] `powers/mandate/locations/tiamming/orbital.md`
- [x] `powers/mandate/locations/marag.md`
- [x] `powers/mandate/locations/index.md`
- [x] `powers/mandate/yansieve-rebellion.md` — after bureau + citizen-subject
- [x] `powers/mandate/yansieve-voices.md` — after the rebellion file

### Union of Frontier Freeholds (13 files) — ✅ DONE

- [x] `powers/union-freeholds/index.md`
- [x] `powers/union-freeholds/governance.md`
- [x] `powers/union-freeholds/economy.md`
- [x] `powers/union-freeholds/culture.md`
- [x] `powers/union-freeholds/military.md`
- [x] `powers/union-freeholds/mercenary-companies.md`
- [x] `powers/union-freeholds/locations/korsen's-anchorage.md`
- [x] `powers/union-freeholds/locations/roughneck.md`
- [x] `powers/union-freeholds/locations/sefkir-reach.md`
- [x] `powers/union-freeholds/locations/veritas-station.md`
- [x] `powers/union-freeholds/locations/dustmote.md`
- [x] `powers/union-freeholds/locations/three-falls.md`
- [x] `powers/union-freeholds/locations/index.md`

### Vega Commercial Throne (16 files) — ✅ DONE

- [x] `powers/vega-throne/index.md`
- [x] `powers/vega-throne/government.md`
- [x] `powers/vega-throne/economy.md`
- [x] `powers/vega-throne/media.md`
- [x] `powers/vega-throne/culture.md`
- [x] `powers/vega-throne/military.md`
- [x] `powers/vega-throne/houses/index.md`
- [x] `powers/vega-throne/houses/house-valdorian.md`
- [x] `powers/vega-throne/houses/house-cassiline.md`
- [x] `powers/vega-throne/houses/house-kraeven.md` — load-bearing for the Banking War
- [x] `powers/vega-throne/houses/house-meridian.md`
- [x] `powers/vega-throne/locations/lyra.md`
- [x] `powers/vega-throne/locations/radiant-court.md`
- [x] `powers/vega-throne/locations/stellavista.md`
- [x] `powers/vega-throne/locations/manufactories.md`
- [x] `powers/vega-throne/locations/index.md` — §4.9 open: a Vega agricultural world could be added here
- [x] *(open, §5.1)* name-collision decisions touching Vega (Meridian ×4, Aurelian echoes) — settle while rewriting the houses

### Sable Cartel (7 files) — ✅ DONE

- [x] `powers/sable-cartel/index.md`
- [x] `powers/sable-cartel/structure.md` — Veil Protocol; canon for banking-war
- [x] `powers/sable-cartel/operations.md`
- [x] `powers/sable-cartel/fronts.md`
- [x] `powers/sable-cartel/relations.md`
- [x] `powers/sable-cartel/culture.md`
- [x] `powers/sable-cartel/solano.md` — ground-level leaf, last

### Neo-Solar Republic (7 files) — ✅ DONE

- [x] `powers/neo-solar-republic/index.md`
- [x] `powers/neo-solar-republic/governance.md`
- [x] `powers/neo-solar-republic/technology.md`
- [x] `powers/neo-solar-republic/culture.md`
- [x] `powers/neo-solar-republic/military.md`
- [x] `powers/neo-solar-republic/locations/synthesis.md`
- [x] `powers/neo-solar-republic/locations/index.md`

### Elysian Collective (7 files) — ✅ DONE

- [x] `powers/elysian-collective/index.md`
- [x] `powers/elysian-collective/governance.md`
- [x] `powers/elysian-collective/technology.md`
- [x] `powers/elysian-collective/culture.md`
- [x] `powers/elysian-collective/lazarus-project.md` — the Anomalies must stay consistent with `appendices/mysteries.md`
- [x] `powers/elysian-collective/locations/the-garden.md`
- [x] `powers/elysian-collective/locations/index.md`

### Drift Communities (8 files) — ✅ DONE

- [x] `powers/drift-communities/overview.md`
- [x] `powers/drift-communities/haven-ascendant/index.md`
- [x] `powers/drift-communities/haven-ascendant/society.md`
- [x] `powers/drift-communities/haven-ascendant/preservation.md`
- [x] `powers/drift-communities/haven-ascendant/promenade.md`
- [x] `powers/drift-communities/haven-ascendant/visiting.md`
- [x] `powers/drift-communities/haven-ascendant/characters.md`
- [x] `powers/drift-communities/lesser-havens.md`

### Gazetteer and digest — ✅ DONE

- [x] `powers/minor-powers.md`
- [x] `powers/index.md` — summary table, last in the phase

---

## Phase 3 — Independent worlds (`worlds/`, non-Arrhenos) — ✅ DONE

Small phase; each file depends on a power done above.

- [x] `worlds/tethys-var.md` — after Cartel (Consortium, futures division)
- [x] `worlds/sol-system.md` — after NSR; §4.12 (Sol expansion) still open, good moment for it
- [x] `worlds/unique-worlds.md`

---

## Phase 4 — Arrhenos core (`worlds/arrhenos/`) — ✅ DONE

Order matters.

- [x] `society.md` — the hub; cited by nearly every sibling
- [x] `intimacy.md`
- [x] `fatherhood-and-brotherhood.md` — cites intimacy
- [x] `culture.md` ┐
- [x] `government.md` │
- [x] `economy.md` ├ any order
- [x] `military.md` │
- [x] `women-and-gender.md` ┘ — keep the audit doctrine (other gender experiments; the naif stereotype)
- [x] `external-relations.md` — needs powers canon
- [x] `banking-war.md` — needs Kraeven, Cassiline, Cartel structure/operations settled
- [x] `index.md` — founding narrative early if you like; finalise nav table last
- [x] `vessels/polletio.md`
- [x] `diaspora.md` — after polletio; touches almost everything

---

## Phase 5 — Arrhenos locations — ✅ DONE

Leaves; clusters in any order. Lighter sessions.

### Campottonì

- [x] `locations/campottoni.md`

### Landwick

- [x] `locations/landwick/index.md`
- [x] `locations/landwick/the-tep.md`

### Brovdingonai (9 files)

- [x] `locations/brovdingonai/index.md` — fix/keep the shambles link
- [x] `locations/brovdingonai/shambles.md`
- [x] `locations/brovdingonai/stadium.md`
- [x] `locations/brovdingonai/university.md` — merged into brovdingonai/index.md
- [x] `locations/brovdingonai/transit-hub.md` — merged into brovdingonai/index.md
- [x] `locations/brovdingonai/industrial-district.md` — merged into brovdingonai/index.md
- [x] `locations/brovdingonai/westslope-gardens.md` — ⚠ the Makris-Webbs are the worked example in intimacy + fatherhood; changes ripple back
- [x] `locations/brovdingonai/fountain-plazas.md` — merged into brovdingonai/index.md
- [x] `locations/brovdingonai/nightlife.md`

### Nemora–Zespol

- [x] `locations/nemora-zespol/index.md` — §4.11 open: the other Nemora cities
- [x] `locations/nemora-zespol/zespol.md`

### Verenstad–Gamma

- [x] `locations/verenstad-gamma/index.md`
- [x] `locations/verenstad-gamma/verenstad.md` — merged into verenstad-gamma/index.md
- [x] `locations/verenstad-gamma/gamma.md` — merged into verenstad-gamma/index.md
- [x] `locations/verenstad-gamma/transient-quarter.md` — merged into verenstad-gamma/index.md

### Off-world and odds and ends

- [x] `locations/little-arrhenos.md` — after diaspora + Vega
- [x] `locations/other.md` — merged into locations/index.md
- [x] `locations/index.md` — last in the phase

---

## Phase 6 — The integrative layer — ✅ DONE

Summaries of everything else; last for a reason.

- [x] `appendices/conversion-tables.md` — quick; only depends on Phase 1
- [x] `appendices/navigation-data.md`
- [x] `appendices/diplomatic-protocols.md`
- [x] `appendices/mysteries.md` — keep all three mysteries unsolved
- [x] `appendices/timeline.md` — reconcile against the canon ledger; every date and name must match the rewritten corpus
- [x] `README.md`
- [x] Final pass on `rewrites/setting/overview.md` in light of everything downstream

---

## Throughout

- [x] Keep a **canon ledger** — written up as `REWRITE-CANON-LEDGER.md`; original text: — one file logging every number, date, or name changed in rewriting; check before each new file, reconcile against the timeline in Phase 6
- [x] Honour the audit doctrine (corridor standard, not universal; niche, not monopoly) — it's the corpus's hard-won consistency layer
- [x] §5.1 name collisions — Roughneck's Covenant Basin renamed; the rest judged tolerable (see ledger). Original note: (Covenant ×4, Tam ×3, Vex ×2) — decide each as you pass through its file

---

## Consolidation pass — ✅ DONE

134 files → 116. Ten merges, recorded with reasons in `REWRITE-CANON-LEDGER.md`.
