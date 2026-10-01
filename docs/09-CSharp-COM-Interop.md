# C# / COM / WinRT 互操作：从“能调用”到“长期稳定运行”

> 状态：🟢 Public API + 🟡 Observed + 🔴 Undocumented + ✅ SonicRoute Verified

Windows Audio 原生接口大量基于 COM。C# 里最危险的问题往往不是“GUID 写错”，而是 ABI、ownership、apartment、native memory 与 RCW 生命周期。

## 1. 四类资源不要混淆

| 类型 | 示例 | 常见释放方式 |
|---|---|---|
| RCW | `IMMDevice` C# COM object | `Marshal.ReleaseComObject`（明确 ownership 时） |
| raw COM pointer | `QueryInterface` 得到的 `IntPtr` | `Marshal.Release` |
| HSTRING | `WindowsCreateString` | `WindowsDeleteString` |
| PROPVARIANT | `IPropertyStore.GetValue` | `PropVariantClear` |

这四类对象释放错方法，结果完全不同。

## 2. PreserveSig 与 HRESULT

SonicRoute 对底层接口大量使用：

```csharp
[PreserveSig]
int Method(...);
```

优点是保留原始 HRESULT。

研究和兼容性排查时，建议同时记录：

```text
hex
signed decimal
operation
endpoint / PID
Windows Build
```

比只抛一个 `COMException` 更有信息量。

## 3. COM vtable 顺序

`[ComImport]` 接口的方法顺序必须和原生 ABI 一致。

如果为了 C# 方便把继承接口“扁平声明”，必须保证：

```text
base interface methods
→ derived interface methods
```

完整对应原始 vtable。

漏一个方法会导致之后所有 slot 偏移。

## 4. Undocumented vtable 更危险

AudioPolicyConfig 当前使用 raw pointer + fixed slot。

大致：

```text
Marshal.ReadIntPtr(interface)
        ↓
vtable pointer
        ↓
ReadIntPtr(vtable, slot * IntPtr.Size)
        ↓
GetDelegateForFunctionPointer
        ↓
invoke
```

这类做法只适用于：

> 明确知道自己在调用 internal ABI，并愿意为 Windows Build 变化承担验证成本。

它不应该成为普通 MMDevice / WASAPI 的默认封装方式。

## 5. HSTRING

WinRT 的 HSTRING 不是 LPWSTR。

SonicRoute internal AudioPolicyConfig 使用：

```text
WindowsCreateString
WindowsGetStringRawBuffer
WindowsDeleteString
```

原因是项目希望明确控制 internal WinRT ABI，而不是依赖不确定的自动封送。

## 6. PROPVARIANT

设备 PropertyStore 常返回 `PROPVARIANT`。

```text
IPropertyStore.GetValue
        ↓
inspect vt
        ↓
read union
        ↓
PropVariantClear
```

结构布局要按目标架构认真核对，尤其不能只因为 x64 能跑就默认 ARM64 一定正确。

## 7. COM apartment

需要关注：

- STA / MTA；
- callback 从哪个线程进入；
- interface 是否要求在创建线程释放；
- UI Dispatcher 与 COM worker 边界。

Microsoft 对部分 WASAPI service interface 明确要求：`GetService` 得到的对象应在同一线程 Release。

详见：

[COM Threading & Apartments](14-COM-Threading-and-Apartments.md)

## 8. RCW Release 的两个极端都不对

### 从不释放

长期驻留程序会积累 COM 引用。

### 到处 FinalReleaseComObject

如果其他代码还持有同一 RCW，可能提前把对象释放。

更重要的是：

> ownership 必须清楚。

SonicRoute meter worker 的模式比较清晰：

- worker 创建；
- worker 使用；
- worker 刷新时释放；
- worker 退出时统一释放。

## 9. Callback 对象生命周期

注册：

```text
RegisterXXX(callback)
```

要确保 managed callback 仍有强引用。

退出时也应成对：

```text
UnregisterXXX(callback)
```

否则可能出现：

- native 仍想回调；
- managed 对象已经不可达；
- 或 callback 持有对象导致资源长期不释放。

## 10. Exception 不应该取代 HRESULT

对公开 COM API：

- 可让 .NET 自动转换异常；
- 也可保留 `PreserveSig` 手工处理。

对 undocumented API，更建议保留原始 HRESULT，因为“具体失败码”常常比异常类型更重要。

## 11. 参考源码

- COM / PROPVARIANT / HSTRING  
  https://github.com/kunkunkunQoQ/SonicRoute/blob/master/SonicRoute.Core/Interop/ComInterop.cs
- Public Core Audio declarations  
  https://github.com/kunkunkunQoQ/SonicRoute/blob/master/SonicRoute.Core/Interop/WasapiInterfaces.cs
- Internal AudioPolicyConfig  
  https://github.com/kunkunkunQoQ/SonicRoute/blob/master/SonicRoute.Core/Interop/AudioPolicyConfig.cs
