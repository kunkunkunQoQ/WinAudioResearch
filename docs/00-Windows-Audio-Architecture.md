# Windows Audio 架构与接口地图

> 状态：🟢 Public API + ✅ SonicRoute Verified

Windows Core Audio 不是单一 API，而是一组围绕“设备、会话、音频流”组织的 COM 接口。

## 1. 三个最重要的层次

### Endpoint：设备层

耳机、音箱、麦克风等最终都以 audio endpoint 的形式暴露。

入口通常是：

```text
MMDeviceEnumerator
    ↓
IMMDeviceEnumerator
    ↓
IMMDevice
```

`IMMDevice` 是很多后续接口的入口。通过 `IMMDevice::Activate` 可以取得：

- `IAudioClient`
- `IAudioSessionManager2`
- `IAudioEndpointVolume`
- `IAudioMeterInformation`

### Session：会话层

Windows 会把共享模式音频流组织进 audio session。

```text
IMMDevice
   ↓ Activate
IAudioSessionManager2
   ↓
IAudioSessionEnumerator
   ↓
IAudioSessionControl2
   ├─ PID
   ├─ State
   ├─ SessionIdentifier
   ├─ GroupingParam
   ├─ ISimpleAudioVolume
   └─ IAudioMeterInformation
```

需要特别注意：**一个进程不一定只有一个 session**。以 PID 聚合多个 session 是应用层策略，不是 Core Audio 对“一进程一会话”的保证。

### Stream：数据流层

WASAPI 负责应用和 audio engine / endpoint 之间的数据流。

```text
IMMDevice
   ↓ Activate
IAudioClient
   ↓ Initialize
IAudioRenderClient / IAudioCaptureClient / ...
```

## 2. API 家族

| API | 主要用途 |
|---|---|
| MMDevice API | 枚举 endpoint、默认设备、设备属性、设备事件 |
| Audio Session API | 枚举/管理 session、会话音量、session 事件 |
| EndpointVolume API | 设备主音量、静音、峰值 |
| WASAPI | 真正的 render / capture 数据流 |
| DeviceTopology | 设备硬件拓扑 |
| Policy / internal audio config | Windows 内部策略；部分按应用路由能力位于这里 |

## 3. SonicRoute 为什么同时需要多个层

SonicRoute 的功能并不是由某一个 API 完成：

- 找设备：MMDevice
- 找应用音频：Audio Session
- 应用音量：ISimpleAudioVolume
- 麦克风全局静音：IAudioEndpointVolume
- 应用实时声音活动：IAudioMeterInformation
- 按应用选择输出/输入：Windows 内部 AudioPolicyConfig

最后一项不是普通 WASAPI 功能，也不是 `IAudioSessionManager2` 的一部分。

## 4. 官方资料

- Core Audio APIs: https://learn.microsoft.com/windows/win32/coreaudio/core-audio-apis-in-windows-vista
- Core Audio Interfaces: https://learn.microsoft.com/windows/win32/coreaudio/core-audio-interfaces
- Header files and components: https://learn.microsoft.com/windows/win32/coreaudio/header-files-and-system-components
- WASAPI: https://learn.microsoft.com/windows/win32/coreaudio/wasapi
