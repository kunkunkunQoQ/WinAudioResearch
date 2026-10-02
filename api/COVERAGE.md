# API Database Coverage

Last verified: **2026-10-02**

## Current size

| Layer | Records |
|---|---:|
| Symbol / type / property / HRESULT records | **1074** |
| Method records | **604** |
| Member / property / event records | **130** |
| Capability/version records | **20** |
| Dependency records | **24** |
| Official sample records | **14** |
| API relationship records | **185** |
| **Total** | **2051** |

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
| WaveRT | 12 | 28 | Strong / integrated |
| PortCls | 112 | 64 | Integrated; header-index baseline |
| ACX | 288 | 226 | Strong; header audit active |
| KS Audio | 281 | - | Strong core; 27/27 audio sets + generic KS foundation |
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

1. **PortCls per-interface method exhaustiveness audit + DirectMusic dmusicks.h coverage**
2. **ACX per-header exhaustiveness audit and newer-version deltas using the new coverage audit**
3. **WaveRT supporting structs/RTAudio mappings + KS method/media-seeking/allocator details**
4. **remaining Audio INF / APO effect property GUIDs and processing-mode property IDs**
5. **larger AUDCLNT / Media Foundation / XAudio2 error catalog**
6. **exact SDK Header / Library / DLL / NuGet requirements**
7. **API relationship path tests and graph completeness checks**
8. **source provenance / verification metadata per record**
9. **codec / subtype GUID expansion**
10. **cross-version regression evidence linked to capability rows**

## Master planning

- [Windows Audio Master Coverage Plan](../docs/99-Windows-Audio-Master-Coverage-Plan.md)
- [Machine-readable domain matrix](../coverage/windows-audio-domains.csv)

## Coverage audits

- [ACX Public Header Coverage Audit](../docs/97-ACX-Public-Header-Coverage-Audit.md)
- [KS Audio Property Set Coverage](../docs/98-KS-Audio-Property-Set-Coverage.md)
- [PortCls Reference and Coverage](../docs/101-PortCls-Reference-and-Coverage.md)

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
