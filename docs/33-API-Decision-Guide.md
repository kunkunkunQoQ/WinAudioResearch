# Windows Audio API 选择指南：我到底应该用哪个 API？

> 目标：从“我要做什么”反推 API，而不是从接口名开始。

---

## 1. 只是播放一个声音文件

### 很简单的系统提示音 / WAV

可用：

- PlaySound（legacy / simple）
- MediaPlayer
- AudioGraph

### 真正媒体文件播放

优先：

- MediaPlayer
- Media Foundation
- AudioGraph

如果是游戏音频：

- XAudio2

---

## 2. 播放 PCM / 自己生成音频

如果需要直接控制 buffer：

- WASAPI

如果想用 graph：

- AudioGraph

如果是 game voice engine：

- XAudio2

---

## 3. 录麦克风

现代高层：

- MediaCapture
- AudioGraph

低层：

- WASAPI capture

需要 raw / low latency / format control：

- WASAPI / IAudioClient2 / IAudioClient3

---

## 4. 录系统正在播放的声音

全 endpoint / system mix：

- WASAPI Loopback

只录一个应用 / process tree：

- Process Loopback Capture
- ActivateAudioInterfaceAsync
- AUDIOCLIENT_PROCESS_LOOPBACK_PARAMS

---

## 5. 做音量合成器

枚举 session：

- IAudioSessionManager2
- IAudioSessionEnumerator
- IAudioSessionControl2

应用音量：

- ISimpleAudioVolume

应用 peak：

- IAudioMeterInformation

设备总音量：

- IAudioEndpointVolume

---

## 6. 监听设备插拔 / 默认设备变化

传统 Core Audio：

- IMMNotificationClient

现代设备枚举：

- DeviceWatcher
- Windows.Devices.Enumeration

---

## 7. 找默认扬声器 / 麦克风

Core Audio：

- IMMDeviceEnumerator::GetDefaultAudioEndpoint

现代 WinRT：

- MediaDevice / DeviceInformation selectors

---

## 8. 设置系统默认设备

公开 MMDevice API：

> 没有和 GetDefaultAudioEndpoint 对称的稳定 setter。

桌面工具常见：

- 🔴 undocumented IPolicyConfig

必须理解兼容性风险。

---

## 9. 按应用选择输出 / 输入设备

普通 Audio Session API：

> 不提供稳定公开 setter。

常见实现：

- 🔴 Windows.Media.Internal.AudioPolicyConfig
- 🔴 IAudioPolicyConfigFactory

这属于 internal / undocumented 范围。

---

## 10. 做实时音频电平

设备整体：

- IAudioMeterInformation on endpoint

应用 / session：

- IAudioMeterInformation on session object

真正音频分析：

- loopback / capture PCM
- 自己算 RMS / FFT / LUFS

Peak meter 不等于完整 analyzer。

---

## 11. 做 EQ / DSP

### 只处理你自己的 stream

可选：

- AudioGraph effect
- XAudio2 XAPO
- 自己 WASAPI + DSP
- Media Foundation Transform

### 想作用到系统 endpoint

复杂度显著提高：

- APO
- virtual audio device
- driver integration
- 或 capture → process → render pipeline

---

## 12. 做虚拟扬声器 / 虚拟麦克风

普通 user-mode app 不足以创建真正 Windows endpoint。

研究：

- audio driver
- SysVAD
- WDM / WaveRT
- ACX

---

## 13. 做游戏声音引擎

优先看：

- XAudio2
- X3DAudio
- Spatial Audio

需要自己做 endpoint control：

- 再结合 WASAPI

---

## 14. 做 3D / Spatial Audio

Windows Sonic object model：

- ISpatialAudioClient
- ISpatialAudioObjectRenderStream

高层 graph：

- AudioGraph spatial features

游戏传统 matrix / HRTF：

- XAudio2 + X3DAudio / HRTF

---

## 15. 做音频文件解码 / 转码

Windows 原生：

- Media Foundation

跨平台库：

- FFmpeg
- libsndfile
- miniaudio 等

但这些第三方不是 Windows API。

---

## 16. 做 MIDI

新项目：

- Windows MIDI Services
- MIDI 2.0 / UMP

兼容旧设备 / 旧代码：

- WinMM MIDI
- Windows.Devices.Midi

---

## 17. 做低延迟

优先研究：

- IAudioClient3
- shared-mode low period
- event-driven WASAPI
- AudioGraph LowestLatency
- driver period

需要 bit-exact / 特殊格式再评估：

- exclusive mode

---

## 18. 做设备内部硬件拓扑分析

- DeviceTopology
- IDeviceTopology
- IConnector
- IPart

更底层：

- KS topology
- WDM / ACX driver docs

---

## 19. 一张选择图

```text
Need audio?
  │
  ├─ File / codec?
  │    └─ Media Foundation / MediaPlayer
  │
  ├─ Game playback?
  │    └─ XAudio2
  │
  ├─ Graph / C# routing?
  │    └─ AudioGraph
  │
  ├─ Raw PCM endpoint stream?
  │    └─ WASAPI
  │
  ├─ Mixer / per-app volume?
  │    └─ Audio Session API
  │
  ├─ Device master volume?
  │    └─ EndpointVolume
  │
  ├─ System / app capture?
  │    └─ WASAPI Loopback / Process Loopback
  │
  ├─ System-wide DSP?
  │    └─ APO / driver / virtual endpoint
  │
  ├─ Game 3D / object audio?
  │    └─ Spatial Audio / XAudio2
  │
  └─ MIDI?
       └─ Windows MIDI Services
```
