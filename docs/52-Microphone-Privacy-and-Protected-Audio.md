# Microphone Privacy、Protected Media 与 Audio Capture 边界

> 状态：🟢 Public Windows security / media behavior

“API 能枚举到 microphone”不等于：

> 应用一定能录到 microphone。

“loopback 能录系统声音”也不等于：

> 所有 protected content 都允许 capture。

Windows audio 还受到 privacy / protected media policy 影响。

## 1. Microphone Capability

打包 Windows app 使用 microphone 时，需要：

```text
microphone capability
```

用户还可以在 Windows Settings 中禁止 microphone access。

应用必须准备：

- permission denied
- user later disables access
- enterprise policy override

## 2. Enterprise Privacy Policy

Windows 提供 policy：

```text
LetAppsAccessMicrophone
```

管理员可以：

- user control
- force allow
- force deny
- per-app policy

因此企业机器上：

> “用户设置里看起来允许”也不一定代表最终 policy 允许。

## 3. Desktop / Packaged 差异

不同：

- Win32 unpackaged app
- packaged desktop app
- UWP / WinRT app

在 capability / privacy model 上可能表现不同。

开发时应该按你实际 deployment model 验证，而不是套用一个 app model 的结论。

## 4. MediaCapture

MediaCapture 与 Windows privacy / capability 集成更紧密。

如果做：

- microphone record
- speech capture
- camera + audio

它通常比直接假设 device always accessible 更符合现代 app model。

## 5. Protected Media Path

Media Foundation 提供：

```text
Protected Media Path (PMP)
```

用于 protected content playback。

PMP 在受保护进程中运行。

应用主要交换：

- control
- commands

而不是直接访问解密后的 protected media data。

## 6. PUMA

Core Audio 历史上还有：

```text
Protected User Mode Audio
```

用于 protected audio rendering。

可以参与：

- SCMS
- HDMI HDCP
- output protection

## 7. Loopback Capture 的 DRM 边界

系统 loopback capture 并不是一个：

> “任何声音都必然可以复制出来”

的保证。

protected media 可以通过：

- trusted audio path
- output protection
- DRM policy

限制 capture / output behavior。

## 8. HDCP

对 HDMI protected media：

- endpoint
- display sink
- HDCP capability

可能共同参与 output policy。

所以：

> HDMI 正常播放普通声音

不代表：

> protected media 一定允许同样的 capture / route。

## 9. 开发建议

音频 capture app 应区分：

- device exists
- device active
- permission allowed
- stream opened
- protected content unavailable

不要全部显示成：

> “麦克风坏了”。

## 10. 官方资料

- App Capability Declarations  
  https://learn.microsoft.com/windows/apps/package-and-deploy/app-capability-declarations

- Privacy Policy CSP  
  https://learn.microsoft.com/windows/client-management/mdm/policy-csp-privacy

- Protected Media Path  
  https://learn.microsoft.com/windows/win32/medfound/protected-media-path

- Protected User Mode Audio  
  https://learn.microsoft.com/windows/win32/coreaudio/protected-user-mode-audio--puma-
