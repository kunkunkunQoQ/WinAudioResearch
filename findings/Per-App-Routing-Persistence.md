# Per-App Audio Routing：持久化与重置的 SonicRoute 观察

> 状态：🟡 Observed + ✅ SonicRoute Verified + 🔴 touches undocumented behavior

这篇不是 Microsoft 规范说明，而是记录 SonicRoute 当前实现中观察到的 persisted audio policy 行为。

## 1. 单应用“系统默认”

SonicRoute 的 per-app route UI 里，“系统默认”不是一个真实 endpoint。

当前做法：

```text
SetPersistedDefaultAudioEndpoint(..., null)
```

目标语义：

> 清除该应用的持久化 endpoint，让它重新跟随系统默认。

## 2. ClearAll

当前 AudioPolicyConfig 还记录：

```text
ClearAllPersistedApplicationDefaultEndpoints
```

SonicRoute 用它尝试执行全局 reset。

当前代码还保留 fallback：逐进程对 render / capture 清除 persisted endpoint。

## 3. 注册表 PropertyStore 观察

SonicRoute 当前代码还会处理用户注册表中的：

```text
HKCU\Software\Microsoft\Internet Explorer\LowRegistry\Audio\PolicyConfig\PropertyStore
```

项目注释记录：

> 已退出应用的持久化路由可能存在于这里；仅调用 ClearAll 后，磁盘条目可能仍使旧路由在应用重新启动时恢复。

这属于：

- 🟡 实测 / 项目观察
- 🔴 Windows 内部实现细节

不是公开 API 契约。

## 4. 为什么风险很高

直接修改内部注册表路径意味着：

- Windows 未来可能改变存储格式；
- key / data schema 没有公开兼容保证；
- 相邻结构可能还有其他 audio policy；
- “整树删除”必须对应非常明确的用户动作。

所以：

> 可以研究和记录，但通用库不应轻易包装成“无风险重置 API”。

## 5. 后续应该验证什么

### Case A

```text
set per-app route
→ exit app
→ restart app
```

### Case B

```text
set route
→ call ClearAll
→ restart app
```

### Case C

```text
set route
→ remove related PropertyStore entry
→ restart app
```

### Case D

```text
set route
→ restart audiosrv
```

### Case E

```text
set route
→ reboot Windows
```

每一步记录：

- Windows Build；
- endpoint ID；
- persisted endpoint query；
- 实际应用输出设备；
- registry before / after；
- HRESULT。

## 6. 当前结论

这条记录说明：

> per-app route 更接近 Windows audio policy 的持久化配置，而不是“给当前 Audio Session 改一个字段”。

也说明为什么本仓库必须分开：

- public API behavior；
- observed Windows implementation；
- internal storage detail。
