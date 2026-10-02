# Audio Session Disconnect：为什么 Stream 突然失效，以及怎么恢复

> 状态：🟢 Public API

Audio session 并不是创建后就永远有效。

Windows 会因为系统事件主动 disconnect session。

---

## 1. OnSessionDisconnected

`IAudioSessionEvents`：

```text
OnSessionDisconnected(
    AudioSessionDisconnectReason reason)
```

通知 client：

> 这个 audio session 已被系统断开。

---

## 2. DisconnectReasonDeviceRemoval

原因：

- USB device 拔出
- Bluetooth endpoint 消失
- HDMI display disconnect
- virtual driver removed

处理：

```text
release old stream
→ re-enumerate endpoint
→ create new stream
```

---

## 3. DisconnectReasonServerShutdown

Windows Audio Service 停止。

旧：

- IAudioClient
- render/capture service interfaces

都不应继续使用。

等服务恢复后重新构建 audio graph。

---

## 4. DisconnectReasonFormatChanged

设备 stream format 改变。

例如：

- user 在 Sound Settings 修改 Default Format
- driver / endpoint format reconfiguration

Client 应：

- release
- get new format
- reinitialize

不要继续使用旧 buffer assumptions。

---

## 5. DisconnectReasonSessionLogoff

WTS user session logoff。

常见：

- RDP
- Fast User Switching
- Windows session lifecycle

---

## 6. DisconnectReasonSessionDisconnected

WTS session 被 disconnect。

和“应用窗口最小化”完全不是一个概念。

---

## 7. DisconnectReasonExclusiveModeOverride

一个 shared-mode session 可能被断开，以便 endpoint 给 exclusive-mode client 使用。

如果你的应用是 shared-mode player：

> 不能假设 exclusive app 只会 Initialize 失败而完全不影响你。

系统可能 disconnect existing shared session。

---

## 8. Microsoft 官方恢复建议

OnSessionDisconnected 后：

- release IAudioClient
- release previously obtained GetService interfaces

因为 outstanding service request 已失效。

---

## 9. 不要只 catch AUDCLNT_E_DEVICE_INVALIDATED

有些应用恢复代码只处理：

```text
AUDCLNT_E_DEVICE_INVALIDATED
```

但 session disconnect 还可能来自：

- server shutdown
- format change
- WTS
- exclusive override

完整实现应同时监听 session events。

---

## 10. State Machine

建议：

```text
Running
   ↓ disconnect
Invalidated
   ↓ release
WaitingForEndpoint
   ↓ endpoint/service available
Reinitializing
   ↓ success
Running
```

避免多个 callback 同时启动 3 次重建。

---

## 11. UI / Product

恢复期间：

- 不要假装 still playing
- 不要丢用户选择
- 可以显示 Reconnecting
- default device app 可在恢复时重新 resolve default endpoint

---

## 12. 官方资料

- OnSessionDisconnected  
  https://learn.microsoft.com/windows/win32/api/audiopolicy/nf-audiopolicy-iaudiosessionevents-onsessiondisconnected

- AudioSessionDisconnectReason  
  Windows SDK: audiopolicy.h / audiosessiontypes.h
