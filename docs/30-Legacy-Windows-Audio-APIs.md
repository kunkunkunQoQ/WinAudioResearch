# Legacy Windows Audio APIs：WinMM、DirectSound、DirectShow 等

> 状态：🟢 Public / Legacy  
> 目标不是鼓励新项目使用，而是帮助理解旧代码、兼容层与 Windows 音频历史。

---

## 1. Microsoft 当前架构建议

Windows 10/11 Audio Architecture 文档把一些旧 API 明确列为 deprecated / older：

- DirectShow
- DirectSound
- PlaySound
- Windows.Media.MediaControl

同时 Microsoft 对 Waveform Audio 文档明确建议：

> 新代码优先 WASAPI / AudioGraph。

---

## 2. WinMM Wave APIs

经典：

```text
waveOutOpen
waveOutWrite
waveOutPrepareHeader
waveOutClose

waveInOpen
waveInAddBuffer
waveInStart
waveInStop
```

数据结构：

- WAVEFORMATEX
- WAVEHDR
- WAVEOUTCAPS
- WAVEINCAPS

---

## 3. Mixer APIs

经典：

- mixerOpen
- mixerGetLineInfo
- mixerGetLineControls
- mixerSetControlDetails

这些 API 来自更早期的 Windows audio mixer model。

在现代 Vista+ endpoint / session 架构中，不应把 mixerXxx 与 Core Audio EndpointVolume 简单等同。

---

## 4. DirectSound

DirectSound 曾经是 Windows game / multimedia audio 的核心 API。

现代 Windows 中很多 DirectSound 路径最终建立在新音频栈之上。

新 game audio 通常更应该研究：

- XAudio2
- WASAPI

---

## 5. DirectSoundCapture

用于 legacy capture。

新开发通常优先：

- WASAPI
- AudioGraph
- MediaCapture

---

## 6. DirectShow

DirectShow 是旧媒体 pipeline。

仍有大量 legacy 软件、capture filter、codec graph 使用它。

新 Windows media app 通常更应该研究：

- Media Foundation

---

## 7. PlaySound / sndPlaySound

适合非常简单的：

- system sound
- WAV playback

不适合：

- mixer
- low latency
- per-app routing
- modern capture
- serious media playback

---

## 8. MCI

MCI（Media Control Interface）是更古老的高层 multimedia command API。

现代新项目通常没有理由优先使用。

---

## 9. 为什么仓库仍然收录 Legacy API

因为开发中经常遇到：

- 老软件 hook
- compatibility
- reverse engineering
- driver behavior
- legacy .NET library
- old sample code

知道旧 API 最终如何映射到现代 audio stack，对排错很有帮助。

---

## 10. Wave / DirectSound 与 WDMAud

Microsoft driver docs 解释：

WinMM waveIn / waveOut 和 DirectSound 会通过系统组件向 WDM / KS audio driver 传递。

这也是为什么旧 API 和现代 driver stack 仍然相互关联。

---

## 11. 官方资料

- Windows Audio Architecture  
  https://learn.microsoft.com/windows-hardware/drivers/audio/windows-audio-architecture

- Waveform Audio  
  https://learn.microsoft.com/windows/win32/multimedia/waveform-audio

- Waveform Structures  
  https://learn.microsoft.com/windows/win32/multimedia/waveform-structures

- Wave and DirectSound Components  
  https://learn.microsoft.com/windows-hardware/drivers/audio/wave-and-directsound-components
