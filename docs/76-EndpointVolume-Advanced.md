# IAudioEndpointVolume 深入：dB、Scalar、Steps、Channels 与 Hardware Support

> 状态：🟢 Public API

`IAudioEndpointVolume` 不只是：

```text
SetMasterVolumeLevelScalar
```

它还暴露 endpoint volume 的：

- dB range
- step model
- per-channel level
- mute
- hardware support

---

## 1. Scalar Volume

```text
0.0 .. 1.0
```

接口：

- GetMasterVolumeLevelScalar
- SetMasterVolumeLevelScalar

这是 normalized、audio-tapered UI 友好值。

不要理解成：

```text
0.5 = -6.02 dB
```

Windows 的 endpoint scalar 使用 audio-tapered curve。

---

## 2. dB Volume

接口：

- GetMasterVolumeLevel
- SetMasterVolumeLevel

直接用：

```text
dB
```

描述 level。

---

## 3. GetVolumeRange

可以取得：

- min dB
- max dB
- increment dB

所以 endpoint 真正支持的 volume range 不应该 hardcode。

---

## 4. Volume Steps

接口：

```text
GetVolumeStepInfo
VolumeStepUp
VolumeStepDown
```

Windows endpoint volume 有离散 step model。

系统键盘音量键 / UI 通常按 step 变化，而不是每次固定 +1%。

---

## 5. Channel Volume

接口：

- GetChannelCount
- GetChannelVolumeLevel
- SetChannelVolumeLevel
- GetChannelVolumeLevelScalar
- SetChannelVolumeLevelScalar

可单独控制 endpoint channel。

例如 stereo：

```text
L
R
```

---

## 6. Master vs Channel

最终每声道 effective endpoint gain 与：

- master
- channel level

共同有关。

不要简单把“left = master * leftScalar”当规范公式，具体 volume model 应按 API 定义使用。

---

## 7. Mute

```text
GetMute
SetMute
```

mute 不一定等于：

```text
volume scalar = 0
```

应该把两种状态分别保存 / 显示。

---

## 8. RegisterControlChangeNotify

callback：

```text
IAudioEndpointVolumeCallback
```

收到：

```text
AUDIO_VOLUME_NOTIFICATION_DATA
```

包含：

- event context
- mute
- master scalar
- channel count
- channel volume array

---

## 9. Event Context GUID

设置 volume/mute 时可以传：

```text
eventContext
```

callback 再拿到相同 GUID。

用于区分：

- 自己改的
- 外部 app 改的
- Windows UI 改的

防止反馈循环。

---

## 10. QueryHardwareSupport

查询：

- volume
- mute
- meter

是否由 endpoint hardware support。

如果硬件不支持：

> Windows 仍可能提供 software implementation。

所以 hardware flag 不是“API 是否能用”的等价判断。

---

## 11. Exclusive Mode

EndpointVolume 对 exclusive-mode endpoint volume control 仍然有意义。

但修改 endpoint master volume 会影响：

> 使用同 endpoint 的其他场景 / 系统状态。

因此 Microsoft 明确提醒 specialized app 使用时要谨慎。

---

## 12. UI 建议

如果做 mixer：

### 普通模式

用：

```text
Scalar 0..100%
```

### Advanced diagnostics

再显示：

- dB
- current step / total steps
- hardware support
- channel levels

---

## 13. 官方资料

- IAudioEndpointVolume  
  https://learn.microsoft.com/windows/win32/api/endpointvolume/nn-endpointvolume-iaudioendpointvolume

- EndpointVolume API  
  https://learn.microsoft.com/windows/win32/coreaudio/endpointvolume-api
