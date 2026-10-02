# Core Audio / WASAPI 接口目录

> 状态：🟢 Public API  
> 目标：按 Header 把常用 Windows Audio 接口集中列出，方便按接口名检索。

---

## mmdeviceapi.h

官方 Header：
https://learn.microsoft.com/windows/win32/api/mmdeviceapi/

### Interfaces

| 接口 | 用途 |
|---|---|
| `IMMDeviceEnumerator` | 枚举 endpoint、读取默认设备、注册设备通知 |
| `IMMDeviceCollection` | endpoint 集合 |
| `IMMDevice` | 单个 multimedia/audio endpoint |
| `IMMEndpoint` | 获取 endpoint 的 data-flow direction |
| `IMMNotificationClient` | 设备新增、删除、状态、属性、默认设备变化通知 |
| `IActivateAudioInterfaceAsyncOperation` | 异步激活 WASAPI family interface |
| `IActivateAudioInterfaceCompletionHandler` | ActivateAudioInterfaceAsync 完成回调 |
| `IAudioSystemEffectsPropertyStore` | 管理 audio system effects property store |
| `IAudioSystemEffectsPropertyChangeNotificationClient` | system effects property change callback |

### Function

```text
ActivateAudioInterfaceAsync
```

用于通过 device interface path 异步激活 WASAPI interface。

### Enumerations

- `EDataFlow`
- `ERole`
- `EndpointFormFactor`
- `AUDIO_SYSTEMEFFECTS_PROPERTYSTORE_TYPE`

---

## audioclient.h

官方 Header：
https://learn.microsoft.com/windows/win32/api/audioclient/

### Stream / Buffer

| 接口 | 用途 |
|---|---|
| `IAudioClient` | WASAPI stream 初始化 / 控制 |
| `IAudioClient2` | offload / client properties |
| `IAudioClient3` | shared-mode engine period / low latency |
| `IAudioRenderClient` | 写 render endpoint buffer |
| `IAudioCaptureClient` | 读 capture endpoint buffer |
| `IAudioClock` | stream data rate / position |
| `IAudioClock2` | device position |
| `IAudioClockAdjustment` | 调整 sample rate |
| `IAudioStreamVolume` | stream channel volume |

### Session Volume

| 接口 | 用途 |
|---|---|
| `ISimpleAudioVolume` | session master volume / mute |
| `IChannelAudioVolume` | session per-channel volume |

### Modern Audio Client Services

| 接口 | 用途 |
|---|---|
| `IAudioClientDuckingControl` | 当前 stream 是否导致其他 stream duck |
| `IAudioEffectsManager` | 查询/控制 stream audio effects |
| `IAudioEffectsChangedNotificationClient` | effect list/state 变化通知 |
| `IAudioViewManagerService` | 把 HWND 与 audio stream 关联 |
| `IAcousticEchoCancellationControl` | 查询 capture endpoint AEC 支持并设置 reference render endpoint |

### Structures

- `AudioClientProperties`
- `AUDIO_EFFECT`

### Enumerations

- `AUDCLNT_BUFFERFLAGS`
- `AUDCLNT_STREAMOPTIONS`
- `AUDIO_DUCKING_OPTIONS`
- `AUDIO_EFFECT_STATE`

---

## audiopolicy.h

官方 Header：
https://learn.microsoft.com/windows/win32/api/audiopolicy/

| 接口 | 用途 |
|---|---|
| `IAudioSessionManager` | session control / volume access |
| `IAudioSessionManager2` | session enumeration / notification / ducking |
| `IAudioSessionControl` | session metadata / events |
| `IAudioSessionControl2` | PID / identifier / system sounds / duck preference |
| `IAudioSessionEnumerator` | 枚举 endpoint 上的 session |
| `IAudioSessionEvents` | session 事件 |
| `IAudioSessionNotification` | 新 session 创建通知 |
| `IAudioVolumeDuckNotification` | duck / unduck 通知 |

---

## endpointvolume.h

官方 Header：
https://learn.microsoft.com/windows/win32/api/endpointvolume/

| 接口 | 用途 |
|---|---|
| `IAudioEndpointVolume` | endpoint master/channel volume 与 mute |
| `IAudioEndpointVolumeEx` | endpoint volume extended control |
| `IAudioEndpointVolumeCallback` | endpoint volume/mute 变化通知 |
| `IAudioMeterInformation` | peak meter |

结构：

- `AUDIO_VOLUME_NOTIFICATION_DATA`

---

## devicetopology.h

官方 Header：
https://learn.microsoft.com/windows/win32/api/devicetopology/

### Core topology

- `IDeviceTopology`
- `IConnector`
- `IPart`
- `IPartsList`
- `ISubunit`
- `IControlInterface`

### Jack / KS bridge

- `IKsJackDescription`
- `IKsJackDescription2`
- `IKsJackSinkInformation`
- `IKsFormatSupport`

### Hardware control interfaces

常见：

- `IAudioVolumeLevel`
- `IAudioMute`
- `IAudioAutoGainControl`
- `IAudioBass`
- `IAudioTreble`
- `IAudioLoudness`
- `IAudioInputSelector`
- `IAudioOutputSelector`
- `IAudioChannelConfig`
- `IDeviceSpecificProperty`
- `IPerChannelDbLevel`

---

## spatialaudioclient.h

官方 Header：
https://learn.microsoft.com/windows/win32/api/spatialaudioclient/

| 接口 | 用途 |
|---|---|
| `ISpatialAudioClient` | 创建 spatial audio stream |
| `ISpatialAudioClient2` | spatial stream 扩展 / offload capability |
| `ISpatialAudioObject` | 3D audio object |
| `ISpatialAudioObjectBase` | spatial object base |
| `ISpatialAudioObjectRenderStream` | object render stream |
| `ISpatialAudioObjectRenderStreamBase` | render stream base |
| `ISpatialAudioObjectRenderStreamNotify` | stream dynamic object state callback |
| `IAudioFormatEnumerator` | spatial object supported formats |

结构：

- `SpatialAudioClientActivationParams`
- `SpatialAudioObjectRenderStreamActivationParams`
- `SpatialAudioObjectRenderStreamActivationParams2`

枚举：

- `AudioObjectType`
- `SPATIAL_AUDIO_STREAM_OPTIONS`

---

## 怎么使用这份目录

### 找设备

先看：

```text
mmdeviceapi.h
```

### 真正读写 PCM

看：

```text
audioclient.h
```

### 找应用 / session

看：

```text
audiopolicy.h
```

### 控设备音量

看：

```text
endpointvolume.h
```

### 看硬件连接 / jack / topology

看：

```text
devicetopology.h
```

### 3D object audio

看：

```text
spatialaudioclient.h
```

---

## 注意

这份目录只收录 **Public Windows SDK API**。

以下不在这里当 Public API 列出：

- `IPolicyConfig`
- `IAudioPolicyConfigFactory`
- `Windows.Media.Internal.AudioPolicyConfig`

这些统一放在：

[Undocumented 专区](../undocumented/README.md)
