# Windows 音频驱动栈：WDM / PortCls / WaveRT / KS / ACX

> 状态：🟢 Public WDK / Driver Documentation  
> 这篇面向想从应用层继续往驱动层理解 Windows Audio 的开发者。

---

## 1. Windows Audio Stack 的驱动侧

高层可以简化为：

```text
Application APIs
   ↓
Windows Audio Service / Audio Engine
   ↓
Audio Endpoint Builder
   ↓
Audio Driver
   ↓
Hardware
```

驱动需要向系统暴露：

- render / capture path
- formats
- pins
- topology
- properties
- processing modes
- jack / endpoint information

---

## 2. WDM Audio

Windows 长期使用 WDM audio driver model。

传统 audio miniport 常结合：

```text
PortCls
+
miniport driver
```

PortCls 提供大量通用 audio class driver 支持。

---

## 3. WaveRT

WaveRT 是 Windows Vista 后的重要 audio miniport model。

目标：

- 低延迟
- 高性能
- 让 audio engine 更直接访问 cyclic audio buffer
- 减少传统 kernel streaming copy / transition 成本

现代 Windows 音频驱动大量围绕 WaveRT。

---

## 4. Kernel Streaming (KS)

KS 是更底层的 streaming / filter model。

关键概念：

- filter
- pin
- node
- property
- event
- topology

音频驱动可以通过 KS topology 描述：

```text
input pin
  ↓
volume node
  ↓
mux
  ↓
DAC
  ↓
output pin
```

用户态 DeviceTopology 能看到的部分信息与这里密切相关。

---

## 5. Audio Topology Nodes

驱动可暴露标准 node type。

例如：

- volume
- mute
- DAC
- ADC
- mux
- audio engine
- connector

每个 node 通过 ID / property 被访问。

---

## 6. AudioEndpointBuilder

Audio Endpoint Builder service 会监控底层 audio device interface。

当新音频设备出现时，它会：

- 分析 driver topology
- 创建 software audio endpoint
- 设置 form factor
- 计算默认 endpoint ranking
- 暴露给 MMDevice / Windows UI

因此：

> IMMDevice 并不是简单地“一比一对应一个 PnP device”。

它是 Windows 根据 audio topology 建出来的 endpoint abstraction。

---

## 7. ACX

ACX（Audio Class Extensions）是 Microsoft 新一代 audio driver framework。

官方说明：

- legacy PortCls / KS 与 ACX 可以并存
- 不强制已有驱动迁移
- 当前 ACX 主要支持 WaveRT-based streaming
- 新驱动可选择使用 ACX 简化结构

ACX 关键概念：

- Circuit
- Stream
- Element
- Pin
- Target
- Request

---

## 8. SysVAD

Microsoft SysVAD 是最重要的 Windows Audio driver sample 之一。

它展示：

- virtual audio device
- multiple endpoints
- WaveRT
- audio offload
- APO
- Bluetooth / USB sideband related patterns
- topology
- formats

项目：

https://github.com/microsoft/Windows-driver-samples/tree/main/audio/sysvad

---

## 9. Simple Audio Sample

如果 SysVAD 太大，可以先看：

https://github.com/microsoft/Windows-driver-samples/tree/main/audio/simpleaudiosample

它展示一个更简单的 speaker + microphone driver。

---

## 10. ACX Samples

Microsoft Driver Samples：

https://github.com/microsoft/Windows-driver-samples/tree/main/audio/Acx

适合学习：

- ACX circuit
- audio codec
- stream
- data format
- endpoint composition

---

## 11. Virtual Audio Device

如果目标是做：

- virtual speaker
- virtual microphone
- system-wide DSP endpoint

那么“普通 C# 软件”无法凭空创建一个真正的 Windows audio endpoint。

通常需要：

- audio driver
- virtual audio device
- 或已有 virtual device infrastructure

SysVAD 是官方研究入口。

---

## 12. 官方资料

- Audio Devices Design Guide  
  https://learn.microsoft.com/windows-hardware/drivers/audio/

- Windows Audio Architecture  
  https://learn.microsoft.com/windows-hardware/drivers/audio/windows-audio-architecture

- Audio DDI  
  https://learn.microsoft.com/windows-hardware/drivers/ddi/_audio/

- ACX Overview  
  https://learn.microsoft.com/windows-hardware/drivers/audio/acx-audio-class-extensions-overview

- Audio Topology Nodes  
  https://learn.microsoft.com/windows-hardware/drivers/audio/audio-topology-nodes

- SysVAD  
  https://github.com/microsoft/Windows-driver-samples/tree/main/audio/sysvad
