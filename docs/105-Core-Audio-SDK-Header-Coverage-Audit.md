# Core Audio SDK Header Coverage Audit

> Baseline: **2026-10-02**  
> Scope: public Windows SDK Core Audio headers and their method surfaces.

This audit turns the classic application-facing Windows Audio layer into a header-driven reference, rather than a loose collection of interface names.

## Audited headers

| Header / surface | Symbol records | Method records | Status |
|---|---:|---:|---|
| `mmdeviceapi.h` | 17 | 26 | **L5 / header surface audited** |
| `audioclient.h` + `audioclientactivationparams.h` | 27 | 50 | **L5 / header surface audited** |
| `audiopolicy.h` / session surface | 11 | 33 | **L5 / method surface audited** |
| `endpointvolume.h` | 8 | 24 | **L5 / header surface audited** |
| `devicetopology.h` | 32 | 64 | **L5 / header surface audited** |
| `audiostatemonitorapi.h` | 11 | 3 | **L5 / header surface audited** |

L5 here means the public reference surface was compared against the current Microsoft Learn header/reference pages used for this baseline.

It does **not** mean every behavior has been verified on every Windows build.

## 1. mmdeviceapi.h

The repository now represents the complete public header categories shown by Microsoft.

Interfaces: `IActivateAudioInterfaceAsyncOperation`, `IActivateAudioInterfaceCompletionHandler`, `IAudioSystemEffectsPropertyChangeNotificationClient`, `IAudioSystemEffectsPropertyStore`, `IMMDevice`, `IMMDeviceCollection`, `IMMDeviceEnumerator`, `IMMEndpoint`, `IMMNotificationClient`.

Function: `ActivateAudioInterfaceAsync`.

Structures: `AudioExtensionParams`, `DIRECTX_AUDIO_ACTIVATION_PARAMS`.

Enumerations: `AUDIO_SYSTEMEFFECTS_PROPERTYSTORE_TYPE`, `EDataFlow`, `EndpointFormFactor`, `ERole`.

The database additionally records the `MMDeviceEnumerator` COM class because it is required to acquire `IMMDeviceEnumerator`.

### Async activation path

```text
ActivateAudioInterfaceAsync
        ↓
IActivateAudioInterfaceAsyncOperation
        ↓
IActivateAudioInterfaceCompletionHandler::ActivateCompleted
        ↓
GetActivateResult
        ↓
requested WASAPI interface
```

### Windows 11 effects property stores

```text
IMMDevice
   ↓ Activate
IAudioSystemEffectsPropertyStore
   ├─ OpenDefaultPropertyStore
   ├─ OpenUserPropertyStore
   ├─ OpenVolatilePropertyStore
   └─ property-change notifications
```

This is a public Windows 11 endpoint/effects configuration surface and should not be confused with undocumented audio policy interfaces.

## 2. audioclient.h

The interface inventory now covers the current Microsoft header page, including classic WASAPI plus `IAudioClientDuckingControl`, `IAudioEffectsManager`, `IAudioEffectsChangedNotificationClient`, `IAudioViewManagerService`, and `IAcousticEchoCancellationControl`.

The method table now includes the previously missing modern methods: effects callback unregister, `OnAudioEffectsChanged`, HWND/audio-stream association, Windows 11 AEC reference endpoint selection, complete `IAudioStreamVolume`, and complete `IChannelAudioVolume`.

### Windows 11 effects

```text
IAudioClient::GetService
        ↓
IAudioEffectsManager
   ├─ GetAudioEffects
   ├─ SetAudioEffectState
   ├─ Register...
   └─ Unregister...
        ↓
IAudioEffectsChangedNotificationClient
```

### AEC reference endpoint control

On Windows build 22621+, an initialized capture client can query `IAcousticEchoCancellationControl`. Failure to obtain the interface does not necessarily mean the endpoint has no AEC; it can mean the implementation does not expose reference-endpoint selection.

## 3. audioclientactivationparams.h

The process-loopback activation contract is now complete at header level: `AUDIOCLIENT_ACTIVATION_PARAMS`, `AUDIOCLIENT_PROCESS_LOOPBACK_PARAMS`, `AUDIOCLIENT_ACTIVATION_TYPE`, `PROCESS_LOOPBACK_MODE`.

Minimum documented client: **Windows 10 Build 20348**.

## 4. audiopolicy.h / Audio Session

The session surface already had strong method coverage before this pass. The database contains the public session manager/control/enumerator/event/ducking interfaces and **33 method records**.

## 5. endpointvolume.h

Public header surface includes `IAudioEndpointVolume`, `IAudioEndpointVolumeEx`, `IAudioEndpointVolumeCallback`, `IAudioMeterInformation`, and `AUDIO_VOLUME_NOTIFICATION_DATA`. The method audit now includes `IAudioEndpointVolumeEx::GetVolumeRangeChannel`.

## 6. devicetopology.h

This pass is substantially larger than the previous DeviceTopology database. Method coverage increased from **25 → 64**.

Added areas include part/control lifecycle, `IPartsList`, control-change callbacks, jack descriptions, jack sink information, KS format support, generic per-channel dB controls, AGC, loudness, hardware mute, mux/demux selectors, channel configuration, peak meter and device-specific properties.

Important user-mode ↔ KS mappings are now explicit:

```text
IKsJackDescription      ↔ KSPROPERTY_JACK_DESCRIPTION
IKsJackDescription2     ↔ KSPROPERTY_JACK_DESCRIPTION2
IKsJackSinkInformation  ↔ KSPROPERTY_JACK_SINK_INFO
IKsFormatSupport        ↔ KSPROPERTY_PIN_DATAINTERSECTION
IAudioAutoGainControl   ↔ KSPROPERTY_AUDIO_AGC
IAudioMute              ↔ KSPROPERTY_AUDIO_MUTE
```

`IAudioBass`, `IAudioMidrange`, `IAudioTreble` and `IAudioVolumeLevel` inherit the generic `IPerChannelDbLevel` contract and therefore are not duplicated as independent method rows.

## 7. audiostatemonitorapi.h

A dedicated machine-readable family has now been added: `api/audio-state-monitor.csv` and `api/methods-audio-state-monitor.csv`.

Microsoft documents this API from **Windows build 19043**.

Public surface: `IAudioStateMonitor`, `AudioStateMonitorCallback`, `AudioStateMonitorSoundLevel`, and eight capture/render factory functions.

Methods: `GetSoundLevel`, `RegisterCallback`, `UnregisterCallback`.

```text
Create*AudioStateMonitor
       ↓
IAudioStateMonitor
   ├─ GetSoundLevel
   └─ RegisterCallback
          ↓
AudioStateMonitorCallback
```

## 8. What L5 does not cover yet

The next application-layer audit should focus on adjacent Windows Audio contracts rather than repeatedly re-auditing the classic five: APO/system-effects registration headers, Media-Class INF contracts, full Core Audio HRESULTs, endpoint/device property keys, processing-mode GUIDs, exact IID/CLSID catalogs, SDK version deltas, and real-build callback/threading behavior.

## Primary Microsoft sources

- mmdeviceapi.h — https://learn.microsoft.com/windows/win32/api/mmdeviceapi/
- audioclient.h — https://learn.microsoft.com/windows/win32/api/audioclient/
- audiopolicy.h — https://learn.microsoft.com/windows/win32/api/audiopolicy/
- endpointvolume.h — https://learn.microsoft.com/windows/win32/api/endpointvolume/
- devicetopology.h — https://learn.microsoft.com/windows/win32/api/devicetopology/
- audioclientactivationparams.h — https://learn.microsoft.com/windows/win32/api/audioclientactivationparams/
- audiostatemonitorapi.h — https://learn.microsoft.com/windows/win32/api/audiostatemonitorapi/
