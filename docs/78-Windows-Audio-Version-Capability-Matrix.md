# Windows Audio Version / Capability Matrix

> 状态：🟢 Public API + 🔴 internal API notes separated

这是一张开发导航表。具体最低 Build 应以对应 Microsoft interface page 为最终依据。

## 时代概览

### Windows Vista

- MMDevice
- WASAPI / IAudioClient
- IAudioRenderClient / IAudioCaptureClient
- EndpointVolume
- DeviceTopology
- Peak Meter
- WaveRT

### Windows 7

- IAudioSessionManager2
- IAudioSessionControl2
- session notification
- ducking
- IKsJackDescription2

### Windows 8 / 8.1

- IAudioClient2
- AudioClientProperties
- hardware offload APIs
- ActivateAudioInterfaceAsync
- modern stream categories

### Windows 10

- IAudioClient3
- low-period shared mode
- AudioGraph
- Spatial Audio (1703)
- inbox USB Audio 2.0 driver (1703)
- improved event-driven loopback

### Build 19043

- IAudioStateMonitor

### Build 20348

- Process Loopback activation params
- IAudioClientDuckingControl

### Windows 11 Build 22000

- IAudioEffectsManager
- IAudioSystemEffectsPropertyStore
- Windows 11 APO CAPX frameworks

### Windows 11 Build 22621

- IAcousticEchoCancellationControl
- IAudioViewManagerService
- modern LE Audio platform generation

### Windows 11 24H2

- Deep Noise Suppression public effect identity
- Media Foundation services for AEC/effects
- continuing Bluetooth / LE Audio improvements

## 快速矩阵

| 能力 | 最低大致版本 |
|---|---|
| MMDevice / WASAPI | Vista |
| EndpointVolume / DeviceTopology | Vista |
| AudioSessionManager2 | Windows 7 |
| IAudioClient2 | Windows 8 |
| ActivateAudioInterfaceAsync | Windows 8 |
| IAudioClient3 | Windows 10 |
| Spatial Audio Objects | Windows 10 1703 |
| USB Audio 2.0 inbox driver | Windows 10 1703 |
| IAudioStateMonitor | Build 19043 |
| Process Loopback | Build 20348 |
| IAudioClientDuckingControl | Build 20348 |
| IAudioEffectsManager | Build 22000 |
| IAudioSystemEffectsPropertyStore | Build 22000 |
| IAcousticEchoCancellationControl | Build 22621 |
| IAudioViewManagerService | Build 22621 |
| Deep Noise Suppression effect ID | Windows 11 24H2 |

## Undocumented 不进入 Public Compatibility Matrix

例如：

- `IPolicyConfig`
- `Windows.Media.Internal.AudioPolicyConfig`
- internal routing IID

只能写：

```text
Observed / verified on Build X
```

不能写成 Microsoft 官方“Supported since Windows X”。

## Build 比“Win10 / Win11”更重要

Windows 11 的 22000、22621 与 24H2 已经有不同公开 API。推荐使用：

- API availability
- build check
- graceful fallback

而不是仅判断“Windows 11”。

## 相关文档

- [Windows Compatibility](10-Windows-Version-Compatibility.md)
- [Modern Core Audio Timeline](67-Modern-Core-Audio-API-Timeline.md)
- [Research Validation Checklist](16-Research-Validation-Checklist.md)
