# Windows 版本兼容性

> 状态：🟢 Public API + 🟡 Observed + 🔴 Undocumented

公开 Core Audio 接口和未公开 AudioPolicyConfig 的兼容性要分开讨论。

## 公开 Core Audio

MMDevice、EndpointVolume 和基础 WASAPI 从 Windows Vista 时代就存在；`IAudioSessionManager2` 从 Windows 7 起可用于桌面应用。

这部分应直接以 Microsoft Learn 的 Minimum supported client 为准。

## AudioPolicyConfig

SonicRoute 当前实测代码区分：

| 系统 | IID |
|---|---|
| Windows 11 21H2+ | `ab3d4648-e242-459f-b02f-541c70306324` |
| Downlevel / Windows 10 | `2a59116d-6c4f-45e0-a74f-707e3fef9258` |

这些 IID 属于未公开实现细节，不存在 Microsoft 稳定兼容承诺。

## Build 判断

SonicRoute 在兼容 .NET Framework 4.8 时遇到过一个典型问题：

`Environment.OSVersion` 可能受到应用 manifest / compatibility 行为影响，从而返回与真实 Windows Build 不一致的兼容版本信息。

项目最终使用原生版本查询路径获得真实 Build，再决定 AudioPolicyConfig IID。

这是 **项目实测结论**，不是建议所有程序都绕过标准版本辅助 API。

## 建议记录格式

研究未公开接口时，每个验证结果至少记录：

```text
Windows edition:
Build:
Architecture:
Runtime:
Interface IID:
Operation:
HRESULT:
Result:
```

不要只记录“Win11 可用”。

## 兼容性原则

1. Public API 看 Microsoft 文档。
2. Undocumented API 看具体 Build 实测。
3. Windows 大版本升级后重新验证内部 IID / ABI。
4. 失败时优先安全降级，不要静默写入未知策略。
