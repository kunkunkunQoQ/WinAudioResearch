# WinAudioResearch

> Windows Audio API research, implementation notes and reproducible experiments.  
> Windows 音频接口、实现机制、兼容性与实战研究笔记。

这个仓库用于整理 Windows 音频开发中的接口关系、调用链、兼容性差异、未公开机制和真实项目中的踩坑经验。

它不是一个新的音频管理器，也不是 WinAudioRoute 的替代品。这里的重点是 **分析、解释、记录和分享技术**；代码仅用于最小复现和验证。

## 为什么建立这个仓库

在开发 [SonicRoute](https://github.com/kunkunkunQoQ/SonicRoute) 的过程中，实际使用并验证了 Windows Core Audio / WASAPI 的多组接口，包括：

- MMDevice 设备枚举与设备属性
- Audio Session 会话枚举
- 按应用音量 / 静音
- 设备级 EndpointVolume
- 实时音频电平
- 设备变化通知
- 按应用输出 / 输入路由
- Windows 10 / Windows 11 接口差异
- C# / COM / WinRT 互操作与生命周期管理

其中有些属于 Microsoft 正式公开的 API，有些则依赖 Windows 内部、未文档化接口。长期把这些知识只留在产品源码里，很难看清边界，也不方便其他开发者复用经验，因此单独建立本仓库。

## 内容状态标记

文档会尽量标明结论来源和稳定程度：

| 标记 | 含义 |
|---|---|
| 🟢 **Public API** | Microsoft 文档化、Windows SDK 中公开的接口 |
| 🟡 **Observed** | 在真实系统 / 项目中观察到的行为，但不代表 Microsoft 提供兼容性保证 |
| 🔴 **Undocumented** | Windows 内部或未公开接口，可能随系统版本变化 |
| 🧪 **Experiment** | 仍在验证的实验或推断 |
| ✅ **SonicRoute Verified** | 已在 SonicRoute 的实际实现中使用或验证 |

> “已验证”不等于“Microsoft 承诺稳定”。尤其是未公开接口，两者必须分开看待。

## 导航

### 基础架构

- [Windows Audio 架构与接口地图](docs/00-Windows-Audio-Architecture.md)
- [MMDevice：设备枚举与端点](docs/01-MMDevice.md)
- [Audio Session：应用音频会话](docs/02-Audio-Sessions.md)
- [音量、静音与 EndpointVolume](docs/03-Volume-and-Mute.md)
- [IAudioMeterInformation：实时声音活动](docs/04-Audio-Meter.md)
- [设备变化与通知机制](docs/05-Device-Notifications.md)
- [WASAPI 与 IAudioClient](docs/08-WASAPI.md)
- [C# / COM / WinRT 互操作](docs/09-CSharp-COM-Interop.md)
- [Windows 版本兼容性](docs/10-Windows-Version-Compatibility.md)

### 按应用音频路由

- [按应用音频路由原理](docs/06-Per-App-Audio-Routing.md)
- [未公开接口研究入口](undocumented/README.md)
- [AudioPolicyConfig](undocumented/AudioPolicyConfig.md)
- [IAudioPolicyConfigFactory](undocumented/IAudioPolicyConfigFactory.md)

### 实战记录

- [SonicRoute 实测结论](findings/SonicRoute.md)
- [COM 生命周期与资源释放](findings/COM-Lifetime.md)
- [已知坑点](findings/Known-Pitfalls.md)
- [PolicyConfig：ERole / EDataFlow 参数语义复核](findings/PolicyConfig-Role-vs-DataFlow.md)

## Windows Audio 的核心关系

```text
MMDeviceEnumerator
       |
       +--> IMMDevice ------------------------------+
       |                                            |
       |                                            +--> IAudioClient / WASAPI
       |                                            |
       |                                            +--> IAudioEndpointVolume
       |                                            |
       |                                            +--> IAudioMeterInformation
       |
       +--> default endpoint / endpoint notifications
       
IMMDevice
   |
   +--> IAudioSessionManager2
            |
            +--> IAudioSessionEnumerator
                    |
                    +--> IAudioSessionControl2
                              |
                              +--> PID / state / identifier
                              +--> ISimpleAudioVolume
                              +--> IAudioMeterInformation
```

这里最容易混淆的一点是：

- **Endpoint** 是设备层，例如耳机、音箱、麦克风。
- **Session** 是会话层，例如某个应用在某个设备上的音频会话。
- **WASAPI stream** 是实际的数据流层。
- Windows 的“按应用默认设备”不是普通 Audio Session API 的一部分。

## 与其他仓库的关系

| 仓库 | 定位 |
|---|---|
| [SonicRoute](https://github.com/kunkunkunQoQ/SonicRoute) | 最终用户音频控制工具，也是本仓库的重要实战来源 |
| [WinAudioRoute](https://github.com/kunkunkunQoQ/WinAudioRoute) | 可复用的 Windows 音频控制库 |
| **WinAudioResearch** | 对 Windows 音频接口和实现机制本身进行分析、记录与分享 |

SonicRoute Wiki 中与底层实现有关的内容会逐步提炼到这里，但不会简单复制产品文档。

## 参考原则

1. 优先引用 Microsoft Learn / Windows SDK。
2. 对未公开接口同时给出第三方实现参考和实际验证结果。
3. 明确区分“官方定义”和“项目实测”。
4. 尽量给出最小调用链，而不是堆一整套框架。
5. 涉及 Windows 内部接口时必须注明版本风险。
6. 发现结论失效时，保留历史和系统 Build 信息。

## 当前重点

第一阶段重点整理 SonicRoute 已实际涉及的接口：

- `IMMDeviceEnumerator`
- `IMMDevice`
- `IPropertyStore`
- `IAudioSessionManager2`
- `IAudioSessionEnumerator`
- `IAudioSessionControl2`
- `ISimpleAudioVolume`
- `IAudioEndpointVolume`
- `IAudioMeterInformation`
- `IMMNotificationClient`
- `IAudioPolicyConfigFactory` / `AudioPolicyConfig`（未公开）

后续再扩展：

- WASAPI render / capture
- Loopback capture
- Exclusive mode
- IAudioClient2 / IAudioClient3
- Spatial Audio
- AudioGraph / WinRT Audio
- Audio Processing Objects (APO)
- DeviceTopology
- Bluetooth / communications role 行为

## License

MIT

---

如果你正在研究 Windows 音频接口，也欢迎提交 Issue / PR 补充不同 Windows Build、驱动和设备上的行为差异。
