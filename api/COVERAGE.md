# API Database Coverage

Last verified: **2026-10-02**

## Current size

| Layer | Records |
|---|---:|
| Symbol / type / property / HRESULT records | **560** |
| Method records | **383** |
| Member / property / event records | **130** |
| Capability/version records | **20** |
| Dependency records | **20** |
| Official sample records | **14** |
| API relationship records | **111** |
| **Total** | **1238** |

The database is intentionally split from the long-form documentation:

```text
docs/ → concepts / architecture / explanations / findings
api/  → machine-readable symbol / method / version / source database
```

## Family coverage

| Family | Symbol DB | Method DB | Current level |
|---|---:|---:|---|
| MMDevice | 15 | 18 | Strong |
| WASAPI / AudioClient | 26 | 36 | Strong |
| Audio Session | 11 | 33 | Strong |
| EndpointVolume | 8 | 23 | Strong |
| DeviceTopology | 32 | 25 | Strong |
| WaveRT | 12 | 20 | Strong core |
| ACX | 80 | 77 | Strong core |
| KS Audio | 87 | - | Strong core |
| Spatial Audio | 40 | 58 | Strong |
| Media Foundation / MFT | 17 | 40 | Strong |
| XAudio2 / XAPO | 21 | 38 | Strong |
| APO / System Effects | 18 | 15 | Strong core |
| MIDI: WinMM + Windows MIDI Services | 28 | 82 members | Strong modern + legacy symbols |
| WinRT Audio / Device / Capture | 16 | 48 members | Strong core |
| Driver / ACX / KS / WaveRT | 19 | - | Platform-level |
| Audio Properties | 62 | - | Strong core |
| HRESULT | 36 | - | Growing |
| Undocumented | 9 | - | Explicitly separated |

## Definition of coverage levels

### Strong

Includes:

- primary interfaces/types;
- important version data;
- official source links;
- common acquisition path;
- method-level index for main interfaces.

### Strong core

Core interfaces and important methods are indexed, but the framework still has a much larger specialized surface.

### Symbol-level

Includes interface/class/type inventory but method/property/event tables are not complete yet.

### Platform-level

Describes important driver/framework entry points. WDK surface area is much larger and is intentionally expanded in stages.

## Next database targets

1. **callback / COM apartment / realtime / lifetime constraints database**
2. **ACX target / request / factory / data-format APIs beyond the expanded core + element index**
3. **KS AudioEngine / jack / topology property sets beyond the expanded KSPROPSETID_Audio catalog**
4. **remaining Audio INF / APO effect property GUIDs and processing-mode property IDs**
5. **larger AUDCLNT / Media Foundation / XAudio2 error catalog**
6. **exact SDK Header / Library / DLL / NuGet requirements**
7. **API relationship path tests and graph completeness checks**
8. **source provenance / verification metadata per record**
9. **codec / subtype GUID expansion**
10. **cross-version regression evidence linked to capability rows**

## Accuracy rule

A blank version/GUID field means:

> not yet verified or not applicable.

It does **not** mean the value does not exist.

The database intentionally prefers an empty cell over an invented version number or IID.

## Validation

Every change under `api/` is checked by:

```text
python scripts/validate_api_db.py
```

GitHub Actions also runs the same validator for API database changes.

The validator checks:

- schema/header shape;
- record count against `api/catalog.json`;
- status values;
- verification date format;
- duplicate records;
- HTTPS source links;
- catalog consistency.
