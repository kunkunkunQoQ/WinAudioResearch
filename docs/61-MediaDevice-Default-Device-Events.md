# MediaDevice：现代默认音频设备 API 与事件

> 状态：🟢 Public WinRT API

传统 Win32：

```text
IMMDeviceEnumerator
GetDefaultAudioEndpoint
IMMNotificationClient
```

现代 WinRT 还有：

```text
Windows.Media.Devices.MediaDevice
```

---

## 1. GetAudioRenderSelector

```text
MediaDevice.GetAudioRenderSelector()
```

返回设备 selector。

搭配：

```text
DeviceInformation.FindAllAsync
```

枚举 render devices。

---

## 2. GetAudioCaptureSelector

同理：

```text
MediaDevice.GetAudioCaptureSelector()
```

枚举 capture devices。

---

## 3. GetDefaultAudioRenderId

```text
GetDefaultAudioRenderId(AudioDeviceRole)
```

取得指定 role 的默认 render device ID。

---

## 4. GetDefaultAudioCaptureId

```text
GetDefaultAudioCaptureId(AudioDeviceRole)
```

取得指定 role 的默认 capture device ID。

---

## 5. DefaultAudioRenderDeviceChanged

静态 event：

```text
MediaDevice.DefaultAudioRenderDeviceChanged
```

默认输出设备改变时触发。

---

## 6. DefaultAudioCaptureDeviceChanged

静态 event：

```text
MediaDevice.DefaultAudioCaptureDeviceChanged
```

默认 capture 设备改变时触发。

---

## 7. 与 IMMNotificationClient 怎么选

### Win32 System Tool

例如 SonicRoute：

- MMDevice
- Audio Session
- EndpointVolume

通常直接使用 IMMNotificationClient 更自然。

### WinRT / Modern App

如果已经大量使用：

- DeviceInformation
- AudioGraph
- MediaCapture

MediaDevice events 更自然。

---

## 8. 不要混用 ID Contract

WinRT device ID 与：

- IMMDevice endpoint ID
- internal AudioPolicyConfig device interface path

不要靠字符串观察自行假设可互换。

应按 API 文档的 ID contract 使用。

---

## 9. Threading

MediaDevice 是 WinRT static class，Microsoft metadata 标记为：

- Agile
- MTA threading model

这和传统 WPF STA / COM audio object 的 threading 习惯不同，混用时要理解边界。

---

## 10. 最低系统

MediaDevice 在 Windows 10 Universal API Contract v1 起存在。

---

## 11. 官方资料

- MediaDevice  
  https://learn.microsoft.com/uwp/api/windows.media.devices.mediadevice

- DefaultAudioRenderDeviceChanged  
  https://learn.microsoft.com/uwp/api/windows.media.devices.mediadevice.defaultaudiorenderdevicechanged

- DefaultAudioCaptureDeviceChanged  
  https://learn.microsoft.com/uwp/api/windows.media.devices.mediadevice.defaultaudiocapturedevicechanged
