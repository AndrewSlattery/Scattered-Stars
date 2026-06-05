# FTL: Communication

## The Fundamental Constraint

There is no faster-than-light signalling. The AV drive moves *matter*; it does not transmit information independently of the ship that carries it. The only direct signal anyone can send is light-speed radio—and across interstellar distances that is useless. A radio message from Arrhenos to Tiamming arrives in roughly **180 years**.

The consequence is the organising fact of inter-system life: **information is cargo, and the fastest message is a fast ship.** News travels with vessels, relayed through the jump shells. Everything downstream—politics, finance, war, family—follows from this.

> **On quantum systems.** Entanglement enables instantaneous *local* coordination—the Neo-Solar Republic's Lattice is the famous example—but it cannot carry information faster than light *between* systems. Beyond a single system's neighbourhood, even the Lattice degrades to light-speed and must be synchronised by ship. There is no exception. "Quantum relay," where the term survives in marketing, denotes a fast courier feed, not a literal superluminal link.

## The Two-Speed Asymmetry

The curvature limit (see The AV Drive) divides every journey into in-system and interstellar legs, and light behaves oppositely on each:

| Leg | Span | Light (radio) | Ship |
|---|---|---|---|
| **In-system** (planet ↔ jump shell) | ~300 AU | **~1.7 days** | ~8 days (5–14) |
| **Interstellar** (shell → shell) | tens to hundreds of ly | centuries | effectively instantaneous |

So *within* a system, light beats any ship by roughly five-fold; *between* systems, any ship beats light by four orders of magnitude. The two technologies are complementary—each wins precisely the leg the other loses. The optimal message therefore **uses radio for the first and last legs and a warp courier for the interstellar trunk.** This is not a clever trick; it is the only sensible way to route a dispatch, and the entire relay industry is built on it.

## The Relay Method

A well-run dispatch never flies its payload door to door. Instead:

1. **Stage couriers at the shell.** Fast packet boats loiter at a jump-shell node, fuelled and pre-calculated for their next jump.
2. **Beam up.** The origin planet squirts the dispatch outward by tight-beam laser or maser at light speed (~1.7 days to the shell), so the courier never wastes its outbound crawl carrying stale data.
3. **Warp the trunk.** The courier jumps to the destination shell (effectively instantaneous, regardless of distance).
4. **Beam down.** The receiving node relays the dispatch the final ~300 AU to the destination planet by radio (~1.7 days)—again, faster than flying it in.

At waypoints, a pure relay node lives *at the shell*: traffic passing through is buffered and handed to the next outbound courier without ever descending to a planet, skipping the sublight legs entirely.

### Worked Timing: Arrhenos ↔ Tiamming (~180 ly)

| Method | One-way time | Notes |
|---|---|---|
| Pure radio (light speed) | **~180 years** | Why "news travels with ships" |
| Door-to-door ship (data flown both legs) | **~17–18 days** | The standard passenger/freight trip |
| Express dispatch (beam up · warp · beam down) | **~4–6 days** | Floor ~3.5 days; the rest is scheduling and handoff |

Beaming the first and last legs rather than flying them saves roughly twelve days over a single hop. Across a multi-hop trunk of well-staffed relay nodes, a dispatch crosses many systems in **ten to fourteen days**; on a sparse frontier route, where outbound couriers are rare, the same message may take **weeks to months**, waiting at each node for a ship going the right way. (The merchant *Polletio*'s loaded commercial circuit takes fourteen *months*—express relay and bulk freight are different services riding the same physics.)

Note that even express dispatch is **not real-time**. A reply doubles the one-way figure, so the fastest possible "conversation" across systems still turns around in days. Genuine real-time exchange between star systems is impossible for anyone, at any price.

## Two Tiers: Latency versus Bandwidth

The relay network splits naturally by what is being sent:

| Tier | Payload | Latency | Bandwidth | Cost |
|---|---|---|---|---|
| **Express dispatch** | Small, urgent: prices, orders, warnings | Days | Low (limited by the beam legs) | High |
| **Bulk freight** | Archives, full feeds, libraries, media | Days to weeks | Enormous (a ship's data hold) | Negligible per byte |

A freighter's hold is the highest-bandwidth channel in human space; it is merely slow. Hence the rule of thumb among dispatchers: *never underestimate the bandwidth of a packet boat full of drives.* The most urgent single signals compress this further into **codebook flags**—a pre-agreed one-bit meaning ("the succession failed") squirted on the first available courier, requiring almost no bandwidth and no decryption time at the far end.

## Institutions of the Lag

- **Dispatch lines and packet boats.** Scheduled courier runs, sovereign (imperial dispatch service) and commercial, so urgent news need not wait for a freighter. The mail run is strategic infrastructure.
- **Relay nodes.** Buffering-and-forwarding stations at the jump shells, the backbone of the interstellar "telegraph."
- **Information brokers.** Because fresh, verified information is money, institutions arise to gather, date, authenticate, and sell it. The Sable Cartel's intelligence and insurance arms keep the most accurate hazard data; the Arrhenos houses trade on lag directly through time-arbitrage derivatives; the Vega Throne syndicates feeds by priority courier.
- **Authentication.** Since nothing can be verified by a timely round-trip, trust must be portable and forgery-resistant—offline-verifiable credentials, quantum-encrypted tokens, letters of credit honoured without phoning home.
- **Standing orders.** Governors, admirals, and traders operate on cached instructions and contingency trees ("if X, do Y"), because asking the capital and waiting for an answer can take weeks.

## Consequences

There is no galactic "now." Every system inhabits its own informational light-cone, and the map of human space is always a map of the past—staler the farther one looks. Knowledge has a freshness gradient; falsehoods outrun their corrections by weeks; and every compiled document carries, of necessity, the standing caveat that some of its contents may already be out of date.

## Further Reading

- The AV Drive — The curvature limit and the jump shell
- Travel and Navigation — Transit times and system geography
- Infrastructure — Jump-shell nodes and relay stations
