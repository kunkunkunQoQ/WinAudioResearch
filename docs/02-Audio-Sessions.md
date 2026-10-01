# Audio Session：应用音频会话

> 状态：🟢 Public API + ✅ SonicRoute Verified

Audio Session 是 Windows 共享模式音频控制中最容易被误解的概念之一。

它不是“进程”，也不是“设备”，而是 Windows Audio Engine 用来组织相关音频流的一层逻辑控制对象。

## 1. 核心接口

| 接口 | IID | 主要用途 |
|---|---|---|
| `IAudioSessionManager2` | `77AA99A0-1BD6-484F-8BC7-2C654C9A9B6F` | 枚举 / 监听 session |
| `IAudioSessionEnumerator` | `E2F5BB11-0570-40CA-ACDD-3AA01277DEE8` | 遍历 session |
| `IAudioSessionControl2` | `BFB7FF88-7239-4FC9-8FA2-07C950BE9C6D` | session metadata / PID |
| `ISimpleAudioVolume` | `87CE5498-68D6-44E5-9215-6DA47EF883D8` | session master volume / mute |

## 2. 基本调用链

```text
IMMDevice
   ↓ Activate(IID_IAudioSessionManager2)
IAudioSessionManager2
   ↓ GetSessionEnumerator
IAudioSessionEnumerator
   ↓ GetCount
   ↓ GetSession(index)
IAudioSessionControl2
```

注意：这个 manager 是 **针对某个 endpoint** 的。

所以：

> 一个 session enumerator 并不能天然看到“整个 Windows 的所有 session”。

如果目标是全系统应用列表，需要明确枚举哪些 endpoint。

## 3. IAudioSessionControl2 可以提供什么

常用方法：

- `GetState`
- `GetDisplayName`
- `GetIconPath`
- `GetGroupingParam`
- `GetSessionIdentifier`
- `GetSessionInstanceIdentifier`
- `GetProcessId`
- `IsSystemSoundsSession`
- `SetDuckingPreference`

### Session state

```text
Inactive = 0
Active   = 1
Expired  = 2
```

不要把 `Inactive` 当成“应该删除”。

Inactive 只表示当前没有活动音频，session 仍然可以存在。

## 4. PID 不是一对一主键

很多应用为了 UI 方便会做：

```text
session.GetProcessId()
      ↓
group by PID
      ↓
显示成一行应用
```

但这是产品层聚合。

Microsoft 的 `GetProcessId` 还可能返回成功状态 `AUDCLNT_S_NO_SINGLE_PROCESS`，表示 session 涉及多个进程；此时会返回创建该 session 的初始进程 ID。

因此 PID 应理解为“关联信息”，不是 session 的规范唯一标识。

真正区分 session 还可以看：

- SessionIdentifier
- SessionInstanceIdentifier
- GroupingParam

## 5. 一个 PID 多 session

真实情况可能是：

```text
PID 1234
   ├─ Device A / Session 1
   ├─ Device A / Session 2
   └─ Device B / Session 3
```

产品层必须定义：

- 全部显示还是合并；
- 音量修改作用于哪个 session；
- mute 如何合并；
- meter 取 max / average / 分别显示；
- endpoint 怎么展示。

SonicRoute 当前更偏向按 PID 聚合产品 UI。

## 6. Session Enumerator 不是绝对实时数据库

Microsoft 文档特别指出：

> session enumerator 可能不知道通过 `IAudioSessionNotification` 新报告的 session。

因此对实时性要求很高的程序，不能把一次 `GetSessionEnumerator` 当成永远完整的真相。

更稳妥的思路：

1. 初始枚举；
2. 注册 session notification；
3. 自己维护集合；
4. 定期或在异常时重新同步。

## 7. RegisterSessionNotification 的两个常见坑

### 先调用 GetCount

Microsoft 文档要求应用先通过 session enumerator 调一次 `GetCount`，再期待新 session notification。

否则可能出现：

> 注册返回成功，但没有 OnSessionCreated。

### COM apartment

通知线程要正确初始化 COM；相关文档特别强调 MTA 场景。

详见：
[COM Threading & Apartments](14-COM-Threading-and-Apartments.md)

## 8. “幽灵 session”

SonicRoute 实测会遇到：

- session state 尚未 Expired；
- 但对应 PID 已不存在；
- 任务管理器里也找不到进程。

当前 SonicRoute 会额外检查进程是否存活，并过滤这类 UI 无法操作的残留项。

状态：

> 🟡 Observed + ✅ SonicRoute Verified

这不代表诊断工具也应该删除它。诊断工具反而可以保留，用来研究 session 生命周期。

## 9. DisplayName 可能为空

不要假设：

```text
GetDisplayName() always returns a useful app name
```

实用 fallback 可以是：

1. session display name；
2. process name；
3. PID；
4. system sounds 特殊标识。

## 10. Session volume

`IAudioSessionControl2` 对象通常还能取得 / 转换成：

```text
ISimpleAudioVolume
```

用于 master volume / mute。

但 `ISimpleAudioVolume` 面向 Audio Session，并不用于 exclusive-mode stream。

## 11. SonicRoute 的枚举策略

当前应用列表大致：

```text
for flow in render + capture
    enumerate ACTIVE endpoints
        enumerate sessions
            skip PID = 0
            skip Expired
            inspect process
            aggregate by PID
```

当前还有约 **1 秒缓存**，减少多个 UI 功能短时间反复枚举音频子系统。

这是产品性能策略，不是 Windows API 行为。

## 12. 官方资料

- IAudioSessionManager2  
  https://learn.microsoft.com/windows/win32/api/audiopolicy/nn-audiopolicy-iaudiosessionmanager2
- GetSessionEnumerator  
  https://learn.microsoft.com/windows/win32/api/audiopolicy/nf-audiopolicy-iaudiosessionmanager2-getsessionenumerator
- IAudioSessionControl2  
  https://learn.microsoft.com/windows/win32/api/audiopolicy/nn-audiopolicy-iaudiosessioncontrol2
- GetProcessId  
  https://learn.microsoft.com/windows/win32/api/audiopolicy/nf-audiopolicy-iaudiosessioncontrol2-getprocessid
