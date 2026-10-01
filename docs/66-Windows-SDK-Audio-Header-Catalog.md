# Windows SDK Audio Header Catalog

> 状态：🟢 Public Windows SDK  
> 目标：按 Header 建立接口目录，让开发者能从 ABI / SDK 结构出发检索 Windows Audio。

这不是复制 Windows SDK，而是建立：

```text
Header
→ Interfaces
→ Structures
→ Enumerations
→ 典型用途
→ 对应仓库文档
```

的快速地图。

---

# 1. mmdeviceapi.h

核心用途：

- endpoint enumeration
- default endpoint
- endpoint notifications
- async audio interface activation
- Windows 11 system effects property store

## Interfaces

- `IActivateAudioInterfaceAsyncOperation`
- `IActivateAudioInterfaceCompletionHandler`
- `IAudioSystemEffectsPropertyChangeNotificationClient`
- `IAudioSystemEffectsPropertyStore`
- `IMMDevice`
- `IMMDeviceCollection`
- `IMMDeviceEnumerator`
- `IMMEndpoint`
- `IMMNotificationClient`

## Function

- `ActivateAudioInterfaceAsync`

## Structures

- `AudioExtensionParams`
- `DIRECTX_AUDIO_ACTIVATION_PARAMS`

## Enumerations

- `AUDIO_SYSTEMEFFECTS_PROPERTYSTORE_TYPE`
- `EDataFlow`
- `EndpointFormFactor`
- `ERole`

官方：

https://learn.microsoft.com/windows/win32/api/mmdeviceapi/

仓库：

- [MMDevice](01-MMDevice.md)
- [Default Device](07-Default-Audio-Device.md)
- [Device IDs & Properties](12-Device-IDs-and-Properties.md)
- [Windows 11 Effects APIs](64-Windows11-AEC-and-Effects-APIs.md)

---

# 2. audioclient.h

核心用途：

- WASAPI stream
- render / capture buffer
- clocks
- session / stream volume
- offload
- low latency
- AEC
- ducking
- effects
- stream ↔ HWND association

## Interfaces

### Core Stream

- `IAudioClient`
- `IAudioClient2`
- `IAudioClient3`
- `IAudioRenderClient`
- `IAudioCaptureClient`

### Clock

- `IAudioClock`
- `IAudioClock2`
- `IAudioClockAdjustment`

### Volume

- `IAudioStreamVolume`
- `IChannelAudioVolume`
- `ISimpleAudioVolume`

### Modern controls

- `IAcousticEchoCancellationControl`
- `IAudioClientDuckingControl`
- `IAudioEffectsManager`
- `IAudioEffectsChangedNotificationClient`
- `IAudioViewManagerService`

## Structures

- `AUDIO_EFFECT`
- `AudioClientProperties`

## Enumerations

- `_AUDCLNT_BUFFERFLAGS`
- `AUDCLNT_STREAMOPTIONS`
- `AUDIO_DUCKING_OPTIONS`
- `AUDIO_EFFECT_STATE`

官方：

https://learn.microsoft.com/windows/win32/api/audioclient/

仓库：

- [WASAPI](08-WASAPI.md)
- [WASAPI Advanced](19-WASAPI-Advanced.md)
- [Low Latency](26-Low-Latency-Raw-Offload.md)
- [Realtime / MMCSS](56-Realtime-Audio-Threading-and-MMCSS.md)
- [Windows 11 Effects APIs](64-Windows11-AEC-and-Effects-APIs.md)

---

# 3. audiopolicy.h

核心用途：

- Audio Session
- session events
- session enumeration
- ducking notifications

## Interfaces

- `IAudioSessionControl`
- `IAudioSessionControl2`
- `IAudioSessionEnumerator`
- `IAudioSessionEvents`
- `IAudioSessionManager`
- `IAudioSessionManager2`
- `IAudioSessionNotification`
- `IAudioVolumeDuckNotification`

官方：

https://learn.microsoft.com/windows/win32/api/audiopolicy/

仓库：

- [Audio Sessions](02-Audio-Sessions.md)
- [Session Edge Cases](15-Session-Enumeration-Edge-Cases.md)
- [Session Persistence / Ducking](40-Audio-Session-Persistence-and-Ducking.md)

---

# 4. endpointvolume.h

核心用途：

- endpoint master volume
- mute
- callback
- peak meter

## Interfaces

- `IAudioEndpointVolume`
- `IAudioEndpointVolumeCallback`
- `IAudioEndpointVolumeEx`
- `IAudioMeterInformation`

## Structure

- `AUDIO_VOLUME_NOTIFICATION_DATA`

官方：

https://learn.microsoft.com/windows/win32/api/endpointvolume/

仓库：

- [Volume / Mute](03-Volume-and-Mute.md)
- [Audio Meter](04-Audio-Meter.md)

---

# 5. devicetopology.h

核心用途：

- audio adapter topology
- connector / jack
- hardware controls
- KS format support

## Hardware control interfaces

- `IAudioAutoGainControl`
- `IAudioBass`
- `IAudioChannelConfig`
- `IAudioInputSelector`
- `IAudioLoudness`
- `IAudioMidrange`
- `IAudioMute`
- `IAudioOutputSelector`
- `IAudioPeakMeter`
- `IAudioTreble`
- `IAudioVolumeLevel`

## Topology interfaces

- `IConnector`
- `IControlChangeNotify`
- `IControlInterface`
- `IDeviceSpecificProperty`
- `IDeviceTopology`
- `IPart`
- `IPartsList`
- `IPerChannelDbLevel`
- `ISubunit`

## KS bridge interfaces

- `IKsFormatSupport`
- `IKsJackDescription`
- `IKsJackDescription2`
- `IKsJackSinkInformation`

## Structures

- `KSJACK_DESCRIPTION`
- `KSJACK_DESCRIPTION2`
- `KSJACK_SINK_INFORMATION`
- `LUID`

## Enumerations

- `ConnectorType`
- `DataFlow`
- `KSJACK_SINK_CONNECTIONTYPE`
- `PartType`

官方：

https://learn.microsoft.com/windows/win32/api/devicetopology/

仓库：

- [DeviceTopology](20-DeviceTopology.md)
- [Jacks / Connectors / Microphone Arrays](49-Jacks-Connectors-and-Microphone-Arrays.md)

---

# 6. spatialaudioclient.h

核心用途：

- Windows Sonic
- object-based spatial rendering
- spatial stream
- static / dynamic audio object

## Interfaces

- `IAudioFormatEnumerator`
- `ISpatialAudioClient`
- `ISpatialAudioClient2`
- `ISpatialAudioObject`
- `ISpatialAudioObjectBase`
- `ISpatialAudioObjectRenderStream`
- `ISpatialAudioObjectRenderStreamBase`
- `ISpatialAudioObjectRenderStreamNotify`

## Structures

- `SpatialAudioClientActivationParams`
- `SpatialAudioObjectRenderStreamActivationParams`
- `SpatialAudioObjectRenderStreamActivationParams2`

## Enumerations

- `AudioObjectType`
- `SPATIAL_AUDIO_STREAM_OPTIONS`

官方：

https://learn.microsoft.com/windows/win32/api/spatialaudioclient/

仓库：

- [Spatial Audio](22-Spatial-Audio.md)

---

# 7. audiostatemonitorapi.h

核心用途：

> 按 render/capture、category、device、role 监控 audio stream sound level state。

## Interface

- `IAudioStateMonitor`

## Render factories

- `CreateRenderAudioStateMonitor`
- `CreateRenderAudioStateMonitorForCategory`
- `CreateRenderAudioStateMonitorForCategoryAndDeviceId`
- `CreateRenderAudioStateMonitorForCategoryAndDeviceRole`

## Capture factories

- `CreateCaptureAudioStateMonitor`
- `CreateCaptureAudioStateMonitorForCategory`
- `CreateCaptureAudioStateMonitorForCategoryAndDeviceId`
- `CreateCaptureAudioStateMonitorForCategoryAndDeviceRole`

官方：

https://learn.microsoft.com/windows/win32/api/audiostatemonitorapi/

仓库：

- [Audio State Monitor](63-Audio-State-Monitor.md)

---

# 8. audioclientactivationparams.h

核心用途：

- process loopback activation

主要：

- `AUDIOCLIENT_ACTIVATION_PARAMS`
- `AUDIOCLIENT_PROCESS_LOOPBACK_PARAMS`
- `AUDIOCLIENT_ACTIVATION_TYPE`
- `PROCESS_LOOPBACK_MODE`

官方：

https://learn.microsoft.com/windows/win32/api/audioclientactivationparams/

仓库：

- [Loopback / Process Audio Capture](27-Loopback-and-Process-Audio-Capture.md)

---

# 9. propsys.h / propkey.h / devpkey

核心用途：

- `IPropertyStore`
- `PROPERTYKEY`
- `PROPVARIANT`
- device property system

相关：

- PKEY_Device_FriendlyName
- PKEY_AudioEndpoint_*
- PKEY_AudioEngine_*

仓库：

- [Device IDs & Properties](12-Device-IDs-and-Properties.md)
- [Audio Endpoint Property Keys](44-Audio-Endpoint-Property-Keys.md)

---

# 10. mmeapi.h / mmreg.h

Legacy multimedia + audio format definitions。

典型：

- `WAVEFORMATEX`
- waveIn / waveOut
- mixer APIs
- MIDI WinMM

仓库：

- [Legacy APIs](30-Legacy-Windows-Audio-APIs.md)
- [Audio Formats](31-Audio-Formats-WAVEFORMAT.md)
- [Windows MIDI](29-Windows-MIDI.md)

---

# 11. ks.h / ksmedia.h

Kernel Streaming / audio driver media definitions。

包括：

- KSPROPERTY
- KSNODETYPE
- KSDATAFORMAT
- WAVEFORMATEXTENSIBLE
- speaker masks
- signal processing mode GUIDs
- effect GUIDs
- jack / audio topology definitions

仓库：

- [Driver Stack](25-Audio-Driver-Stack-WDM-WaveRT-ACX-KS.md)
- [Effects / Processing Modes](34-Audio-Effects-and-Processing-Modes.md)

---

# 12. audioenginebaseapo.h / audioengineextensionapo.h

APO：

- `IAudioProcessingObject`
- `IAudioProcessingObjectRT`
- APO configuration
- Windows 11 CAPX extensions
- effect notifications

仓库：

- [APO](23-Audio-Processing-Objects-APO.md)
- [Windows 11 Effects APIs](64-Windows11-AEC-and-Effects-APIs.md)

---

# 13. Media Foundation headers

常见：

```text
mfapi.h
mfidl.h
mfreadwrite.h
mferror.h
```

用于：

- media source
- Source Reader
- Sink Writer
- MFT
- codec
- media topology

仓库：

- [Media Foundation Audio](24-Media-Foundation-Audio.md)
- [ACM / DMO / MFT](46-ACM-DMO-MFT-Codecs.md)

---

# 14. XAudio2 headers

```text
xaudio2.h
x3daudio.h
xapo.h
xapobase.h
xapofx.h
xaudio2fx.h
hrtfapoapi.h
```

仓库：

- [XAudio2](28-XAudio2.md)

---

# 15. Driver / ACX headers

传统：

- `portcls.h`
- `ks.h`
- `ksmedia.h`

ACX：

- `acxdevice.h`
- `acxcircuit.h`
- `acxstreams.h`
- `acxpin.h`
- `acxelements.h`

仓库：

- [Driver Stack](25-Audio-Driver-Stack-WDM-WaveRT-ACX-KS.md)

---

# 16. 使用这个 Catalog 的原则

写 wrapper / P/Invoke / COM interop 时：

```text
Microsoft Learn
     +
current Windows SDK header
     +
official sample
```

三者交叉核对。

尤其不要：

> 从一篇十年前博客复制 interface，然后假设今天的 header 还是那个集合。

Windows 11 已新增多项公开 audio interfaces。
