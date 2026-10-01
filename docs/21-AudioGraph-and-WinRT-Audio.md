# AudioGraph / Windows.Media.Audio

> 状态：🟢 Public API

AudioGraph 是 Windows Runtime 提供的高层音频图 API。

它和 WASAPI 的关系可以粗略理解为：

```text
AudioGraph
  = higher-level graph / nodes / routing / processing model

WASAPI
  = lower-level endpoint stream / buffer model
```

---

## 1. AudioGraph 能做什么

Microsoft 官方文档把它用于：

- device input
- device output
- file input
- file output
- custom frame input
- custom frame output
- submix
- routing
- effects
- spatial audio
- capture
- low-latency scenarios

---

## 2. 基本结构

```text
AudioGraph
  ├─ AudioDeviceInputNode
  ├─ AudioFileInputNode
  ├─ AudioFrameInputNode
  ├─ AudioSubmixNode
  ├─ AudioDeviceOutputNode
  ├─ AudioFileOutputNode
  └─ AudioFrameOutputNode
```

节点之间通过 connection 形成数据流。

---

## 3. 最简单的文件播放

概念：

```text
AudioFileInputNode
      ↓
AudioDeviceOutputNode
```

Graph Start 后，音频沿连接流动。

---

## 4. 麦克风处理

```text
AudioDeviceInputNode
      ↓
AudioSubmixNode
      ↓
effect / processing
      ↓
AudioDeviceOutputNode / FileOutput
```

对于 C# 应用，这通常比直接手写 WASAPI buffer loop 更容易维护。

---

## 5. Low Latency

AudioGraph 提供：

```text
AudioGraphSettings.QuantumSizeSelectionMode
```

模式包括：

- SystemDefault
- LowestLatency
- ClosestToDesired

Microsoft Low Latency Audio 文档把 AudioGraph 作为 Windows 10+ 低延迟应用方案之一。

---

## 6. 与 XAudio2 怎么选

Microsoft AudioGraph 指南直接讨论“AudioGraph vs XAudio2”。

粗略：

### AudioGraph

更适合：

- C# / WinRT
- capture + routing
- file / device / custom frame graph
- UWP / modern Windows app
- 快速构建音频处理图

### XAudio2

更适合：

- 游戏
- 大量 source voices
- 自定义 voice graph
- game audio effects / 3D
- 更传统 C++ 实时音频引擎

---

## 7. 与 WASAPI 怎么选

如果你需要：

- 最低层 buffer control
- exclusive mode
- endpoint stream timing
- process loopback
- 自己管理 render / capture

优先 WASAPI。

如果你需要：

- 快速把 device/file/custom processing 连成图
- C# 友好
- 不想手写 buffer pump

优先考虑 AudioGraph。

---

## 8. 官方资料

- Audio graphs  
  https://learn.microsoft.com/windows/apps/develop/media-authoring-processing/audio-graphs
- AudioGraph class  
  https://learn.microsoft.com/uwp/api/windows.media.audio.audiograph
- AudioDeviceInputNode  
  https://learn.microsoft.com/uwp/api/windows.media.audio.audiodeviceinputnode
- AudioDeviceOutputNode  
  https://learn.microsoft.com/uwp/api/windows.media.audio.audiodeviceoutputnode
- Microsoft AudioGraph sample  
  https://github.com/microsoft/Windows-universal-samples/tree/main/Samples/AudioCreation
