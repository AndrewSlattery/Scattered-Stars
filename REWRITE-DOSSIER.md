# Scattered Stars — Power-Rewrite Dossier

A working handoff for the great-power lore rewrites: the method, the house style, what's done, and a running-start diagnosis of the powers still to do. Meta-notes, not lore — this file sits deliberately outside the `compile-lore.py` sections, so it never lands in the numbered output (the compiler will print a harmless `! not in any section: REWRITE-DOSSIER.md`).

## Status at a glance

| Power | Status | Thesis used | Commit |
|-------|--------|-------------|--------|
| Sable Cartel | Done | Omniscience is a *cultivated myth* over a fractious, semi-coordinated ecosystem; the reputation is the product | `88c2aec` |
| Elysian Collective | Done | One guild, two classes — the **sworn** and the **Tenders**; a commonwealth in name only; automation does the brute labour | `2383608` |
| Neo-Solar Republic | Done | Famous for its vanguard, lived by its ordinary; a genuine utopia voting, by inches, on whether to remain a society of individuals | `e6f28ad` |
| The Mandate | Done | A patchwork that calls itself a monolith, in its autumn; *unevenness is the point* over a reform-or-repeat fault-line | `3ba9220` |
| Vega Commercial Throne | To do | — | — |
| Union of Frontier Freeholds | To do | — | — |
| Drift Communities | To do | — | — |

(The setting / overview / appendix files were already rewritten before this initiative; these four powers are the work so far.)

## The method (repeatable recipe)

1. **Familiarise.** Read the power's whole directory plus relevant setting context (e.g. `setting/technology/*` for the tech-heavy powers).
2. **Diagnose the hat.** Name the specific cliché — the single trait the power is written to share uniformly (its "Planet of Hats").
3. **Pick the keystone & order.** Almost always **index → culture → governance → the rest**. Index resets the thesis; culture is the diversity-of-lives payoff; governance is where the internal conflict bites.
4. **Agree the thesis + one fork** before drafting. Each power so far has hinged on a single creative decision the owner makes (Elysian's labour model; Neo-Solar's tone).
5. **Draft the whole directory** in the lived-in voice, preserving the good existing texture (named characters, dates, tables, rituals).
6. **Consistency pass → compile → commit.** `python compile-lore.py`, then commit the sources + the regenerated `2-powers.md`.

## House style (what "lived-in, anti-cliché" means here)

The owner wants **complicated, lived-in factions**, not single-trait "Planet of Hats" writing. The five fixes that have applied to *every* power so far:

1. **Find the smoking-gun number** — the figure that disproves the monoculture — and lead with it.
   - Cartel: tens of billions of *ordinary* employees, most unaware whose payroll it is.
   - Elysian: only ~15M of the ~40M are sworn terraformers.
   - Neo-Solar: EX 4+ post-humans are the *plurality, not the majority*.
2. **Kill the frictionless consensus.** Every power was first written with a harmonious ruling body (the Cartel's 13 Directors "by consensus"; the Elysian Council; Neo-Solar "resonance"). Replace with real, unresolved internal conflict / factions / deadlock.
3. **Show the diversity of lives.** Who are the ordinary people, the labour, the underclass, the ones *not* thriving? (The owner's standing priority.)
4. **Make power contingent.** Show where the faction loses, errs, or is held at arm's length (Cartel: the Sefkir Reach; Arrhenos; the fallible fez desk).
5. **Mind the ideology-vs-reality gap** — the self-image (neutral / free / post-human / a "Collective") against the messier truth, and the in-world propaganda the document itself half-repeats.

**Voice & format:**
- Confident, literate, dry-with-personality. Concrete specifics over fog. **British spelling.** Em-dashes and semicolons.
- **Open every file on a concrete hook**, never a three-noun-phrase definition. (Compare the old Cartel "A corporate entity that has achieved Great Power status through financial leverage, infrastructure control, and strategic ambiguity…" to the new "Everyone in human space knows three things about the Sable Cartel…")
- Use **markdown links** `[X](x.md)`, not `[[wikilinks]]` — they render on GitHub and match the polished `worlds/arrhenos/` files. Add a **Topics nav table** to each `index.md`.
- Preserve existing **named characters, dates, numbers and tables** — reframe around them, don't bin them.
- **Terminology collisions to avoid:** "Houses" belongs to the **Vega Throne** — never reuse it for another power's sub-units (use franchises / branches / divisions / firms).

## Cross-power canon to keep consistent

Invented or load-bearing detail introduced during the rewrites:

- **Sable Cartel:** the **Sefkir Reach** (a Freehold that expelled every Cartel subsidiary in 3829 C and survived poorer-but-free — the "they can lose" example); the **Trans-Orion Mercantile** (a dead pre-Cascade firm, in the origins); insider jargon **"the firm" / "upstairs" / "read the watermark."** Divisions: Capital, Transit, Assurance, Security, Commodities, Intelligence, Special Operations. Visible subsidiaries: Nexus (Capital), Wayline (Transit), Aegis (Security), Verdant (Commodities), Blackwell (Intelligence).
- **Elysian Collective:** the two classes — **sworn** (Apprentice→Journeyman→Master→Grandmaster) vs **Tenders** (associate labour: no vote, no naming rights, rarely a Garden berth); **"a commonwealth in name"**; the **world-song naming grievance** (the Tender dead long unsung); Grandmaster leanings — **Lis Valtonen** (First; traditionalist), **Maret Solveig** (Seventh; Tender advocate).
- **Neo-Solar Republic:** the **EX-spectrum** reframe (most citizens EX 1–3, the famous post-humans a ~third-sized vanguard); **"go dark"** (leave the Lattice and lose your civic voice); **amplifiers** (the soft-aristocracy of resonance democracy); the **Lattice is Sol-bound** (the Republic can't expand, only export ideas); the **Registry of Endings**; Consul **Aven Solari-7** (Preservationist).
- **The Mandate:** thesis — a *patchwork that calls itself a monolith*, in its **autumn**. Register (owner's call): **unevenness is the point** — quote the centre's one story (*Harmony*) and let the provinces complicate it; no single benign/cage verdict — carried over a cool **autumn-of-empire** throughline. Centre conflict — the **reform fault-line**: **crush / contain / concede** on Yansieve, fused with the **unspoken succession** (Xuanzong XVII, 96, 41-yr reign, no named heir; the dread's precedent is the **Long Interregnum** 2756–2847 C), all one question — *can it still reform itself, or only repeat itself?* Invented faces: **Marshal Cael Ombros** (Minister of War; of House Ombros; the 'crush' war faction); **Deputy Minister Vasha Toren** (Colonial Affairs; the cautious 'concede'/reform voice); 'contain' = the Emperor's deliberately faceless party-of-inertia. Load-bearing detail: the **polyglot smoking-gun** (200+ living languages; Classical is nobody's mother tongue) + the **citizen-majority** point (~5/6 are citizens; subjects a concentrated minority, not the whole); the **discontinued Sandholm agricultural-citizenship quota** (a mobility ladder pulled up — the autumn concretised); **Yansieve reframed as an *epistemic* blockade** (keeping a working example unseen; the rebels have abolished the distinction in-territory). Mandate scale standardised to **"hundreds of systems"** (matches Union/Cartel).
- **Cross-power relations now agree** — e.g. Cartel⇄Collective "neither pries into the other's trade"; the Cartel covets Lattice tech the Republic will never sell; Cartel debt-leverage over Vega Houses; **Korsen's Anchorage** = Nexus HQ + Drift hub; **Veritas Station** = Aegis HQ; **Roughneck** = a Wayline hub. Keep new files consistent with these.

## Workflow notes

- **Compiled files** (`1-setting.md`…`5-appendices.md`) are generated by `compile-lore.py` from `setting/ powers/ worlds/ appendices/`. Never hand-edit them; regenerate and commit the regenerated `2-powers.md` (and the others only if their sources changed).
- **Commit cadence:** one commit per power (its sources + `2-powers.md`); keep unrelated regenerations in their own commit. (A `git pull`/merge that adds a setting file leaves `1-setting.md` stale — regenerate and commit it separately, as happened with `ftl/communication.md`.)
- **Verify writes:** after drafting, run `git status --short` to confirm every intended file shows as modified. One file silently failed to persist once and was caught exactly this way.
- Commits go to **`main`** (solo repo, direct-to-main history). **Not pushed** unless the owner asks.

## Running-start diagnoses for the remaining three

**UNVERIFIED** — drawn from the overview, `powers/index.md`, and cross-references, *not* a full read of each directory. Confirm by reading the files first. For each: the likely hat, the smoking-gun, candidate theses, and the fork to settle.

### Vega Commercial Throne — ~1.4 trillion; media & luxury feudalism; Vega system; the Houses
- **Likely hat:** the decadent media-aristocracy — everyone a glamorous noble, star, or artist (Planet of Celebrities).
- **Smoking-gun:** a luxury/media economy runs on a vast unseen underclass — who *makes* the goods, films the content, serves the Houses? The **manufactory** workers vs the **Radiant Court**.
- **Candidate theses:** (a) the glamour vs the labour beneath it; (b) media as soft power / population control, not just entertainment; (c) the four **Houses** (Cassiline, Kraeven, Meridian, Valdorian) as cut-throat business under a courtly veneer — with the post-**Andromedan Banking War** (3839) debt to the Cartel as live leverage.
- **Fork:** is Vega's feudalism benign-glamorous, or quietly brutal beneath the sheen?
- **Cross-canon:** the Cartel holds post-war debt over Vega Houses; **Blackwell Media** operates from **Stellavista**.
- **Files:** `index, government, economy, culture, media, military, houses/{cassiline,kraeven,meridian,valdorian}, locations/{radiant-court,stellavista,lyra,manufactories}`.

### Union of Frontier Freeholds — ~1.7 trillion; frontier libertarianism; decentralised
- **Likely hat:** Planet of Libertarians / space-Western — every Freeholder a rugged free individualist.
- **Smoking-gun:** "a fiercely decentralized coalition" should be the *least* uniform power, yet the risk is writing every Freehold identically scrappy-and-free. And the freedom is uneven — the Cartel (Nexus, Wayline) penetrates the Freeholds; company towns, debt, the unfree.
- **Candidate theses:** (a) the gap between libertarian *ideology* and frontier *reality* (who is actually free; the debt-bound, the company towns, the Cartel's grip); (b) genuine *diversity across* Freeholds (no single Freehold culture); (c) the **mercenary-company** economy — how "freedom" is defended and sold.
- **Fork:** how free are the Freeholds really — frontier liberty, or a patchwork where the strong run the weak?
- **Cross-canon:** the **Sefkir Reach** (invented; expelled the Cartel, 3829 C); **Korsen's Anchorage** (Nexus HQ + Drift hub); **Veritas Station** (Aegis HQ); **Roughneck** (Wayline hub).
- **Files:** `index, governance, economy, culture, military, mercenary-companies, locations/{dustmote,korsen's-anchorage,roughneck,three-falls,veritas-station}`.

### Drift Communities — ~900 billion; nomadic station-societies; masters of navigation
- **Likely hat:** the romantic free-spirited space-nomads (Planet of Gypsies) — one uniform wandering culture.
- **Smoking-gun:** ~900 billion nomads across countless flotillas would be *wildly* diverse — different fleets, economies, cultures; the romance vs the hard logistics of perpetual nomadism.
- **Candidate theses:** (a) the *diversity across* Drift communities (Haven Ascendant is one of many, not the template); (b) the hard economics/logistics of nomadism (resupply, dependence on Cartel logistics, **Korsen's Anchorage**); (c) navigation & oral tradition as the real culture vs the romance — plus the live tension over adopting **Neo-Solar enhancement** (canon: some embrace it, others call it identity erosion).
- **Fork:** romance vs hardship — how hard is Drift life beneath the freedom?
- **Cross-canon:** Korsen's Anchorage = primary Drift hub; Cartel logistics service Drift routes few others will; the Drift's **memory/oral** culture vs the Cartel's ledgers (from the Cartel relations file).
- **Files:** `drift-communities/overview`, `drift-communities/haven-ascendant/{index,characters,preservation,promenade,society,visiting}`.

## Suggested resume point

Three remain: **Vega Commercial Throne**, **Union of Frontier Freeholds**, **Drift Communities**. **Drift** and **Union** lean hardest into the diversity-of-lives angle; **Vega** is the glamour-vs-labour media-feudalism piece. The Mandate set the trillion-scale register — *unevenness is the point* with a cool autumn-of-empire throughline — worth matching for the remaining big powers. Whichever you pick: familiarise → diagnose the hat → agree thesis + fork → draft → consistency → compile → commit.
