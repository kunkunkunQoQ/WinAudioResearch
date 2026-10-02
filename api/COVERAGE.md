# API Database Coverage

Last verified: **2026-10-02**

## Current size

| Layer | Records |
|---|---:|
| Symbol / type / property / HRESULT records | **1117** |
| Method records | **818** |
| Member / property / event records | **130** |
| Capability/version records | **20** |
| Dependency records | **26** |
| Official sample records | **20** |
| API relationship records | **228** |
| **Total** | **2359** |

The database is intentionally split from the long-form documentation:

```text
docs/ → concepts / architecture / explanations / findings
api/  → machine-readable symbol / method / version / source database
```

## Family coverage

| Family | Symbol DB | Method DB | Current level |
|---|---:|---:|---|
| MMDevice | 17 | 26 | **Audited / L5** |
| WASAPI / AudioClient | 27 | 50 | **Audited / L5** |
| Audio Session | 11 | 33 | **Audited / L5** |
| EndpointVolume | 8 | 24 | **Audited / L5** |
| DeviceTopology | 32 | 64 | **Audited / L5** |
| AudioStateMonitor | 11 | 3 | **Header audited / L5** |
| WaveRT | 29 | 28 | Strong / integrated; RTAudio contract map added |
| PortCls | 112 | 194 | Integrated; broad method audit complete, final edge audit pending |
| ACX | 288 | 226 | Strong; header audit active |
| KS Audio | 284 | - | Strong core; 27/27 audio sets + generic KS + RTAudio mapping |
| Spatial Audio | 40 | 58 | Strong |
| Media Foundation / MFT | 17 | 40 | Strong |
| XAudio2 / XAPO | 21 | 38 | Strong |
| APO / System Effects | 18 | 15 | Strong core |
| MIDI: WinMM + Windows MIDI Services | 28 | 82 members | Strong modern + legacy symbols |
| DirectMusic Kernel DDI | 9 | 19 | Legacy contract indexed |
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

1. **APO / Media-Class INF contracts and Windows 11 system-effects registration**
2. **Core Audio IID/CLSID + Header/Library/DLL dependency normalization after header audit**
3. **KS method/media-seeking/allocator contracts beyond completed WaveRT/RTAudio map**
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
- [PortCls Method Coverage Audit](../docs/104-PortCls-Method-Coverage-Audit.md)
- [WaveRT / RTAudio Contract Map](../docs/103-WaveRT-RTAudio-Contract-Map.md)
- [DirectMusic Kernel DDI](../docs/102-DirectMusic-Kernel-DDI.md)
- [Core Audio SDK Header Coverage Audit](../docs/105-Core-Audio-SDK-Header-Coverage-Audit.md)

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

GitHub Actions runs the validator on synchronized main-branch snapshots (`catalog.json` / schema / validator changes) and on every API change in pull requests. This avoids expected red runs from intermediate one-file commits while preserving strict PR validation.

The validator checks:

- schema/header shape;
- record count against `api/catalog.json`;
- status values;
- verification date format;
- duplicate records;
- HTTPS source links;
- catalog consistency.
