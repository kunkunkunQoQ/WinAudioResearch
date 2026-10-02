# WinAudioResearch Resources Hub

这个目录作为“外部资料总入口”。

目标不是把网页全文复制进仓库，而是：

- 归类
- 解释为什么值得读
- 标记来源级别
- 保留原始链接
- 关联本仓库文章

---

## Official Microsoft

### Core Audio

https://learn.microsoft.com/windows/win32/coreaudio/

涵盖：

- MMDevice
- WASAPI
- Audio Session
- EndpointVolume
- DeviceTopology
- Spatial Audio

对应：

- ../docs/00-Windows-Audio-Architecture.md
- ../docs/18-Microsoft-Official-Documentation-Index.md

### Windows Audio Driver Docs

https://learn.microsoft.com/windows-hardware/drivers/audio/

涵盖：

- WDM
- WaveRT
- PortCls
- ACX
- APO
- AudioEndpointBuilder
- Bluetooth
- USB Audio
- power

### Media Foundation

https://learn.microsoft.com/windows/win32/medfound/

### Windows AudioGraph

https://learn.microsoft.com/windows/apps/develop/media-authoring-processing/audio-graphs

### Windows MIDI Services

https://github.com/microsoft/MIDI

---

## Official Microsoft Source / Samples

### Windows Classic Samples

https://github.com/microsoft/Windows-classic-samples

### Windows Universal Samples

https://github.com/microsoft/Windows-universal-samples

### Windows Driver Samples

https://github.com/microsoft/Windows-driver-samples

### SysVAD

https://github.com/microsoft/Windows-driver-samples/tree/main/audio/sysvad

---

## Windows SDK / WDK Headers

必查：

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
mmreg.h
mmeapi.h
ks.h
ksmedia.h
portcls.h
audioenginebaseapo.h
```

原则：

> Learn 解释语义，header 定义 ABI。

---

## Mature Open Source

### EarTrumpet

https://github.com/File-New-Project/EarTrumpet

### NAudio

https://github.com/naudio/NAudio

### OBS Studio

https://github.com/obsproject/obs-studio

### Chromium

https://chromium.googlesource.com/chromium/src/

### WebRTC

https://webrtc.googlesource.com/src/

### PortAudio

https://github.com/PortAudio/portaudio

### miniaudio

https://github.com/mackron/miniaudio

### FFmpeg

https://github.com/FFmpeg/FFmpeg

### Wine

https://gitlab.winehq.org/wine/wine

### ReactOS

https://github.com/reactos/reactos

---

## Specialist Blogs

### Matthew van Eerde

https://matthewvaneerde.wordpress.com/

Windows audio internals / Core Audio / endpoint / topology / diagnostics.

### Mark Heath

https://www.markheath.net/category/naudio

.NET / NAudio / WASAPI / audio programming.

---

## Project-Specific Research Sources

### SonicRoute

https://github.com/kunkunkunQoQ/SonicRoute

### SonicRoute Wiki

https://github.com/kunkunkunQoQ/SonicRoute/wiki

### WinAudioRoute

https://github.com/kunkunkunQoQ/WinAudioRoute

---

## Source Levels

### Level 1 — Public Contract

- Windows SDK / WDK headers
- Microsoft Learn API docs

### Level 2 — Microsoft Implementation Guidance

- Microsoft samples
- architecture guides
- driver design docs

### Level 3 — Mature Engineering Implementation

- EarTrumpet
- OBS
- Chromium
- WebRTC
- NAudio

### Level 4 — Community Investigation

- GitHub issues
- StackOverflow
- specialist blogs

### Level 5 — Reverse Engineering

- internal interface probing
- registry observation
- binary / symbol research

任何 Level 4/5 结论都不应自动写成 Public API contract。
