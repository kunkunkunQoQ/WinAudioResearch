# WaveRT Deep Dive：现代 Windows Audio Driver Streaming 基础

> 状态：🟢 Public WDK

WaveRT 是 Windows Vista 后 Windows audio driver 的核心 streaming model 之一。

它的目标：

> 让 Audio Engine 更高效地访问 audio hardware buffer，减少不必要的数据复制和 kernel transition。

---

## 1. PortCls + WaveRT Miniport

传统架构：

```text
PortCls
  +
WaveRT Miniport
  ↓
Audio Hardware
```

WaveRT miniport 负责 hardware-dependent 部分。

---

## 2. 两个核心 Interface

Microsoft 文档要求 WaveRT miniport 实现：

```text
IMiniportWaveRT
IMiniportWaveRTStream
```

### IMiniportWaveRT

负责：

- initialization
- channel enumeration
- stream creation

### IMiniportWaveRTStream

负责：

- stream buffer
- position
- notification
- runtime streaming

---

## 3. WaveRT-friendly Hardware

理想 hardware 有：

- scatter/gather DMA
- 能直接访问 physical memory 中的 cyclic buffer

这样 Audio Engine 可以更高效地和 hardware exchange data。

---

## 4. Cyclic Buffer

概念：

```text
[ audio ring buffer ]
        ↑
hardware DMA
        ↑
audio engine
```

关键问题：

- current hardware position
- write/read position
- notification period
- underrun/overrun

---

## 5. Position Register / Clock

低延迟 driver 必须准确报告：

- stream position
- QPC correlation
- packet timing

否则上层：

- IAudioClock
- latency measurement
- AV sync

都会受到影响。

---

## 6. Event / Notification

WaveRT 可以支持 notification event。

Audio Engine 不必一直 poll position。

这和 user-mode WASAPI event-driven stream 是不同层，但共同目标都是：

> 减少无意义 polling。

---

## 7. Hardware Offload

WaveRT driver 还可以暴露：

- host pin
- offload pin
- loopback pin
- audio engine node

让 DSP / hardware audio engine 处理某些 shared media stream。

---

## 8. USB Audio 2.0

Windows inbox：

```text
usbaudio2.sys
```

本身就是 WaveRT audio port class miniport。

这说明 WaveRT 并不只用于板载 HDA。

---

## 9. ACX 与 WaveRT

Microsoft 当前 ACX：

> 目前 streaming 只支持 WaveRT-based streaming。

所以：

```text
ACX
```

没有把 WaveRT 概念完全淘汰。

更像是：

> 给现代 multi-stack audio driver 提供新的 class extension model。

---

## 10. 对应用开发者的意义

普通 WASAPI app 不需要实现 WaveRT。

但理解 WaveRT 能帮助解释：

- 为什么某 endpoint period 更低
- why hardware offload exists
- why driver bugs cause glitches
- why position/timestamp can be wrong
- why USB / HDA / virtual devices behavior differs

---

## 11. 官方资料

- WaveRT Miniport Driver  
  https://learn.microsoft.com/windows-hardware/drivers/audio/wavert-miniport-driver

- Developing a WaveRT Miniport Driver  
  https://learn.microsoft.com/windows-hardware/drivers/audio/developing-a-wavert-miniport-driver

- Hardware-Offloaded Audio Processing  
  https://learn.microsoft.com/windows-hardware/drivers/audio/hardware-offloaded-audio-processing

- Windows Audio Architecture  
  https://learn.microsoft.com/windows-hardware/drivers/audio/windows-audio-architecture
