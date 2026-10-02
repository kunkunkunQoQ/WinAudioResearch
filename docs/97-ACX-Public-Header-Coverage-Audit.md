# ACX Public Header Coverage Audit

> Baseline: **2026-10-02**  
> Source of truth: Microsoft ACX reference hub + public WDK header documentation.

This document tracks **header-level coverage**, not just total row count.

Microsoft's ACX reference hub currently groups the public ACX surface into 12 core headers:

- `acxdevice.h`
- `acxdriver.h`
- `acxpin.h`
- `acxstreams.h`
- `acxcircuit.h`
- `acxtargets.h`
- `acxdataformat.h`
- `acxelements.h`
- `acxevents.h`
- `acxrequest.h`
- `acxmisc.h`
- `acxmanager.h`

The repository additionally indexes `acxfuncenum.h` for version-safe function / structure availability checks.

## Current repository coverage

| Header | Symbol rows | Method/callback rows | Status |
|---|---:|---:|---|
| `acxcircuit.h` | 15 | 14 | Strong |
| `acxpin.h` | 19 | 11 | Strong |
| `acxstreams.h` | 7 | 25 | Strong; method-heavy |
| `acxelements.h` | 48 | 30 | Strong |
| `acxtargets.h` | 46 | 35 | Strong |
| `acxdataformat.h` | 43 | 34 | Strong |
| `acxmanager.h` | 16 | 9 | Strong |
| `acxrequest.h` | 13 | 7 | Strong |
| `acxdevice.h` | 17 | 12 | Strong |
| `acxdriver.h` | 7 | 4 | Strong |
| `acxmisc.h` | 39 | 31 | Strong |
| `acxevents.h` | 12 | 10 | Strong; gap closed in this audit |
| `acxfuncenum.h` | 6 | 4 | Auxiliary/versioning |

> Row counts are repository records, not unique WDK API counts. Some functions are intentionally represented in both the symbol database and method/DDI index.

## Gap found and fixed

Before this audit, `acxevents.h` appeared only through a few method rows.

The symbol database now also records:

- `ACXEVENT`
- `ACXPNPEVENT`
- `ACX_EVENT_CALLBACKS`
- `ACX_EVENT_CONFIG`
- `ACX_PNPEVENT_CONFIG`
- config flag enums
- init functions
- PnP event creation / generation

Microsoft documents ACX events as asynchronous driver-level notifications that are exposed internally as KS events to upper layers.

## What “Strong” means here

“Strong” does **not** mean byte-for-byte exhaustiveness against every WDK version.

It means the repository has:

- primary public objects and structures;
- main create/config/init functions;
- main callback/DDI surface;
- official documentation links;
- relationship/context coverage.

## Remaining ACX audit work

The next pass should compare each current WDK header page against the CSV rows one interface at a time and classify misses as:

```text
Missing
Newer-version addition
Alias / macro
Internal helper
Intentionally excluded
Duplicate representation
```

Special attention:

- newer ACX additions introduced after the original ACX 1.0 surface;
- per-version structure growth;
- target/factory callback additions;
- object-bag namespace helpers;
- power / synchronization-related additions referenced by conceptual docs.

## Primary sources

- ACX Reference  
  https://learn.microsoft.com/windows-hardware/drivers/audio/acx-reference
- ACX Events header  
  https://learn.microsoft.com/windows-hardware/drivers/ddi/acxevents/
- API database  
  ../api/acx.csv
- Method/DDI database  
  ../api/methods-acx.csv
