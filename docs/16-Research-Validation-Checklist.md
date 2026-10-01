# Windows Audio 研究验证清单

这份清单用于把：

> “我电脑上能用”

变成：

> “在明确环境、明确输入下得到可复现结果”。

## 1. 环境

```text
Date:
Windows edition:
Windows version:
OS build:
Architecture: x64 / ARM64
Runtime:
App bitness:
Audio service status:
```

## 2. Endpoint

```text
Flow:
IMMDevice ID:
FriendlyName:
DeviceState:
Driver:
Transport:
  internal / USB / HDMI / Bluetooth / virtual
Default Console:
Default Multimedia:
Default Communications:
```

## 3. Public API

```text
Interface:
IID:
Method:
Input:
HRESULT:
Output:
Expected:
Observed:
```

## 4. Undocumented API

额外记录：

```text
CLSID / Activatable class:
Interface IID:
Vtable slot:
Calling convention:
Parameter ABI:
Device ID format:
Role:
Flow:
Before state:
After state:
```

## 5. Persistence

研究 route / policy 时：

```text
Immediately after call:
After app restart:
After audiosrv restart:
After sign-out/sign-in:
After Windows restart:
After endpoint unplug/replug:
```

## 6. Cross-version

至少比较：

```text
Windows 10 supported baseline
Windows 11 current stable
newer build / Insider（若有）
```

如果项目支持 ARM64，再加：

```text
x64
ARM64
```

## 7. Failure logging

不要只写：

```text
failed
```

至少：

```text
HRESULT hex:
HRESULT decimal:
Exception:
Operation:
Repro rate:
Last known working build:
```

## 8. 最终结论模板

```text
Status:
  Public / Observed / Undocumented / Experiment

Verified on:
  ...

Result:
  ...

Known limitations:
  ...

Not verified:
  ...

Source:
  Microsoft docs / SDK / SonicRoute / third-party reference
```

## 9. Issue / PR 原则

如果一个 undocumented 行为没有 Build / HRESULT / IID，信息价值会明显降低。

本仓库希望长期积累的是：

> **可比较的实验记录，而不是零散的“能用 / 不能用”。**
