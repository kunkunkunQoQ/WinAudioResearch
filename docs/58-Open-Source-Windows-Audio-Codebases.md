# 值得阅读的开源 Windows Audio Codebase

> 状态：第三方工程参考  
> 这页不是“推荐你一定使用哪个库”，而是告诉你：**某个技术问题去哪看真实实现。**

## 1. NAudio

https://github.com/naudio/NAudio

语言：

- C#

重点：

- WASAPI
- MMDevice
- WinMM
- ASIO wrapper
- Media Foundation
- MIDI
- codecs
- sample providers
- resampling

适合 .NET developer。

## 2. EarTrumpet

https://github.com/File-New-Project/EarTrumpet

重点：

- Core Audio
- session model
- device model
- per-app volume
- Windows audio policy
- undocumented per-app routing

适合研究 Windows mixer。

## 3. SonicRoute

https://github.com/kunkunkunQoQ/SonicRoute

重点：

- C# COM interop
- per-app output/input routing
- endpoint switch
- audio meter
- session enumeration
- product-level caching / lifecycle

本仓库的重要实测来源。

## 4. WinAudioRoute

https://github.com/kunkunkunQoQ/WinAudioRoute

重点：

- reusable .NET Windows audio control API
- device/session/routing abstraction

## 5. CSCore

https://github.com/filoe/cscore

语言：

- C#

重点：

- WASAPI
- DirectSound
- XAudio2
- Media Foundation
- WinMM
- DSP
- codecs

适合比较另一套 .NET audio abstraction。

## 6. SoundSwitch

https://github.com/Belphemur/SoundSwitch

重点：

- Windows output/input device switching
- hotkey / system integration
- endpoint management

适合研究：

> 成熟 Windows 音频切换产品怎么组织 UX + audio backend。

## 7. JUCE

https://github.com/juce-framework/JUCE

语言：

- C++

专业音频生态重要 framework。

Windows 侧可研究：

- WASAPI
- ASIO
- MIDI
- audio device abstraction
- plugin hosting
- VST
- realtime callback

适合：

- DAW
- plugin
- cross-platform pro audio

## 8. PortAudio

https://github.com/PortAudio/portaudio

语言：

- C

Windows backend：

- WASAPI
- DirectSound
- WMME
- WDM-KS

适合比较：

> 同一个 cross-platform stream abstraction 如何映射多代 Windows API。

## 9. miniaudio

https://github.com/mackron/miniaudio

语言：

- C

特点：

- single-file oriented
- playback/capture
- decoder
- graph
- cross-platform

Windows backend 可用于学习：

- WASAPI integration
- fallback architecture

## 10. ManagedBass

https://github.com/ManagedBass/ManagedBass

.NET wrapper around BASS ecosystem。

适合：

- playback
- DSP
- streaming
- plugin wrapper architecture

注意 BASS 本体 license / distribution 与 wrapper license 要分别确认。

## 11. OpenAL Soft

项目常见官方仓库：

https://github.com/kcat/openal-soft

适合：

- 3D positional audio
- HRTF
- backend abstraction
- WASAPI output

## 12. SDL Audio

https://github.com/libsdl-org/SDL

适合研究：

- game cross-platform audio backend
- WASAPI backend
- device hotplug abstraction

## 13. FFmpeg

https://github.com/FFmpeg/FFmpeg

适合：

- codec
- demux/mux
- resample
- filter graph

它不是 Windows Core Audio library。

## 14. Microsoft Samples

### Windows Classic Samples

https://github.com/microsoft/Windows-classic-samples

### Universal Samples

https://github.com/microsoft/Windows-universal-samples

### Driver Samples

https://github.com/microsoft/Windows-driver-samples

### Windows MIDI Services

https://github.com/microsoft/MIDI

公开 Windows API 行为研究应优先这些官方代码。

## 15. 阅读第三方代码时要做什么

不要直接：

> copy interface declaration

而应该记录：

- source repo
- commit
- Windows Build
- interface IID
- API status
- error handling
- architecture assumptions
- license

尤其是 undocumented interface。
