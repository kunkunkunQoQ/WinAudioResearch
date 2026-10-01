# DeviceTopology API：从 Endpoint 往硬件内部拓扑走

> 状态：🟢 Public API

DeviceTopology 是 Core Audio 中更偏硬件拓扑的一层。

它不是用来“列出所有扬声器”的；它更适合探索一个 endpoint 背后的 adapter data path、connector、part 和硬件控制节点。

---

## 1. 入口

```text
IMMDevice
   ↓ Activate(IID_IDeviceTopology)
IDeviceTopology
```

官方接口：

https://learn.microsoft.com/windows/win32/api/devicetopology/nn-devicetopology-idevicetopology

---

## 2. 核心对象

### IDeviceTopology

代表设备拓扑。

### IConnector

连接拓扑中的不同设备 / part。

### IPart

拓扑中的一个 part。

### IPartsList

part 集合。

### IControlInterface

暴露 part 上的控制接口。

### IAudioVolumeLevel / IAudioMute / IAudioAutoGainControl / IAudioBass / IAudioTreble

用于访问某些硬件 / topology control。

---

## 3. 为什么会有 DeviceTopology

假设一个声卡内部是：

```text
Audio Engine
   ↓
DAC
   ↓
Hardware Volume
   ↓
Jack
   ↓
Headphones
```

MMDevice 主要看到用户可操作的 endpoint。

DeviceTopology 则允许程序沿数据路径向 adapter 内部探索。

---

## 4. Endpoint topology 很简单

Microsoft 文档强调：

- endpoint device 自身 topology 很简单
- 真正复杂的 topology 通常位于与 endpoint 连接的 adapter device

因此研究时通常需要通过 connector 跨设备继续遍历。

---

## 5. DataFlow 容易和 EDataFlow 混淆

DeviceTopology 有自己的：

```text
DataFlow.In
DataFlow.Out
```

它描述 connector 中 signal 的方向。

这和：

```text
EDataFlow.eRender
EDataFlow.eCapture
```

不是同一个 enum，也不是完全相同的语义层。

---

## 6. 什么时候应该用

适合：

- 查硬件 volume / mute node
- 查 connector
- 查 audio jack path
- 研究 adapter topology
- 驱动 / endpoint debugging
- 研究硬件控制点

不适合：

- 普通每应用音量控制
- 普通设备列表 UI
- per-app routing

---

## 7. 为什么普通应用很少直接用

EndpointVolume 已经帮应用抽象了很多“寻找 volume control”的过程。

Microsoft 文档指出：

- 如果设备有硬件 volume，EndpointVolume 会利用它
- 如果没有，系统可提供软件 volume

因此仅为了“改主音量”，通常没必要自己遍历 DeviceTopology。

---

## 8. 驱动侧关系

用户态 DeviceTopology 背后和驱动暴露的 KS topology 密切相关。

驱动层常见：

- pin
- node
- connection
- KSNODETYPE
- KS property

所以研究 DeviceTopology 时，最好同时阅读：

- Audio Topology Nodes
- Kernel Streaming / WDM Audio
- SysVAD

---

## 9. 官方资料

- IDeviceTopology  
  https://learn.microsoft.com/windows/win32/api/devicetopology/nn-devicetopology-idevicetopology
- Device Topologies  
  https://learn.microsoft.com/windows/win32/coreaudio/device-topologies
- devicetopology.h  
  https://learn.microsoft.com/windows/win32/api/devicetopology/
- Audio Topology Nodes  
  https://learn.microsoft.com/windows-hardware/drivers/audio/audio-topology-nodes
