# Windows 音量与静音：先确定控制的是哪一层

> 状态：🟢 Public API + ✅ SonicRoute Verified

“把音量设成 50%”在 Windows Audio 里并不完整。

必须先回答：

> **哪个对象的音量？**

## 1. 常见音量层级

| 层 | 接口 | 含义 |
|---|---|---|
| Session master | `ISimpleAudioVolume` | 一个 Audio Session 的主音量 |
| Session channel | `IChannelAudioVolume` | Session 内每声道 |
| Stream channel | `IAudioStreamVolume` | 单个 stream 的每声道 |
| Endpoint master | `IAudioEndpointVolume` | 整个设备的主音量 / mute |

SonicRoute 常用：

- 应用音量 → `ISimpleAudioVolume`
- endpoint / 麦克风静音 → `IAudioEndpointVolume`

## 2. ISimpleAudioVolume

IID：

```text
87CE5498-68D6-44E5-9215-6DA47EF883D8
```

方法：

```text
SetMasterVolume
GetMasterVolume
SetMute
GetMute
```

音量 scalar：

```text
0.0 .. 1.0
```

传入范围之外，`SetMasterVolume` 可返回 `E_INVALIDARG`。

### Exclusive mode

Microsoft 文档明确说明 `ISimpleAudioVolume` 控制 Audio Session，不适用于 exclusive-mode stream。

## 3. IAudioEndpointVolume

IID：

```text
5CDF2C82-841E-4546-9722-0CF74078229A
```

它面向整个 endpoint：

- master dB
- master scalar
- mute
- channel volume
- callback
- hardware support

### Scalar 与 dB

```text
GetMasterVolumeLevel       → dB
GetMasterVolumeLevelScalar → 0.0 .. 1.0
```

UI slider 通常更适合 scalar。

但 scalar 与真实信号衰减不是简单线性关系；Windows 使用听感相关的 audio-tapered curve。

所以：

> UI 50% 不代表 PCM 振幅减半。

## 4. Event Context GUID

设置音量可以带 event-context GUID。

意义：

```text
Client A SetVolume(context=A)
       ↓
系统产生 callback
       ↓
Client A 可判断：
“这次变化是不是我自己引发的？”
```

可用于避免：

- UI 反馈循环；
- 自己设置一次又重复处理 callback；
- 多客户端同时控制时难以区分来源。

## 5. EndpointVolume callback

`IAudioEndpointVolumeCallback` 可以接收 endpoint volume / mute 变化。

常驻程序通常更适合：

```text
callback
  +
必要时低频 fallback polling
```

而不是高频不停 GetMute / GetVolume。

SonicRoute 曾为麦克风 mute 保留低频兜底，这是驱动兼容性的产品策略。

## 6. QueryHardwareSupport

`IAudioEndpointVolume::QueryHardwareSupport` 可以查询设备是否在硬件层支持：

- volume；
- mute；
- peak meter。

如果硬件不支持，Windows 可以提供软件实现。

因此：

> API 能用，不代表功能一定由硬件实现。

## 7. 常见 HRESULT

### E_INVALIDARG

常见于：

- scalar 超出 0..1；
- dB 超出设备范围；
- channel index 越界。

### AUDCLNT_E_DEVICE_INVALIDATED

endpoint 被拔出、禁用、重新配置或驱动资源变化。

常见恢复：

```text
release old objects
→ re-enumerate
→ re-activate
```

### AUDCLNT_E_SERVICE_NOT_RUNNING

Windows Audio service 未运行。

这和“没有设备”不是同一个问题。

## 8. HRESULT 不要只判断是否等于 0

COM 一般应先看：

```text
hr >= 0 → success / success status
hr <  0 → failure
```

有些成功状态不等于 `S_OK`。

详见：
[HRESULT & Diagnostics](13-HRESULT-and-Diagnostics.md)

## 9. 官方资料

- ISimpleAudioVolume  
  https://learn.microsoft.com/windows/win32/api/audioclient/nn-audioclient-isimpleaudiovolume
- SetMasterVolume  
  https://learn.microsoft.com/windows/win32/api/audioclient/nf-audioclient-isimpleaudiovolume-setmastervolume
- IAudioEndpointVolume  
  https://learn.microsoft.com/windows/win32/api/endpointvolume/nn-endpointvolume-iaudioendpointvolume
- EndpointVolume API  
  https://learn.microsoft.com/windows/win32/coreaudio/endpointvolume-api
