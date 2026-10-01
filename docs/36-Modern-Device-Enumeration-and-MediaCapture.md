# Windows.Devices.Enumeration、MediaDevice 与 MediaCapture

> 状态：🟢 Public WinRT APIs

传统 Core Audio 工具常直接使用 MMDevice。

Microsoft 当前 Windows 10/11 架构文档则更推荐现代 Windows 应用使用：

```text
Windows.Devices.Enumeration
```

进行设备枚举。

这两套 API 应该都理解。

---

## 1. DeviceInformation

现代设备对象：

```text
Windows.Devices.Enumeration.DeviceInformation
```

包含：

- Id
- Name
- Kind
- Properties

可以通过 AQS selector 筛选。

---

## 2. Audio Render Selector

```csharp
MediaDevice.GetAudioRenderSelector()
```

返回用于枚举 audio render device 的 selector。

再：

```csharp
DeviceInformation.FindAllAsync(selector)
```

得到输出设备。

---

## 3. Audio Capture Selector

```csharp
MediaDevice.GetAudioCaptureSelector()
```

枚举：

- microphones
- capture endpoints

---

## 4. DeviceWatcher

如果不是一次性 snapshot，而要实时维护设备列表：

```text
DeviceWatcher
```

事件：

- Added
- Updated
- Removed
- EnumerationCompleted

这和 Core Audio 的：

```text
IMMNotificationClient
```

解决的是相似产品问题，但处于不同 API family。

---

## 5. DeviceInformation vs IMMDevice

两者 ID 不应该靠字符串肉眼猜测映射。

如果 API 明确要求：

- DeviceInformation.Id
- endpoint ID
- device interface path

应按目标 API contract 传递。

---

## 6. ActivateAudioInterfaceAsync

WinRT device enumeration 常和：

```text
ActivateAudioInterfaceAsync
```

搭配。

它允许通过 device interface path 异步取得 WASAPI family COM interface。

例如：

- IAudioClient
- IAudioEndpointVolume

---

## 7. MediaCapture

`Windows.Media.Capture.MediaCapture` 是更高层 capture API。

适合：

- microphone
- camera
- audio/video record
- app capability / privacy aware capture

如果只是“我要录麦克风到文件”，它可能比直接 WASAPI 更合适。

---

## 8. MediaCapture vs WASAPI

### MediaCapture

优点：

- 高层
- device / permission integration
- media recording friendly

### WASAPI

优点：

- PCM buffer
- latency
- format
- raw
- loopback
- exact endpoint stream control

---

## 9. AudioGraph 也使用 DeviceInformation

AudioGraph 文档官方示例就是：

```text
MediaDevice.GetAudioRenderSelector
→ DeviceInformation.FindAllAsync
→ selected DeviceInformation
→ AudioGraphSettings.PrimaryRenderDevice
```

因此现代 WinRT audio API 家族之间是互相配合的。

---

## 10. Microsoft 当前推荐语境

Windows Audio Architecture 文档当前把：

- WASAPI
- XAudio2
- MIDI

列为推荐低层 streaming API；

把：

- Windows.Devices.Enumeration

列为推荐 enumeration API。

同时它把传统：

- MMDevice
- DeviceTopology
- EndpointVolume

描述为不推荐给一般 Windows application 的更底层 / 旧控制面。

但对 SonicRoute / mixer / diagnostics 这种 Win32 系统工具，它们仍是非常重要的接口。

所以：

> “not recommended for general Windows apps” 不等于 “接口废弃 / 不可用”。

---

## 11. 官方资料

- Enumerate Devices  
  https://learn.microsoft.com/windows/apps/develop/devices-sensors/enumerate-devices

- Device Information Properties  
  https://learn.microsoft.com/windows/apps/develop/devices-sensors/device-information-properties

- AudioGraph  
  https://learn.microsoft.com/windows/apps/develop/media-authoring-processing/audio-graphs

- ActivateAudioInterfaceAsync  
  https://learn.microsoft.com/windows/win32/api/mmdeviceapi/nf-mmdeviceapi-activateaudiointerfaceasync
