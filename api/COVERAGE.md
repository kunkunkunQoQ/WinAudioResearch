# API Database Coverage

Last verified: **2026-10-02**

## Current size

| Layer | Records |
|---|---:|
| Symbol / type / property / HRESULT records | 169 |
| Method records | 131 |
| **Total** | **300** |

## Family coverage

| Family | Symbol DB | Method DB | Current level |
|---|---:|---:|---|
| MMDevice | 15 | 18 | Strong |
| WASAPI / AudioClient | 26 | 36 | Strong |
| Audio Session | 11 | 33 | Strong |
| EndpointVolume | 8 | 23 | Strong |
| DeviceTopology | 24 | - | Symbol-level |
| Spatial Audio | 11 | 21 | Strong |
| WinRT Audio / Device / Capture | 16 | - | Symbol-level |
| Driver / APO / ACX / KS | 19 | - | Platform-level |
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

### Symbol-level

Includes interface/class/type inventory but method table is not complete yet.

### Platform-level

Describes important driver/framework entry points. WDK surface area is much larger and is intentionally expanded in stages.

## Next database targets

1. **DeviceTopology method table**
2. **WinRT Audio methods/properties/events**
3. **APO interface/method table**
4. **Media Foundation audio/MFT catalog**
5. **XAudio2 interface/type catalog**
6. **Windows MIDI Services + legacy MIDI catalog**
7. **KS / WaveRT / ACX DDI catalog**
8. **complete endpoint property-key catalog**
9. **larger AUDCLNT HRESULT/error catalog**
10. **Windows version/build capability table**
11. **SDK library/DLL/link requirement database**
12. **sample-code cross-reference database**

## Accuracy rule

A blank version/GUID field means:

> not yet verified or not applicable.

It does **not** mean the value does not exist.

The database intentionally prefers an empty cell over an invented version number or IID.
