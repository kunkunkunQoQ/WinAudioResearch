# Audio Session 枚举：边界情况与产品层决策

> 状态：🟢 Public API + 🟡 Observed + ✅ SonicRoute Verified

很多“Windows 音频应用列表 bug”不是接口调用失败，而是产品层做了错误假设。

## 1. 一个 PID 不一定只有一个 session

```text
PID
 ├─ session 1
 ├─ session 2
 └─ session 3
```

聚合时必须定义：

- volume 取哪个；
- mute 如何合并；
- meter 怎么合并；
- endpoint 怎么显示。

## 2. 默认 endpoint 不包含所有应用

应用可以被路由到别的 endpoint。

全系统应用列表更接近：

```text
enumerate endpoints
    ↓
enumerate sessions per endpoint
```

而不是只：

```text
get default endpoint
    ↓
enumerate sessions
```

## 3. Inactive session 仍可能有价值

Inactive 只表示当前没有活动音频。

如果产品希望：

- 提前调音量；
- 显示仍存在的 session；
- 保留最近使用应用；

Inactive 可能仍应显示。

## 4. Expired 不是所有残留情况的唯一判断

SonicRoute 实测发现某些 session：

- state 尚未 Expired；
- PID 已不存在。

因此产品 UI 会再检查进程存活。

诊断工具则可能故意保留这些条目，用于研究生命周期。

## 5. PID 信息读取失败不等于进程不存在

SonicRoute 当前策略：

- `ArgumentException` → PID 不存在；
- 其他异常 → 可能只是权限受限，保留 PID。

这样能避免把 elevated / protected process 错删。

## 6. DisplayName 可能为空

不要依赖：

```text
GetDisplayName() always returns useful text
```

常见 fallback：

1. session display name；
2. process name；
3. PID；
4. system sounds 特殊标记。

## 7. System Sounds

`IAudioSessionControl2::IsSystemSoundsSession` 可以识别系统声音 session。

不要强行套普通应用 PID UI 逻辑。

## 8. Enumerator 与 notification 的同步问题

Microsoft 文档指出 session enumerator 可能不知道 notification 新报告的 session。

严谨程序可以维护：

```text
initial enumeration
      +
OnSessionCreated
      +
session events
      +
periodic reconciliation
```

## 9. 缓存

SonicRoute 当前应用列表有约 1 秒缓存。

适合产品 UI，不适合研究 session 生命周期的严格测试。

研究工具应有：

```text
refresh / no-cache
```

概念上的能力。

## 10. 建议研究数据模型

不要只存：

```text
PID + Volume
```

更完整：

```text
EndpointId
Flow
SessionIdentifier
SessionInstanceIdentifier
GroupingParam
PID
State
DisplayName
ProcessName
Volume
Mute
Peak
IsSystemSounds
```
