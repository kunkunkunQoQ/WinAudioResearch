# System PolicyConfig / SetDefaultEndpoint

> 状态：🔴 Undocumented + ✅ SonicRoute implementation + 🧪 参数语义持续验证

这个接口用于记录桌面工具常见的“设置 Windows 系统默认 endpoint”实现。

它不是公开 MMDevice setter。

## 1. SonicRoute 当前 COM class

```text
CLSID_PolicyConfigClient
870AF99C-171D-4F9E-AF0D-E63DF40C2BC9
```

当前接口：

```text
IID_IPolicyConfig
F8679F50-850A-41CF-9C72-430F290290C8
```

源码：

https://github.com/kunkunkunQoQ/SonicRoute/blob/master/SonicRoute.Core/Interop/PolicyConfigClient.cs

## 2. 当前声明的方法

SonicRoute 接口表保留：

```text
GetMixFormat
GetDeviceFormat
ResetDeviceFormat
SetDeviceFormat
GetProcessingPeriod
SetProcessingPeriod
GetShareMode
SetShareMode
GetPropertyValue
SetPropertyValue
SetDefaultEndpoint
SetEndpointVisibility
```

重点不在于“这些方法都能用”，而在于：

> vtable 顺序必须完整，否则 SetDefaultEndpoint 会落到错误 slot。

## 3. SetDefaultEndpoint 参数语义

SonicRoute 当前第二参数声明成：

```text
EDataFlow
```

多个公开实现则使用：

```text
ERole
```

两组 enum 的底层值恰好都是 0 / 1 / 2：

```text
eRender  0  <-> eConsole        0
eCapture 1  <-> eMultimedia     1
eAll     2  <-> eCommunications 2
```

所以 ABI 层面可能完全不报错，却改变语义。

详细记录：

[PolicyConfig Role vs DataFlow](../findings/PolicyConfig-Role-vs-DataFlow.md)

## 4. Device ID

当前 SonicRoute 注释记录：

```text
SetDefaultEndpoint
→ 使用 IMMDevice.GetId() endpoint ID
```

项目曾观察到如果把 per-app AudioPolicyConfig 的完整 interface path 传入，会得到 `E_INVALIDARG`。

状态：

> ✅ SonicRoute observed

仍应在不同 Windows Build 持续验证。

## 5. 正确验证方式

不要只“设置后看任务栏声音图标”。

建议：

1. 调用前读取全部 flow / role 组合；
2. 执行 SetDefaultEndpoint；
3. 再读全部组合；
4. 记录实际改变的是哪个 role；
5. 观察 notification；
6. 重启 Audio Service / Windows 后继续验证。

## 6. 风险

- 未公开接口；
- 没有 SDK 兼容承诺；
- interface 版本可能变化；
- 参数语义来自社区实现与实测；
- Windows 更新后必须重新验证。

因此本仓库不会把它描述成“Windows 官方切默认设备 API”。
