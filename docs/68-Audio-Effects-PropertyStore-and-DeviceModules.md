# Windows 11 Audio Effects Property Store 与 Audio Device Modules

> 状态：🟢 Public Windows 11 APIs  
> 主要面向 OEM / Hardware Support App / Audio DSP integration。

Windows 11 给 audio effects / hardware control 增加了更现代的公开控制面。

两块非常重要：

1. `IAudioSystemEffectsPropertyStore`
2. `AudioDeviceModulesManager`

---

## 1. IAudioSystemEffectsPropertyStore

Header：

```text
mmdeviceapi.h
```

最低客户端：

```text
Windows Build 22000
```

用途：

> 管理与 audio endpoint system effects 相关的 property store。

---

## 2. 三种 Property Store

`AUDIO_SYSTEMEFFECTS_PROPERTYSTORE_TYPE`：

### DEFAULT

来自 INF / OEM 默认配置。

特点：

- default settings
- 不保证跨 OS upgrade 保留

### USER

用户自定义 effect settings。

特点：

- OS 会尝试跨 upgrade / migration 保留

### VOLATILE

临时 effect state。

特点：

- reboot 后消失
- endpoint 重新 transition to active 时清理

---

## 3. API

`IAudioSystemEffectsPropertyStore` 提供：

- OpenDefaultPropertyStore
- OpenUserPropertyStore
- OpenVolatilePropertyStore
- ResetUserPropertyStore
- ResetVolatilePropertyStore
- RegisterPropertyChangeNotification
- UnregisterPropertyChangeNotification

---

## 4. 权限 / Capability

这个 API 不是普通桌面工具随便拿来写 OEM effect 配置的。

Microsoft 文档明确：

> 需要 restricted `audioDeviceConfiguration` capability。

目标主要是：

- OEM
- Hardware Support App (HSA)
- audio vendor control app

---

## 5. Admin Access

例如打开 default property store：

- admin 可请求 write
- non-admin 通常限制为 read-only

而且：

> OpenDefaultPropertyStore 不会凭空创建不存在的 store。

如果 INF 没有配置相应 store，可能返回 `E_NOTFOUND`。

---

## 6. Property Change Notification

Hardware Support App 可以注册：

```text
IAudioSystemEffectsPropertyChangeNotificationClient
```

监听 effect properties 变化。

注意：

> Microsoft 文档特别说明这个 notification API 面向 HSA，不建议 APO 自己用它订阅。

APO 有自己 Windows 11 notification framework。

---

## 7. Audio Device Modules

WinRT：

```text
AudioDeviceModulesManager
AudioDeviceModule
```

用于 vendor/OEM app 和：

- DSP
- hardware processing module
- driver-defined audio module

通信。

---

## 8. 典型流程

```text
MediaDevice.GetDefaultAudioRenderId(...)
       ↓
AudioDeviceModulesManager(endpointId)
       ↓
FindAll / FindAllById
       ↓
AudioDeviceModule
       ↓
SendCommandAsync(...)
```

---

## 9. Audio Device Module 是什么

它可以代表：

- hardware DSP block
- EQ module
- microphone processor
- vendor-defined processing unit

Driver / OEM 定义：

- module ID
- command protocol
- data format

Windows 提供通用 transport / discovery。

---

## 10. 为什么普通第三方应用很少使用

因为同样需要：

```text
audioDeviceConfiguration
```

restricted capability。

它更偏：

- OEM companion app
- driver vendor control panel
- Store Hardware Support App

---

## 11. 和 APO 的关系

可能同时存在：

```text
HSA
  ↓
AudioDeviceModulesManager
  ↓
DSP hardware module

HSA
  ↓
IAudioSystemEffectsPropertyStore
  ↓
APO effect settings
```

两者都是 modern OEM audio control surface，但负责对象不同。

---

## 12. 对普通 Audio 工具的意义

即使你不能直接使用 restricted API，了解它也很重要：

因为这解释了为什么：

- OEM EQ 设置并不一定存在普通 registry
- DSP state 可能由 hardware module 控制
- Windows 11 effect setting 有官方 property store framework

---

## 13. 官方资料

- IAudioSystemEffectsPropertyStore  
  https://learn.microsoft.com/windows/win32/api/mmdeviceapi/nn-mmdeviceapi-iaudiosystemeffectspropertystore

- AUDIO_SYSTEMEFFECTS_PROPERTYSTORE_TYPE  
  https://learn.microsoft.com/windows/win32/api/mmdeviceapi/ne-mmdeviceapi-audio_systemeffects_propertystore_type

- Configure and query Audio Device Modules  
  https://learn.microsoft.com/windows-hardware/drivers/audio/configure-and-query-audiodevicemodules

- Windows 11 APIs for APO  
  https://learn.microsoft.com/windows-hardware/drivers/audio/windows-11-apis-for-audio-processing-objects
