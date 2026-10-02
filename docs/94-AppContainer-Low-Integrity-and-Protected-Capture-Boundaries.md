# AppContainer、Low Integrity 与 Audio Capture Security Boundaries

> 状态：🟢 Windows security model + 🟢 Public audio API + ⚠️ scenario-dependent behavior

Windows Audio API 存在不代表：

> 任意安全上下文都能访问任意设备、进程或受保护内容。

需要把：

- AppContainer
- Integrity Level
- capabilities
- microphone privacy
- protected media

一起考虑。

---

## 1. AppContainer

AppContainer 的目标是：

> least-privilege isolation。

AppContainer process：

- 使用独立 AppContainer SID
- 依赖 capabilities 获得资源访问
- 通常运行在 Low Integrity

资源访问需要同时满足：

- user/group permission
- AppContainer/capability permission
- integrity policy

---

## 2. Low Integrity

Windows Mandatory Integrity Control：

- Untrusted
- Low
- Medium
- High
- System

低完整性 process 不能随意修改更高 integrity object。

这会影响：

- process interaction
- filesystem
- registry
- IPC

但不能简单推导成：

> Low IL 一定不能播放 / capture audio。

Audio access 还有自己的 broker/capability/policy。

---

## 3. Packaged Audio App

典型 microphone app 需要：

```text
microphone capability
```

并受用户 privacy setting 控制。

因此：

```text
Device exists
```

不等于：

```text
App is authorized to capture it
```

---

## 4. Process Loopback

公开 API：

```text
ActivateAudioInterfaceAsync
+
VIRTUAL_AUDIO_DEVICE_PROCESS_LOOPBACK
+
AUDIOCLIENT_PROCESS_LOOPBACK_PARAMS
```

允许：

- include target process tree
- exclude target process tree

最低 Windows：

```text
Windows 10 Build 20348
```

（ActivateAudioInterfaceAsync documentation newer wording may refer to a nearby build for activation support; use current SDK/OS availability checks rather than hardcoding one source sentence.)

---

## 5. Process Loopback 不等于绕过 Security

即使可以指定 PID：

> 不应推断它可以绕过 DRM、protected media 或 Windows security boundary。

系统 loopback 文档明确存在：

- protected content
- trusted audio driver
- DRM restrictions

所以 capture app 必须把：

```text
silence / no protected data
```

视为可能的合法 policy result。

---

## 6. Protected Content

PUMA / Protected Media Path 可以限制：

- digital copy
- loopback
- output path

正确应用行为：

- 遵守 protection
- 不尝试 bypass
- 明确区分“没有普通 audio”与“content protected”

---

## 7. Session 0 Service

WASAPI loopback 文档有一个很重要的公开行为：

> 默认 endpoint loopback 可以包含不同 Terminal Services session 的 system mix；service running in Session 0 的 loopback client 也可能捕获其他 user session 的 audio。

这不等于：

> service 自动获得 microphone/private capture 权限。

Render loopback 与 microphone capture 必须分开理解。

---

## 8. Remote Desktop

RDP 会创建：

> session-specific virtual audio device。

因此：

- local endpoint
- remote endpoint
- Session 0
- user session

的 device/security boundary 都可能不同。

---

## 9. Security 诊断清单

遇到：

```text
E_ACCESSDENIED
silence
device unavailable
```

检查：

1. app package / AppContainer?
2. integrity level?
3. microphone capability?
4. user privacy setting?
5. enterprise policy?
6. protected media?
7. RDP / session?
8. target endpoint still valid?
9. API availability / OS Build?

---

## 10. 不要用管理员权限掩盖设计问题

如果普通用户环境失败：

> “Run as Administrator” 不应该是默认修复。

更应该确认：

- capability
- ACL
- app model
- API contract

音频工具常驻后台时尤其如此。

---

## 11. 官方资料

- AppContainer isolation  
  https://learn.microsoft.com/windows/win32/secauthz/appcontainer-isolation

- Mandatory Integrity Control  
  https://learn.microsoft.com/windows/win32/secauthz/mandatory-integrity-control

- ActivateAudioInterfaceAsync  
  https://learn.microsoft.com/windows/win32/api/mmdeviceapi/nf-mmdeviceapi-activateaudiointerfaceasync

- Process Loopback Params  
  https://learn.microsoft.com/windows/win32/api/audioclientactivationparams/ns-audioclientactivationparams-audioclient_process_loopback_params

- Loopback Recording / DRM  
  https://learn.microsoft.com/windows/win32/coreaudio/loopback-recording
