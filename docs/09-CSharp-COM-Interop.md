# C# / COM / WinRT 互操作：SonicRoute 中实际遇到的问题

> 状态：🟢 Public API + 🟡 Observed + 🔴 Undocumented

Windows Core Audio 原生接口以 COM 为主。在 C# 中使用时，接口定义只是第一步，生命周期和 ABI 更容易出问题。

## 1. PreserveSig 与 HRESULT

SonicRoute 的底层 COM 声明大量使用：

```csharp
[PreserveSig]
int SomeMethod(...);
```

这样可以保留原始 HRESULT，便于：

- 明确区分失败原因；
- 输出十六进制错误码；
- 对设备切换 / 对象失效做恢复逻辑。

## 2. vtable 顺序必须准确

手工声明 COM 接口时，方法顺序就是 ABI。

漏一个基类方法或顺序错误，后面的调用就会落到错误的函数指针。

对公开接口，应优先根据 Windows SDK / 官方接口定义核对。

## 3. 未公开 WinRT 接口更加危险

SonicRoute 的 `AudioPolicyConfig` 没有依赖普通 RCW 方法调用，而是：

- `WindowsCreateString`
- `RoGetActivationFactory`
- `Marshal.QueryInterface`
- 读取 vtable
- `Marshal.GetDelegateForFunctionPointer`

这是针对未公开接口的项目级实现，不应当推广为普通 Core Audio 的默认写法。

## 4. HSTRING

Windows Runtime 使用 HSTRING，不是传统 LPWSTR。

在 SonicRoute 的 .NET 8 实测实现里，AudioPolicyConfig 的 HSTRING 使用 `WindowsCreateString` / `WindowsDeleteString` 手工管理。

## 5. COM apartment

回调型 API 尤其要关心线程 apartment。

例如 Audio Session notification 文档要求正确初始化 MTA，否则可能出现注册接口成功但收不到 session callback 的情况。

## 6. 资源释放

应区分：

- RCW：`Marshal.ReleaseComObject`
- 原始 COM pointer：`Marshal.Release`
- HSTRING：`WindowsDeleteString`

不要把三者混为一谈。

## SonicRoute 参考实现

- WASAPI declarations: https://github.com/kunkunkunQoQ/SonicRoute/blob/master/SonicRoute.Core/Interop/WasapiInterfaces.cs
- AudioPolicyConfig: https://github.com/kunkunkunQoQ/SonicRoute/blob/master/SonicRoute.Core/Interop/AudioPolicyConfig.cs
