# Windows Audio API Reference Matrix

这是仓库的快速查表页。

> Public 接口的系统版本 / Header 以 Microsoft Learn 和 Windows SDK 为准。  
> Undocumented 接口只记录当前研究状态，不代表 Microsoft 支持。

## 公开接口

| 接口 / class | GUID / IID | Header | 最低客户端 | 作用 | SonicRoute |
|---|---|---|---|---|---|
| MMDeviceEnumerator class | `BCDE0395-E52F-467C-8E3D-C4579291692E` | mmdeviceapi.h | Vista | 创建设备枚举器 | ✅ |
| `IMMDeviceEnumerator` | `A95664D2-9614-4F35-A746-DE8DB63617E6` | mmdeviceapi.h | Vista | endpoint 枚举 / 默认设备 / 通知 | ✅ |
| `IMMDevice` | `D666063F-1587-4E43-81F1-B948E807363F` | mmdeviceapi.h | Vista | endpoint object | ✅ |
| `IMMDeviceCollection` | `0BD7A1BE-7A1A-44DB-8397-CC5392387B5E` | mmdeviceapi.h | Vista | endpoint 集合 | ✅ |
| `IPropertyStore` | `886D8EEB-8CF2-4446-8D02-CDBA1DBDCF99` | propsys.h | - | property store | ✅ |
| `IAudioSessionManager2` | `77AA99A0-1BD6-484F-8BC7-2C654C9A9B6F` | audiopolicy.h | Windows 7 | session 枚举 / notification / duck | ✅ |
| `IAudioSessionEnumerator` | `E2F5BB11-0570-40CA-ACDD-3AA01277DEE8` | audiopolicy.h | Windows 7 | session 遍历 | ✅ |
| `IAudioSessionControl2` | `BFB7FF88-7239-4FC9-8FA2-07C950BE9C6D` | audiopolicy.h | Windows 7 | state / PID / metadata | ✅ |
| `ISimpleAudioVolume` | `87CE5498-68D6-44E5-9215-6DA47EF883D8` | audioclient.h | Vista | session volume / mute | ✅ |
| `IAudioEndpointVolume` | `5CDF2C82-841E-4546-9722-0CF74078229A` | endpointvolume.h | Vista | endpoint volume / mute | ✅ |
| `IAudioMeterInformation` | `C02216F6-8C67-4B5B-9D00-D008E73E0064` | endpointvolume.h | Vista | peak meter | ✅ |
| `IAudioClient` | Windows SDK | audioclient.h | Vista | WASAPI stream | 待深入 |
| `IAudioClient3` | Windows SDK | audioclient.h | Windows 10 | shared engine period | 待研究 |
| `IAudioRenderClient` | Windows SDK | audioclient.h | Vista | render buffer | 待研究 |
| `IAudioCaptureClient` | Windows SDK | audioclient.h | Vista | capture buffer | 待研究 |

> 没有为了“看起来完整”而手填尚未在当前仓库核对过的所有 IID。后续每补一个接口，优先从 Windows SDK / Microsoft 文档核对。

## 相关 enum

### EDataFlow

```text
eRender  = 0
eCapture = 1
eAll     = 2
```

### ERole

```text
eConsole        = 0
eMultimedia     = 1
eCommunications = 2
```

### DeviceState

```text
ACTIVE      = 0x1
DISABLED    = 0x2
NOTPRESENT  = 0x4
UNPLUGGED   = 0x8
```

### AudioSessionState

```text
Inactive = 0
Active   = 1
Expired  = 2
```

## 未公开接口

| 对象 / 接口 | 当前记录 | 用途 | 风险 |
|---|---|---|---|
| `PolicyConfigClient` class | CLSID `870AF99C-171D-4F9E-AF0D-E63DF40C2BC9` | 设置系统默认 endpoint | 🔴 |
| `IPolicyConfig` | IID `F8679F50-850A-41CF-9C72-430F290290C8` | `SetDefaultEndpoint` 等 | 🔴 |
| `Windows.Media.Internal.AudioPolicyConfig` | internal WinRT class | per-app persisted endpoint | 🔴 |
| AudioPolicyConfig Win11 IID | `AB3D4648-E242-459F-B02F-541C70306324` | Win11 internal factory | 🔴 |
| AudioPolicyConfig downlevel IID | `2A59116D-6C4F-45E0-A74F-707E3FEF9258` | downlevel internal factory | 🔴 |

## 常见入口关系

```text
IMMDeviceEnumerator
  ├─ EnumAudioEndpoints
  ├─ GetDefaultAudioEndpoint
  └─ RegisterEndpointNotificationCallback

IMMDevice
  ├─ OpenPropertyStore
  ├─ GetId
  └─ Activate
      ├─ IAudioSessionManager2
      ├─ IAudioEndpointVolume
      ├─ IAudioMeterInformation
      └─ IAudioClient
```

## Public / Internal 边界速查

| 想做的事 | 推荐接口 | 状态 |
|---|---|---|
| 枚举播放 / 录音设备 | MMDevice API | 🟢 |
| 读取默认设备 | `GetDefaultAudioEndpoint` | 🟢 |
| 监听默认设备变化 | `IMMNotificationClient` | 🟢 |
| 枚举 Audio Session | `IAudioSessionManager2` | 🟢 |
| 调 session 音量 | `ISimpleAudioVolume` | 🟢 |
| 调 endpoint 音量 | `IAudioEndpointVolume` | 🟢 |
| 读取 peak meter | `IAudioMeterInformation` | 🟢 |
| PCM render / capture | WASAPI | 🟢 |
| 设置系统默认 endpoint | 常见 `IPolicyConfig` | 🔴 |
| 设置应用持久化 endpoint | AudioPolicyConfig | 🔴 |


## 更广的 Windows Audio API Family

随着仓库扩展，除了最初的 Core Audio COM 接口，还应把下面这些 API family 放进同一张开发地图。

| Family | 主要对象 / 接口 | 用途 | 状态 |
|---|---|---|---|
| MMDevice | `IMMDeviceEnumerator`, `IMMDevice` | Endpoint 枚举 / 属性 / 默认设备读取 | 🟢 |
| Audio Session | `IAudioSessionManager2`, `IAudioSessionControl2` | Session / app audio state | 🟢 |
| EndpointVolume | `IAudioEndpointVolume`, `IAudioMeterInformation` | Endpoint 音量 / meter | 🟢 |
| WASAPI | `IAudioClient`, `IAudioClient2`, `IAudioClient3` | PCM render / capture / low latency | 🟢 |
| WASAPI service | `IAudioRenderClient`, `IAudioCaptureClient`, `IAudioClock` | Buffer 与 timing | 🟢 |
| Process Loopback | `ActivateAudioInterfaceAsync`, `AUDIOCLIENT_PROCESS_LOOPBACK_PARAMS` | 单进程树 render capture | 🟢 |
| DeviceTopology | `IDeviceTopology`, `IConnector`, `IPart` | Adapter / hardware topology | 🟢 |
| WinRT Enumeration | `DeviceInformation`, `DeviceWatcher` | 现代设备发现 | 🟢 |
| MediaCapture | `MediaCapture` | 高层 capture / record | 🟢 |
| AudioGraph | `AudioGraph` + node classes | 高层 routing / mixing / processing graph | 🟢 |
| Spatial Audio | `ISpatialAudioClient`, spatial object stream | Windows Sonic / object audio | 🟢 |
| XAudio2 | `IXAudio2`, source/submix/mastering voice | Game / realtime voice graph | 🟢 |
| Media Foundation | Source Reader / Sink Writer / MFT | Codec / container / transcode | 🟢 |
| Audio Effects | `IAudioEffectsManager`, APO interfaces | Effect discovery / system DSP | 🟢 |
| Driver / KS | WDM / WaveRT / KS / PortCls | Audio driver / streaming / topology | 🟢 WDK |
| ACX | Circuit / Stream / Element / Pin | 新 audio class extension model | 🟢 WDK |
| MIDI | Windows MIDI Services / WinMM MIDI | MIDI 1.0 / 2.0 / UMP | 🟢 |
| Legacy multimedia | waveOut/waveIn, DirectSound | Compatibility / historical APIs | 🟢 Legacy |
| System default policy | `IPolicyConfig` | 设置 system default endpoint | 🔴 |
| Per-app endpoint policy | internal AudioPolicyConfig | persisted app render/capture route | 🔴 |

## 需求到 API 的快速映射

| 需求 | 优先研究 |
|---|---|
| 音量合成器 | Audio Session + EndpointVolume |
| PCM 播放 / 录制 | WASAPI |
| 低延迟 Shared Mode | IAudioClient3 |
| 系统声音录制 | WASAPI Loopback |
| 单应用声音录制 | Process Loopback |
| C# 高层音频图 | AudioGraph |
| 游戏声音引擎 | XAudio2 |
| MP3/AAC/MP4 decode/encode | Media Foundation |
| 3D object audio | Spatial Audio |
| 系统级 DSP | APO / driver |
| 虚拟扬声器 / 麦克风 | Audio driver / SysVAD / ACX/WDM |
| MIDI 2.0 | Windows MIDI Services |
| Endpoint 硬件 topology | DeviceTopology / KS |
| 设置系统默认设备 | 🔴 PolicyConfig |
| 按应用指定设备 | 🔴 AudioPolicyConfig |

更完整的需求导向说明见：

[Windows Audio API 选择指南](33-API-Decision-Guide.md)
