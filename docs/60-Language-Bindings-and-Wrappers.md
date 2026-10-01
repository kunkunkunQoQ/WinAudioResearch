# Windows Audio：语言绑定、Wrapper 与跨平台框架

> 状态：🟢 Public API bindings + 第三方工程生态

Windows Audio 本身主要以：

- Win32 C/C++
- COM
- WinRT
- WDK / driver headers

定义。

不同语言通常通过绑定或 wrapper 访问底层 API。**Wrapper 改善开发体验，但不会改变底层 Windows API 的语义、兼容性或 undocumented 风险。**

---

## 1. C / C++

最直接的 Windows Audio 开发方式。

### Windows SDK

常用 headers：

```text
mmdeviceapi.h
audioclient.h
audiopolicy.h
endpointvolume.h
devicetopology.h
spatialaudioclient.h
audiostatemonitorapi.h
audioclientactivationparams.h
```

优点：

- ABI 与 SDK 一致
- Microsoft samples 基本都可直接参考
- 最适合研究新 API

缺点：

- COM 生命周期
- HRESULT
- PROPVARIANT
- WAVEFORMAT
- threading

都需要自己管理。

---

## 2. .NET / C#

### NAudio

https://github.com/naudio/NAudio

覆盖：

- WASAPI
- MMDevice
- Media Foundation
- WinMM
- MIDI
- ASIO wrapper
- DSP / sample provider

适合：

- 快速做播放器 / recorder
- C# 音频工具
- 学习成熟 wrapper 的设计

但如果研究：

- undocumented AudioPolicyConfig
- 新 Win11 interface
- 精确 COM ABI

仍建议直接核对 SDK / 自己声明 interop。

### CSCore

https://github.com/filoe/cscore

覆盖：

- WASAPI
- DirectSound
- XAudio2
- Media Foundation
- WinMM
- DSP

可作为另一套 .NET Windows audio abstraction 参考。

### SonicRoute / WinAudioRoute

https://github.com/kunkunkunQoQ/SonicRoute  
https://github.com/kunkunkunQoQ/WinAudioRoute

更适合研究：

- C# Core Audio COM
- session
- endpoint
- per-app routing
- internal policy
- Windows product integration

---

## 3. Python

### pycaw

https://github.com/AndreMiras/pycaw

项目定位：

> Python Core Audio Windows

适合：

- endpoint volume
- audio sessions
- process volume
- Core Audio automation

底层仍然是 Windows Core Audio COM。

### python-sounddevice

https://github.com/spatialaudio/python-sounddevice

它基于：

```text
PortAudio
```

Windows 最终可走 WASAPI 等 host API。

适合：

- PCM playback / capture
- NumPy audio processing
- cross-platform code

不适合直接解决：

- Windows per-app session policy
- system default endpoint policy
- undocumented routing

---

## 4. Rust

### windows-rs

Microsoft 官方：

https://github.com/microsoft/windows-rs

Crate：

```text
windows
```

Windows Audio 相关模块可直接映射 Windows metadata，例如：

```text
windows::Win32::Media::Audio
```

适合：

- 直接调用 Core Audio
- COM
- WinRT
- 新 Windows API

它比人工复制 C# COM interface 更接近 SDK metadata 驱动的绑定方式。

### CPAL

https://github.com/RustAudio/cpal

Windows 默认 backend：

```text
WASAPI
```

还可支持：

- ASIO
- JACK

适合：

- cross-platform realtime PCM
- callback stream

如果需要 Windows-specific session / endpoint policy，仍要进入 Windows API。

---

## 5. Go

### malgo

https://github.com/gen2brain/malgo

Go binding for miniaudio。

Windows backend 可包括：

- WASAPI
- DirectSound
- WinMM

适合：

- cross-platform playback/capture
- Go audio apps

### 直接 syscall / COM

也可以自己做 Win32 / COM binding，但维护：

- GUID
- vtable
- HRESULT
- struct layout

成本明显更高。

---

## 6. JUCE

https://github.com/juce-framework/JUCE

C++ framework。

Windows 侧可覆盖：

- WASAPI
- ASIO
- MIDI
- audio device abstraction
- VST host/plugin
- DSP

非常适合：

- DAW
- plugin
- professional audio
- cross-platform app

---

## 7. PortAudio

https://github.com/PortAudio/portaudio

Windows host APIs：

- WASAPI
- DirectSound
- WMME
- WDM-KS

优点：

> 一个 API 横跨 Windows/macOS/Linux。

代价：

> Windows-specific advanced policy 不会全部暴露。

---

## 8. miniaudio

https://github.com/mackron/miniaudio

Windows backend：

- WASAPI
- DirectSound
- WinMM

特点：

- lightweight
- single-file oriented
- playback/capture
- decoder
- node graph

---

## 9. SDL Audio

https://github.com/libsdl-org/SDL

适合：

- 游戏
- cross-platform app
- simple device playback/capture

Windows backend 可使用现代 Windows audio API，但不会替代：

- Audio Session API
- EndpointVolume
- PolicyConfig

---

## 10. OpenAL Soft

https://github.com/kcat/openal-soft

Windows backend 有 WASAPI。

重点：

- 3D audio
- HRTF
- source/listener model
- backend abstraction

适合研究：

> 高层 3D audio engine 如何落到 WASAPI endpoint。

---

## 11. 选择建议

| 目标 | 优先入口 |
|---|---|
| C++ Windows 原生研究 | Windows SDK |
| C# Windows audio | NAudio / direct COM |
| Python Core Audio control | pycaw |
| Python PCM | sounddevice / PortAudio |
| Rust direct Win32 | windows-rs |
| Rust cross-platform PCM | CPAL |
| Go cross-platform PCM | malgo |
| Pro audio / plugins | JUCE |
| C cross-platform | PortAudio / miniaudio |
| 3D audio | OpenAL Soft / XAudio2 / Spatial Audio |

---

## 12. Wrapper 使用原则

### Public API

可以：

```text
wrapper docs
+
Microsoft API docs
```

一起看。

### Undocumented API

必须回到底层确认：

- actual IID
- ABI
- Windows Build
- HRESULT
- source commit

不要因为 wrapper 提供：

```text
SetApplicationDevice()
```

就把它当成 Microsoft 稳定公开 API。
