# References

这个目录负责记录 WinAudioResearch 的**来源层级与外部资料入口**。

如果你只想找 Microsoft 官方文档，优先看：

- [Microsoft 官方 Windows Audio 文档总索引](../docs/18-Microsoft-Official-Documentation-Index.md)
- [Microsoft 官方 Audio Samples / Tools](../docs/32-Microsoft-Audio-Samples-and-Tools.md)
- [Header / Library / DLL 对照表](../docs/37-Headers-Libraries-DLLs.md)

如果你想找第三方工程实现：

- [第三方 Windows Audio 开发生态](../docs/38-Third-Party-Audio-Ecosystem.md)

---

## 1. Microsoft Learn / SDK / WDK

### Windows Audio Architecture

https://learn.microsoft.com/windows-hardware/drivers/audio/windows-audio-architecture

### Core Audio

https://learn.microsoft.com/windows/win32/coreaudio/

重点：

- MMDevice
- WASAPI
- Audio Session
- EndpointVolume
- DeviceTopology

### WASAPI

https://learn.microsoft.com/windows/win32/coreaudio/wasapi

### Audio Driver Design Guide

https://learn.microsoft.com/windows-hardware/drivers/audio/

重点：

- WaveRT
- WDM Audio
- ACX
- APO
- AudioEndpointBuilder
- hardware offload
- processing modes

### Media Foundation

https://learn.microsoft.com/windows/win32/medfound/microsoft-media-foundation-sdk

### AudioGraph / WinRT Audio

https://learn.microsoft.com/windows/apps/develop/media-authoring-processing/audio-graphs

### Spatial Audio

https://learn.microsoft.com/windows/win32/coreaudio/spatial-sound

### XAudio2

https://learn.microsoft.com/windows/win32/xaudio2/xaudio2-introduction

### MIDI

Windows MIDI Services：

https://github.com/microsoft/MIDI

Legacy MIDI：

https://learn.microsoft.com/windows/win32/multimedia/midi-services

---

## 2. Microsoft 官方代码

### Windows Classic Samples

https://github.com/microsoft/Windows-classic-samples

重点：

- WASAPIRendering
- ApplicationLoopback
- Render/Capture Shared Event Driven
- Render Exclusive
- DuckingCaptureSample

### Windows Universal Samples

https://github.com/microsoft/Windows-universal-samples

重点：

- AudioCreation / AudioGraph
- WindowsAudioSession
- MIDI

### Windows Driver Samples

https://github.com/microsoft/Windows-driver-samples

重点：

- audio/sysvad
- audio/simpleaudiosample
- audio/Acx

### Windows MIDI Services

https://github.com/microsoft/MIDI

---

## 3. Microsoft 文档源码

### Win32 Docs

https://github.com/MicrosoftDocs/win32

适合全文搜索：

- interface
- HRESULT
- historical Core Audio notes

### Windows Driver Docs

https://github.com/MicrosoftDocs/windows-driver-docs

适合搜索：

- APO
- WaveRT
- ACX
- AudioEndpointBuilder
- driver property
- KS

---

## 4. 第三方开源实现

### SonicRoute

https://github.com/kunkunkunQoQ/SonicRoute

技术实现 / 实测来源：

https://github.com/kunkunkunQoQ/SonicRoute/wiki

### WinAudioRoute

https://github.com/kunkunkunQoQ/WinAudioRoute

### EarTrumpet

https://github.com/File-New-Project/EarTrumpet

重点：

- Audio Session
- MMDevice
- audio policy
- per-app routing
- internal Windows interfaces

### NAudio

https://github.com/naudio/NAudio

重点：

- .NET audio
- WASAPI
- WinMM
- Media Foundation
- MIDI
- sample provider / resampler

### PortAudio

https://github.com/PortAudio/portaudio

### miniaudio

https://github.com/mackron/miniaudio

### FFmpeg

https://github.com/FFmpeg/FFmpeg

### libsndfile

https://github.com/libsndfile/libsndfile

---

## 5. Windows SDK Headers

Public API 的 ABI 优先核对当前 SDK：

```text
mmdeviceapi.h
audioclient.h
audiopolicy.h
audiosessiontypes.h
endpointvolume.h
devicetopology.h
spatialaudioclient.h
audioclientactivationparams.h
propsys.h
mmeapi.h
mmreg.h
ksmedia.h
```

原则：

> Microsoft Learn 解释语义，SDK header 定义公开 ABI。

---

## 6. WDK / Driver Headers

驱动 / KS / APO：

```text
ks.h
ksmedia.h
portcls.h
audioenginebaseapo.h
ACX headers
```

---

## 7. 证据优先级

### Public API

```text
Windows SDK / WDK public header
        +
Microsoft Learn
        ↓
Microsoft official sample
        ↓
third-party implementation
```

### Undocumented API

没有公开规范时：

```text
multiple independent implementations
        +
Windows Build testing
        +
HRESULT / before-after state
        +
regression history
```

---

## 8. 引用原则

第三方项目只能证明：

> “这个实现存在 / 曾经工作 / 有工程实践价值”。

不能替代 Microsoft 对 public API 的规范。

对 undocumented API，每条重要结论尽量至少保留：

- 来源 URL
- commit / date
- Windows Build
- architecture
- IID / CLSID / vtable slot
- HRESULT
- 实测结果
- 未验证范围
