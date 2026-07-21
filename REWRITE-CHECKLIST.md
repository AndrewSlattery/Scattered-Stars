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

### The Mandate (18 files)

- [ ] `powers/mandate/index.md`
- [ ] `powers/mandate/government.md`
- [ ] `powers/mandate/citizen-subject.md`
- [ ] `powers/mandate/bureau.md`
- [ ] `powers/mandate/culture.md`
- [ ] `powers/mandate/military.md`
- [ ] `powers/mandate/sapphire-courts.md`
- [ ] `powers/mandate/locations/tiamming/index.md`
- [ ] `powers/mandate/locations/tiamming/chrysanthemum-court.md`
- [ ] `powers/mandate/locations/tiamming/xuan.md`
- [ ] `powers/mandate/locations/tiamming/hiveholm.md`
- [ ] `powers/mandate/locations/tiamming/osthavn.md`
- [ ] `powers/mandate/locations/tiamming/parvati.md`
- [ ] `powers/mandate/locations/tiamming/orbital.md`
- [ ] `powers/mandate/locations/marag.md`
- [ ] `powers/mandate/locations/index.md`
- [ ] `powers/mandate/yansieve-rebellion.md` — after bureau + citizen-subject
- [ ] `powers/mandate/yansieve-voices.md` — after the rebellion file

### Union of Frontier Freeholds (13 files)

- [ ] `powers/union-freeholds/index.md`
- [ ] `powers/union-freeholds/governance.md`
- [ ] `powers/union-freeholds/economy.md`
- [ ] `powers/union-freeholds/culture.md`
- [ ] `powers/union-freeholds/military.md`
- [ ] `powers/union-freeholds/mercenary-companies.md`
- [ ] `powers/union-freeholds/locations/korsen's-anchorage.md`
- [ ] `powers/union-freeholds/locations/roughneck.md`
- [ ] `powers/union-freeholds/locations/sefkir-reach.md`
- [ ] `powers/union-freeholds/locations/veritas-station.md`
- [ ] `powers/union-freeholds/locations/dustmote.md`
- [ ] `powers/union-freeholds/locations/three-falls.md`
- [ ] `powers/union-freeholds/locations/index.md`

### Vega Commercial Throne (16 files)

- [ ] `powers/vega-throne/index.md`
- [ ] `powers/vega-throne/government.md`
- [ ] `powers/vega-throne/economy.md`
- [ ] `powers/vega-throne/media.md`
- [ ] `powers/vega-throne/culture.md`
- [ ] `powers/vega-throne/military.md`
- [ ] `powers/vega-throne/houses/index.md`
- [ ] `powers/vega-throne/houses/house-valdorian.md`
- [ ] `powers/vega-throne/houses/house-cassiline.md`
- [ ] `powers/vega-throne/houses/house-kraeven.md` — load-bearing for the Banking War
- [ ] `powers/vega-throne/houses/house-meridian.md`
- [ ] `powers/vega-throne/locations/lyra.md`
- [ ] `powers/vega-throne/locations/radiant-court.md`
- [ ] `powers/vega-throne/locations/stellavista.md`
- [ ] `powers/vega-throne/locations/manufactories.md`
- [ ] `powers/vega-throne/locations/index.md` — §4.9 open: a Vega agricultural world could be added here
- [ ] *(open, §5.1)* name-collision decisions touching Vega (Meridian ×4, Aurelian echoes) — settle while rewriting the houses

### Sable Cartel (7 files)

- [ ] `powers/sable-cartel/index.md`
- [ ] `powers/sable-cartel/structure.md` — Veil Protocol; canon for banking-war
- [ ] `powers/sable-cartel/operations.md`
- [ ] `powers/sable-cartel/fronts.md`
- [ ] `powers/sable-cartel/relations.md`
- [ ] `powers/sable-cartel/culture.md`
- [ ] `powers/sable-cartel/solano.md` — ground-level leaf, last

### Neo-Solar Republic (7 files)

- [ ] `powers/neo-solar-republic/index.md`
- [ ] `powers/neo-solar-republic/governance.md`
- [ ] `powers/neo-solar-republic/technology.md`
- [ ] `powers/neo-solar-republic/culture.md`
- [ ] `powers/neo-solar-republic/military.md`
- [ ] `powers/neo-solar-republic/locations/synthesis.md`
- [ ] `powers/neo-solar-republic/locations/index.md`

### Elysian Collective (7 files)

- [ ] `powers/elysian-collective/index.md`
- [ ] `powers/elysian-collective/governance.md`
- [ ] `powers/elysian-collective/technology.md`
- [ ] `powers/elysian-collective/culture.md`
- [ ] `powers/elysian-collective/lazarus-project.md` — the Anomalies must stay consistent with `appendices/mysteries.md`
- [ ] `powers/elysian-collective/locations/the-garden.md`
- [ ] `powers/elysian-collective/locations/index.md`

### Drift Communities (8 files)

- [ ] `powers/drift-communities/overview.md`
- [ ] `powers/drift-communities/haven-ascendant/index.md`
- [ ] `powers/drift-communities/haven-ascendant/society.md`
- [ ] `powers/drift-communities/haven-ascendant/preservation.md`
- [ ] `powers/drift-communities/haven-ascendant/promenade.md`
- [ ] `powers/drift-communities/haven-ascendant/visiting.md`
- [ ] `powers/drift-communities/haven-ascendant/characters.md`
- [ ] `powers/drift-communities/lesser-havens.md`

### Gazetteer and digest

- [ ] `powers/minor-powers.md`
- [ ] `powers/index.md` — summary table, last in the phase

---

## Phase 3 — Independent worlds (`worlds/`, non-Arrhenos)

Small phase; each file depends on a power done above.

- [ ] `worlds/tethys-var.md` — after Cartel (Consortium, futures division)
- [ ] `worlds/sol-system.md` — after NSR; §4.12 (Sol expansion) still open, good moment for it
- [ ] `worlds/unique-worlds.md`

---

## Phase 4 — Arrhenos core (`worlds/arrhenos/`)

Order matters.

- [ ] `society.md` — the hub; cited by nearly every sibling
- [ ] `intimacy.md`
- [ ] `fatherhood-and-brotherhood.md` — cites intimacy
- [ ] `culture.md` ┐
- [ ] `government.md` │
- [ ] `economy.md` ├ any order
- [ ] `military.md` │
- [ ] `women-and-gender.md` ┘ — keep the audit doctrine (other gender experiments; the naif stereotype)
- [ ] `external-relations.md` — needs powers canon
- [ ] `banking-war.md` — needs Kraeven, Cassiline, Cartel structure/operations settled
- [ ] `index.md` — founding narrative early if you like; finalise nav table last
- [ ] `vessels/polletio.md`
- [ ] `diaspora.md` — after polletio; touches almost everything

---

## Phase 5 — Arrhenos locations

Leaves; clusters in any order. Lighter sessions.

### Campottonì

- [ ] `locations/campottoni.md`

### Landwick

- [ ] `locations/landwick/index.md`
- [ ] `locations/landwick/the-tep.md`

### Brovdingonai (9 files)

- [ ] `locations/brovdingonai/index.md` — fix/keep the shambles link
- [ ] `locations/brovdingonai/shambles.md`
- [ ] `locations/brovdingonai/stadium.md`
- [ ] `locations/brovdingonai/university.md`
- [ ] `locations/brovdingonai/transit-hub.md`
- [ ] `locations/brovdingonai/industrial-district.md`
- [ ] `locations/brovdingonai/westslope-gardens.md` — ⚠ the Makris-Webbs are the worked example in intimacy + fatherhood; changes ripple back
- [ ] `locations/brovdingonai/fountain-plazas.md`
- [ ] `locations/brovdingonai/nightlife.md`

### Nemora–Zespol

- [ ] `locations/nemora-zespol/index.md` — §4.11 open: the other Nemora cities
- [ ] `locations/nemora-zespol/zespol.md`

### Verenstad–Gamma

- [ ] `locations/verenstad-gamma/index.md`
- [ ] `locations/verenstad-gamma/verenstad.md`
- [ ] `locations/verenstad-gamma/gamma.md`
- [ ] `locations/verenstad-gamma/transient-quarter.md`

### Off-world and odds and ends

- [ ] `locations/little-arrhenos.md` — after diaspora + Vega
- [ ] `locations/other.md`
- [ ] `locations/index.md` — last in the phase

---

## Phase 6 — The integrative layer

Summaries of everything else; last for a reason.

- [ ] `appendices/conversion-tables.md` — quick; only depends on Phase 1
- [ ] `appendices/navigation-data.md`
- [ ] `appendices/diplomatic-protocols.md`
- [ ] `appendices/mysteries.md` — keep all three mysteries unsolved
- [ ] `appendices/timeline.md` — reconcile against the canon ledger; every date and name must match the rewritten corpus
- [ ] `README.md`
- [ ] Final pass on `rewrites/setting/overview.md` in light of everything downstream

---

## Throughout

- [ ] Keep a **canon ledger** — one file logging every number, date, or name changed in rewriting; check before each new file, reconcile against the timeline in Phase 6
- [ ] Honour the audit doctrine (corridor standard, not universal; niche, not monopoly) — it's the corpus's hard-won consistency layer
- [ ] §5.1 name collisions (Covenant ×4, Tam ×3, Vex ×2) — decide each as you pass through its file
