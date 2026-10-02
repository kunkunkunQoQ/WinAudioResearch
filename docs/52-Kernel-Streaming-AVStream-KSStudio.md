# Kernel Streaming / AVStream / KSStudio

> 状态：🟢 Public WDK / Driver Documentation

如果 Core Audio 是“应用开发者看到的 audio world”，那么 Kernel Streaming（KS）更接近：

> driver 暴露给 Windows multimedia stack 的底层 filter / pin / node world。

---

## 1. KS 基本模型

```text
Filter
  ├─ Pin
  ├─ Pin
  └─ Node
       ↓
Properties / Events / Methods
```

Audio driver 用 KS 描述：

- stream pins
- topology
- volume node
- mute
- mux
- jack
- format
- clock

---

## 2. AVStream

现代 multimedia driver framework：

```text
AVStream
```

建立在 KS model 上。

适用：

- audio
- video capture
- streaming devices

Microsoft PortCls 文档说明：

- 厂商可以自己写 AVStream KS filter
- 但典型 PCI/DMA audio driver 更常使用 PortCls / miniport 来减少重复工作

---

## 3. PortCls

系统组件：

```text
PortCls.sys
```

提供大量通用 audio KS filter 功能。

厂商主要实现：

- miniport
- hardware-specific logic

这比从零写 KS filter 简单。

---

## 4. WaveRT 与 KS

WaveRT miniport 仍建立在 Windows audio driver / KS 架构之上。

它主要优化：

- cyclic buffer
- low latency
- direct position / notification
- Audio Engine data path

---

## 5. KS Property

很多硬件属性以：

```text
KSPROPERTY
```

暴露。

例如：

- KSPROPERTY_JACK_DESCRIPTION
- format
- topology
- volume
- pin capability

User-mode DeviceTopology 其实是在帮应用更方便地访问部分 KS topology 信息。

---

## 6. KSStudio

WDK 自带：

```text
KsStudio.exe
```

它是非常重要但经常被应用开发者忽略的工具。

用途：

- enumerate filter factory
- instantiate filter / pin
- build graph
- topology visualization
- set/get properties
- enable events
- stream data
- basic tests

---

## 7. 为什么 KSStudio 特别适合音频调试

KSStudio 不通过：

- DirectSound
- MMSystem
- DirectShow

去访问 driver。

所以当：

```text
Windows Sound UI / WASAPI 出错
```

你可以直接检查 KS driver 暴露的：

- pin
- format
- node
- property

帮助判断：

> 问题在 driver 下面，还是上层 Audio Engine / endpoint policy。

---

## 8. Bridge Pin

Bridge pin 通常代表：

- jack
- internal connector
- endpoint connection

很多 jack property 都挂在 bridge pin 上。

---

## 9. Node

KS topology node 可表示：

- volume
- mute
- ADC
- DAC
- mux
- AEC
- audio engine
- processing unit

DeviceTopology 的 Subunit 概念与这些底层 topology node 有密切关系。

---

## 10. 何时应用开发者需要了解 KS

如果只是：

- app volume
- endpoint volume
- playback

通常不需要。

如果遇到：

- driver 不暴露格式
- jack detection 错误
- virtual endpoint
- hardware topology
- multi-channel
- driver / OEM property

就值得深入 KS。

---

## 11. 官方资料

- Introduction to Port Class  
  https://learn.microsoft.com/windows-hardware/drivers/audio/introduction-to-port-class

- KsStudio Utility  
  https://learn.microsoft.com/windows-hardware/drivers/audio/ksstudio-utility

- DeviceTopology Header  
  https://learn.microsoft.com/windows/win32/api/devicetopology/

- Audio Topology Nodes  
  https://learn.microsoft.com/windows-hardware/drivers/audio/audio-topology-nodes
