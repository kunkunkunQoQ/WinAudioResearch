# Audio Session：应用音频会话

> 状态：🟢 Public API + ✅ SonicRoute Verified

Audio Session 是 Windows 音量合成器和按应用音量控制的核心概念之一。

## 基本调用链

```text
IMMDevice
   ↓ Activate(IID_IAudioSessionManager2)
IAudioSessionManager2
   ↓ GetSessionEnumerator
IAudioSessionEnumerator
   ↓ GetSession
IAudioSessionControl2
```

`IAudioSessionControl2` 可以取得：

- Session state
- Display name
- Icon path
- Grouping parameter
- Session identifier
- Session instance identifier
- Process ID
- 是否为 system sounds session

## PID 不是 session 的唯一身份

真实程序中经常为了 UI 方便按 PID 聚合 session，例如：

```text
chrome.exe PID 1234
 ├─ session A
 ├─ session B
 └─ session C
```

这时应用层可以把多个 session 的音量或峰值聚合显示，但不要反过来假设 Core Audio 保证“一个 PID 一个 session”。

## ISimpleAudioVolume

`IAudioSessionControl2` 可以 QueryInterface / cast 到 `ISimpleAudioVolume`，用于：

- `GetMasterVolume`
- `SetMasterVolume`
- `GetMute`
- `SetMute`

这控制的是 **session 级音量**，不是设备总音量。

## Session notification 的隐藏坑

使用 `IAudioSessionManager2::RegisterSessionNotification` 时，Microsoft 文档明确要求先通过 session enumerator 调用一次 `GetCount`，让枚举机制开始发送新 session 通知。

此外，接收 session notification 的线程应正确初始化 MTA COM。

这类细节很容易造成“注册成功但没有回调”的假象。

## 官方资料

- IAudioSessionManager2: https://learn.microsoft.com/windows/win32/api/audiopolicy/nn-audiopolicy-iaudiosessionmanager2
- IAudioSessionControl2: https://learn.microsoft.com/windows/win32/api/audiopolicy/nn-audiopolicy-iaudiosessioncontrol2
- ISimpleAudioVolume: https://learn.microsoft.com/windows/win32/api/audioclient/nn-audioclient-isimpleaudiovolume
- RegisterSessionNotification: https://learn.microsoft.com/windows/win32/api/audiopolicy/nf-audiopolicy-iaudiosessionmanager2-registersessionnotification
