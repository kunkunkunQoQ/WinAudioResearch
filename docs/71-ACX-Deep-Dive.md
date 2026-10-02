# ACX Deep Dive：Audio Class Extensions

> 状态：🟢 Public WDK

ACX 是 Microsoft 面向现代 audio driver 的 class extension framework。

重要结论：

> ACX 不是要求所有旧 PortCls driver 立即迁移。

Microsoft 明确保持 legacy WDM audio driver binary compatibility。

---

## 1. ACX 与 Legacy 共存

```text
Legacy:
PortCls / KS / WaveRT

Modern:
ACX / KMDF / WaveRT
```

两套 stack 可以 side-by-side。

---

## 2. 当前 Streaming Foundation

Microsoft 当前文档：

> ACX 目前只支持 WaveRT-based streaming。

所以理解 ACX 前仍应理解 WaveRT。

---

## 3. Circuit

```text
ACXCIRCUIT
```

表示：

> 一段完整或部分 audio path。

Circuit 可以代表：

- codec
- DSP
- amp
- stream-side component

---

## 4. Endpoint Audio Path

一个用户看到的 speaker endpoint 可能由多个 circuit 组成：

```text
Stream Circuit
      ↓
DSP Circuit
      ↓
Codec Circuit
      ↓
Amp Circuit
```

甚至这些 circuit 可以来自：

- 不同 device stack
- 不同 vendor driver

这正是 ACX 针对 modern SoC audio architecture 的重要设计。

---

## 5. Core Circuit

在 multi-stack architecture：

```text
Core Circuit
```

负责给 endpoint identity。

---

## 6. Stream Circuit

直接与：

> 上层 user-mode streaming service

交互的 circuit。

---

## 7. ACXPIN

每个 ACXCIRCUIT 至少需要：

- input pin
- output pin

streaming circuit 创建实际 render/capture pins。

ACX framework 再负责 circuit 之间连接所需的另一端。

---

## 8. ACXSTREAM

代表 runtime audio stream。

由 Circuit 创建。

Stream 会基于 parent circuit elements 创建对应 elements。

---

## 9. ACXELEMENT

表示硬件 / DSP capability。

例如：

- Volume
- Mute
- Jack
- Module
- Peak Meter
- Keyword Spotter
- Stream Audio Engine

---



---

## 10. Audio Engine / Audio Module

ACX 把现代 DSP / offload 场景中的 audio engine 也建模为 element：

```text
ACXAUDIOENGINE
  ├─ host pin
  ├─ offload pin
  ├─ loopback pin
  ├─ device format list
  └─ effects / engine-format callbacks

ACXSTREAMAUDIOENGINE
  └─ per-offload-stream state / position / loopback protection
```

Audio Module 使用：

```text
ACXAUDIOMODULE
  └─ EvtAcxAudioModuleProcessCommand
```

用于把模块化 DSP / hardware processing block 暴露到 ACX 模型中。

---

## 11. 常用控制 Element

当前结构库已经索引：

- `ACXVOLUME`
- `ACXMUTE`
- `ACXPEAKMETER`
- `ACXKEYWORDSPOTTER`
- `ACXJACK`
- microphone-array geometry

它们不是简单的常量名，每类都有自己的：

```text
CONFIG
CALLBACKS
Create()
state / level notification
```

例如 Volume driver callback 包含 assign/retrieve level；Mute 包含 assign/retrieve state；PeakMeter 提供 level retrieval；KeywordSpotter 包含 arm / patterns / reset。

---

## 12. Jack 与 Microphone Array

`acxpin.h` 还定义：

- jack description / sink information
- jack presence callback
- microphone coordinates
- microphone-array geometry
- physical microphone configuration

因此 ACX endpoint topology 并不只描述 streaming pin，还能把物理连接与 microphone geometry 作为公开 WDK contract 暴露。

---

## 13. ACX Targets

multi-driver architecture 中，一个 driver 需要和另一个 circuit / driver 通信时，可以使用：

- ACX target abstractions
- circuit communication

这减少 vendor 自己发明 private cross-stack communication。

---

## 14. Power

ACX 建在：

```text
KMDF / WDF
```

power / PnP 需要遵循现代 WDF lifecycle。

---

## 15. Driver Verifier

Microsoft 官方 ACX docs 明确建议：

> 对所有 Windows driver，包括 ACX，使用 Driver Verifier。

用于提前发现：

- latent errors
- power bugs
- reliability issue

---

## 16. Sample

Microsoft：

https://github.com/microsoft/Windows-driver-samples/tree/main/audio/Acx/Samples

包括：

- circuit
- codec
- data formats
- elements
- stream

参考实现。

---

## 17. 什么时候选 ACX

新 driver：

- modern SoC
- multi-component stack
- future Windows audio development

应认真评估 ACX。

已有稳定 PortCls driver：

> 不必为了“新”而无条件重写。

---

## 18. 官方资料

- ACX Overview  
  https://learn.microsoft.com/windows-hardware/drivers/audio/acx-audio-class-extensions-overview

- ACX Circuits  
  https://learn.microsoft.com/windows-hardware/drivers/audio/acx-circuits

- ACX Streaming  
  https://learn.microsoft.com/windows-hardware/drivers/audio/acx-streaming

- ACX Samples  
  https://github.com/microsoft/Windows-driver-samples/tree/main/audio/Acx/Samples
