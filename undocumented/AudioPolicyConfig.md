# Windows.Media.Internal.AudioPolicyConfig

> 状态：🔴 Undocumented + ✅ SonicRoute Verified

SonicRoute 使用 Windows Runtime 内部 activatable class：

```text
Windows.Media.Internal.AudioPolicyConfig
```

来获取按应用默认音频 endpoint 的内部策略接口。

## 激活

项目当前实现的大致步骤：

```text
WindowsCreateString(class name)
        ↓
RoGetActivationFactory
        ↓
QueryInterface(target IID)
        ↓
IAudioPolicyConfigFactory pointer
```

## SonicRoute 当前记录的 ABI

项目代码当前使用的 vtable slot：

| Operation | slot |
|---|---:|
| SetPersistedDefaultAudioEndpoint | 25 |
| GetPersistedDefaultAudioEndpoint | 26 |
| ClearAllPersistedApplicationDefaultEndpoints | 27 |

这些值是内部 ABI 细节。

**它们不是 Windows SDK 公共契约。**

## 为什么使用手动 vtable

SonicRoute 的 .NET 8 实测中，项目没有直接依赖自定义 ComImport RCW 调用该 internal WinRT interface，而是保留原始 interface pointer 并读取 vtable function pointer。

这样可以精确控制 ABI 和 HSTRING，但也意味着兼容性责任完全落在应用自身。

## 安全原则

调用内部策略 API 时：

- 先识别 Windows Build；
- 明确目标 flow；
- 记录 HRESULT；
- 不要把失败吞掉；
- 不要在未知系统版本上盲目调用固定 slot；
- 提供恢复 / 清除策略的路径。
