# Windows Services / Session 0 与 Audio

> 状态：🟢 Public Windows behavior

桌面应用和 Windows service 运行环境不同。

音频工具如果想：

- 开机即运行
- 无用户登录时处理
- system service capture/render

必须单独理解 Session 0。

## 1. Session 0

Windows services 通常运行在：

```text
Session 0
```

用户桌面则在其他 interactive session。

所以 service 没有普通桌面 UI environment。

## 2. Audio Service 本身

Windows audio architecture 由系统 service / Audio Engine / EndpointBuilder 等组件共同完成。

你的自定义 service 不应该假设：

> 只要是 LocalSystem 就比普通用户 app 更容易访问所有音频。

权限与 app model 是不同维度。

## 3. ActivateAudioInterfaceAsync

Microsoft 明确列出：

> 从 Session 0 service 调用 ActivateAudioInterfaceAsync 属于显式 safe activation 场景之一。

这意味着某些 render / WASAPI activation 不需要 desktop consent prompt 逻辑。

## 4. Microphone / Privacy

“Service”不等于自动绕过：

- privacy
- protected content
- driver / endpoint policy

设计录音 service 时需要单独验证目标 Windows 版本与安全模型。

## 5. Interactive UI

service 不应该直接：

- MessageBox
- tray icon
- WPF window

现代 Windows service 与用户 UI 通常需要：

```text
Service
  ↕ IPC
User-session UI process
```

## 6. Audio Session Scope

Audio Session 是音频流逻辑概念，不等于 Windows logon session。

不要把：

```text
Audio Session
```

和：

```text
Windows Session 0
```

混在一起。

## 7. User-specific Policy

一些设置位于：

- HKCU
- user audio policy
- user default endpoint preference

service 运行账户未必就是当前 interactive user。

所以系统 service 修改 user audio policy 很容易出现：

> 改到了错误 user profile。

## 8. Per-user App Routing

如果产品要做 per-user route：

更自然的位置通常是：

> 当前用户 session 的 agent / app

而不是 LocalSystem service 直接猜当前 user registry hive。

## 9. Service Restart

Audio service 自身重启可能让旧：

- IAudioClient
- session
- endpoint reference

失效。

自定义 service 也要有 re-enumeration / rebuild 能力。

## 10. 安全设计

IPC 需要考虑：

- named pipe ACL
- user identity
- command validation
- privilege boundary

不要让普通 user 通过音频 helper service 获得任意 system operation。

## 11. 官方资料

- ActivateAudioInterfaceAsync  
  https://learn.microsoft.com/windows/win32/api/mmdeviceapi/nf-mmdeviceapi-activateaudiointerfaceasync

- Services  
  https://learn.microsoft.com/windows/win32/services/services

- Windows Audio Architecture  
  https://learn.microsoft.com/windows-hardware/drivers/audio/windows-audio-architecture
