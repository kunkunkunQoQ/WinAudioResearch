# Windows Audio 架构与接口地图

> 状态：🟢 Public API + ✅ SonicRoute Verified

Windows Core Audio 不是一个“音量 API”，而是一组围绕 **设备（Endpoint）/ 会话（Session）/ 音频流（Stream）/ 策略（Policy）** 组织的组件。

理解这四层，是后续避免混用接口的关键。

## 1. 从应用到硬件

```text
Application
   │
   ├─ Audio Session
   │    ├─ session metadata
   │    ├─ session volume
   │    └─ session events / ducking
   │
   ├─ WASAPI Client
   │    ├─ render stream
   │    └─ capture stream
   │
   ▼
Windows Audio Engine
   │
   ├─ shared-mode mixing
   ├─ format conversion
   └─ endpoint processing
   │
   ▼
Audio Endpoint
   │
   ├─ speaker / headphone
   ├─ microphone
   ├─ HDMI / DP
   ├─ Bluetooth endpoint
   └─ virtual audio endpoint
   │
   ▼
Audio Driver / Hardware
```

这不是 Windows 音频驱动架构的完整图，而是面向普通桌面应用的控制面视角。

## 2. Endpoint：设备层

Core Audio 中最常用的设备对象是 `IMMDevice`。

```text
MMDeviceEnumerator
        ↓
IMMDeviceEnumerator
        ├─ EnumAudioEndpoints
        ├─ GetDefaultAudioEndpoint
        ├─ GetDevice
        └─ RegisterEndpointNotificationCallback
                ↓
             IMMDevice
```

`IMMDevice` 可用于：

- 获取 endpoint ID；
- 获取设备状态；
- 打开 PropertyStore；
- Activate 其他设备相关接口。

常见 Activate 目标：

- `IAudioClient`
- `IAudioSessionManager2`
- `IAudioEndpointVolume`
- `IAudioMeterInformation`

## 3. Session：应用音频控制层

```text
IMMDevice
  ↓ Activate
IAudioSessionManager2
  ↓ GetSessionEnumerator
IAudioSessionEnumerator
  ↓ GetSession
IAudioSessionControl2
```

Session 可以提供：

- state；
- display name；
- icon path；
- grouping parameter；
- session identifier；
- session instance identifier；
- process ID；
- system sounds 判断。

Session 还可关联：

- `ISimpleAudioVolume`
- `IAudioMeterInformation`
- session event callback

### Session ≠ Process

一个 PID 可能：

- 有多个 session；
- 跨多个 endpoint 有 session；
- 没有 session；
- 进程已退出但 session 暂时残留。

因此“按 PID 聚合”是产品层策略，不是 Core Audio 的一对一保证。

## 4. Stream：WASAPI 数据层

真正需要读写 PCM buffer 时，会进入 `IAudioClient` / WASAPI。

```text
IMMDevice
  ↓ Activate
IAudioClient
  ↓ Initialize
  ↓ GetService
  ├─ IAudioRenderClient
  └─ IAudioCaptureClient
```

### Shared mode

多个应用通过 Windows Audio Engine 共享 endpoint。

系统负责混音与必要的格式转换，适合绝大多数普通桌面音频应用。

### Exclusive mode

应用独占 endpoint stream。

适合部分低延迟 / 专业音频场景，但会提高格式、设备兼容和占用冲突的复杂度。

## 5. Volume 有多个控制层

| 层级 | 常用接口 | 控制对象 |
|---|---|---|
| Session master | `ISimpleAudioVolume` | 一个 Audio Session |
| Session channel | `IChannelAudioVolume` | Session 内每声道 |
| Stream channel | `IAudioStreamVolume` | 单个 stream |
| Endpoint master | `IAudioEndpointVolume` | 整个 endpoint |
| Peak meter | `IAudioMeterInformation` | endpoint 或可查询的 session |

因此：

> 应用音量和设备总音量不是同一层。

## 6. Policy：最容易和公开 API 混淆的一层

Windows UI 可以修改：

- 系统默认输出 / 输入设备；
- 单应用持久化输出 / 输入设备。

但这两类能力并不都有与公开 getter 对称的稳定 Win32 setter。

### 读取系统默认设备

公开：

```text
IMMDeviceEnumerator.GetDefaultAudioEndpoint(flow, role)
```

### 设置系统默认设备

桌面工具常见实现依赖未公开 `IPolicyConfig`。

### 设置每应用默认设备

SonicRoute / EarTrumpet 一类实现会进入内部 AudioPolicyConfig：

```text
Windows.Media.Internal.AudioPolicyConfig
      ↓
IAudioPolicyConfigFactory
      ↓
SetPersistedDefaultAudioEndpoint
```

所以必须明确：

```text
Audio Session control
     ≠
Per-app endpoint policy
```

## 7. SonicRoute 的真实接口组合

| 功能 | 接口 / 机制 |
|---|---|
| 枚举设备 | `IMMDeviceEnumerator` |
| 设备名称 | `IPropertyStore` |
| 默认设备读取 | `GetDefaultAudioEndpoint` |
| 应用枚举 | `IAudioSessionManager2` |
| 应用音量 | `ISimpleAudioVolume` |
| 麦克风 endpoint mute | `IAudioEndpointVolume` |
| 应用声音活动 | `IAudioMeterInformation` |
| 系统默认设备切换 | 🔴 `IPolicyConfig` |
| 按应用输出 / 输入路由 | 🔴 AudioPolicyConfig |

产品层一个“切音频设备”按钮，背后可能跨越多个完全不同的 Windows Audio 子系统。

## 8. 最低系统版本概览

按 Microsoft Learn 当前公开文档：

| 接口 | 最低客户端 |
|---|---|
| `IMMDeviceEnumerator` | Windows Vista |
| `IAudioClient` | Windows Vista |
| `ISimpleAudioVolume` | Windows Vista |
| `IAudioEndpointVolume` | Windows Vista |
| `IAudioSessionManager2` | Windows 7 |
| `IAudioSessionControl2` | Windows 7 |
| `IAudioClient3` | Windows 10 |

未公开 PolicyConfig / AudioPolicyConfig 不能用“最低支持版本”表达兼容保证，只能记录具体 Build 实测。

## 9. 官方资料

- Core Audio APIs  
  https://learn.microsoft.com/windows/win32/coreaudio/core-audio-apis-in-windows-vista
- Core Audio Interfaces  
  https://learn.microsoft.com/windows/win32/coreaudio/core-audio-interfaces
- WASAPI  
  https://learn.microsoft.com/windows/win32/coreaudio/wasapi
- Header Files and System Components  
  https://learn.microsoft.com/windows/win32/coreaudio/header-files-and-system-components
