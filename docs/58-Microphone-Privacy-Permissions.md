# Microphone Privacy、Capabilities 与 Capture Permission

> 状态：🟢 Public Windows application model

“设备存在”不代表“应用一定能录音”。

Windows microphone access 还受到：

- user privacy settings
- packaged app capability
- enterprise policy
- app model
- remote / session environment

影响。

---

## 1. Packaged / WinRT App

使用 microphone 的 packaged app 通常需要声明：

```xml
<DeviceCapability Name="microphone" />
```

然后用户可以在 Windows Settings 中允许 / 禁止该 app 的 microphone access。

---

## 2. 用户可以随时关闭权限

即使第一次运行时用户允许：

之后也可以在 Settings → Privacy / Microphone 中关闭。

所以 capture app 不能只在安装时检查一次。

---

## 3. Enterprise Policy

管理员可通过：

- Group Policy
- MDM / CSP

控制 microphone access。

包括：

- user in control
- force allow
- force deny
- per package family settings

因此企业环境中：

> 用户 UI 看起来正常，但 policy 仍可能阻止应用。

---

## 4. Desktop Apps

传统 Win32 desktop app 的 privacy model 和 packaged UWP 不完全一样。

Windows Settings 通常还会有：

> Let desktop apps access your microphone

这样的控制。

实际行为要按：

- Windows version
- packaging
- capture API

测试。

---

## 5. MediaCapture / Speech Recognition

高层 API 往往更明显地参与 privacy permission model。

例如 Speech Recognition 文档要求：

- microphone capability
- user permission

并建议在真正 capture 前检查 access。

---

## 6. WASAPI Capture

低层 WASAPI 可以直接面向 endpoint。

但不要因此假设：

> privacy / policy 对所有桌面环境都不存在。

Windows 应用模型、设备访问控制、enterprise policy 仍可能影响真实 deployment。

---

## 7. 错误处理

用户禁用麦克风时，UI 不应该显示：

> “找不到设备”

更好的区分：

- No capture endpoint
- Permission denied / privacy blocked
- Device disabled
- Device invalidated
- Driver failure

---

## 8. UI 建议

如果权限被禁用：

- 明确告诉用户是 permission
- 不要自动修改 privacy setting
- 可以提供打开系统设置的入口
- 不要死循环重试 capture

---

## 9. 测试

```text
permission allow
permission deny
permission toggled while app open
packaged
unpackaged desktop
enterprise policy
RDP microphone redirect disabled
```

---

## 10. 官方资料

- App capability declarations  
  https://learn.microsoft.com/windows/apps/package-and-deploy/app-capability-declarations

- Speech recognition / microphone permission  
  https://learn.microsoft.com/windows/apps/develop/input/speech-recognition

- Privacy Policy CSP  
  https://learn.microsoft.com/windows/client-management/mdm/policy-csp-privacy
