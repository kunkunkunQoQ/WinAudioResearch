# APO / CAPX / Media-Class INF Coverage Audit

> Baseline: **2026-10-02**  
> Scope: public APO runtime contracts, Windows 11 CAPX extensions, effects property registration, and APO deployment packaging.

## Current machine-readable coverage

| Area | Records | Status |
|---|---:|---|
| APO symbols/types | **51** | Strong / header-oriented |
| APO methods | **35** | Strong |
| Audio/FX property keys | **66 total property records** | Strong core |
| Media-Class INF / packaging | **16** | New dedicated table |
| APO-related dependencies | integrated | SDK/WDK/runtime mapped |
| Official APO samples | SwapAPO + AecAPO + DelayAPO + KWSApo | Linked |

Structured files:

- `api/apo.csv`
- `api/methods-apo.csv`
- `api/audio-properties.csv`
- `api/audio-inf.csv`
- `api/relationships.csv`
- `api/samples.csv`

## 1. Core APO contract

Microsoft requires custom system-effects APOs to implement the core processing interfaces:

```text
IAudioProcessingObject
IAudioProcessingObjectConfiguration
IAudioProcessingObjectRT
IAudioSystemEffects
```

The split is intentional: initialization/format negotiation is non-realtime, while `IAudioProcessingObjectRT::APOProcess` and related realtime methods must not block or touch paged memory.

Core initialization types now indexed include:

- `APOInitBaseStruct`
- `APOInitSystemEffects`
- `APOInitSystemEffects2`
- `APOInitSystemEffects3`
- `APO_REG_PROPERTIES`
- `APO_FLAG`

## 2. APO format model

The repository now indexes `IAudioMediaType` from `audiomediatype.h` plus its four public methods:

- `GetAudioFormat`
- `GetUncompressedAudioFormat`
- `IsCompressedFormat`
- `IsEqual`

`IAudioSystemEffectsCustomFormats` is also complete at the public method level:

- `GetFormatCount`
- `GetFormat`
- `GetFormatRepresentation`

This connects custom system-effects formats back to `IAudioMediaType`.

## 3. Realtime connection model

The APO database now includes the realtime connection types from `audioapotypes.h`:

```text
APO_CONNECTION_DESCRIPTOR
APO_CONNECTION_PROPERTY
APO_CONNECTION_PROPERTY_V2
APO_BUFFER_FLAGS
```

`APO_CONNECTION_PROPERTY_V2` adds a QPC timestamp and is important for AEC synchronization. An APO can inspect the connection signature before treating a base connection property as V2.

## 4. AEC CAPX contract

The capture AEC path is now modeled as:

```text
capture MFX
   ↓ implements
IApoAcousticEchoCancellation
   ↓
IApoAuxiliaryInputConfiguration
   ├─ AddAuxiliaryInput
   ├─ IsInputFormatSupported
   └─ RemoveAuxiliaryInput
   ↓
IApoAuxiliaryInputRT::AcceptInput
   ↓
reference audio circular buffer
   ↓
IAudioProcessingObjectRT::APOProcess
```

`IApoAcousticEchoCancellation` is a marker interface with no explicit methods. Microsoft restricts it to capture MFX APOs; if multiple APOs are chained, only the one closest to the device can implement it.

`IApoAcousticEchoCancellation2::GetDesiredReferenceStreamProperties` adds the ability to request reference-loopback properties such as post-volume loopback when supported.

## 5. Windows 11 notification framework

`audioengineextensionapo.h` adds a notification framework based on:

- `IAudioProcessingObjectNotifications`
- `IAudioProcessingObjectNotifications2`
- `APO_NOTIFICATION_TYPE`
- `APO_NOTIFICATION_DESCRIPTOR`
- `APO_NOTIFICATION`
- endpoint volume/property notifications
- system-effects property notifications
- microphone boost notifications
- environment/orientation notifications

Registration and delivery flow:

```text
GetApoNotificationRegistrationInfo[2]
            ↓
APO_NOTIFICATION_DESCRIPTOR[]
            ↓
Windows registers sources
            ↓
HandleNotification(APO_NOTIFICATION)
```

## 6. Windows 11 logging and threading services

`APOInitSystemEffects3` supplies an `IServiceProvider`. The APO can query:

```text
SID_AudioProcessingObjectLoggingService
      ↓
IAudioProcessingObjectLoggingService::ApoLog

SID_AudioProcessingObjectRTQueue
      ↓
IAudioProcessingObjectRTQueueService::GetRealTimeWorkQueue
```

The logging service is ETW-based and must not be called from the realtime-priority processing thread.

The realtime work queue gives the APO an OS-managed queue ID for short real-time-priority work items.

## 7. System-effect discovery and control

Windows 11's `IAudioSystemEffects3` exposes:

- `GetControllableSystemEffectsList`
- `SetAudioSystemEffectState`

Each `AUDIO_SYSTEMEFFECT` contains an effect GUID, current state and whether its state is changeable.

At the application side, `IAudioEffectsManager` represents the client-facing discovery/control surface; at the APO side, `IAudioSystemEffects3` represents the provider contract.

## 8. Effects registration: SFX / MFX / EFX

The repository already indexes the major CLSID keys:

```text
PKEY_FX_StreamEffectClsid     → SFX
PKEY_FX_ModeEffectClsid       → MFX
PKEY_FX_EndpointEffectClsid   → EFX
```

along with keyword-detector, offload and composite variants.

Processing-mode keys are also indexed, including streaming, offload and keyword-detector variants for SFX/MFX/EFX.

Microsoft documents `PKEY_CompositeFX_*` as REG_MULTI_SZ forms that allow multiple effects in a single graph position, introduced with Windows 10 version 1803.

## 9. Association and matching

Newly indexed:

- `PKEY_FX_Association`
- `PKEY_EP_Association`

The value is compared with the `KSPINDESCRIPTOR.Category` at the hardware end of the signal path.

Third-party audio drivers should use:

```text
FX\n  effects property stores
EP\n  endpoint property stores
```

while `MSFX` and `MSEP` are reserved for Microsoft inbox class-driver scenarios.

Property-store indices must be sequential; gaps can prevent later stores from being discovered.

## 10. Windows 11 CAPX settings property store

The Windows 11 settings framework moves custom effect settings under an APO context:

```text
FX\0\{ApoContext}\Default
FX\0\{ApoContext}\User
FX\0\{ApoContext}\Volatile
```

Semantics:

- **Default** — INF-populated defaults; suitable for driver/OEM defaults.
- **User** — user settings persisted by Windows across upgrade/migration.
- **Volatile** — runtime/time-varying state cleared on reboot and endpoint activation transitions.

These are exposed through `IAudioSystemEffectsPropertyStore` on Windows 11.

The same endpoint must not mix the new `IAudioSystemEffectsPropertyStore` settings model with the old generic `IPropertyStore` model for the same effects settings.

## 11. APO packaging by Windows version

Deployment class is version-sensitive:

| Windows target | Required APO package class |
|---|---|
| Windows 10 | `Class=SoftwareComponent` |
| Windows 11 21H2 / Build 22000+ | `Class=AudioProcessingObject` |

Known class GUIDs:

```text
SoftwareComponent
{5C4C3332-344D-483C-8739-259E934C9CC8}

AudioProcessingObject
{5989FCE8-9CD0-467D-8A6A-5419E31529D4}
```

Microsoft explicitly requires an OS ceiling for a Windows 10 SoftwareComponent APO package so that it does not deploy to Windows 11, plus a corresponding Windows 11 AudioProcessingObject package.

## 12. wdmaudio / CAPX registration helpers

Windows 11 drivers can reuse inbox registration support with:

```inf
Include=wdmaudio.inf
Needs=mssysfx.CopyFilesAndRegisterCapX
```

`wdmaudioapo.inf` is the AudioProcessingObject class extension INF used for device-specific SFX/MFX registration.

These contracts are now separately indexed in `api/audio-inf.csv` rather than being buried only in prose.

## 13. Official SysVAD examples

The sample graph now includes:

- **SwapAPO** — SFX/MFX registration and effects settings;
- **AecAPO** — capture MFX AEC reference-stream APIs;
- **DelayAPO** — custom processing / APOProcess;
- **KWSApo** — keyword-stream format and channel handling.

This makes it possible to navigate from a public interface or INF property key to a Microsoft implementation example.

## 14. Remaining APO gaps

Before promoting the whole APO domain to a strict L5, remaining work is:

1. audit `baseaudioprocessingobject.h` helper classes/macros separately from COM contracts;
2. audit `msapofxproxy.h` and inbox-proxy contracts;
3. normalize exact IIDs/SIDs/CLSIDs where public headers expose them;
4. finish `AUDIO_SIGNALPROCESSINGMODE_*` GUID inventory;
5. expand APO HRESULTs (`APOERR_*`);
6. map APO package/component INF examples by Windows build;
7. verify current installed WDK headers in addition to Microsoft Learn.

## Follow-up

The processing-mode GUID inventory, canonical `APOERR_*` values and `MsApoFxProxy` discovery contract are completed in [APO Processing Modes / APOERR / MsApoFxProxy Coverage Audit](107-APO-Processing-Modes-and-APOERR-Audit.md).

## Primary sources

- Audio Devices DDI Reference — https://learn.microsoft.com/windows/win32/api/_audio/
- audioenginebaseapo.h — https://learn.microsoft.com/windows/win32/api/audioenginebaseapo/
- audioengineextensionapo.h — https://learn.microsoft.com/windows/win32/api/audioengineextensionapo/
- Windows 11 APIs for APOs — https://learn.microsoft.com/windows-hardware/drivers/audio/windows-11-apis-for-audio-processing-objects
- Implementing APOs — https://learn.microsoft.com/windows-hardware/drivers/audio/implementing-audio-processing-objects
- Media-Class INF settings — https://learn.microsoft.com/windows-hardware/drivers/audio/media-class-inf-extensions
- Deploying APOs — https://learn.microsoft.com/windows-hardware/drivers/dashboard/deploying-audio-processing-objects
