# 第三方 Windows Audio 开发生态索引

> 状态：第三方项目 / 社区参考  
> 原则：第三方项目非常适合学习工程实现，但**不能替代 Microsoft 对公开 API 的规范定义**。

本页整理 Windows 音频开发中常见、值得参考的开源项目和库，并说明它们分别适合研究什么。

---

## 1. NAudio

仓库：

https://github.com/naudio/NAudio

NAudio 是 .NET 音频生态中最有代表性的项目之一。

当前 NAudio 3 已拆分成多个更聚焦的 package，包括：

- NAudio.Core
- NAudio.Midi
- NAudio.Wasapi
- NAudio.WinMM
- NAudio.Asio
- NAudio.Dmo
- NAudio.Effects
- NAudio.Sampler
- NAudio.Vst3
- NAudio.Alsa
- NAudio.SoundFile

其中 Windows 相关重点：

### NAudio.Wasapi

适合参考：

- WASAPI playback
- capture
- loopback
- Core Audio COM interop
- Media Foundation codec integration

### NAudio.WinMM

适合参考：

- WaveOut / WaveIn
- legacy MIDI
- ACM
- mixer API

### NAudio.Midi

适合参考：

- MIDI event model
- MIDI file
- Windows MIDI backend

### 为什么值得看

如果你在 C# 里研究：

- WAVEFORMAT
- sample provider
- resampler
- mixer
- WASAPI
- MMDevice
- Media Foundation

NAudio 是很好的工程参考。

但如果你的目标是**真正理解 Windows 原生接口**，不要只停在 NAudio wrapper 上，仍然应该回到：

- Windows SDK Header
- Microsoft Learn
- 原始 COM ABI

---

## 2. EarTrumpet

仓库：

https://github.com/File-New-Project/EarTrumpet

EarTrumpet 是 Windows 音量合成器 / session 控制 / per-app routing 研究的重要参考。

适合研究：

- MMDevice
- Audio Session
- per-app volume
- endpoint changes
- audio policy
- undocumented routing
- Windows version differences

尤其值得关注：

- `IAudioPolicyConfigFactory`
- internal AudioPolicyConfig
- policy helper
- session / device model

### 使用原则

EarTrumpet 可以证明：

> “这个 Windows 内部机制曾被成熟项目使用。”

但不能证明：

> “Microsoft 承诺这个 internal interface 永久兼容。”

因此本仓库引用 EarTrumpet 时仍统一标记：

🔴 Undocumented / third-party verified

---

## 3. SonicRoute

仓库：

https://github.com/kunkunkunQoQ/SonicRoute

SonicRoute 是 WinAudioResearch 最重要的**真实产品验证来源之一**。

适合研究：

- 设备枚举
- session 枚举
- session volume
- endpoint mute
- audio meter
- per-app output / input route
- default endpoint switching
- C# COM lifecycle
- Win10 / Win11 internal API behavior

本仓库会把 SonicRoute 中可泛化的经验重新整理，而不是简单复制产品源码。

---

## 4. WinAudioRoute

仓库：

https://github.com/kunkunkunQoQ/WinAudioRoute

定位更接近：

> 可复用的 Windows 音频控制库。

和 WinAudioResearch 的区别：

```text
WinAudioRoute
→ library / API usability

WinAudioResearch
→ mechanism / evidence / docs / research
```

---

## 5. PortAudio

官网：

https://www.portaudio.com/

GitHub 镜像 / 源码：

https://github.com/PortAudio/portaudio

PortAudio 是经典跨平台 C 音频 I/O 库。

Windows backend 常见包括：

- WASAPI
- WMME
- DirectSound
- WDM-KS

适合研究：

- 跨平台 abstraction 怎么映射 Windows backend
- host API selection
- device enumeration
- callback / blocking stream model

它不会替你解释所有 Windows Audio policy / session 行为，因为它重点是音频 I/O portability。

---

## 6. miniaudio

官方仓库：

https://github.com/mackron/miniaudio

特点：

- single-file C library
- playback / capture
- resource manager
- decoder
- node graph
- cross-platform

Windows backend 包括：

- WASAPI
- DirectSound
- WinMM

适合：

- 小型 native audio tool
- cross-platform playback / capture
- 比较 WASAPI 与 legacy fallback backend

---

## 7. FFmpeg

官网：

https://ffmpeg.org/

源码：

https://github.com/FFmpeg/FFmpeg

它不是 Windows Audio API wrapper。

更适合：

- container
- codec
- decode / encode
- resample
- filter graph
- media conversion

Windows 音频程序经常组合：

```text
FFmpeg
  ↓ decoded PCM
WASAPI / XAudio2 / AudioGraph
  ↓
endpoint
```

不要把 FFmpeg 和 WASAPI 当同一层竞争 API。

---

## 8. libsndfile

https://github.com/libsndfile/libsndfile

适合：

- WAV
- FLAC
- AIFF
- OGG 等文件 I/O

主要解决：

> audio file format

而不是：

> Windows endpoint stream / session / routing。

---

## 9. RtAudio

https://github.com/thestk/rtaudio

跨平台 realtime audio I/O abstraction。

适合比较：

- WASAPI
- ASIO
- DirectSound
- CoreAudio
- ALSA
- JACK

之间的 API abstraction。

---

## 10. SDL Audio

https://github.com/libsdl-org/SDL

SDL audio 是游戏 / 跨平台程序常见高层 audio device layer。

适合：

- 不想直接写 WASAPI
- game / multimedia portability

但若需要：

- Windows session volume
- endpoint policy
- per-app route
- AudioEndpointVolume

仍需 Windows-specific API。

---

## 11. ASIO

ASIO 是 Steinberg 定义的专业音频 driver / API 生态，不属于 Microsoft Windows Audio API。

典型目标：

- DAW
- low latency professional audio
- audio interface

研究 Windows 专业音频时，通常需要把：

```text
WASAPI Exclusive / IAudioClient3
vs
ASIO
```

作为不同技术路径比较。

---

## 12. 参考项目优先级

本仓库建议：

### Public API 语义

```text
Microsoft Learn / SDK
→ Microsoft Samples
→ third-party wrappers
```

### Undocumented API

```text
multiple independent projects
+
Windows Build testing
+
SonicRoute / EarTrumpet observations
```

不能仅因为 GitHub 上有一个实现就把 internal ABI 写成事实标准。

---

## 13. 什么时候看哪一个项目

| 需求 | 优先参考 |
|---|---|
| C# Windows Audio | NAudio |
| Windows mixer / sessions | EarTrumpet / SonicRoute |
| per-app routing internal API | EarTrumpet / SonicRoute |
| 跨平台 C I/O | PortAudio / miniaudio |
| codec / transcode | FFmpeg |
| audio files | libsndfile |
| game cross-platform | SDL / miniaudio |
| professional low latency | ASIO + WASAPI |
