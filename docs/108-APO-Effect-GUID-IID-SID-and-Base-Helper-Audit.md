# APO Effect GUID / IID-SID / Base Helper Final Audit

> Baseline: **2026-10-02**  
> Scope: current SDK `AUDIO_EFFECT_TYPE_*` identifiers, APO interface/service IDs, `baseaudioprocessingobject.h` helpers, AERT dependencies, and remaining Media-Class INF property IDs.

## Result

This is the final header/reference-level APO audit after docs 106 and 107.

| Area | Result |
|---|---|
| Current `AUDIO_EFFECT_TYPE_*` SDK identifiers | **19 / 19 indexed** |
| Existing public APO interfaces with IID fields normalized | **18** |
| Newly indexed `IAudioProcessingObjectVBR` | **1 interface + 2 methods** |
| APO service IDs | **2 exact SIDs** |
| Base APO implementation helper | `CBaseAudioProcessingObject` + 10 protected helpers |
| Realtime memory helpers | `AERT_Allocate` / `AERT_Free` + Audioeng dependencies |
| Media-Class INF keyword/property audit | remaining direct PROPERTYKEY gaps closed |
| APO maturity | **L5 audited** |

Machine-readable updates:

- `api/audio-effects.csv`
- `api/apo.csv`
- `api/methods-apo.csv`
- `api/audio-properties.csv`
- `api/dependencies.csv`
- `api/relationships.csv`

## 1. Current SDK audio-effect GUID family

The long-standing effect family occupies the contiguous `6F64ADBE...` through `6F64ADCE...` range. Current Microsoft SDK metadata also exposes far-field beamforming at `ADCF` and deep noise suppression at `ADD0`.

| Symbol | GUID |
|---|---|
| `AUDIO_EFFECT_TYPE_ACOUSTIC_ECHO_CANCELLATION` | `{6F64ADBE-8211-11E2-8C70-2C27D7F001FA}` |
| `AUDIO_EFFECT_TYPE_NOISE_SUPPRESSION` | `{6F64ADBF-8211-11E2-8C70-2C27D7F001FA}` |
| `AUDIO_EFFECT_TYPE_AUTOMATIC_GAIN_CONTROL` | `{6F64ADC0-8211-11E2-8C70-2C27D7F001FA}` |
| `AUDIO_EFFECT_TYPE_BEAMFORMING` | `{6F64ADC1-8211-11E2-8C70-2C27D7F001FA}` |
| `AUDIO_EFFECT_TYPE_CONSTANT_TONE_REMOVAL` | `{6F64ADC2-8211-11E2-8C70-2C27D7F001FA}` |
| `AUDIO_EFFECT_TYPE_EQUALIZER` | `{6F64ADC3-8211-11E2-8C70-2C27D7F001FA}` |
| `AUDIO_EFFECT_TYPE_LOUDNESS_EQUALIZER` | `{6F64ADC4-8211-11E2-8C70-2C27D7F001FA}` |
| `AUDIO_EFFECT_TYPE_BASS_BOOST` | `{6F64ADC5-8211-11E2-8C70-2C27D7F001FA}` |
| `AUDIO_EFFECT_TYPE_VIRTUAL_SURROUND` | `{6F64ADC6-8211-11E2-8C70-2C27D7F001FA}` |
| `AUDIO_EFFECT_TYPE_VIRTUAL_HEADPHONES` | `{6F64ADC7-8211-11E2-8C70-2C27D7F001FA}` |
| `AUDIO_EFFECT_TYPE_SPEAKER_FILL` | `{6F64ADC8-8211-11E2-8C70-2C27D7F001FA}` |
| `AUDIO_EFFECT_TYPE_ROOM_CORRECTION` | `{6F64ADC9-8211-11E2-8C70-2C27D7F001FA}` |
| `AUDIO_EFFECT_TYPE_BASS_MANAGEMENT` | `{6F64ADCA-8211-11E2-8C70-2C27D7F001FA}` |
| `AUDIO_EFFECT_TYPE_ENVIRONMENTAL_EFFECTS` | `{6F64ADCB-8211-11E2-8C70-2C27D7F001FA}` |
| `AUDIO_EFFECT_TYPE_SPEAKER_PROTECTION` | `{6F64ADCC-8211-11E2-8C70-2C27D7F001FA}` |
| `AUDIO_EFFECT_TYPE_SPEAKER_COMPENSATION` | `{6F64ADCD-8211-11E2-8C70-2C27D7F001FA}` |
| `AUDIO_EFFECT_TYPE_DYNAMIC_RANGE_COMPRESSION` | `{6F64ADCE-8211-11E2-8C70-2C27D7F001FA}` |
| `AUDIO_EFFECT_TYPE_FAR_FIELD_BEAMFORMING` | `{6F64ADCF-8211-11E2-8C70-2C27D7F001FA}` |
| `AUDIO_EFFECT_TYPE_DEEP_NOISE_SUPPRESSION` | `{6F64ADD0-8211-11E2-8C70-2C27D7F001FA}` |

The public overview historically describes seventeen effect types. The repository does not freeze its database at that prose count: it follows current Microsoft SDK metadata and indexes the additional far-field and deep-noise identifiers. Minimum-client fields stay blank when no direct version baseline was verified. Deep Noise Suppression is explicitly documented for Windows 11 24H2.

## 2. Effect identifiers connect application and APO views

```text
IAudioEffectsManager::GetAudioEffects
        ↓ AUDIO_EFFECT.id
AUDIO_EFFECT_TYPE_*
        ↑
IAudioSystemEffects2::GetEffectsList
        ↑
IAudioSystemEffects3 / AUDIO_SYSTEMEFFECT
```

The GUID tells the consumer what an effect represents; it does not identify a vendor APO COM class. APO CLSIDs and effect-type GUIDs are different namespaces and remain separate in the database.

## 3. Public APO IID normalization

Exact UUIDs were cross-checked against Microsoft's recompiled SDK IDL.

| Interface | IID |
|---|---|
| `IAudioProcessingObject` | `FD7F2B29-24D0-4B5C-B177-592C39F9CA10` |
| `IAudioProcessingObjectRT` | `9E1D6A6D-DDBC-4E95-A4C7-AD64BA37846C` |
| `IAudioProcessingObjectVBR` | `7BA1DB8F-78AD-49CD-9591-F79D80A17C81` |
| `IAudioProcessingObjectConfiguration` | `0E5ED805-ABA6-49C3-8F9A-2B8C889C4FA8` |
| `IAudioDeviceModulesClient` | `98F37DAC-D0B6-49F5-896A-AA4D169A4C48` |
| `IAudioSystemEffects` | `5FA00F27-ADD6-499A-8A9D-6B98521FA75B` |
| `IAudioSystemEffects2` | `BAFE99D2-7436-44CE-9E0E-4D89AFBFFF56` |
| `IAudioSystemEffects3` | `C58B31CD-FC6A-4255-BC1F-AD29BB0A4A17` |
| `IAudioSystemEffectsCustomFormats` | `B1176E34-BB7F-4F05-BEBD-1B18A534E097` |
| `IApoAuxiliaryInputConfiguration` | `4CEB0AAB-FA19-48ED-A857-87771AE1B768` |
| `IApoAuxiliaryInputRT` | `F851809C-C177-49A0-B1B2-B66F017943AB` |
| `IApoAcousticEchoCancellation` | `25385759-3236-4101-A943-25693DFB5D2D` |
| `IApoAcousticEchoCancellation2` | `F235855F-F06D-45B3-A63F-EE4B71509DC2` |
| `IAudioProcessingObjectRTQueueService` | `ACD65E2F-955B-4B57-B9BF-AC297BB752C9` |
| `IAudioProcessingObjectLoggingService` | `698F0107-1745-4708-95A5-D84478A62A65` |
| `IAudioProcessingObjectPreferredFormatSupport` | `51CBD3C4-F1F3-4D2F-A0E1-7E9C4DD0FEB3` |
| `IAudioProcessingObjectNotifications` | `56B0C76F-02FD-4B21-A52E-9F8219FC86E4` |
| `IAudioProcessingObjectNotifications2` | `CA2CFBDE-A9D6-4EB0-BC95-C4D026B380F0` |
| `IAudioMediaType` | `4E997F73-B71F-4798-873B-ED7DFCF15B4D` |

`IAudioProcessingObjectVBR` was missing from the prior structured APO table. Its two non-realtime sizing methods are now indexed: `CalcMaxInputFrames` and `CalcMaxOutputFrames`.

## 4. Service IDs are not interface IDs

| Service | SID |
|---|---|
| `SID_AudioProcessingObjectLoggingService` | `{8B8008AF-09F9-456E-A173-BDB58499BCE7}` |
| `SID_AudioProcessingObjectRTQueue` | `{458C1A1F-6899-4C12-99AC-E2E6AC253104}` |

Windows 11 APO initialization exposes these services through `APOInitSystemEffects3.pServiceProvider`. The relationship database now makes the QueryService paths explicit.

## 5. CBaseAudioProcessingObject audit

The SDK helper class implements common plumbing for `IAudioProcessingObject`, `IAudioProcessingObjectRT`, and `IAudioProcessingObjectConfiguration`.

Protected helpers indexed in `methods-apo.csv`:

- `IsFormatTypeSupported`
- `ValidateConnection`
- `ValidateAndCacheConnectionInfo`
- `BuffersOverlap`
- `GetSamplesPerFrame`
- `GetBytesPerSampleContainer`
- `GetValidBitsPerSample`
- `GetFramesPerSecond`
- `ValidateInitializeParameters`
- `ValidateDefaultAPOFormat`

The base class still requires an APO implementation to supply its actual realtime signal-processing behavior through `APOProcess`.

## 6. AERT helpers and runtime dependency

`baseaudioprocessingobject.h` exposes `AERT_Allocate` and `AERT_Free`. Both are available from Windows Vista, link through **Audioeng.lib**, and execute from **Audioeng.dll**. They are represented as both APO symbols and dependency records.

## 7. Remaining Media-Class PROPERTYKEY gaps closed

| Property | PROPERTYKEY |
|---|---|
| `PKEY_CompositeFX_KeywordDetector_StreamEffectClsid` | `D04E05A6-594B-4FB6-A80D-01AF5EED7D1D:16` |
| `PKEY_CompositeFX_KeywordDetector_ModeEffectClsid` | `D04E05A6-594B-4FB6-A80D-01AF5EED7D1D:17` |
| `PKEY_CompositeFX_KeywordDetector_EndpointEffectClsid` | `D04E05A6-594B-4FB6-A80D-01AF5EED7D1D:18` |
| `PKEY_SFX_KeywordDetector_ProcessingModes_Supported_For_Streaming` | `D3993A3F-99C2-4402-B5EC-A92A0367664B:8` |
| `PKEY_MFX_KeywordDetector_ProcessingModes_Supported_For_Streaming` | `D3993A3F-99C2-4402-B5EC-A92A0367664B:9` |

Also normalized:

- `PKEY_AudioEndpoint_Default_VolumeInDb` → `1DA5D803-D492-4EDD-8C23-E0C0FFEE7F0E:9`
- `PKEY_AudioEndpoint_Max_VolumeInDb` → `...:10`
- `PKEY_AudioEndpoint_Min_VolumeInDb` → `...:11`
- `PKEY_AudioEngine_OEMFormat` → `E4870E26-3CC5-4CD2-BA46-CA0A9A70ED04:3`
- `PKEY_APO_SWFallback_ProcessingModes` → `D3993A3F-99C2-4402-B5EC-A92A0367664B:13`

The previous database labeled Max/Min VolumeInDb as Windows 10. Current Microsoft requirements place both at **Windows 11 24H2 / build 26100**, so those rows are corrected.

## 8. What APO L5 means

The L5 claim is limited to the current public reference/header baseline: interfaces, methods, exact public IIDs/SIDs, processing-mode/effect GUIDs, APOERR values, SFX/MFX/EFX and CompositeFX property keys, CAPX property stores, package model, AEC/auxiliary inputs, notifications/logging/RT work queues, MsApoFxProxy discovery and the base helper surface.

It does not claim every vendor APO or Windows build behaves identically. L6 requires reproducible runtime evidence on real packages/builds: effect-state transitions, CAPX upgrade/migration, processing-mode negotiation, driver property responses and architecture-specific behavior.

## Primary sources

- Audio Signal Processing Modes — https://learn.microsoft.com/windows-hardware/drivers/audio/audio-signal-processing-modes
- Implementing Audio Processing Objects — https://learn.microsoft.com/windows-hardware/drivers/audio/implementing-audio-processing-objects
- Windows 11 APIs for APOs — https://learn.microsoft.com/windows-hardware/drivers/audio/windows-11-apis-for-audio-processing-objects
- Media-Class INF Extensions — https://learn.microsoft.com/windows-hardware/drivers/audio/media-class-inf-extensions
- win32metadata audioenginebaseapo.idl — https://github.com/microsoft/win32metadata/blob/main/generation/WinSDK/RecompiledIdlHeaders/um/audioenginebaseapo.idl
- win32metadata audioengineextensionapo.idl — https://github.com/microsoft/win32metadata/blob/main/generation/WinSDK/RecompiledIdlHeaders/um/audioengineextensionapo.idl
- win32metadata baseaudioprocessingobject.h — https://github.com/microsoft/win32metadata/blob/main/generation/WinSDK/RecompiledIdlHeaders/um/baseaudioprocessingobject.h
- Windows SDK metadata ksmedia — https://github.com/microsoft/windows-rs/blob/master/metadata/win32/ksmedia.rdl
