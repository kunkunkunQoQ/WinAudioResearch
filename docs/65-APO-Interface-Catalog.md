# APO / Windows Audio Effects 接口目录

> 状态：🟢 Public SDK / WDK API

这页专门整理 Audio Processing Object (APO) 相关接口。

---

## audioenginebaseapo.h

官方 Header：
https://learn.microsoft.com/windows/win32/api/audioenginebaseapo/

### Core APO

| 接口 | 用途 |
|---|---|
| `IAudioProcessingObject` | APO 非 realtime 配置 / 初始化 / format negotiation |
| `IAudioProcessingObjectConfiguration` | lock / unlock APO processing |
| `IAudioProcessingObjectRT` | realtime audio processing |
| `IAudioSystemEffects` | system effects APO base |
| `IAudioSystemEffects2` | processing mode aware system effects |
| `IAudioSystemEffectsCustomFormats` | APO custom formats |

### AEC / Auxiliary Input

| 接口 | 用途 |
|---|---|
| `IApoAcousticEchoCancellation` | APO 声明 AEC 能力 |
| `IApoAcousticEchoCancellation2` | 请求 reference stream properties |
| `IApoAuxiliaryInputConfiguration` | 配置辅助输入 |
| `IApoAuxiliaryInputRT` | realtime auxiliary stream input |

### Device Modules

`IAudioDeviceModulesClient`

让 APO 获取 audio device modules manager。

### Structures

- `APO_REG_PROPERTIES`
- `APOInitBaseStruct`
- `APOInitSystemEffects`
- `APOInitSystemEffects2`

### Enumerations

- `APO_FLAG`
- `APO_REFERENCE_STREAM_PROPERTIES`

---

## audioengineextensionapo.h

官方 Header：
https://learn.microsoft.com/windows/win32/api/audioengineextensionapo/

Windows 11 对 APO 增加更多 framework。

### Interfaces

| 接口 | 用途 |
|---|---|
| `IAudioSystemEffects3` | controllable effects + Windows 11 framework opt-in |
| `IAudioProcessingObjectLoggingService` | APO logging |
| `IAudioProcessingObjectRTQueueService` | OS-managed realtime work queue |
| `IAudioProcessingObjectNotifications` | endpoint / effect notification |
| `IAudioProcessingObjectNotifications2` | notification support discovery |
| `IAudioProcessingObjectPreferredFormatSupport` | APO preferred format |

### APOInitSystemEffects3

包含：

- endpoint property store
- service provider
- IMMDeviceCollection
- software I/O connector
- AudioProcessingMode
- discovery-only flag

Windows Build 22000+ 才会给支持 IAudioSystemEffects3 的 APO 传这个结构。

---

## System Effect Discovery / Control

`IAudioSystemEffects3`：

- `GetControllableSystemEffectsList`
- `SetAudioSystemEffectState`

effect 由：

```text
AUDIO_SYSTEMEFFECT
```

描述：

- effect GUID
- canSetState
- state

---

## Application-side Effects API

普通应用也可以通过：

```text
IAudioEffectsManager
```

查询当前 stream 相关 effect。

接口位于：

```text
audioclient.h
```

它和“自己实现 APO”不是一回事。

### Application

```text
IAudioEffectsManager
→ query / control available effects
```

### Driver / APO Vendor

```text
IAudioSystemEffects3
IAudioProcessingObjectRT
...
→ implement processing
```

---

## APO 的实时边界

`IAudioProcessingObjectRT` 方法运行在 realtime audio thread。

不要：

- blocking
- heap allocation
- file I/O
- long locks
- UI call
- arbitrary COM activation

Realtime processing 要和 control/configuration path 分开。

---

## 与 XAPO 的关系

XAudio2 也有：

```text
XAPO
```

概念相似但 deployment / hosting 场景不同。

不要把：

- XAudio2 effect chain 中 XAPO
- Windows system endpoint APO

当成同一种安装 / policy 机制。

---

## 相关阅读

- [APO 总览](23-Audio-Processing-Objects-APO.md)
- [Voice / AEC / NS](49-Voice-AEC-Noise-Suppression.md)
- [Processing Modes](34-Audio-Effects-and-Processing-Modes.md)
