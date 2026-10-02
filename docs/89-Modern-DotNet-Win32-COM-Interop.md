# Modern .NET Windows Audio Interop：CsWin32、GeneratedComInterface 与 NativeAOT

> 状态：🟢 Microsoft .NET / Win32 tooling + engineering guidance

传统 C# Windows Audio interop 常见：

```text
[ComImport]
[Guid]
[InterfaceType]
[DllImport]
Marshal.ReleaseComObject
```

这仍然能工作，但现代 .NET 又增加了更强的 source-generated interop 方案。

---

## 1. CsWin32

Microsoft 项目：

https://github.com/microsoft/CsWin32

定位：

> 从 Win32 metadata 生成强类型 C# P/Invoke / COM interop projection。

不是：

> 直接解析你本机的 .h 文件。

---

## 2. Win32Metadata

CsWin32 的第一方 metadata 来源：

```text
Microsoft.Windows.SDK.Win32Metadata
```

其核心产物：

```text
Windows.Win32.winmd
```

Windows SDK header 会先被 Win32Metadata pipeline 转换成 metadata，再由语言 projection 使用。

---

## 3. NativeMethods.txt

CsWin32 典型使用：

```text
NativeMethods.txt
```

列出需要生成的：

- functions
- COM interfaces
- structs
- constants

例如 Windows Audio 项目可尝试请求：

```text
IMMDeviceEnumerator
IMMDevice
IAudioClient
IAudioClient3
IAudioRenderClient
IAudioCaptureClient
IAudioSessionManager2
IAudioEndpointVolume
```

实际 metadata availability 要以当前 Win32Metadata 为准。

---

## 4. 为什么比手写 P/Invoke 好

手写 Audio interop 最常见错误：

- wrong vtable order
- wrong enum underlying type
- wrong packing
- wrong pointer indirection
- wrong string marshalling
- ARM64 layout bug

如果接口已经存在于 public metadata：

> source-generated binding 可以显著减少手写 ABI 错误。

---

## 5. 但 undocumented API 仍然要手工处理

例如：

```text
Windows.Media.Internal.AudioPolicyConfig
IPolicyConfig internal/community definition
```

不属于正常 public Win32 metadata contract。

CsWin32 不会因为你输入一个内部接口名字，就自动帮你生成正确 ABI。

所以：

```text
Public API
→ generated binding preferred

Undocumented API
→ explicit research / manual ABI
```

仍然要分开。

---

## 6. .NET 8 GeneratedComInterface

.NET 8 引入 source-generated COM interop：

```csharp
[GeneratedComInterface]
```

配合：

```text
ComWrappers source generation
```

目标：

- build-time stub generation
- better NativeAOT support
- trimming compatibility
- 更容易诊断 marshalling

---

## 7. 为什么传统 COM interop 对 NativeAOT 不友好

传统 Windows-only built-in COM interop：

> runtime 生成 IL stub，再 JIT。

NativeAOT / trimming 环境中：

- runtime codegen 不适合
- metadata trimming 可能破坏 reflection-based assumptions

source-generated COM 则在编译期生成。

---

## 8. PreserveSig 差异

Source-generated COM 与 built-in COM interop：

- HRESULT handling
- PreserveSig
- marshalling default

存在差异。

迁移 Audio COM declaration 时：

> 不要把 `[ComImport]` interface 原封不动换成 `[GeneratedComInterface]` 就假设行为完全一样。

必须逐接口验证。

---

## 9. CsWin32 的新 COM Source Generator 模式

CsWin32 近年也在发展：

- GeneratedComInterface
- LibraryImport
- source-generator based COM

其 config / build-task 模式仍在持续演进。

因此生产项目：

> 固定 package version，并做生成代码 / ABI regression test。

---

## 10. SonicRoute 为什么目前仍适合显式 Declaration

SonicRoute 有两类接口：

### Public Core Audio

可以逐步评估：

- CsWin32
- Generated COM

### Undocumented AudioPolicyConfig

仍然需要：

- manual vtable
- HSTRING
- raw pointer
- build-specific IID

所以即使未来迁移 public declarations：

> internal 部分仍应该保持独立 interop layer。

---

## 11. NativeAOT Audio Tool

如果未来做 NativeAOT：

优先审计：

- COM activation
- callbacks
- source-generated COM
- HSTRING
- dynamic delegate generation
- Marshal.GetDelegateForFunctionPointer
- reflection

特别是：

> manual runtime function-pointer delegate construction

需要确认 NativeAOT compatibility。

---

## 12. 推荐目录结构

```text
Interop/
  Public/
    MMDevice.cs
    Wasapi.cs
    Session.cs
  Generated/
    ...
  Undocumented/
    AudioPolicyConfig.cs
```

不要把：

- generated public API
- hand-written internal ABI

混在同一文件。

---

## 13. 官方资料

- CsWin32  
  https://github.com/microsoft/CsWin32

- Win32Metadata  
  https://github.com/microsoft/win32metadata

- .NET ComWrappers source generation  
  https://learn.microsoft.com/dotnet/standard/native-interop/comwrappers-source-generation
