# Windows Spatial Audio / Windows Sonic

> 状态：🟢 Public API

Windows Spatial Audio 是 Microsoft 的空间音频平台。

它不是简单的“7.1 输出”。

核心思想是让应用提交：

- static spatial objects
- dynamic spatial objects

由系统空间音频引擎进行最终渲染。

---

## 1. 核心接口

```text
ISpatialAudioClient
       ↓
ActivateSpatialAudioStream
       ↓
ISpatialAudioObjectRenderStream
       ↓
ActivateSpatialAudioObject
       ↓
ISpatialAudioObject
```

---

## 2. Static Objects

Static object 对应固定 speaker / spatial channel 位置。

例如：

- front left
- front right
- center
- top
- etc.

由 `AudioObjectType` 描述。

---

## 3. Dynamic Objects

Dynamic object 可以：

- 设置任意 3D position
- 随时间移动
- 设置 volume

典型接口：

```text
ISpatialAudioObject::SetPosition
ISpatialAudioObject::SetVolume
```

---

## 4. 动态对象数量不是无限的

客户端需要查询可用 dynamic object 数量。

系统可能因为：

- endpoint
- spatial renderer
- 当前资源

限制可同时激活的对象数。

客户端必须能处理可用数量变化。

---

## 5. Stream 激活

`SpatialAudioObjectRenderStreamActivationParams` 包含：

- ObjectFormat
- StaticObjectTypeMask
- MinDynamicObjectCount
- MaxDynamicObjectCount
- AUDIO_STREAM_CATEGORY
- EventHandle
- NotifyObject

这说明 Spatial Audio 本质上仍然是 event-driven 实时音频流，只是数据模型从固定 channel buffer 提升到 audio objects。

---

## 6. 最低系统

主要 `ISpatialAudioObjectRenderStream` / object API 从 Windows 10 version 1703 开始用于 desktop apps。

---

## 7. 与普通多声道 PCM 的区别

普通：

```text
PCM channels
→ 5.1 / 7.1 speaker layout
```

Spatial Object：

```text
object + position
→ Windows spatial renderer
→ actual endpoint / headphones / speakers
```

后者让应用不必自己把每个声源永久“烤”进固定 speaker channel。

---

## 8. AudioGraph 也可以接入 spatial 场景

AudioGraph 的 device input / graph model 也有 spatial-enabled 能力。

因此 Windows 有两种常见层次：

- Win32 Spatial Audio COM API
- WinRT AudioGraph spatial model

---

## 9. 官方资料

- Spatial Sound  
  https://learn.microsoft.com/windows/win32/coreaudio/spatial-sound
- Render Spatial Sound Using Spatial Audio Objects  
  https://learn.microsoft.com/windows/win32/coreaudio/render-spatial-sound-using-spatial-audio-objects
- ISpatialAudioClient  
  https://learn.microsoft.com/windows/win32/api/spatialaudioclient/nn-spatialaudioclient-ispatialaudioclient
- ISpatialAudioObject  
  https://learn.microsoft.com/windows/win32/api/spatialaudioclient/nn-spatialaudioclient-ispatialaudioobject
- ISpatialAudioObjectRenderStream  
  https://learn.microsoft.com/windows/win32/api/spatialaudioclient/nn-spatialaudioclient-ispatialaudioobjectrenderstream
