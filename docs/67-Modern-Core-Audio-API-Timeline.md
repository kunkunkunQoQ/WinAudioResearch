# Modern Core Audio API Timeline：旧教程之后 Windows 又加了什么？

> 状态：🟢 Public API  
> 目标：帮助开发者区分 Vista-era Core Audio 与 Windows 10/11 新增接口。

网上大量 Core Audio 教程仍停留在：

```text
Windows Vista / 7 era
```

但现代 Windows 已加入不少新的公开接口。

---

## Windows Vista

Core Audio 基础建立：

- MMDevice
- WASAPI / IAudioClient
- IAudioRenderClient
- IAudioCaptureClient
- IAudioClock
- EndpointVolume
- DeviceTopology
- ISimpleAudioVolume

这也是大量“经典教程”的基础。

---

## Windows 7

Audio Session 能力扩展：

- `IAudioSessionManager2`
- `IAudioSessionControl2`
- session notification
- ducking
- communications scenarios

---

## Windows 8

### IAudioClient2

增加：

- AudioClientProperties
- hardware offload capability
- buffer size limits

### ActivateAudioInterfaceAsync

提供现代 async activation 路径，尤其适合：

- UWP
- DeviceInformation
- WinRT audio device selection

---

## Windows 10

### IAudioClient3

增加 shared-mode engine period 控制：

- GetSharedModeEnginePeriod
- GetCurrentSharedModeEnginePeriod
- InitializeSharedAudioStream

目标：

> 在 shared mode 下获得更低 latency。

### Spatial Audio

Windows 10 1703 起：

- ISpatialAudioClient
- ISpatialAudioObject
- object render stream

成为 Windows Sonic 的公开 object audio API。

---

## Windows 10 Build 19043

### IAudioStateMonitor

公开：

- render/capture sound state
- category filter
- device ID filter
- role filter
- callback

Header：

```text
audiostatemonitorapi.h
```

它是一套很多旧 Core Audio wrapper 甚至没有覆盖的接口。

---

## Windows 10 Build 20348

### Process Loopback Activation

```text
AUDIOCLIENT_ACTIVATION_PARAMS
AUDIOCLIENT_PROCESS_LOOPBACK_PARAMS
```

允许：

- include PID tree
- exclude PID tree

做 per-process render capture。

### IAudioClientDuckingControl

最低：

```text
Windows 10 Build 20348
```

应用可对当前 render stream 设置：

> 当这个 stream 活跃时，不要由它触发系统去 duck 其他 stream。

获取：

```text
IAudioClient::GetService
```

注意：

> 它只控制“这个 stream 是否触发 ducking”，不会阻止其他 communications stream 造成 ducking。

---

## Windows 11 Build 22000

### IAudioEffectsManager

公开管理当前 stream effect pipeline：

- enumerate effects
- query state
- set state if allowed
- change notification

### IAudioSystemEffectsPropertyStore

面向：

- OEM
- HSA
- audio device configuration

支持：

- default store
- user store
- volatile store
- property notifications

需要 restricted:

```text
audioDeviceConfiguration
```

### Windows 11 APO CAPX

新增更标准化：

- settings
- notifications
- logging
- threading
- effect discovery/control

---

## Windows 11 Build 22621

### IAcousticEchoCancellationControl

允许 capture stream 指定：

```text
AEC reference render endpoint
```

获取：

```text
IAudioClient::GetService
```

### IAudioViewManagerService

允许把：

```text
HWND
```

关联到：

```text
audio stream
```

接口：

```text
IAudioViewManagerService::SetAudioStreamWindow
```

最低：

```text
Windows Build 22621
```

这也是一个很多旧 wrapper 未覆盖的现代接口。

---

## Windows 11 24H2

Media Foundation service integration 增加：

- `MF_ACOUSTIC_ECHO_CANCELLATION_CONTROL_SERVICE`
- `MF_AUDIO_EFFECTS_MANAGER_SERVICE`

使：

- AEC control
- effect manager

进入更多 Media Foundation source / service 场景。

---

## 这对 Wrapper 开发的意义

如果一个 wrapper 只声明：

- IAudioClient
- IAudioSessionManager2
- EndpointVolume

它可能对传统 mixer 足够。

但如果目标是：

> “完整 Windows Audio SDK wrapper”

现代 Windows 还应考虑：

- IAudioClient2
- IAudioClient3
- AudioStateMonitor
- Process Loopback
- IAudioClientDuckingControl
- IAudioEffectsManager
- IAcousticEchoCancellationControl
- IAudioViewManagerService
- IAudioSystemEffectsPropertyStore
- Spatial Audio Client 2

---

## 不要用 OS 名字代替 Build Check

更稳妥：

```text
API minimum build
+
runtime availability
```

而不是：

```text
if Windows11 then assume all APIs
```

因为 Windows 11 自身不同 Build 的公开接口也不同。

---

## 版本速查

| API | 最低系统 |
|---|---|
| IAudioClient | Vista |
| IAudioSessionManager2 | Windows 7 |
| IAudioClient2 | Windows 8 |
| IAudioClient3 | Windows 10 |
| Spatial Audio Objects | Windows 10 1703 |
| IAudioStateMonitor | Build 19043 |
| Process Loopback params | Build 20348 |
| IAudioClientDuckingControl | Build 20348 |
| IAudioEffectsManager | Build 22000 |
| IAudioSystemEffectsPropertyStore | Build 22000 |
| IAcousticEchoCancellationControl | Build 22621 |
| IAudioViewManagerService | Build 22621 |

---

## 官方入口

- audioclient.h  
  https://learn.microsoft.com/windows/win32/api/audioclient/

- mmdeviceapi.h  
  https://learn.microsoft.com/windows/win32/api/mmdeviceapi/

- Audio State Monitor  
  https://learn.microsoft.com/windows/win32/api/audiostatemonitorapi/

- Audio Client Activation Params  
  https://learn.microsoft.com/windows/win32/api/audioclientactivationparams/

- Spatial Audio  
  https://learn.microsoft.com/windows/win32/api/spatialaudioclient/
