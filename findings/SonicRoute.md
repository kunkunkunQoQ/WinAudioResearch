# SonicRoute 实战来源与已验证结论

> 状态：✅ SonicRoute Verified

WinAudioResearch 的第一批资料主要来自 SonicRoute 的实际开发经验，并与 Microsoft 文档交叉整理。

## 当前源码中可以直接核对的接口

SonicRoute Core 当前包含：

- `IMMDeviceEnumerator`
- `IMMDevice`
- `IMMDeviceCollection`
- `IPropertyStore`
- `IAudioSessionManager2`
- `IAudioSessionEnumerator`
- `IAudioSessionControl2`
- `IAudioMeterInformation`
- `IAudioEndpointVolume`

源码：

https://github.com/kunkunkunQoQ/SonicRoute/blob/master/SonicRoute.Core/Interop/WasapiInterfaces.cs

## 按应用路由

当前实现：

https://github.com/kunkunkunQoQ/SonicRoute/blob/master/SonicRoute.Core/Interop/AudioPolicyConfig.cs

已记录的实际问题包括：

- Win10 / Win11 internal IID 区分
- HSTRING 手工构造
- internal WinRT activation factory
- raw COM pointer / vtable 调用
- per-app render / capture device ID 包装
- Console + Multimedia role
- COM factory 生命周期

## 实时应用声音活动

当前实现：

https://github.com/kunkunkunQoQ/SonicRoute/blob/master/SonicRoute.Core/AudioMeterService.cs

重要实测设计：

1. 枚举全部 ACTIVE render endpoint，而不只是系统默认设备；
2. 每个 endpoint 枚举 session；
3. 用 PID 选择目标 session；
4. 从 session 取得 `IAudioMeterInformation`；
5. 同 PID 多个 session 取有效峰值；
6. UI 层做 attack / release 平滑；
7. 面板关闭时停止采样线程并释放 COM。

## Wiki

SonicRoute Wiki 仍然保留面向 SonicRoute 用户 / 贡献者的技术实现说明：

https://github.com/kunkunkunQoQ/SonicRoute/wiki

其中产品相关说明继续留在 Wiki；可泛化的 Windows Audio 知识逐步整理到本仓库。

## 原则

WinAudioResearch 不把 SonicRoute 的“当前实现”自动等同于“Windows 官方规范”。

每条结论会尽量拆成：

- Microsoft documented
- SonicRoute observed
- third-party reference
- undocumented implementation detail
