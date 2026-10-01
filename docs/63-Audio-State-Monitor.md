# IAudioStateMonitor：监控系统 Render / Capture 声音状态

> 状态：🟢 Public API  
> 最低支持：Windows Build 19043

`IAudioStateMonitor` 是较新的 Core Audio API。

它解决的并不是：

> 获取每个 sample 的 peak。

而是：

> 查询 / 监听某一组 audio streams 当前处于什么声音级别状态。

---

## 1. Header

```text
audiostatemonitorapi.h
```

Library：

```text
windows.media.mediacontrol.lib
```

---

## 2. Interface

```text
IAudioStateMonitor
```

方法：

- GetSoundLevel
- RegisterCallback
- UnregisterCallback

---

## 3. Factory Functions

Render：

```text
CreateRenderAudioStateMonitor
CreateRenderAudioStateMonitorForCategory
CreateRenderAudioStateMonitorForCategoryAndDeviceId
CreateRenderAudioStateMonitorForCategoryAndDeviceRole
```

Capture：

```text
CreateCaptureAudioStateMonitor
CreateCaptureAudioStateMonitorForCategory
CreateCaptureAudioStateMonitorForCategoryAndDeviceId
CreateCaptureAudioStateMonitorForCategoryAndDeviceRole
```

---

## 4. 可以按什么过滤

可以根据：

- render / capture
- AUDIO_STREAM_CATEGORY
- device ID
- ERole

组合监控。

例如：

> 当前 communications render streams 是否有声音。

或者：

> 某个 endpoint 上某类 capture stream 当前状态。

---

## 5. Device ID

`CreateRenderAudioStateMonitorForCategoryAndDeviceId` 支持：

- MMDevice ID
- SWD ID

来源可以是：

- IMMDevice::GetId
- Windows.Devices.Enumeration
- MediaDevice

这是一条很有价值的 public API interoperability 线索。

---

## 6. Callback

注册：

```text
RegisterCallback
```

系统 sound level 改变时调用：

```text
AudioStateMonitorCallback
```

注册会返回：

```text
AudioStateMonitorRegistrationHandle
```

之后：

```text
UnregisterCallback(handle)
```

---

## 7. 为什么它和 IAudioMeterInformation 不一样

### IAudioMeterInformation

返回：

```text
0.0 .. 1.0 peak
```

适合：

- meter bar
- activity visualization

### IAudioStateMonitor

返回：

```text
AudioStateMonitorSoundLevel
```

更接近系统级：

> silent / low / full 等声音状态类别。

适合：

- policy
- state awareness
- feature activation

不要把它当 waveform meter。

---

## 8. 和 Audio Session Enumerator 的区别

Session Enumerator：

> 给你 session object。

AudioStateMonitor：

> 给你符合过滤条件的一组 stream 的 aggregate sound level state。

所以它不能直接替代：

- PID
- session volume
- app name

等 mixer 数据。

---

## 9. 对常驻工具的价值

如果某功能只想知道：

> 系统现在有没有特定类别的 render/capture activity？

AudioStateMonitor 可能比：

```text
每 30ms 扫 session + GetPeakValue
```

更符合目标。

但 UI peak meter 仍然需要 meter / PCM analysis。

---

## 10. 最低系统

官方文档：

```text
Windows Build 19043
```

所以如果软件还支持较早 Win10 build：

- runtime API availability check
- fallback

仍然必要。

---

## 11. 官方资料

- audiostatemonitorapi.h  
  https://learn.microsoft.com/windows/win32/api/audiostatemonitorapi/

- IAudioStateMonitor  
  https://learn.microsoft.com/windows/win32/api/audiostatemonitorapi/nn-audiostatemonitorapi-iaudiostatemonitor

- CreateRenderAudioStateMonitor  
  https://learn.microsoft.com/windows/win32/api/audiostatemonitorapi/nf-audiostatemonitorapi-createrenderaudiostatemonitor
