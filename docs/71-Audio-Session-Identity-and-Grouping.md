# Audio Session Identity、Instance Identifier 与 Grouping Parameters

> 状态：🟢 Public API

如果做一个比 Windows SndVol 更复杂的 mixer，不能只保存：

```text
PID
```

Audio Session 自己有多个身份 / 分组概念。

---

## 1. Session Identifier

`IAudioSessionControl2::GetSessionIdentifier`

返回：

> session identifier string。

它描述 logical audio session identity。

---

## 2. Session Instance Identifier

`GetSessionInstanceIdentifier`

用于区分：

> 同一个 session identifier 下的不同 session instance。

所以：

```text
Identifier
≠
InstanceIdentifier
```

---

## 3. PID

`GetProcessId`

非常有用，但不是 session identity 的完整替代。

原因：

- 一个 PID 多 session
- cross-process session
- system sounds session
- process 生命周期比 session 短

---

## 4. Session GUID

应用在创建 WASAPI stream 时可以传：

```text
session GUID
```

相同 session GUID 可用于让相关 stream 进入同一 logical session。

如果使用默认：

```text
GUID_NULL
```

Windows 通常采用 process-specific default session behavior。

---

## 5. CROSSPROCESS

如果希望多个 process 的 stream 加入同一 audio session：

```text
AUDCLNT_STREAMFLAGS_CROSSPROCESS
```

并使用相同 session GUID。

这也是为什么：

> Audio Session 不是 PID 的别名。

---

## 6. Grouping Parameter

每个 session 还可以有：

```text
GroupingParam GUID
```

用途：

> 把多个独立 session 在 volume-control UI 里组合成一组。

---

## 7. SndVol 如何使用 Grouping Parameter

Microsoft 文档说明：

如果多个 session 具有相同 grouping parameter：

- volume mixer 可以把它们显示成一个 control
- 修改这个 group control 时，对所有 session 应同步更新

---

## 8. 为什么需要 GroupingParam

假设 app 架构：

```text
Process A → session A
Process B → session B
Process C → session C
```

它们逻辑上都属于：

> 同一个产品 / 同一音频体验。

Grouping parameter 可以帮助 mixer 避免显示 3 个重复 slider。

---

## 9. Session GUID vs Grouping Parameter

### Session GUID

决定：

> stream 属于哪个 audio session。

### Grouping Parameter

决定：

> 多个已经独立存在的 session 如何在 volume UI 上形成一组。

它们解决不同问题。

---

## 10. SonicRoute 当前策略

SonicRoute 当前产品 UI 更常按：

```text
PID
```

聚合。

这是简洁工具的实用选择。

但如果以后做完整 diagnostics / advanced mixer，应同时记录：

- PID
- SessionIdentifier
- InstanceIdentifier
- GroupingParam

---

## 11. 存储 Identity 时的风险

不要简单长期保存：

```text
SessionInstanceIdentifier
```

然后期待 app 下次启动还完全一样。

Session 是 runtime object。

长期 app identity 更适合结合：

- executable
- package identity
- app model
- policy identifiers

具体要看产品需求。

---

## 12. 官方资料

- IAudioSessionControl2  
  https://learn.microsoft.com/windows/win32/api/audiopolicy/nn-audiopolicy-iaudiosessioncontrol2

- Grouping Parameters  
  https://learn.microsoft.com/windows/win32/coreaudio/grouping-parameters

- Audio Sessions  
  https://learn.microsoft.com/windows/win32/coreaudio/audio-sessions
