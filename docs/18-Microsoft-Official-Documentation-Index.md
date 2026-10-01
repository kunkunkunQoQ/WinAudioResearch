# Microsoft 官方 Windows Audio 文档总索引

> 目标：把 Windows 音频开发中最常用、最容易散落的 Microsoft 官方文档整理到一个入口。  
> 本页优先收录 Microsoft Learn、Windows SDK/WDK 文档和 Microsoft 官方示例仓库。

---

## 1. Windows 音频总架构

### Windows 10 / 11 Audio Architecture
https://learn.microsoft.com/windows-hardware/drivers/audio/windows-audio-architecture

适合先看。它把 Windows 音频栈分成：

- 应用层 API
- Audio Engine
- Audio Service
- Audio Endpoint Builder
- Audio Driver
- Hardware

Microsoft 当前架构页还明确区分了“推荐用于现代 Windows 应用的 API”和传统 Core Audio 控制面。

### Audio Devices Design Guide
https://learn.microsoft.com/windows-hardware/drivers/audio/

这是驱动侧音频文档总入口。

### About the Windows Core Audio APIs
https://learn.microsoft.com/windows/win32/coreaudio/about-the-windows-core-audio-apis

Core Audio 总览，包括：

- MMDevice API
- WASAPI
- DeviceTopology
- EndpointVolume

---

## 2. MMDevice / Endpoint / Device Enumeration

### IMMDeviceEnumerator
https://learn.microsoft.com/windows/win32/api/mmdeviceapi/nn-mmdeviceapi-immdeviceenumerator

### Enumerating Audio Devices
https://learn.microsoft.com/windows/win32/coreaudio/enumerating-audio-devices

### Endpoint ID Strings
https://learn.microsoft.com/windows/win32/coreaudio/endpoint-id-strings

### Device Properties
https://learn.microsoft.com/windows/win32/coreaudio/device-properties

### EndpointFormFactor
https://learn.microsoft.com/windows/win32/api/mmdeviceapi/ne-mmdeviceapi-endpointformfactor

### PKEY_AudioEndpoint_FormFactor
https://learn.microsoft.com/windows/win32/coreaudio/pkey-audioendpoint-formfactor

### Modern device enumeration / DeviceInformation
https://learn.microsoft.com/windows/apps/develop/devices-sensors/device-information-properties

Microsoft 的 Windows 10/11 架构文档更推荐现代应用使用 `Windows.Devices.Enumeration` 做设备枚举；传统桌面音频工具仍大量直接使用 MMDevice。

---

## 3. Default Endpoint / Endpoint Builder

### GetDefaultAudioEndpoint
https://learn.microsoft.com/windows/win32/api/mmdeviceapi/nf-mmdeviceapi-immdeviceenumerator-getdefaultaudioendpoint

### EDataFlow
https://learn.microsoft.com/windows/win32/api/mmdeviceapi/ne-mmdeviceapi-edataflow

### ERole
https://learn.microsoft.com/windows/win32/api/mmdeviceapi/ne-mmdeviceapi-erole

### Default Audio Endpoint Selection
https://learn.microsoft.com/windows-hardware/drivers/audio/default-audio-endpoint-selection

这篇非常重要，解释 Windows 如何根据：

- 用户首选项
- jack detection
- form factor
- KSNodeType
- bus type
- location
- role

选择默认 endpoint。

### Audio Endpoint Builder Algorithm
https://learn.microsoft.com/windows-hardware/drivers/audio/audio-endpoint-builder-algorithm

### PKEY_AudioDevice_EnableEndpointByDefault
https://learn.microsoft.com/windows-hardware/drivers/audio/pkey-audiodevice-enableendpointbydefault

---

## 4. Audio Session

### Audio Sessions
https://learn.microsoft.com/windows/win32/coreaudio/audio-sessions

### IAudioSessionManager2
https://learn.microsoft.com/windows/win32/api/audiopolicy/nn-audiopolicy-iaudiosessionmanager2

### IAudioSessionEnumerator
https://learn.microsoft.com/windows/win32/api/audiopolicy/nn-audiopolicy-iaudiosessionenumerator

### IAudioSessionControl2
https://learn.microsoft.com/windows/win32/api/audiopolicy/nn-audiopolicy-iaudiosessioncontrol2

### IAudioSessionEvents
https://learn.microsoft.com/windows/win32/api/audiopolicy/nn-audiopolicy-iaudiosessionevents

### RegisterSessionNotification
https://learn.microsoft.com/windows/win32/api/audiopolicy/nf-audiopolicy-iaudiosessionmanager2-registersessionnotification

### ISimpleAudioVolume
https://learn.microsoft.com/windows/win32/api/audioclient/nn-audioclient-isimpleaudiovolume

---

## 5. EndpointVolume / Meter

### EndpointVolume API
https://learn.microsoft.com/windows/win32/coreaudio/endpointvolume-api

### endpointvolume.h
https://learn.microsoft.com/windows/win32/api/endpointvolume/

### IAudioEndpointVolume
https://learn.microsoft.com/windows/win32/api/endpointvolume/nn-endpointvolume-iaudioendpointvolume

### IAudioEndpointVolumeCallback
https://learn.microsoft.com/windows/win32/api/endpointvolume/nn-endpointvolume-iaudioendpointvolumecallback

### IAudioMeterInformation
https://learn.microsoft.com/windows/win32/api/endpointvolume/nn-endpointvolume-iaudiometerinformation

### Peak Meters
https://learn.microsoft.com/windows/win32/coreaudio/peak-meters

### Volume Controls
https://learn.microsoft.com/windows/win32/coreaudio/volume-controls

---

## 6. WASAPI

### About WASAPI
https://learn.microsoft.com/windows/win32/coreaudio/wasapi

### audioclient.h
https://learn.microsoft.com/windows/win32/api/audioclient/

### IAudioClient
https://learn.microsoft.com/windows/win32/api/audioclient/nn-audioclient-iaudioclient

### IAudioClient2
https://learn.microsoft.com/windows/win32/api/audioclient/nn-audioclient-iaudioclient2

### IAudioClient3
https://learn.microsoft.com/windows/win32/api/audioclient/nn-audioclient-iaudioclient3

### IAudioRenderClient
https://learn.microsoft.com/windows/win32/api/audioclient/nn-audioclient-iaudiorenderclient

### IAudioCaptureClient
https://learn.microsoft.com/windows/win32/api/audioclient/nn-audioclient-iaudiocaptureclient

### IAudioClock
https://learn.microsoft.com/windows/win32/api/audioclient/nn-audioclient-iaudioclock

### Stream Management
https://learn.microsoft.com/windows/win32/coreaudio/stream-management

### Exclusive-Mode Streams
https://learn.microsoft.com/windows/win32/coreaudio/exclusive-mode-streams

### AUDCLNT stream flags
https://learn.microsoft.com/windows/win32/coreaudio/audclnt-streamflags-xxx-constants

### AUDCLNT_STREAMOPTIONS
https://learn.microsoft.com/windows/win32/api/audioclient/ne-audioclient-audclnt_streamoptions

---

## 7. Low Latency / IAudioClient3

### Low Latency Audio
https://learn.microsoft.com/windows-hardware/drivers/audio/low-latency-audio

### IAudioClient3
https://learn.microsoft.com/windows/win32/api/audioclient/nn-audioclient-iaudioclient3

### GetSharedModeEnginePeriod
https://learn.microsoft.com/windows/win32/api/audioclient/nf-audioclient-iaudioclient3-getsharedmodeengineperiod

### InitializeSharedAudioStream
https://learn.microsoft.com/windows/win32/api/audioclient/nf-audioclient-iaudioclient3-initializesharedaudiostream

---

## 8. Loopback / Process Loopback

### Loopback Recording
https://learn.microsoft.com/windows/win32/coreaudio/loopback-recording

### ActivateAudioInterfaceAsync
https://learn.microsoft.com/windows/win32/api/mmdeviceapi/nf-mmdeviceapi-activateaudiointerfaceasync

### audioclientactivationparams.h
https://learn.microsoft.com/windows/win32/api/audioclientactivationparams/

### AUDIOCLIENT_ACTIVATION_PARAMS
https://learn.microsoft.com/windows/win32/api/audioclientactivationparams/ns-audioclientactivationparams-audioclient_activation_params

### AUDIOCLIENT_PROCESS_LOOPBACK_PARAMS
https://learn.microsoft.com/windows/win32/api/audioclientactivationparams/ns-audioclientactivationparams-audioclient_process_loopback_params

### PROCESS_LOOPBACK_MODE
https://learn.microsoft.com/windows/win32/api/audioclientactivationparams/ne-audioclientactivationparams-process_loopback_mode

### Application Loopback Audio Capture sample
https://learn.microsoft.com/samples/microsoft/windows-classic-samples/applicationloopbackaudio-sample/

---

## 9. DeviceTopology

### IDeviceTopology
https://learn.microsoft.com/windows/win32/api/devicetopology/nn-devicetopology-idevicetopology

### DeviceTopology API overview
https://learn.microsoft.com/windows/win32/coreaudio/device-topologies

### devicetopology.h
https://learn.microsoft.com/windows/win32/api/devicetopology/

用途：

- 查看 adapter 内部 audio path
- connector
- part
- control interface
- hardware volume / mux 等拓扑控制

---

## 10. AudioGraph / Windows.Media.Audio

### Audio graphs
https://learn.microsoft.com/windows/apps/develop/media-authoring-processing/audio-graphs

### AudioGraph class
https://learn.microsoft.com/uwp/api/windows.media.audio.audiograph

### AudioDeviceInputNode
https://learn.microsoft.com/uwp/api/windows.media.audio.audiodeviceinputnode

### AudioDeviceOutputNode
https://learn.microsoft.com/uwp/api/windows.media.audio.audiodeviceoutputnode

AudioGraph 适合：

- routing
- mixing
- capture
- processing
- file nodes
- custom audio frames
- spatial-enabled nodes

---

## 11. Spatial Audio / Windows Sonic

### Spatial Sound
https://learn.microsoft.com/windows/win32/coreaudio/spatial-sound

### Render Spatial Sound Using Spatial Audio Objects
https://learn.microsoft.com/windows/win32/coreaudio/render-spatial-sound-using-spatial-audio-objects

### ISpatialAudioClient
https://learn.microsoft.com/windows/win32/api/spatialaudioclient/nn-spatialaudioclient-ispatialaudioclient

### ISpatialAudioObject
https://learn.microsoft.com/windows/win32/api/spatialaudioclient/nn-spatialaudioclient-ispatialaudioobject

### ISpatialAudioObjectRenderStream
https://learn.microsoft.com/windows/win32/api/spatialaudioclient/nn-spatialaudioclient-ispatialaudioobjectrenderstream

---

## 12. Audio Effects / APO

### Windows Audio Processing Objects
https://learn.microsoft.com/windows-hardware/drivers/audio/windows-audio-processing-objects

### Audio Processing Object Architecture
https://learn.microsoft.com/windows-hardware/drivers/audio/audio-processing-object-architecture

### Implementing Audio Processing Objects
https://learn.microsoft.com/windows-hardware/drivers/audio/implementing-audio-processing-objects

### Windows 11 APIs for APO
https://learn.microsoft.com/windows-hardware/drivers/audio/windows-11-apis-for-audio-processing-objects

### Audio Signal Processing Modes
https://learn.microsoft.com/windows-hardware/drivers/audio/audio-signal-processing-modes

### IAudioEffectsManager
https://learn.microsoft.com/windows/win32/api/audioclient/nn-audioclient-iaudioeffectsmanager

---

## 13. Driver / WDM / WaveRT / ACX / KS

### Audio Devices Design Guide
https://learn.microsoft.com/windows-hardware/drivers/audio/

### Windows Audio Architecture
https://learn.microsoft.com/windows-hardware/drivers/audio/windows-audio-architecture

### ACX Audio Class Extensions
https://learn.microsoft.com/windows-hardware/drivers/audio/acx-audio-class-extensions-overview

### Audio DDI reference
https://learn.microsoft.com/windows-hardware/drivers/ddi/_audio/

### Audio Topology Nodes
https://learn.microsoft.com/windows-hardware/drivers/audio/audio-topology-nodes

### Hardware-Offloaded Audio Processing
https://learn.microsoft.com/windows-hardware/drivers/audio/hardware-offloaded-audio-processing

### SysVAD sample
https://github.com/microsoft/Windows-driver-samples/tree/main/audio/sysvad

### Simple Audio Sample
https://github.com/microsoft/Windows-driver-samples/tree/main/audio/simpleaudiosample

### ACX samples
https://github.com/microsoft/Windows-driver-samples/tree/main/audio/Acx

---

## 14. Media Foundation Audio

### Media Foundation
https://learn.microsoft.com/windows/win32/medfound/microsoft-media-foundation-sdk

### Source Reader
https://learn.microsoft.com/windows/win32/medfound/source-reader

### Sink Writer
https://learn.microsoft.com/windows/win32/medfound/sink-writer

### Supported Media Formats
https://learn.microsoft.com/windows/win32/medfound/supported-media-formats-in-media-foundation

适合：

- MP3 / AAC / WMA / M4A / MP4 等媒体解析
- decode / encode
- resample
- transcode
- file-to-PCM / PCM-to-file

---

## 15. XAudio2

### XAudio2 Introduction
https://learn.microsoft.com/windows/win32/xaudio2/xaudio2-introduction

### XAudio2 API Reference
https://learn.microsoft.com/windows/win32/api/_xaudio2/

典型对象：

- IXAudio2
- SourceVoice
- SubmixVoice
- MasteringVoice
- XAPO
- X3DAudio

特别适合游戏、复杂 voice graph 和低级实时播放场景。

---

## 16. MIDI

### Windows MIDI Services official repository
https://github.com/microsoft/MIDI

### Current Windows MIDI Services docs
https://aka.ms/midi

### Legacy WinMM MIDI Services
https://learn.microsoft.com/windows/win32/multimedia/midi-services

Windows MIDI Services 是 Microsoft 当前下一代 Windows MIDI 项目，包含 MIDI 1.0、MIDI 2.0、UMP、新 USB driver、transport 和工具。

---

## 17. Legacy APIs

### Waveform Audio
https://learn.microsoft.com/windows/win32/multimedia/waveform-audio

### Waveform Structures
https://learn.microsoft.com/windows/win32/multimedia/waveform-structures

Microsoft 当前明确把 Waveform Audio 视为 legacy，并建议新代码优先 WASAPI / AudioGraph。

### DirectSound
https://learn.microsoft.com/windows/win32/directsound/directsound

### Windows Audio Architecture
https://learn.microsoft.com/windows-hardware/drivers/audio/windows-audio-architecture

当前架构页把 DirectSound、DirectShow、PlaySound 等放在旧 API / deprecated 范畴，应避免新项目仅因为“简单”而默认选择旧栈。

---

## 18. Audio Formats

### WAVEFORMATEX
https://learn.microsoft.com/windows/win32/api/mmeapi/ns-mmeapi-waveformatex

### WAVEFORMATEXTENSIBLE
https://learn.microsoft.com/windows-hardware/drivers/ddi/ksmedia/ns-ksmedia-waveformatextensible

### Channel Mask
https://learn.microsoft.com/windows-hardware/drivers/audio/channel-mask

---

## 19. Microsoft 官方样例仓库

### Windows Classic Samples
https://github.com/microsoft/Windows-classic-samples

重点：

- WASAPIRendering
- CaptureSharedEventDriven
- RenderSharedEventDriven
- RenderExclusiveEventDriven
- ApplicationLoopback

### Windows Universal Samples
https://github.com/microsoft/Windows-universal-samples

重点：

- AudioCreation / AudioGraph
- WindowsAudioSession
- Spatial audio
- MIDI
- Media capture

### Windows Driver Samples
https://github.com/microsoft/Windows-driver-samples

重点：

- audio/sysvad
- audio/simpleaudiosample
- audio/Acx

---

## 20. 使用这个索引时的原则

优先级建议：

```text
Microsoft Learn / Windows SDK / WDK
        ↓
Microsoft sample
        ↓
长期维护的第三方项目
        ↓
社区文章 / issue / reverse engineering
```

当第三方项目与 Microsoft 文档冲突时：

- Public API：优先 Microsoft 文档 / SDK
- Undocumented API：保留冲突并按 Windows Build 实测
