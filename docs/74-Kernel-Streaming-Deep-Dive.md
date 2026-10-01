# Kernel Streaming (KS) Deep Dive：Filter、Pin、Node、Property

> 状态：🟢 Public WDK

Kernel Streaming（KS）是理解 Windows audio driver topology 的基础之一。DeviceTopology、Jack、WaveRT、PortCls、driver property 和 legacy mixer translation 都与 KS model 紧密相关。

## Filter / Pin / Node

WDM audio adapter driver 将硬件暴露为 filter factory；factory 创建 KS filter instance。Filter 内部用 pin 表示数据入口/出口，用 node 表示 volume、mute、DAC、ADC、mixer、mux、audio engine 等处理/控制点，再用 connection 描述 signal path。

```text
source pin → node → node → sink pin
```

Pin 还声明支持的数据格式范围、通信方式、data flow、instance 数量和 category。

## Property 与 Event

KS 支持 filter property、pin property、node property。请求通常由 property-set GUID、property ID 和 target 共同确定。Jack state、control change 等也可以通过 KS event 暴露。

## Wave Filter 与 Topology Filter

Wave filter 主要负责 PCM streaming；topology filter 更偏硬件控制、jack、volume、mux 和物理连接。一个 audio adapter 往往同时暴露多类 filter。

## DeviceTopology 的来源

可粗略理解为：

```text
KS topology
  ↓
AudioEndpointBuilder / Core Audio
  ↓
IDeviceTopology / IConnector / IPart
```

所以用户态看到的 connector / subunit 与 driver topology 密切相关。

## Legacy Mixer Translation

历史 Windows 还会把 KS topology 翻译为 WinMM mixer lines / controls。这解释了为什么老 mixer API 与现代 endpoint/session API 不是一回事，却仍能映射到底层 WDM hardware control。

## KsStudio

Microsoft 的 `KsStudio.exe` 可以查看 filters、pin factories、nodes、properties、events，实例化 pin，构建 KS graph 并测试 streaming。它是分析 audio driver 实际暴露能力的重要工具。

## 什么时候需要深入 KS

普通播放器或音量工具通常不需要；但以下场景很有价值：

- virtual audio driver
- endpoint missing / wrong topology
- unsupported format
- jack detection
- hardware control
- Bluetooth sideband
- USB / HDMI driver analysis
- APO / offload debugging

## 官方资料

- Audio Filters, Pins, and Nodes  
  https://learn.microsoft.com/windows-hardware/drivers/audio/audio-filters--pins--and-nodes
- Filter, Pin, and Node Properties  
  https://learn.microsoft.com/windows-hardware/drivers/audio/filter--pin--and-node-properties
- KS Minidriver Architecture  
  https://learn.microsoft.com/windows-hardware/drivers/stream/ks-minidriver-architecture
- KsStudio  
  https://learn.microsoft.com/windows-hardware/drivers/audio/ksstudio-utility
