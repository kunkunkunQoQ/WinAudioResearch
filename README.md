# WinAudioResearch

> Windows Audio API research hub — public APIs, driver interfaces, undocumented behavior, compatibility notes and real-world findings.

**WinAudioResearch** 把 Windows 音频开发中分散在 Microsoft Learn、Windows SDK / WDK、官方 samples、成熟开源项目与真实应用中的资料，整理成一套 **可查、可验证、可复现** 的开发参考。

它不是音频控制软件，也不是另一个封装库。这里关注的是：**接口是什么、它们如何连接、哪些是公开契约、哪些只是实测行为，以及不同 Windows 版本下有什么边界。**

第一批实战资料来自 [SonicRoute](https://github.com/kunkunkunQoQ/SonicRoute)，并持续与 Microsoft 官方资料交叉核对。

## 快速入口

| 想做什么 | 从这里开始 |
|---|---|
| 查某个 API / Header / IID / 最低系统版本 | **[API Database](api/README.md)** |
| 看当前数据库覆盖范围 | **[API Coverage](api/COVERAGE.md)** · [Core Audio Audit](docs/105-Core-Audio-SDK-Header-Coverage-Audit.md) |
| 看大型资料库总体建设计划 | **[Master Coverage Plan](docs/99-Windows-Audio-Master-Coverage-Plan.md)** |
| 看机器可读领域覆盖矩阵 | **[Domain Coverage Matrix](coverage/windows-audio-domains.csv)** · [Coverage Matrix Guide](coverage/README.md) |
| 从需求选择 Windows Audio API | **[API Decision Guide](docs/33-API-Decision-Guide.md)** |
| 理解 Windows Audio 整体架构 | **[Architecture](docs/00-Windows-Audio-Architecture.md)** |
| 查 Microsoft 官方资料入口 | **[Official Documentation Index](docs/18-Microsoft-Official-Documentation-Index.md)** |
| 查 SDK / WDK / Samples / 开源资料 | **[Resources Hub](resources/README.md)** |
| 研究内部 / 未公开接口 | **[Undocumented](undocumented/README.md)** |
| 看 SonicRoute 实战结论 | **[SonicRoute Findings](findings/SonicRoute.md)** |

## Machine-readable API Database

当前数据库包含 **2504 条结构化记录**：

| 类型 | 数量 |
|---|---:|
| Symbol / type / property / HRESULT | **1198** |
| Method / callback / DDI | **838** |
| WinRT / MIDI members | **130** |
| Capability / version | **20** |
| Dependency | **30** |
| Official samples | **23** |
| API relationships | **265** |

主要覆盖：

- Core Audio / MMDevice / Audio Session / Endpoint Volume / AudioStateMonitor
- WASAPI / IAudioClient / Loopback / Process Loopback
- DeviceTopology
- Spatial Audio
- Media Foundation / XAudio2
- WinRT Audio / AudioGraph / MediaCapture
- MIDI / Windows MIDI Services
- APO / Effects / Processing Modes
- Audio INF / APO packaging / Windows 11 CAPX property stores
- WaveRT / Kernel Streaming
- **ACX：Circuit、Stream、Element、DataFormat、Target、Manager、Factory、Device、Driver、ObjectBag**
- Audio endpoint / DeviceInformation / Driver INF property keys
- HRESULT / capability / dependency / relationship graph
- Undocumented PolicyConfig / per-app routing research

查询示例：

```bash
python scripts/query_api.py IAudioClient
python scripts/query_api.py --family ACX
python scripts/query_api.py --status Undocumented
python scripts/query_api.py --type relationship IMMDevice

python scripts/query_relations.py IMMDevice --depth 2
python scripts/validate_api_db.py
```

数据库由 GitHub Actions 自动校验 schema、重复项、来源链接和 catalog 计数。

## Windows Audio 分层

```text
Application
   │
   ├─ Core Audio / Audio Session / WASAPI
   ├─ WinRT Audio / AudioGraph / MediaCapture
   ├─ Media Foundation / XAudio2 / MIDI
   │
   ▼
Windows Audio Engine / Policy / Effects
   │
   ├─ Endpoint / DeviceTopology
   ├─ APO / Processing Modes
   │
   ▼
Driver Layer
   ├─ ACX
   ├─ PortCls / WaveRT
   └─ Kernel Streaming
   │
   ▼
Hardware / DSP / Codec / USB / Bluetooth / HDMI
```

Windows 还存在一部分不属于稳定公开 Core Audio 控制面的策略接口，例如系统默认设备和 per-app persisted endpoint。此类内容统一放在 [undocumented/](undocumented/README.md)，不会与 Public API 混写。

## 文档导航

不再在首页逐条展开全部文档。完整内容位于 **[docs/](docs/)**，推荐按主题进入：

| 方向 | 推荐入口 |
|---|---|
| Core Audio / Endpoint / Session | [MMDevice](docs/01-MMDevice.md) · [Audio Sessions](docs/02-Audio-Sessions.md) · [Volume](docs/03-Volume-and-Mute.md) |
| WASAPI / Latency / Loopback | [WASAPI](docs/08-WASAPI.md) · [Advanced](docs/19-WASAPI-Advanced.md) · [Loopback](docs/27-Loopback-and-Process-Audio-Capture.md) |
| Device / Property / Lifecycle | [Device IDs](docs/12-Device-IDs-and-Properties.md) · [Property Keys](docs/44-Audio-Endpoint-Property-Keys.md) · [Lifecycle](docs/73-Audio-Device-Lifecycle-and-Recovery.md) |
| Effects / APO | [APO](docs/23-Audio-Processing-Objects-APO.md) · [Effects](docs/34-Audio-Effects-and-Processing-Modes.md) |
| Driver / WDK | [Driver Stack](docs/25-Audio-Driver-Stack-WDM-WaveRT-ACX-KS.md) · [WaveRT](docs/70-WaveRT-Deep-Dive.md) · [PortCls](docs/101-PortCls-Reference-and-Coverage.md) · [DMus DDI](docs/102-DirectMusic-Kernel-DDI.md) · [ACX](docs/71-ACX-Deep-Dive.md) · [ACX Audit](docs/97-ACX-Public-Header-Coverage-Audit.md) · [KS](docs/74-Kernel-Streaming-Deep-Dive.md) · [KS Coverage](docs/98-KS-Audio-Property-Set-Coverage.md) |
| Hardware / Protocol | [Bluetooth](docs/41-Bluetooth-Audio-Classic-LE.md) · [USB Audio](docs/42-USB-Audio.md) · [HDMI / DP](docs/43-HDMI-DisplayPort-Digital-Audio.md) |
| Diagnostics / Testing | [ETW / WPR / WPA](docs/45-Audio-ETW-WPR-WPA-Diagnostics.md) · [Testing](docs/76-Audio-Testing-and-Measurement.md) · [HRESULT](docs/82-WASAPI-HRESULT-Troubleshooting-Catalog.md) |
| Modern / Specialized | [Spatial Audio](docs/22-Spatial-Audio.md) · [MIDI](docs/29-Windows-MIDI.md) · [Voice Activation](docs/50-Voice-Activation-and-Keyword-Detection.md) |

## 证据等级

| 标记 | 含义 |
|---|---|
| 🟢 **Public** | Microsoft 文档化的 SDK / WDK / WinRT 契约 |
| 🟡 **Observed** | 在真实系统或项目中观察到，但不是兼容性保证 |
| 🔴 **Undocumented** | Windows 内部、未公开或 ABI 不稳定接口 |
| 🧪 **Experimental** | 仍需更多 Windows Build / 硬件验证 |

> “项目里能用”不等于“Microsoft 保证未来稳定”。内部接口、固定 vtable slot 和观察到的 Registry 行为都会单独标注。

## 数据来源

优先级：

1. Windows SDK / WDK public headers
2. Microsoft Learn
3. Microsoft official samples
4. 成熟开源实现
5. SonicRoute / WinAudioRoute 实测
6. 社区资料与 reverse engineering

外部资料统一从 **[references/](references/README.md)** 和 **[Resources Hub](resources/README.md)** 进入，避免 README 变成链接堆积。

## 相关项目

| 仓库 | 定位 |
|---|---|
| [SonicRoute](https://github.com/kunkunkunQoQ/SonicRoute) | Windows per-app 音频控制工具，也是本仓库的重要实战来源 |
| [WinAudioRoute](https://github.com/kunkunkunQoQ/WinAudioRoute) | 可复用 Windows 音频控制库 |
| **WinAudioResearch** | Windows Audio API / Driver / Policy / Compatibility 研究资料库 |

## Roadmap

当前重点：

- 继续对照 Windows SDK / WDK 做 ACX 与 KS 全量覆盖审计
- 建立 callback / realtime / COM apartment / lifetime constraints 数据库
- 扩展 HRESULT、codec subtype、Header / Library / DLL 依赖
- 增加可直接运行的最小实验项目与诊断样例
- 记录不同 Windows Build、x64 / ARM64、USB / Bluetooth 设备的回归证据

详见 **[API Coverage](api/COVERAGE.md)**。

## Contributing

欢迎补充：

- 缺失的公开 API / DDI / property key
- 不同 Windows Build 的行为差异
- x64 / ARM64 差异
- USB / Bluetooth / HDMI / DSP 实测
- 官方 samples 与高质量开源实现
- 可复现的 undocumented regression 记录

提交结论时请尽量附带 **Windows Build、Header / IID / GUID、HRESULT、复现条件和来源**。Public / Observed / Undocumented 不应混写。

## License

MIT
