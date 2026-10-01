# Windows ARM64 Audio Development

> 状态：🟢 Public Windows / WDK guidance

ARM64 音频开发至少要分成：

1. User-mode audio app
2. Native library / COM interop
3. Kernel / audio driver

三者的架构要求不同。

## 1. User-mode .NET

.NET 应用可以分别发布：

- win-x64
- win-arm64

如果全部调用 Windows system DLL / COM，源码通常可以共用，但：

- P/Invoke struct layout
- IntPtr
- function pointer
- COM vtable
- native dependency

必须验证 ARM64 ABI。

## 2. COM / Core Audio

MMDevice / WASAPI 本身是 Windows system API。

从 API 语义上：

- x64
- ARM64

使用同一套 COM contract。

真正容易出错的是人工 interop declaration。

重点审计：

- pointer size
- struct packing
- PROPVARIANT
- WAVEFORMAT
- callback calling convention
- raw vtable slot

## 3. Native Libraries

如果程序依赖：

- FFmpeg
- ASIO helper
- codec DLL
- DSP library

必须有 ARM64 binary 或可用 emulation path。

“主程序 AnyCPU”不会自动让 native DLL 变成 ARM64。

## 4. Driver

Audio kernel driver 必须针对目标 architecture 构建。

一个 x64 `.sys` 不会自动成为 ARM64 native driver。

## 5. WDK ARM64

当前 WDK 支持在 ARM64 主机上原生：

- development
- testing
- deployment

同时可以从：

- x64 host
- ARM64 host

debug / deploy 到 ARM64 target。

WDK 10.0.26100.1 起 ARM64 host support 明显加强。

## 6. Build

典型：

```text
MSBuild
Platform=ARM64
```

driver sample 也可以切 ARM64 target build。

## 7. WDK / SDK Version

Microsoft 当前建议使用匹配的：

- Windows SDK
- WDK
- Visual Studio toolchain

驱动开发尤其不要把非常旧 WDK 与新 target build 混搭。

## 8. Driver Signing

ARM64 driver 同样受到 kernel-mode signing policy。

测试环境：

- test signing
- local/development certificate

生产：

- Microsoft signing / Hardware Dev Center
- HLK / dashboard workflow

## 9. HLK

如果产品宣称：

- ARM64 support

最好把 ARM64 target 纳入：

- install
- streaming
- sleep/resume
- endpoint
- glitch
- uninstall

实际测试，而不是只确认 PE machine type。

## 10. ARM64EC

某些 user-mode C++ 场景可以研究 ARM64EC，以便：

- ARM64 process
- 与部分 x64 ecosystem interoperability

但 kernel driver 不应把 ARM64EC 当作“通用 driver binary”。

## 11. WASAPI / COM 测试矩阵

建议：

```text
x64 native
ARM64 native
x64 emulated on ARM64（如果场景支持）
```

分别验证：

- endpoint enum
- session
- render/capture
- loopback
- internal APIs

尤其 undocumented API 不应仅凭 x64 结果推断 ARM64。

## 12. 官方资料

- Download the WDK  
  https://learn.microsoft.com/windows-hardware/drivers/download-the-wdk

- Building Arm64 Drivers  
  https://learn.microsoft.com/windows-hardware/drivers/develop/building-arm64-drivers

- Windows on Arm  
  https://learn.microsoft.com/windows/arm/
