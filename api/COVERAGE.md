# API Database Coverage

Last verified: **2026-10-02**

## Current size

| Layer | Records |
|---|---:|
| Symbol / type / property / HRESULT records | **253** |
| Method records | **249** |
| **Total** | **502** |

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
| DeviceTopology | 24 | 25 | Strong |
| Spatial Audio | 11 | 21 | Strong |
| Media Foundation / MFT | 17 | 40 | Strong |
| XAudio2 / XAPO | 21 | 38 | Strong |
| APO / System Effects | 18 | 15 | Strong core |
| MIDI: WinMM + Windows MIDI Services | 28 | - | Symbol-level |
| WinRT Audio / Device / Capture | 16 | - | Symbol-level |
| Driver / ACX / KS / WaveRT | 19 | - | Platform-level |
| Audio Properties | 16 | - | Growing |
| HRESULT | 14 | - | Growing |
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

1. **WinRT Audio methods / properties / events**
2. **Windows MIDI Services + WinMM method/event database**
3. **KS / WaveRT / ACX DDI catalog**
4. **complete endpoint / DeviceInformation property-key catalog**
5. **larger AUDCLNT / MF / XAudio2 HRESULT catalog**
6. **Windows version/build capability matrix**
7. **SDK Header / Library / DLL / NuGet dependency database**
8. **Microsoft sample-code cross-reference database**
9. **WAVEFORMAT / codec / subtype GUID database**
10. **callback / threading / COM apartment constraints database**
11. **API relationship graph: acquisition and QueryInterface edges**
12. **source provenance / verification metadata per record**

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
