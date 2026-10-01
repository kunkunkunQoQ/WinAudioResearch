# XAudio2：游戏与实时播放的 Voice Graph API

> 状态：🟢 Public API

XAudio2 是 Microsoft 面向高性能游戏与实时音频播放的重要 API。

它和 WASAPI 的主要差异：

```text
WASAPI
  → endpoint / buffer / stream 级别

XAudio2
  → source voice / submix / mastering voice 组成的音频图
```

---

## 1. Voice Graph

典型：

```text
Source Voice A ─┐
Source Voice B ─┼─→ Submix Voice ─→ Mastering Voice ─→ Device
Source Voice C ─┘
```

### Source Voice

提交音频 sample / buffer。

### Submix Voice

把多个 voice 合并，适合：

- effects bus
- music bus
- SFX bus
- UI sounds bus

### Mastering Voice

代表最终输出路径。

---

## 2. 为什么游戏常用 XAudio2

适合：

- 大量短音效
- 多 voice 同时播放
- pitch / frequency ratio
- volume matrix
- routing
- effects chain
- 3D audio
- voice callbacks

它避免游戏自己直接手写每个 WASAPI endpoint buffer loop。

---

## 3. IXAudio2

核心 engine interface：

```text
IXAudio2
```

负责：

- engine state
- processing thread
- voice graph
- engine callbacks

---

## 4. Source Voice

`IXAudio2SourceVoice`：

常用：

- SubmitSourceBuffer
- Start
- Stop
- FlushSourceBuffers
- SetFrequencyRatio
- SetVolume
- SetOutputMatrix

---

## 5. Effects

XAudio2 支持：

- voice effect chain
- XAPO
- built-in reverb / EQ / echo / limiter 等
- custom XAPO

注意：

> XAPO 是 XAudio2 effect chain 的 APO model，不应和系统音频驱动中的 system APO placement 简单等同。

---

## 6. X3DAudio

XAudio2 常与：

```text
X3DAudio
```

搭配做传统 game 3D audio。

它根据：

- listener
- emitter
- orientation
- distance
- channel layout

计算 output matrix / DSP parameters。

---

## 7. HRTF

Windows XAudio2 API 还包含 HRTF APO 接口。

适用于：

- binaural processing
- headphones 3D positioning

但现代 Windows 也有 Spatial Audio / Windows Sonic，需要按场景比较。

---

## 8. AudioGraph vs XAudio2

### 选 XAudio2

如果：

- game engine
- C++
- many voices
- game DSP
- submix graph
- low overhead playback

### 选 AudioGraph

如果：

- C# / WinRT
- device capture + routing
- file node
- custom frame processing
- graph 逻辑比游戏 voice engine 更重要

---

## 9. XAudio2 vs WASAPI

如果你需要：

- exclusive endpoint stream
- process loopback
- precise endpoint buffer control

WASAPI 更直接。

如果你只是需要：

- 播放很多声音
- 混音
- effects
- routing

XAudio2 更适合。

---

## 10. 官方资料

- XAudio2 Introduction  
  https://learn.microsoft.com/windows/win32/xaudio2/xaudio2-introduction

- XAudio2 API Reference  
  https://learn.microsoft.com/windows/win32/api/_xaudio2/

- XAudio2 Voices  
  https://learn.microsoft.com/windows/win32/xaudio2/xaudio2-voices

- XAudio2 Audio Graph  
  https://learn.microsoft.com/windows/win32/xaudio2/xaudio2-audio-graph
