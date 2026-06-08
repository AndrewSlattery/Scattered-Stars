# Hood — *The Glitch in the Hesperine Plateau*

A man from present-day Earth wakes in [the Shambles](../../worlds/arrhenos/locations/brovdingonai/shambles.md) of [Brovdingonai](../../worlds/arrhenos/locations/brovdingonai/index.md), eighteen-odd centuries out of his depth, and his mind — unable to parse a future it was never built for — quietly reformats the world into a game. He sees health bars and loot rarities. The men around him see a stranger with a bare neck and no [torc](../../worlds/arrhenos/society.md), and draw their own conclusions. This is the spec pallet for writing that story.

This directory is the **story project**, not lore. It lives in the vault so it can point at the vault: the rule throughout is that the setting is canon and lives under `worlds/`, `setting/`, and `powers/`, while these files describe only what the *story* adds — the protagonist, the cast, the System conceit, the arc, and how to write it. Where a fact about Arrhenos is needed, the spec **links to canon** rather than restating it. (This directory sits outside `compile-lore.py`'s four roots, so it never lands in the compiled lore; expect a harmless `! not in any section` line, exactly as `REWRITE-DOSSIER.md` produces.)

## The pallet

| File | What it is |
|------|------------|
| [premise.md](premise.md) | The pitch: genre, hook, central conflict, themes, tone, audience |
| [protagonist.md](protagonist.md) | Milo — his Earth life, his arrival, his arc and voice |
| [cast.md](cast.md) | The story's people: Lex (canon) and his household, Devan (the love interest), Sorian, the medic, the runner network, the antagonist, and canon regulars to reincorporate |
| [system.md](system.md) | The "Hood" interface: what the System is, diegetically, and how its mechanics work |
| [system-state-card.md](system-state-card.md) | The State Card template appended to every instalment, fully specified and canon-consistent |
| [outline.md](outline.md) | The narrative arc: the renovated Book 1, three acts through climax and denouement |
| [act-1-storyboard.md](act-1-storyboard.md) | Act I opened out into chapter-by-chapter, beat-by-beat blocking |
| [drafts/](drafts/) | Prose drafts of instalments ([Ch 1](drafts/chapter-01-earth.md), [Ch 2](drafts/chapter-02-initialisation.md) so far) |
| [setting-brief.md](setting-brief.md) | How to write Arrhenos for *this* story — tonal rules, pitfalls, and the lore-touchpoints table |
| [craft.md](craft.md) | General long-form serial-fiction technique (reincorporation, plant/payoff, scene-sequel) |
| [direction.md](direction.md) | Operating instructions for the writing collaborator — the per-instalment loop |
| [bible.md](bible.md) | The running continuity scratchpad: live state of characters, threads, plants, timeline |

## The conceit in one paragraph

There is **no magic and no game** — only [advanced biotechnology and physics](../../setting/technology/enhancement.md) that Milo cannot read. The "System" *presents* as a coping artefact of his own mind: a [HUD](system.md) overlay rendering trauma and incomprehension as something he knows how to play. (That it is [more than that](system.md) — that something real crossed over — is the series' buried truth.) The whole story runs on a **double exposure** — the sci-fi reality the locals inhabit, and Milo's gamified misreading of it — and most of its pleasure and most of its danger live in the gap between the two. The romance is the counterweight: where the System reduces people to affinity scores, the men Milo actually comes to know refuse to stay numbers.

## Reading order

For first contact with the project: [premise](premise.md) → [protagonist](protagonist.md) → [system](system.md) → [outline](outline.md) → [act-1-storyboard](act-1-storyboard.md). For writing an instalment: [direction](direction.md) (which pulls in [setting-brief](setting-brief.md), [craft](craft.md), and [system-state-card](system-state-card.md)), with the [storyboard](act-1-storyboard.md) for scene-level blocking and [bible](bible.md) as the live working memory updated each turn.

## Status

Spec drafted; **Book 1 arc scaffolded; Act I storyboarded beat-by-beat**. The original draft was diagnosed as too frictionless and renovated — [outline.md](outline.md) holds the re-tensioned three-act arc through climax and denouement, and [act-1-storyboard.md](act-1-storyboard.md) opens Act I into chapter blocking. Founding forks [locked](bible.md#locked-decisions-book-1): genuine SF mystery; systems-literacy edge; canon **Lex** (19) as the reckless friend who ropes Milo in; the romance a separate adult, **Devan**; a woven [agritech-data/Cartel antagonist](cast.md#antagonist-position); an intrigue-resolved-at-a-cost ending with the origin secret intact. Prose-writing of instalments is the next step; remaining open choices (the antagonist's visible face; Devan's secret and surname; the drive's exact contents) are flagged in [cast.md](cast.md) and the [bible](bible.md).

## Conventions

British spelling; the vault [house style](../../REWRITE-DOSSIER.md) (concrete over abstract, dry-with-personality, markdown links not wikilinks). In-world units are canon: the [20-hour day and C-calendar months](../../setting/calendar.md), the [quid (ϟ)](../../setting/trade-and-currency.md), the [EX enhancement scale](../../setting/technology/enhancement.md). Milo's gamer-brain translates all of these into its own argot — that mistranslation is a feature, and the spec keeps the two registers explicitly apart.
