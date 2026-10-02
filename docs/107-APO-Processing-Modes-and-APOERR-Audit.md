# APO Processing Modes / APOERR / MsApoFxProxy Coverage Audit

> Baseline: **2026-10-02**  
> Scope: signal-processing-mode GUIDs, KS mode discovery, Microsoft generic APO proxy discovery, and canonical APO HRESULTs.

## Result

This stage closes three machine-readable gaps left by the previous APO/CAPX audit:

| Area | Added / covered | Result |
|---|---:|---|
| Signal-processing-mode database | 10 records | GUID inventory + KS discovery contract |
| APO proxy-discovery records | 4 records | `MsApoFxProxy` contract mapped |
| Canonical `APOERR_*` values | 14 records | Complete SDK-header error family |
| Relationship graph | 10 edges | mode-return and proxy-query paths |
| API database total | **2504** | synchronized catalog |

Structured files:

- `api/audio-processing-modes.csv`
- `api/apo.csv`
- `api/hresults.csv`
- `api/relationships.csv`

## 1. Standard signal-processing modes

Microsoft's public Windows audio overview documents seven standard modes.

| Mode | Direction | Baseline | GUID |
|---|---|---|---|
| `AUDIO_SIGNALPROCESSINGMODE_DEFAULT` | render + capture | Windows 8.1 | `{C18E2F7E-933D-4965-B7D1-1EEF228D2AF3}` |
| `AUDIO_SIGNALPROCESSINGMODE_RAW` | render + capture | Windows 8.1 | `{9E90EA20-B493-4FD1-A1A8-7E1361A956CF}` |
| `AUDIO_SIGNALPROCESSINGMODE_COMMUNICATIONS` | render + capture | Windows 10 | `{98951333-B9CD-48B1-A0A3-FF40682D73F7}` |
| `AUDIO_SIGNALPROCESSINGMODE_SPEECH` | capture | Windows 10 | `{FC1CFC9B-B9D6-4CFA-B5E0-4BB2166878B2}` |
| `AUDIO_SIGNALPROCESSINGMODE_MEDIA` | render + capture | Windows 10 | `{4780004E-7133-41D8-8C74-660DADD2C0EE}` |
| `AUDIO_SIGNALPROCESSINGMODE_MOVIE` | render | Windows 10 | `{B26FEB0D-EC94-477C-9494-D1AB8E753F6E}` |
| `AUDIO_SIGNALPROCESSINGMODE_NOTIFICATION` | render | Windows 10 | `{9CF2A70B-F377-403B-BD6B-360863E0355C}` |

Windows 8.1 introduced Default and Raw. Windows 10 added the five workload-oriented modes.

## 2. FAR_FIELD_SPEECH is indexed conservatively

Current Microsoft SDK metadata also defines:

```text
AUDIO_SIGNALPROCESSINGMODE_FAR_FIELD_SPEECH
{28941CBA-3BE6-4A78-9A76-30FD91559B64}
```

The public seven-mode overview does not list this identifier. The database therefore records the exact public SDK symbol and GUID but intentionally leaves `min_client` blank instead of inventing a version.

This follows the repository's rule that **header presence and product-version support are separate facts**.

## 3. KS mode-discovery contract

The public driver query is:

```text
KSPROPSETID_Audio
    ↓
KSPROPERTY_AUDIOSIGNALPROCESSING_MODES
    ↓ GET on pin factory
KSMULTIPLE_ITEM
    ↓
GUID[]
```

The query is get-only. Microsoft documents host and offload pins as the pins that advertise processing modes; loopback and bridge pins return an empty mode list.

The corresponding mode attribute is:

```text
KSATTRIBUTEID_AUDIOSIGNALPROCESSING_MODE
{E1F89EB5-5F46-419B-967B-FF6770B98401}
```

It identifies `KSATTRIBUTE_AUDIOSIGNALPROCESSING_MODE` in a KS attribute list attached to a data-range/format path.

## 4. Stream category and processing mode are different layers

Applications normally choose a stream category or request Raw behavior. Windows maps that workload into a signal-processing mode consumed by the engine, APOs and driver stack:

```text
application stream category / RAW request
        ↓
Windows audio-engine policy
        ↓
AUDIO_SIGNALPROCESSINGMODE_*
        ↓
APO + driver pin processing
```

The processing-mode GUID should not be treated as a replacement for the public application stream-category APIs.

## 5. Raw-mode constraint

Raw is not merely another preset. For raw capture, Microsoft specifies that adaptive or time-varying processing must not be applied. Fixed linear processing such as equalization is treated differently under the platform rules.

A device claiming Raw support therefore needs a genuinely appropriate processing path, not only a relabeled Default path.

## 6. Microsoft generic effects-discovery APO

Windows supplies a generic proxy path that can ask a driver which hardware effects are active:

```text
PKEY_FX_*EffectClsid
    ↓
FX_DISCOVER_EFFECTS_APO_CLSID
{889C03C8-ABAD-4004-BF0A-BC7BB825E166}
    ↓ implemented by
MsApoFxProxy.dll
    ↓ queries
KSPROPSETID_AudioEffectsDiscovery
{0B217A72-16B8-4A4D-BDED-F9D6BBEDCD8F}
    ↓
KSPROPERTY_AUDIOEFFECTSDISCOVERY_EFFECTSLIST
    ↓
active effect GUID list
```

`KSPROPERTY_AUDIOEFFECTSDISCOVERY_EFFECTSLIST` has enumeration value **1** in `KSPROPERTY_AUDIOEFFECTSDISCOVERY`.

This is distinct from a vendor implementing a complete custom APO: the proxy provides a standardized discovery bridge to effects implemented by the driver/hardware path.

## 7. Complete APOERR catalog

The current public `audioenginebaseapo.h` header assigns the APO error family to facility **0x87D**.

| HRESULT | Value | Meaning |
|---|---|---|
| `APOERR_ALREADY_INITIALIZED` | `0x887D0001` | object already initialized |
| `APOERR_NOT_INITIALIZED` | `0x887D0002` | object/structure not initialized |
| `APOERR_FORMAT_NOT_SUPPORTED` | `0x887D0003` | requested format unsupported |
| `APOERR_INVALID_APO_CLSID` | `0x887D0004` | invalid CLSID in initialization data |
| `APOERR_BUFFERS_OVERLAP` | `0x887D0005` | illegal input/output buffer overlap |
| `APOERR_ALREADY_UNLOCKED` | `0x887D0006` | APO already unlocked |
| `APOERR_NUM_CONNECTIONS_INVALID` | `0x887D0007` | invalid connection count |
| `APOERR_INVALID_OUTPUT_MAXFRAMECOUNT` | `0x887D0008` | output max-frame count too small |
| `APOERR_INVALID_CONNECTION_FORMAT` | `0x887D0009` | invalid connection format |
| `APOERR_APO_LOCKED` | `0x887D000A` | APO locked for processing |
| `APOERR_INVALID_COEFFCOUNT` | `0x887D000B` | invalid coefficient count |
| `APOERR_INVALID_COEFFICIENT` | `0x887D000C` | invalid coefficient |
| `APOERR_INVALID_CURVE_PARAM` | `0x887D000D` | invalid curve parameter |
| `APOERR_INVALID_INPUTID` | `0x887D000E` | invalid auxiliary input identifier |

## 8. Documentation typo caught by the audit

The canonical Microsoft SDK header defines:

```text
APOERR_INVALID_CONNECTION_FORMAT
```

Some Learn method text has shown the misspelled form `APOERR_INVALID_CONNECITON_FORMAT`. The machine-readable database follows the SDK header and does not propagate that documentation typo.

## 9. Coverage result

The APO domain now has machine-readable coverage for base/realtime interfaces, AEC auxiliary inputs, Windows 11 notifications/services, controllable effects, CAPX property stores and deployment, SFX/MFX/EFX registration, processing modes, generic proxy discovery, and the public `APOERR_*` family.

Remaining work is mostly edge/header completeness rather than a missing architectural block.

## 10. Next APO targets

1. audit helper classes/macros in `baseaudioprocessingobject.h`;
2. normalize every public APO IID/SID/CLSID against current SDK metadata;
3. index the `AUDIO_EFFECT_TYPE_*` GUID family and connect it to discovery/control APIs;
4. finish remaining Media-Class INF keywords/property IDs and version provenance;
5. add cross-version regression evidence for processing modes and CAPX packages.

## Primary sources

- Audio Signal Processing Modes — https://learn.microsoft.com/windows-hardware/drivers/audio/audio-signal-processing-modes
- KSPROPERTY_AUDIOSIGNALPROCESSING_MODES — https://learn.microsoft.com/windows-hardware/drivers/audio/ksproperty-audiosignalprocessing-modes
- KSPROPSETID_AudioEffectsDiscovery — https://learn.microsoft.com/windows-hardware/drivers/audio/kspropsetid-audioeffectsdiscovery
- KSPROPERTY_AUDIOEFFECTSDISCOVERY_EFFECTSLIST — https://learn.microsoft.com/windows-hardware/drivers/audio/ksproperty-audioeffectsdiscovery-effectslist
- Implementing Audio Processing Objects — https://learn.microsoft.com/windows-hardware/drivers/audio/implementing-audio-processing-objects
- Microsoft SDK header mirror (win32metadata): audioenginebaseapo.h — https://github.com/microsoft/win32metadata/blob/main/generation/WinSDK/RecompiledIdlHeaders/um/audioenginebaseapo.h
- Microsoft Windows SDK metadata: ksmedia — https://github.com/microsoft/windows-rs/blob/master/metadata/win32/ksmedia.rdl
