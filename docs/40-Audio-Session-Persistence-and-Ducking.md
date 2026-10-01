# Audio Session 持久化、Session GUID 与 Ducking

> 状态：🟢 Public API

Audio Session 不只是“一个应用的音量条”。

Windows 还会管理：

- session identity
- volume persistence
- cross-process sessions
- communications ducking

---

## 1. Rendering Session 音量默认持久化

Microsoft 官方 Audio Sessions 文档说明：

> rendering session 的 volume 和 mute 默认会跨应用 / 系统重启持久化。

也就是说：

```text
App volume = 35%
close app
reopen
→ session may restore 35%
```

这属于公开 Audio Session 行为。

---

## 2. Capture Session 不持久化

Capture session 的：

- volume
- mute

不会像 rendering session 一样持久化。

Loopback session 也按 capture session 对待，因此其 session setting 不持久化。

---

## 3. AUDCLNT_STREAMFLAGS_NOPERSIST

如果 render client 不希望 session volume / mute 跨 restart 持久化：

```text
AUDCLNT_STREAMFLAGS_NOPERSIST
```

可用于初始化 stream。

它的语义是：

> 禁止该 rendering session 的 volume / mute persistence。

---

## 4. 这和 Per-App Endpoint Persistence 完全不同

请区分：

### Audio Session volume persistence

🟢 Public

保存：

- volume
- mute

### Per-App endpoint route persistence

🔴 Undocumented / policy

保存：

- output endpoint
- input endpoint

两者不是同一套 storage / API contract。

---

## 5. Session GUID

`IAudioClient::Initialize` 可以把 stream 加入某个 session GUID。

如果传：

```text
GUID_NULL
```

Windows 会使用默认 session behavior。

应用也可以给相关 stream 使用相同 session GUID，让它们属于同一 session。

---

## 6. Cross-process Session

```text
AUDCLNT_STREAMFLAGS_CROSSPROCESS
```

允许 session 跨 process。

这也是为什么：

> Audio Session 不能简单理解为“PID 的别名”。

---

## 7. Ducking 是什么

Communications app 活跃时，Windows 可以自动降低其他非 communications stream 的音量。

例如：

```text
Music 100%
incoming voice call
→ music temporarily reduced
```

这就是 ducking。

---

## 8. Windows 谁负责 Ducking Policy

Microsoft Windows Audio Architecture 文档说明：

```text
Audio Service (audiosrv)
```

负责包括 ducking 在内的 audio policy。

---

## 9. IAudioVolumeDuckNotification

应用可以注册 ducking notification。

常见接口：

```text
IAudioSessionManager2::RegisterDuckNotification
IAudioVolumeDuckNotification
```

回调：

- OnVolumeDuckNotification
- OnVolumeUnduckNotification

---

## 10. 应用自己处理 Ducking

如果应用注册 ducking notification，它可以得到：

- communications session count
- duck / unduck signal

然后自己决定：

- 降多少
- fade curve
- UI 状态

---

## 11. SetDuckingPreference

`IAudioSessionControl2::SetDuckingPreference` 允许 session 表达是否选择退出默认 ducking behavior。

这个方法本身并不是：

> “设置别的应用音量”。

它修改的是 session 对系统 ducking policy 的 preference。

---

## 12. Ducking 和 Communications Role

两者相关但不是同一概念：

- ERole.eCommunications → default endpoint role
- audio category / communications session → stream / session policy
- ducking → system policy response

不要因为名字都含 communications 就混成一个 API。

---

## 13. UI 工具需要不要显示 Ducking？

如果做高级 mixer / diagnostics，可以记录：

- session category
- ducking preference
- current duck state
- communications active count

普通 volume mixer 不一定需要暴露这些。

---

## 14. 官方资料

- Audio Sessions  
  https://learn.microsoft.com/windows/win32/coreaudio/audio-sessions

- AUDCLNT_STREAMFLAGS constants  
  https://learn.microsoft.com/windows/win32/coreaudio/audclnt-streamflags-xxx-constants

- IAudioVolumeDuckNotification  
  https://learn.microsoft.com/windows/win32/api/audiopolicy/nn-audiopolicy-iaudiovolumeducknotification

- SetDuckingPreference  
  https://learn.microsoft.com/windows/win32/api/audiopolicy/nf-audiopolicy-iaudiosessioncontrol2-setduckingpreference
