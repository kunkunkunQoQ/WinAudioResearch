# 按应用音频路由：Windows 的 persisted endpoint policy

> 状态：🔴 Undocumented + ✅ SonicRoute Verified

Windows 设置允许为某个应用选择输出 / 输入设备。

从用户视角它像“Audio Session 的属性”，但从接口角度，它不是普通 `IAudioSessionManager2` 提供的公开 setter。

## 1. 先区分三个概念

### 当前 Audio Session 在哪个 endpoint 上

这是运行时状态。

### 系统默认 endpoint

这是：

```text
flow + role → default endpoint
```

### 应用持久化 endpoint policy

这是：

```text
application/process audio policy
    → preferred render/capture endpoint
```

三个概念不能混用。

## 2. SonicRoute 当前内部调用链

```text
"Windows.Media.Internal.AudioPolicyConfig"
              ↓
WindowsCreateString
              ↓
RoGetActivationFactory
              ↓
QueryInterface(version-specific IID)
              ↓
raw COM interface pointer
              ↓
vtable slot
              ↓
SetPersistedDefaultAudioEndpoint
```

这条链不属于 Windows SDK 提供的稳定公共接口。

## 3. 当前记录的 IID

SonicRoute 当前实现：

```text
Windows 11 21H2+:
AB3D4648-E242-459F-B02F-541C70306324

Downlevel / Windows 10:
2A59116D-6C4F-45E0-A74F-707E3FEF9258
```

这些值应描述为：

> 🔴 当前 Windows 版本中观察到的 internal implementation detail

而不是“Windows Audio 官方稳定 IID”。

## 4. 当前记录的 vtable slot

```text
SetPersistedDefaultAudioEndpoint   slot 25
GetPersistedDefaultAudioEndpoint   slot 26
ClearAllPersisted...               slot 27
```

固定 slot 是风险最高的部分之一。

原因：

- 编译器不会替你验证 ABI；
- slot 改变后可能调用到完全不同的方法；
- “没有崩”不代表语义正确。

## 5. 参数结构

当前 Set 调用概念上使用：

```text
processId
flow
role
deviceId
```

SonicRoute 会对目标应用同时处理：

```text
eMultimedia
eConsole
```

这是 SonicRoute 的产品策略。

是否需要 Communications role，应按产品语义单独决定。

## 6. HSTRING

内部 WinRT API 使用 HSTRING。

SonicRoute .NET 8 实现中手动：

```text
WindowsCreateString
        ↓
pass IntPtr
        ↓
WindowsDeleteString
```

这样可以明确控制 internal WinRT ABI。

## 7. Device ID 格式

SonicRoute 对 per-app route 使用内部策略 API 期望的完整 device-interface path。

概念：

```text
\\?\SWD#MMDEVAPI#...
    + render/capture interface suffix
```

而系统默认设备 `IPolicyConfig::SetDefaultEndpoint` 使用的 ID 形式并不相同。

所以：

> 参数都叫 deviceId，不代表字符串格式可以互换。

详见：
[Device IDs & Properties](12-Device-IDs-and-Properties.md)

## 8. “系统默认”在 per-app route 中的含义

SonicRoute UI 有一个虚拟的“系统默认”选项。

它不是一个真实 `IMMDevice`。

当前语义：

> 清除该应用已持久化的 endpoint，使其重新跟随系统默认。

项目当前通过 null endpoint 实现。

这是 internal API 实测行为，必须继续按 Windows Build 验证。

## 9. Persistence

SonicRoute 观察到 per-app route 具有持久化行为，应用退出并重新启动后仍可能使用之前指定的 endpoint。

项目还记录了用户注册表中的 Audio PolicyConfig PropertyStore 与该行为有关。

这属于：

> 🟡 Observed / implementation-specific

不是 Microsoft 公开 API 契约。

详见：
[Per-App 路由持久化与重置观察](../findings/Per-App-Routing-Persistence.md)

## 10. 为什么不能“封装成 SDK”后忘掉风险

即使外层写成：

```csharp
SetAppDevice(...)
```

底层仍依赖：

- internal activation class；
- version-specific IID；
- fixed vtable slot；
- undocumented device ID convention；
- undocumented persistence behavior。

漂亮的 C# API 不会改变底层稳定性等级。

## 11. 建议验证矩阵

至少验证：

- Windows 10；
- Windows 11 当前稳定 Build；
- x64；
- ARM64（若支持）；
- render；
- capture；
- Console / Multimedia / Communications role；
- 应用运行中；
- 应用退出后重启；
- endpoint 拔插；
- Windows 重启后的 persistence。

建议使用：
[Research Validation Checklist](16-Research-Validation-Checklist.md)

## 12. 参考

SonicRoute：

https://github.com/kunkunkunQoQ/SonicRoute/blob/master/SonicRoute.Core/Interop/AudioPolicyConfig.cs

EarTrumpet：

https://github.com/File-New-Project/EarTrumpet
