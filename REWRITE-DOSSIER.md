# Scattered Stars — Power-Rewrite Dossier

A working handoff for the great-power lore rewrites: the method, the house style, what's done, and a running-start diagnosis of the powers still to do. Meta-notes, not lore — this file sits deliberately outside the `compile-lore.py` sections, so it never lands in the numbered output (the compiler will print a harmless `! not in any section: REWRITE-DOSSIER.md`).

## Status at a glance

| Power | Status | Thesis used | Commit |
|-------|--------|-------------|--------|
| Sable Cartel | Done | Omniscience is a *cultivated myth* over a fractious, semi-coordinated ecosystem; the reputation is the product | `88c2aec` |
| Elysian Collective | Done | One guild, two classes — the **sworn** and the **Tenders**; a commonwealth in name only; automation does the brute labour | `2383608` |
| Neo-Solar Republic | Done | Famous for its vanguard, lived by its ordinary; a genuine utopia voting, by inches, on whether to remain a society of individuals | `e6f28ad` |
| The Mandate | Done | A patchwork that calls itself a monolith, in its autumn; *unevenness is the point* over a reform-or-repeat fault-line | `3ba9220` |
| Vega Commercial Throne | Done | An honest meritocracy with a closed door—a few thousand players, ~1.4T audience; *savagely honest* market over a *seen-and-unseen* fault-line | `ab63b13` |
| Union of Frontier Freeholds | Done | The freedom that abolished the state and so cannot defend itself; *real-but-privatised freedom* over *the capture* (the commons already the Cartel's) | `dab1704` |
| Drift Communities | Done | Not one people, and freedom is not free; *hard-won joy* over a *gulf-between-decks* — Haven Ascendant is the lucky postcard, not the template | `d22e5e5` |

(The setting / overview / appendix files were already rewritten before this initiative; with the Union, all seven great powers are now done — the initiative is complete.)

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
- **Terminology collisions to avoid:** "Houses" belongs to the **Vega Throne** — never reuse it for another power's sub-units (use franchises / branches / divisions / firms; the Mandate's aristocratic families are **clans**).

## Cross-power canon to keep consistent

Invented or load-bearing detail introduced during the rewrites:

- **Sable Cartel:** the **Sefkir Reach** (a Freehold that expelled every Cartel subsidiary in 3829 C and survived poorer-but-free — the "they can lose" example); the **Trans-Orion Mercantile** (a dead pre-Cascade firm, in the origins); insider jargon **"the firm" / "upstairs" / "read the watermark."** Divisions: Capital, Transit, Assurance, Security, Commodities, Intelligence, Special Operations. Visible subsidiaries: Nexus (Capital), Wayline (Transit), Aegis (Security), Verdant (Commodities), Blackwell (Intelligence).
- **Elysian Collective:** the two classes — **sworn** (Apprentice→Journeyman→Master→Grandmaster) vs **Tenders** (associate labour: no vote, no naming rights, rarely a Garden berth); **"a commonwealth in name"**; the **world-song naming grievance** (the Tender dead long unsung); Grandmaster leanings — **Lis Valtonen** (First; traditionalist), **Maret Solveig** (Seventh; Tender advocate).
- **Neo-Solar Republic:** the **EX-spectrum** reframe (most citizens EX 1–3, the famous post-humans a ~third-sized vanguard); **"go dark"** (leave the Lattice and lose your civic voice); **amplifiers** (the soft-aristocracy of resonance democracy); the **Lattice is Sol-bound** (the Republic can't expand, only export ideas); the **Registry of Endings**; Consul **Aven Solari-7** (Preservationist).
- **The Mandate:** thesis — a *patchwork that calls itself a monolith*, in its **autumn**. Register (owner's call): **unevenness is the point** — quote the centre's one story (*Harmony*) and let the provinces complicate it; no single benign/cage verdict — carried over a cool **autumn-of-empire** throughline. Centre conflict — the **reform fault-line**: **crush / contain / concede** on Yansieve, fused with the **unspoken succession** (Xuanzong XVII, 96, 41-yr reign, no named heir; the dread's precedent is the **Long Interregnum** 2756–2847 C), all one question — *can it still reform itself, or only repeat itself?* Invented faces: **Marshal Cael Ombros** (Minister of War; of the Ombros clan; the 'crush' war faction); **Deputy Minister Vasha Toren** (Colonial Affairs; the cautious 'concede'/reform voice); 'contain' = the Emperor's deliberately faceless party-of-inertia. Load-bearing detail: the **polyglot smoking-gun** (200+ living languages; Classical is nobody's mother tongue) + the **citizen-majority** point (~5/6 are citizens; subjects a concentrated minority, not the whole); the **discontinued Sandholm agricultural-citizenship quota** (a mobility ladder pulled up — the autumn concretised); **Yansieve reframed as an *epistemic* blockade** (keeping a working example unseen; the rebels have abolished the distinction in-territory). Mandate scale standardised to **"hundreds of systems"** (matches Union/Cartel).
- **Vega Commercial Throne:** thesis — *an honest meritocracy with a closed door*: the market discipline is genuine (houses rise and fall on performance; **attainder** falls even on archdukes), but the arena holds only a few thousand families and the other **~1.4 trillion** are the audience it performs for and the workforce that builds the stage. Register (owner's call): **savagely honest** — take the Throne's market-meritocracy claim seriously, then show its closed-arena limit. Engine: **the seen and the unseen** (the manufactory + entertainment precariat who make a glamour they can't afford), with two woven threads — **House Valdorian** as the overmighty winner the market *cannot* correct (largest private army; ~35% of entertainment; Duke Caelum, loyal-but-capable), and the **post-Caspian succession void** (heir Prince Caspian, 89, childless). Load-bearing: **media-as-governance** ("Vega needs no Bureau"—entertainment + a press *free except where it counts*; Prince Octavian's royal **Stellar Networks**); **Blackwell Media** (Cartel) as a listening-post in the ecosystem, and some Vega reconstruction debt quietly **Cartel-held** (not just Arrhenos); currency the **quid (ϟ)** / internal **crown**. Through-line: *effortlessness is the manufactured product*. **File note:** Vega had **16** files all along — `economy`/`media`/`stellavista` already existed (a truncated glob hid them); all rewritten, none added.
- **Drift Communities:** thesis — *not one people, and freedom is not free*: ~900 billion across thousands of havens, and **Haven Ascendant** (~4.2M) is the rich, lucky postcard, *not* the template. Register (owner's call): **hard-won joy** — celebration/memory/welcome as defiance built to outlast real hardship, not naivety. Engine: **the gulf between decks** — Grand Havens vs Trade Havens (thin margins), salvage crews, and **Refugee Havens** (the disappeared / debt-fleeing); and *within* Ascendant, the **2.6M transient Outring** (most of the population, fewest of the Convocation seats) vs the famous Core. Load-bearing: the **Cascade-2756 diaspora** origin; the **leash** (Cartel logistics fly Drift routes none else will, hub at **Korsen's Anchorage**; **Arrhenos** neutral banking for the stateless — wealth buys a longer leash); the **Neo-Solar enhancement schism** (identity erosion vs the future, sharpest for memory-keeping havens); the **Chronicle Service** (the Haven sells the stateless proof-of-existence). Haven types: **Grand / Trade / Refugee** + specialised (vice/medical/salvage/info/diplomatic). Invented face: **Tamsin Ord** (Outring dock-gang chief, 31 yrs aboard and still 'transient'). The `overview.md` stub was promoted to the keystone; **7** files, none added.
- **Union of Frontier Freeholds:** thesis — *abolished the state to be free, and so has no one to defend it*: liberty is real and privately owned (genuine for those with a ship/claim/gun; a change of master for the company-store worker, the debt-bound, the Dustmote native born unable to leave), and a confederation with no one empowered to command has no one empowered to refuse a buyer. Register (owner's call): **real freedom, privately owned** (genuine + uneven + chosen). Engine: **the capture** — the neutral commons are *already* Cartel infrastructure (**Korsen's Anchorage** = Nexus seat; **Veritas Station** = Aegis seat), debt disciplines without a soldier (Arrhenos + unprovably Cartel), the Mandate border creeps, the commons decay (voluntarism can't fund them). Counter-example: the **Sefkir Reach** (now homed here — expelled the Cartel 3829 C, poorer-but-free, each Freehold pays alone). Load-bearing: the Charter's **dead-letter rule** (no sovereignty over the unwilling, unenforced because enforcement was abolished); the **company-store/scrip** unfreedom; decentralised defence = unconquerable *and* undefendable; **Wayline** hub at Roughneck. Invented face: **Wren Aldis** (indebted Three Falls washout, free to leave and unable to). Cross-canon reconciled: Korsen's/Nexus and Veritas/Aegis are the frontier's own beloved hubs, captured in plain sight.
- **Cross-power relations now agree** — e.g. Cartel⇄Collective "neither pries into the other's trade"; the Cartel covets Lattice tech the Republic will never sell; Cartel debt-leverage over Vega Houses; **Korsen's Anchorage** = Nexus HQ + Drift hub; **Veritas Station** = Aegis HQ; **Roughneck** = a Wayline hub. Keep new files consistent with these.

## Workflow notes

- **Compiled files** (`1-setting.md`…`5-appendices.md`) are generated by `compile-lore.py` from `setting/ powers/ worlds/ appendices/`. Never hand-edit them; regenerate and commit the regenerated `2-powers.md` (and the others only if their sources changed).
- **Commit cadence:** one commit per power (its sources + `2-powers.md`); keep unrelated regenerations in their own commit. (A `git pull`/merge that adds a setting file leaves `1-setting.md` stale — regenerate and commit it separately, as happened with `ftl/communication.md`.)
- **Verify writes:** after drafting, run `git status --short` to confirm every intended file shows as modified. One file silently failed to persist once and was caught exactly this way.
- **Confirm the full file list first.** `Glob` sorts by mtime and can truncate; cross-check the directory against this dossier's per-power *Files* line before deciding scope. (The Vega rewrite briefly missed `economy`/`media`/`stellavista` this way.)
- Commits go to **`main`** (solo repo, direct-to-main history). **Not pushed** unless the owner asks.

## Status: initiative complete

All seven great powers have been rewritten. Thesis and register for each, for quick reference:

- **Sable Cartel** — omniscience a *cultivated myth* over a quarrelsome, semi-coordinated ecosystem; the reputation is the product.
- **Elysian Collective** — one guild, two classes (**sworn** vs **Tenders**); a commonwealth in name only.
- **Neo-Solar Republic** — famous for its vanguard, lived by its ordinary; voting, by inches, on whether to stay a society of individuals.
- **The Mandate** — a *patchwork that calls itself a monolith*, in its autumn; *unevenness is the point* over a reform-or-repeat fault-line.
- **Vega Commercial Throne** — an *honest meritocracy with a closed door*; *savage honesty* over the *seen and unseen*.
- **Drift Communities** — *not one people, and freedom is not free*; *hard-won joy* over the *gulf between decks*.
- **Union of Frontier Freeholds** — *the freedom that abolished the state and so cannot defend itself*; *real-but-privatised freedom* over *the capture*.

This dossier stays the canon record: keep any future edits consistent with **Cross-power canon** above. What's left is touch-ups and consistency, not new rewrites — and the **method** and **house style** above are preserved for whenever the setting wants this treatment again.

**Optional future polish (all noticed in passing, none blocking):**
- `powers/index.md`'s power-table links are pre-existing and partly broken (e.g. the Mandate row points to `powers/mandate/index.md` from inside `powers/`; the Union/Drift rows are off too).
- Setting-wide character names repeat — several **Vance** / **Mira** / **Cassia** across powers (mostly pre-existing; the rewrites avoided adding more).
- The **Sefkir Reach** is currently woven through the Union (index, economy, locations) rather than given its own file; it could earn `locations/sefkir-reach.md` if ever wanted.
