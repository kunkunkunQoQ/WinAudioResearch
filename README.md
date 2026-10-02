# WinAudioResearch

> **Windows Audio API research, implementation notes, compatibility records and real-world findings.**  
> Windows 音频接口、实现机制、兼容性、未公开接口与实战研究笔记。

WinAudioResearch 是一个面向 Windows 音频开发者的技术资料仓库。它不是另一个音频控制软件，也不是简单复制一套 COM 接口声明，而是把 Windows 音频开发里分散在 Microsoft Learn、Windows SDK、开源项目与真实产品源码中的知识整理成一套 **可查、可验证、可复现** 的资料。

第一批内容主要来自 [SonicRoute](https://github.com/kunkunkunQoQ/SonicRoute) 的真实开发经验，并与 Microsoft 官方文档和其他公开实现交叉核对。

## 这个仓库主要回答什么

这里希望逐步回答：

- Endpoint、Audio Session、WASAPI Stream 分别是什么？
- 为什么一个进程可能对应多个 Audio Session？
- 为什么只扫描默认播放设备会漏掉被路由到其他设备的应用？
- 应用音量、设备主音量、每声道音量分别应该用什么接口？
- `IAudioMeterInformation` 测的是设备电平还是应用电平？
- USB / 蓝牙设备切换后为什么旧 COM 对象会突然失效？
- `GetDefaultAudioEndpoint` 是公开 API，为什么“设置默认设备”常依赖未公开 `IPolicyConfig`？
- Windows 的“每应用输出 / 输入设备”为什么不属于普通 Audio Session API？
- `Windows.Media.Internal.AudioPolicyConfig`、内部 IID 与 vtable slot 有什么风险？
- C# 里的 RCW、raw COM pointer、HSTRING、PROPVARIANT 应该怎么管理？
- 怎样记录 HRESULT、Windows Build 和接口 IID，才能让一次“能用”变成研究结论？

## 仓库边界

这个仓库 **不是**：

- 第二个 SonicRoute；
- 一个完整音频 SDK；
- NAudio / EarTrumpet 的替代品；
- 把未公开接口包装成“稳定 API”。

这里更关心：

1. 接口为什么这样连接；
2. 哪些能力是 Microsoft 明确公开支持的；
3. 哪些只是项目实测；
4. 哪些依赖 Windows 内部接口；
5. Windows 更新后应该怎么重新验证。

## 证据与稳定性标记

| 标记 | 含义 |
|---|---|
| 🟢 **Public API** | Microsoft Learn / Windows SDK 文档化接口 |
| 🟡 **Observed** | 在真实系统 / 项目中观察到的行为，但不是 Microsoft 兼容性承诺 |
| 🔴 **Undocumented** | Windows 内部、未公开或没有稳定 SDK 契约的接口 |
| 🧪 **Experiment** | 仍需要更多 Build / 设备验证 |
| ✅ **SonicRoute Verified** | 已在 SonicRoute 实际实现中使用或验证 |

> **“SonicRoute 已验证”不等于“Microsoft 保证未来稳定”。**

## Windows Audio 的核心分层

```text
Application
    │
    ├── Audio Session
    │     ├─ IAudioSessionManager2
    │     ├─ IAudioSessionControl2
    │     └─ ISimpleAudioVolume
    │
    ├── WASAPI Stream
    │     ├─ IAudioClient
    │     ├─ IAudioRenderClient
    │     └─ IAudioCaptureClient
    │
    ▼
Windows Audio Engine
    │
    ▼
Audio Endpoint
    │
    ├─ IMMDevice
    ├─ IPropertyStore
    ├─ IAudioEndpointVolume
    ├─ IAudioMeterInformation
    └─ endpoint notifications
    │
    ▼
Driver / Hardware
```

另有不属于普通公开 Core Audio 控制面的策略层：

```text
Audio Policy
   ├─ System default endpoint
   └─ Per-app persisted endpoint
           ▲
           └─ 部分能力依赖未公开 PolicyConfig / AudioPolicyConfig
```

## 快速接口表

| 接口 / 对象 | 状态 | 主要用途 | SonicRoute |
|---|---|---|---|
| `IMMDeviceEnumerator` | 🟢 | 枚举 endpoint、默认设备、设备通知 | ✅ |
| `IMMDevice` | 🟢 | endpoint 入口、Activate、PropertyStore、ID | ✅ |
| `IPropertyStore` | 🟢 | 读取 FriendlyName 等设备属性 | ✅ |
| `IAudioSessionManager2` | 🟢 | 枚举 / 监听 Audio Session | ✅ |
| `IAudioSessionControl2` | 🟢 | PID、state、identifier、grouping | ✅ |
| `ISimpleAudioVolume` | 🟢 | session master volume / mute | ✅ |
| `IAudioEndpointVolume` | 🟢 | endpoint master volume / mute | ✅ |
| `IAudioMeterInformation` | 🟢 | endpoint / session peak meter | ✅ |
| `IAudioClient` | 🟢 | WASAPI stream 初始化和控制 | 研究中 |
| `IAudioClient3` | 🟢 | shared engine period / low-latency 相关 | 待扩展 |
| `IPolicyConfig` | 🔴 | 常见于设置系统默认 endpoint | ✅ / 需持续验证 |
| `IAudioPolicyConfigFactory` | 🔴 | 持久化 per-app endpoint | ✅ |

完整 IID / Header / 最低系统版本：  
**[API Reference Matrix](docs/11-API-Reference-Matrix.md)**

### Machine-readable API Database

仓库同时维护独立的结构化 API 数据库：

- **[API Database](api/README.md)** — 当前 **970 条**结构化记录
- **[Coverage](api/COVERAGE.md)** — 各 API family 覆盖率
- **[catalog.json](api/catalog.json)** — 机器可读表清单与记录计数

可直接查询：

```bash
python scripts/query_api.py IAudioClient
python scripts/query_api.py --status Undocumented
python scripts/query_api.py --family MediaFoundation
```

数据库修改由 GitHub Actions 自动执行 `scripts/validate_api_db.py` 校验。

想直接从需求选择技术栈：  
**[Windows Audio API 选择指南](docs/33-API-Decision-Guide.md)**

想查 Microsoft 官方入口：  
**[Microsoft 官方 Windows Audio 文档总索引](docs/18-Microsoft-Official-Documentation-Index.md)**

## 推荐阅读顺序

刚开始研究 Windows Audio：

1. [Windows Audio 架构与接口地图](docs/00-Windows-Audio-Architecture.md)
2. [MMDevice：设备枚举与端点](docs/01-MMDevice.md)
3. [Audio Session：应用音频会话](docs/02-Audio-Sessions.md)
4. [音量与静音](docs/03-Volume-and-Mute.md)
5. [实时声音活动 / Peak Meter](docs/04-Audio-Meter.md)

已经熟悉 Core Audio：

6. [按应用音频路由](docs/06-Per-App-Audio-Routing.md)
7. [默认音频设备](docs/07-Default-Audio-Device.md)
8. [C# / COM / WinRT](docs/09-CSharp-COM-Interop.md)
9. [Windows 版本兼容性](docs/10-Windows-Version-Compatibility.md)
10. [HRESULT 与诊断](docs/13-HRESULT-and-Diagnostics.md)

研究未公开接口：

11. [Undocumented 入口](undocumented/README.md)
12. [AudioPolicyConfig](undocumented/AudioPolicyConfig.md)
13. [IAudioPolicyConfigFactory](undocumented/IAudioPolicyConfigFactory.md)
14. [System PolicyConfig](undocumented/System-PolicyConfig.md)
15. [研究验证清单](docs/16-Research-Validation-Checklist.md)

## 完整文档目录

### Core Audio / WASAPI

- [00 - Windows Audio 架构](docs/00-Windows-Audio-Architecture.md)
- [01 - MMDevice / Endpoint](docs/01-MMDevice.md)
- [02 - Audio Session](docs/02-Audio-Sessions.md)
- [03 - Volume / Mute](docs/03-Volume-and-Mute.md)
- [04 - Audio Meter](docs/04-Audio-Meter.md)
- [05 - Device Notifications](docs/05-Device-Notifications.md)
- [06 - Per-App Audio Routing](docs/06-Per-App-Audio-Routing.md)
- [07 - Default Audio Device](docs/07-Default-Audio-Device.md)
- [08 - WASAPI / IAudioClient](docs/08-WASAPI.md)
- [09 - C# / COM / WinRT Interop](docs/09-CSharp-COM-Interop.md)
- [10 - Windows Compatibility](docs/10-Windows-Version-Compatibility.md)
- [11 - API Reference Matrix](docs/11-API-Reference-Matrix.md)
- [12 - Device IDs & Properties](docs/12-Device-IDs-and-Properties.md)
- [13 - HRESULT & Diagnostics](docs/13-HRESULT-and-Diagnostics.md)
- [14 - COM Threading & Apartments](docs/14-COM-Threading-and-Apartments.md)
- [15 - Session Enumeration Edge Cases](docs/15-Session-Enumeration-Edge-Cases.md)
- [16 - Research Validation Checklist](docs/16-Research-Validation-Checklist.md)
- [17 - Glossary](docs/17-Glossary.md)

### Windows Audio 全栈 / 官方平台

- [18 - Microsoft 官方 Windows Audio 文档总索引](docs/18-Microsoft-Official-Documentation-Index.md)
- [19 - WASAPI 深入：IAudioClient / Event / Exclusive / IAudioClient3](docs/19-WASAPI-Advanced.md)
- [20 - DeviceTopology](docs/20-DeviceTopology.md)
- [21 - AudioGraph / Windows.Media.Audio](docs/21-AudioGraph-and-WinRT-Audio.md)
- [22 - Spatial Audio / Windows Sonic](docs/22-Spatial-Audio.md)
- [23 - Audio Processing Objects (APO)](docs/23-Audio-Processing-Objects-APO.md)
- [24 - Media Foundation Audio](docs/24-Media-Foundation-Audio.md)
- [25 - Audio Driver Stack：WDM / WaveRT / KS / ACX](docs/25-Audio-Driver-Stack-WDM-WaveRT-ACX-KS.md)
- [26 - Low Latency / RAW / Hardware Offload](docs/26-Low-Latency-Raw-Offload.md)
- [27 - WASAPI Loopback / Process Loopback](docs/27-Loopback-and-Process-Audio-Capture.md)
- [28 - XAudio2](docs/28-XAudio2.md)
- [29 - Windows MIDI / MIDI 2.0](docs/29-Windows-MIDI.md)
- [30 - Legacy Windows Audio APIs](docs/30-Legacy-Windows-Audio-APIs.md)
- [31 - WAVEFORMATEX / WAVEFORMATEXTENSIBLE / Channel Mask](docs/31-Audio-Formats-WAVEFORMAT.md)
- [32 - Microsoft 官方 Audio Samples / Tools](docs/32-Microsoft-Audio-Samples-and-Tools.md)
- [33 - Windows Audio API 选择指南](docs/33-API-Decision-Guide.md)
- [34 - Audio Effects / Processing Modes](docs/34-Audio-Effects-and-Processing-Modes.md)
- [35 - AudioEndpointBuilder / 默认设备选择算法](docs/35-Endpoint-Builder-and-Default-Selection.md)
- [36 - Windows.Devices.Enumeration / MediaCapture](docs/36-Modern-Device-Enumeration-and-MediaCapture.md)
- [37 - Header / Library / DLL 对照表](docs/37-Headers-Libraries-DLLs.md)
- [38 - 第三方 Windows Audio 开发生态](docs/38-Third-Party-Audio-Ecosystem.md)
- [39 - Windows Audio 系统进程与服务](docs/39-Windows-Audio-Services-and-Processes.md)
- [40 - Audio Session 持久化与 Ducking](docs/40-Audio-Session-Persistence-and-Ducking.md)
- [41 - Bluetooth Classic / LE Audio](docs/41-Bluetooth-Audio-Classic-LE.md)
- [42 - USB Audio / UAC1 / UAC2](docs/42-USB-Audio.md)
- [43 - HDMI / DisplayPort / Digital Audio](docs/43-HDMI-DisplayPort-Digital-Audio.md)
- [44 - Audio Endpoint Property Keys](docs/44-Audio-Endpoint-Property-Keys.md)
- [45 - Audio ETW / WPR / WPA Diagnostics](docs/45-Audio-ETW-WPR-WPA-Diagnostics.md)
- [46 - ACM / DMO / MFT / Codecs](docs/46-ACM-DMO-MFT-Codecs.md)
- [47 - Audio Power Management](docs/47-Audio-Power-Management.md)
- [48 - ASIO / Pro Audio](docs/48-ASIO-and-Pro-Audio.md)
- [49 - Jacks / Connectors / Microphone Arrays](docs/49-Jacks-Connectors-and-Microphone-Arrays.md)
- [50 - Voice Activation / Keyword Detection](docs/50-Voice-Activation-and-Keyword-Detection.md)
- [51 - Audio Device Modules / HSA](docs/51-Audio-Device-Modules-and-HSA.md)
- [52 - Microphone Privacy / Protected Audio](docs/52-Microphone-Privacy-and-Protected-Audio.md)
- [53 - VST3 Plug-in Ecosystem](docs/53-VST3-Plugin-Ecosystem.md)
- [54 - Audio HLK Testing / Certification](docs/54-Audio-HLK-Testing-and-Certification.md)
- [55 - Microphone / Communications Audio](docs/55-Microphone-Communications-Audio.md)
- [56 - Realtime Audio Threading / MMCSS](docs/56-Realtime-Audio-Threading-and-MMCSS.md)
- [57 - Digital Audio Fundamentals](docs/57-Digital-Audio-Fundamentals-for-Windows-Developers.md)
- [58 - Open-source Windows Audio Codebases](docs/58-Open-Source-Windows-Audio-Codebases.md)
- [59 - Community Articles / Learning Resources](docs/59-Community-Articles-and-Learning-Resources.md)
- [60 - Language Bindings / Wrappers](docs/60-Language-Bindings-and-Wrappers.md)
- [61 - Virtual Audio Devices / Network Audio](docs/61-Virtual-Audio-Devices-and-Network-Audio.md)
- [62 - Windows Audio Developer Tools](docs/62-Windows-Audio-Developer-Tools.md)
- [63 - IAudioStateMonitor](docs/63-Audio-State-Monitor.md)
- [64 - Windows 11 AEC / Effects APIs](docs/64-Windows11-AEC-and-Effects-APIs.md)
- [65 - App Model / MSIX / AppContainer Audio](docs/65-AppModel-MSIX-AppContainer-Audio.md)
- [66 - Windows SDK Audio Header Catalog](docs/66-Windows-SDK-Audio-Header-Catalog.md)
- [67 - Modern Core Audio API Timeline](docs/67-Modern-Core-Audio-API-Timeline.md)
- [68 - Audio Stream Categories / Client Properties](docs/68-Audio-Stream-Categories-and-Client-Properties.md)
- [69 - Remote Desktop / Remote Audio](docs/69-Remote-Desktop-and-Remote-Audio.md)
- [70 - WaveRT Deep Dive](docs/70-WaveRT-Deep-Dive.md)
- [71 - ACX Deep Dive](docs/71-ACX-Deep-Dive.md)
- [72 - Deep Noise Suppression / Speech Effects](docs/72-Deep-Noise-Suppression-and-Modern-Speech-Effects.md)
- [73 - Audio Device Lifecycle / Recovery](docs/73-Audio-Device-Lifecycle-and-Recovery.md)
- [74 - Kernel Streaming Deep Dive](docs/74-Kernel-Streaming-Deep-Dive.md)
- [75 - Driver INF / Endpoint Configuration](docs/75-Audio-Driver-INF-and-Endpoint-Configuration.md)
- [76 - Audio Testing / Measurement](docs/76-Audio-Testing-and-Measurement.md)
- [77 - Exclusive Mode / Bit-perfect](docs/77-Exclusive-Mode-and-Bit-Perfect-Audio.md)
- [78 - Windows Audio Version Capability Matrix](docs/78-Windows-Audio-Version-Capability-Matrix.md)
- [79 - Windows ARM64 Audio Development](docs/79-Windows-ARM64-Audio-Development.md)
- [80 - Driver Signing / Distribution](docs/80-Driver-Signing-and-Distribution.md)
- [81 - Services / Session 0 / Windows Audio](docs/81-Services-Session0-and-Windows-Audio.md)
- [82 - WASAPI HRESULT / Troubleshooting Catalog](docs/82-WASAPI-HRESULT-Troubleshooting-Catalog.md)

### Resources / 外部资料总入口

- [Resources Hub：官方文档、SDK/WDK、Microsoft Samples、成熟开源、博客](resources/README.md)
- [References：来源分级与引用原则](references/README.md)

### Undocumented

- [Undocumented 入口](undocumented/README.md)
- [AudioPolicyConfig](undocumented/AudioPolicyConfig.md)
- [IAudioPolicyConfigFactory](undocumented/IAudioPolicyConfigFactory.md)
- [System PolicyConfig / SetDefaultEndpoint](undocumented/System-PolicyConfig.md)

### SonicRoute 实战记录

- [SonicRoute 已验证结论](findings/SonicRoute.md)
- [COM 生命周期](findings/COM-Lifetime.md)
- [Known Pitfalls](findings/Known-Pitfalls.md)
- [PolicyConfig：ERole / EDataFlow 参数复核](findings/PolicyConfig-Role-vs-DataFlow.md)
- [Per-App 路由持久化观察](findings/Per-App-Routing-Persistence.md)

## SonicRoute 提供的真实案例

### 设备枚举

当前源码：

```text
IMMDeviceEnumerator
  → EnumAudioEndpoints
  → IMMDevice
  → OpenPropertyStore
  → PKEY_Device_FriendlyName
```

SonicRoute 当前为播放 / 录音设备列表设置约 **3 秒短 TTL 缓存**，用于减少启动和快速连续操作时重复 COM 枚举。这是应用层性能策略，不是 Windows API 要求。

### 全系统 Audio Session

SonicRoute 会扫描 render + capture 的 ACTIVE endpoint，再逐个枚举 session，并按 PID 做产品层聚合。

当前实现还处理一种“幽灵会话”情况：

> session 尚未标记 Expired，但对应进程已经不存在。

SonicRoute 会额外检查进程存活并过滤这类 UI 无法操作的项。这是 **Observed / product behavior**。

### 应用实时声音活动

当前实现会：

- 扫描全部 ACTIVE render endpoint；
- 从 session 获取 `IAudioMeterInformation`；
- 同 PID 多 session 聚合 peak；
- 约 33ms 采样；
- 约 2s 重新扫描 session；
- UI 层使用 attack / release 平滑；
- 面板关闭后停止 worker 并释放 COM。

这些数字属于 SonicRoute 的实现经验，不是 Windows API 固定值。

### Per-App Audio Routing

当前实现：

```text
Windows.Media.Internal.AudioPolicyConfig
        ↓
RoGetActivationFactory
        ↓
IAudioPolicyConfigFactory
        ↓
SetPersistedDefaultAudioEndpoint
```

这一整条链属于 **Undocumented** 研究范围。

## 关于未公开接口

对未公开接口，至少记录：

- Windows edition / build
- x64 / ARM64
- runtime
- interface IID
- CLSID / activatable class
- vtable slot（若有）
- 参数
- HRESULT
- 调用前状态
- 调用后状态
- 重启 / 注销后是否保持
- 是否存在公开替代接口

建议使用 [研究验证清单](docs/16-Research-Validation-Checklist.md)。

## 与其他仓库的关系

| 仓库 | 定位 |
|---|---|
| [SonicRoute](https://github.com/kunkunkunQoQ/SonicRoute) | 最终用户 Windows 音频控制工具，也是本仓库的重要实战来源 |
| [SonicRoute Wiki](https://github.com/kunkunkunQoQ/SonicRoute/wiki) | 面向 SonicRoute 用户 / 贡献者的产品和技术说明 |
| [WinAudioRoute](https://github.com/kunkunkunQoQ/WinAudioRoute) | 可复用 Windows 音频控制库 |
| **WinAudioResearch** | 分析 Windows Audio API、内部策略、兼容性与实测行为 |

## 全网检索覆盖

当前仓库已经不仅整理 Microsoft Core Audio，还持续维护一份外部资料覆盖表：

- [Web Research Index](references/Web-Research-Index.md)
- [References 总入口](references/README.md)
- [第三方 Windows Audio 开发生态](docs/38-Third-Party-Audio-Ecosystem.md)
- [开源 Windows Audio Codebase 索引](docs/58-Open-Source-Windows-Audio-Codebases.md)
- [社区文章 / 学习资料](docs/59-Community-Articles-and-Learning-Resources.md)

目标是逐步把 Windows 音频开发需要查的 **官方 API、SDK/WDK、驱动、协议、专业音频标准、开源实现、社区经验与 undocumented 研究** 集中到一个仓库里，同时保留来源等级，避免把社区经验误写成 Windows 官方契约。

## 参考原则

1. Public API 优先引用 Microsoft Learn / Windows SDK。
2. 第三方项目不能替代 Microsoft 对公开接口的定义。
3. Undocumented API 必须明确风险。
4. “别人也这样实现”只算交叉参考，不算官方保证。
5. SonicRoute 行为写成 Verified / Observed，不自动升级成 Windows 规范。
6. Windows 大版本更新后，对内部接口重新验证。
7. 保留失败结果与 HRESULT；失败同样是研究数据。

## Roadmap

已覆盖：

- MMDevice / Endpoint / PropertyStore
- Audio Session / volume / mute / meter / persistence / ducking
- WASAPI shared / exclusive / loopback / process loopback / IAudioClient3
- DeviceTopology
- AudioGraph / MediaCapture / Windows.Devices.Enumeration
- Spatial Audio / Windows Sonic
- XAudio2
- Media Foundation Audio
- Audio formats / WAVEFORMATEXTENSIBLE / channel masks
- APO / processing modes / IAudioEffectsManager
- Windows Audio Engine / audiodg / audiosrv / AudioEndpointBuilder
- WDM / WaveRT / Kernel Streaming / ACX / virtual audio driver concepts
- Hardware offload / RAW / low latency
- MIDI / Windows MIDI Services / MIDI 2.0
- Legacy WinMM / DirectSound / DirectShow context
- per-app persisted endpoint / system-default internal policy
- C# / COM / WinRT interop
- Headers / DLLs / official samples / third-party ecosystem
- SonicRoute 实战案例与 undocumented 验证方法

后续重点：

- 可直接运行的最小实验项目
- Bluetooth A2DP / HFP / LE Audio
- USB Audio / HDMI / DisplayPort endpoint 行为
- Audio device property 全量索引
- Windows audio ETW / glitch / latency diagnostics
- ASIO 与 WASAPI 对比
- Codec / ACM / DMO 历史兼容
- ARM64 真机行为记录
- Windows 新 Build 的 undocumented API regression matrix

## License

MIT

欢迎提交 Issue / PR，特别欢迎补充 **不同 Windows Build、驱动、USB / 蓝牙设备、x64 / ARM64** 下的行为差异。
