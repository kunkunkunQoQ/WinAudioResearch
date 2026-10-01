# App Model：Win32、MSIX、AppContainer、UWP 与 Audio API

> 状态：🟢 Public Windows app model

Windows audio API 的可用性有时不仅由：

- Windows Build
- interface version

决定。

还会受到：

- app packaging
- package identity
- AppContainer
- capability
- integrity level

影响。

---

## 1. 四种常见组合

Windows desktop app 大致可能是：

| Packaging | Process model |
|---|---|
| unpackaged | Medium IL Win32 |
| packaged | Medium IL desktop |
| packaged | AppContainer desktop |
| packaged | UWP / AppContainer |

所以：

> “MSIX app”不等于“必然 AppContainer”。

---

## 2. Capability 主要影响谁

例如：

- microphone
- bluetooth
- device-specific restricted capability

主要与：

```text
packaged + AppContainer
```

模型相关。

普通 unpackaged Medium IL Win32 的权限模型不同。

---

## 3. Microphone

现代 packaged / AppContainer app 访问 microphone：

- manifest capability
- user privacy consent
- enterprise policy

都可能影响结果。

所以测试 capture 时必须记录 app model。

---

## 4. ActivateAudioInterfaceAsync

这个 API 最初的重要用途之一就是：

> 让 UWP / WinRT device enumeration 后激活 WASAPI family COM interface。

典型：

```text
DeviceInformation
      ↓ device interface path
ActivateAudioInterfaceAsync
      ↓
IAudioClient
```

---

## 5. UI Thread / Consent Prompt

某些 capture activation 可能需要：

- main UI thread
- ability to show consent prompt

否则用户无法授予 microphone access。

Windows 10 之前还有更严格的 STA / agile callback 要求。

---

## 6. 安全的 Render Activation

Microsoft 文档说明某些 activation 明确属于 safe activation，例如：

- render device + IAudioClient
- render device + IAudioEndpointVolume
- Session 0 service 某些 activation

这类不需要 microphone consent UI。

---

## 7. HSA Restricted Capability

Windows audio hardware support app 常用：

```text
audioDeviceConfiguration
```

这是 restricted capability。

用于：

- Audio Device Modules
- IAudioSystemEffectsPropertyStore
- OEM device settings

不能把它当作普通 Store app 自动拥有的 capability。

---

## 8. Desktop SonicRoute 类应用

传统 WPF / Win32 Medium IL：

- MMDevice
- Audio Session
- EndpointVolume
- WASAPI

通常不需要 UWP microphone capability model 才能调用普通 public desktop API。

但如果：

- 使用 MSIX
- 改为 AppContainer
- 使用 restricted HSA API

就需要重新评估 app model。

---

## 9. Store Packaging 不等于 API 变成 WinRT

把 Win32 app 放进 MSIX：

> 不会自动把所有 Core Audio COM 调用改成 WinRT。

代码仍可以是传统 desktop API。

---

## 10. Service / Session 0

audio interface activation 在：

- desktop user process
- AppContainer
- service

行为可能不同。

Microsoft 对 `ActivateAudioInterfaceAsync` 特别说明了 Session 0 service 的 safe activation 场景。

---

## 11. 调试建议

记录：

```text
Packaged?
Package identity?
AppContainer?
Integrity level?
Capabilities?
Windows Build?
API?
HRESULT?
Consent state?
```

这样才能区分：

- API bug
- privacy denied
- capability missing
- packaging behavior

---

## 12. 官方资料

- Windows apps packaging / process model  
  https://learn.microsoft.com/windows/apps/get-started/intro-pack-dep-proc

- App Capability Declarations  
  https://learn.microsoft.com/windows/apps/package-and-deploy/app-capability-declarations

- ActivateAudioInterfaceAsync  
  https://learn.microsoft.com/windows/win32/api/mmdeviceapi/nf-mmdeviceapi-activateaudiointerfaceasync

- IAudioSystemEffectsPropertyStore  
  https://learn.microsoft.com/windows/win32/api/mmdeviceapi/nn-mmdeviceapi-iaudiosystemeffectspropertystore
