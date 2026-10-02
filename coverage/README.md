# Coverage

This directory tracks **what WinAudioResearch intends to cover**, independently from the raw API record count.

## Files

- [windows-audio-domains.csv](windows-audio-domains.csv) — machine-readable domain maturity matrix
- [Master Coverage Plan](../docs/99-Windows-Audio-Master-Coverage-Plan.md) — detailed roadmap and scope

## Maturity levels

| Level | Meaning |
|---|---|
| L0 | Not indexed |
| L1 | Concept mapped |
| L2 | Major symbols indexed |
| L3 | Methods/members/properties indexed |
| L4 | Relationships, versions, dependencies and samples integrated |
| L5 | Audited against current official references/headers |
| L6 | Important behavior verified with reproducible build/device evidence |

These levels are **not percentages**.

A domain at L5 can still have documented gaps. The purpose is to make gaps explicit rather than claim a false “Windows Audio is X% complete”.

## Priority

- **P1** — foundational / high-value Windows audio development surface
- **P2** — important specialist / hardware / diagnostic domain
- **P3** — historical, niche or evidence-heavy domain

## Updating the matrix

1. Link the structured database if one exists.
2. Link the main long-form documentation.
3. State the next audit target.
4. Do not promote to L5 without an explicit official-reference audit.
5. Do not promote to L6 without reproducible evidence.

The matrix complements [api/COVERAGE.md](../api/COVERAGE.md):

- `api/COVERAGE.md` tracks database-family size and audit status.
- `coverage/windows-audio-domains.csv` tracks the wider Windows Audio knowledge-base roadmap.
