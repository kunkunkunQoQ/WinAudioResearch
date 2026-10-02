# Modern C++ Core Audio COM Patterns：C++/WinRT、WIL 与 WRL

> 状态：🟢 Microsoft-supported/open-source tooling

Core Audio 是经典 COM API。

现代 C++ 代码不应该到处手写：

```cpp
ptr->AddRef();
...
ptr->Release();
```

Microsoft 当前 COM 文档明确推荐使用 smart pointer wrapper。

---

## 1. C++/WinRT winrt::com_ptr

Header：

```cpp
#include <winrt/base.h>
```

类型：

```cpp
winrt::com_ptr<T>
```

可用于：

- Windows Runtime
- classic COM

典型：

```cpp
winrt::com_ptr<IAudioClient> client;
```

它自动管理 COM reference count。

---

## 2. Microsoft 当前建议

Microsoft COM portal 当前建议：

### 新 Windows Runtime / classic COM code

```text
C++/WinRT winrt::com_ptr<T>
```

### 现有 classic COM code / 不想依赖 C++/WinRT

```text
WRL Microsoft::WRL::ComPtr<T>
```

---

## 3. WRL ComPtr

Header：

```cpp
#include <wrl/client.h>
```

使用：

```cpp
Microsoft::WRL::ComPtr<IMMDevice> device;
```

提供：

- automatic Release
- QueryInterface helpers
- Attach / Detach
- GetAddressOf

大量 Microsoft classic samples 都能看到 WRL ComPtr。

---

## 4. WIL

Microsoft open-source：

https://github.com/microsoft/wil

Windows Implementation Library 是 header-only C++ library。

它提供：

- RAII resource wrappers
- HRESULT helpers
- registry helpers
- COM pointer helpers
- TraceLogging
- Win32 usability helpers

---

## 5. wil::com_ptr

WIL 的：

```text
wil::com_ptr<T>
wil::com_ptr_nothrow<T>
wil::com_ptr_failfast<T>
```

可以根据错误策略选择：

- exception
- HRESULT / error code
- fail-fast

对于 Core Audio 这种大量 HRESULT 的代码很实用。

---

## 6. 为什么 WIL 对 Audio Tool 很有价值

Audio code 有大量：

- COM pointer
- HANDLE
- event
- HKEY
- CoTaskMem string
- HRESULT

WIL 可以把：

```cpp
goto cleanup;
Release();
CloseHandle();
RegCloseKey();
```

变成 RAII。

---

## 7. HRESULT Strategy

Windows Audio 研究代码不应该把所有 error 直接 throw 后丢失 context。

WIL 可以：

- exception style
- fail-fast style
- nothrow style

做音频 engine / realtime path 时：

> 尽量避免 realtime callback 中抛异常。

Control/configuration path 才适合更高级的 exception wrapper。

---

## 8. C++/WinRT 和 WinRT Audio

如果使用：

- AudioGraph
- MediaDevice
- DeviceInformation
- AudioStateMonitor

C++/WinRT 是很自然的 projection。

同时如果需要 classic Core Audio：

```text
winrt::com_ptr<IAudioClient>
```

可以在同一项目使用。

---

## 9. WRL 是否过时

WRL 仍然可用，并且很多现有 classic COM codebase 使用。

但新代码如果已经使用 C++/WinRT：

> 不需要为了 Core Audio 单独引入另一套 COM ownership style。

项目内一致性很重要。

---

## 10. QueryInterface

无论 wrapper 是什么，本质仍然是 COM：

```text
IUnknown
  ↓ QueryInterface(IID)
desired interface
```

smart pointer 不会改变：

- IID
- vtable
- apartment
- HRESULT
- object lifetime contract

它只是让 ownership 更安全。

---

## 11. Realtime Audio 注意

RAII 不等于：

> 任意 destructor 都适合在 realtime audio callback 中执行。

如果 destructor 会：

- Release 一个复杂 COM object
- free memory
- trigger system work

仍然可能破坏 realtime deadline。

Audio stream lifetime 应尽量在：

- initialization
- shutdown
- control thread

处理。

---

## 12. 官方资料

- COM Portal  
  https://learn.microsoft.com/windows/win32/com/component-object-model--com--portal

- Consume COM with C++/WinRT  
  https://learn.microsoft.com/windows/uwp/cpp-and-winrt-apis/consume-com

- WRL namespace / ComPtr  
  https://learn.microsoft.com/cpp/cppcx/wrl/microsoft-wrl-namespace

- WIL  
  https://github.com/microsoft/wil
