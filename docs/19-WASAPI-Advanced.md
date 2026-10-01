# WASAPI 深入：从 IAudioClient 到低延迟、Event Driven 与 Exclusive Mode

> 状态：🟢 Public API

WASAPI 是 Windows 最底层、最常用的用户态音频流 API 之一。

它负责应用和 audio endpoint 之间的实际 PCM 数据流。

---

## 1. 核心对象

```text
IMMDevice
  ↓ Activate
IAudioClient
  ↓ Initialize
  ↓ GetService
  ├─ IAudioRenderClient
  ├─ IAudioCaptureClient
  ├─ IAudioClock
  ├─ IAudioStreamVolume
  └─ other services
```

---

## 2. Shared Mode

共享模式中：

```text
App A ─┐
App B ─┼─→ Windows Audio Engine → Endpoint
App C ─┘
```

Audio Engine 可以负责：

- mixing
- format conversion
- volume
- APO / effects
- endpoint processing

普通桌面应用通常应该优先 shared mode。

---

## 3. Exclusive Mode

Exclusive mode：

```text
Application
   ↓
exclusive stream
   ↓
endpoint
```

优点：

- 更直接的设备格式控制
- 可用于 bit-exact / 特定 sample rate
- 某些专业音频场景

缺点：

- 其他应用可能无法播放
- 用户可在设备设置中禁用 exclusive access
- 格式协商更严格
- buffer / period 要求更严格

Microsoft 当前文档建议：Windows 10+ 应先评估 `IAudioClient3` 的低周期 shared mode；只有确实需要 bit-exact 或自定义硬件格式时再考虑 exclusive mode。

---

## 4. Event Driven vs Timer Driven

### Timer-driven

客户端按时间间隔轮询 / 唤醒：

```text
sleep / timer
→ GetCurrentPadding
→ write/read buffer
```

### Event-driven

设置：

```text
AUDCLNT_STREAMFLAGS_EVENTCALLBACK
```

再通过 `SetEventHandle` 注册事件。

Audio Engine 在需要客户端处理 buffer 时 signal event。

通常事件驱动更适合低延迟和稳定调度。

---

## 5. GetCurrentPadding

Render 流中：

```text
availableFrames = bufferSize - currentPadding
```

不要假设每次都可以写满整个 buffer。

Capture 则通过 `IAudioCaptureClient::GetNextPacketSize` / `GetBuffer` 读取可用 packet。

---

## 6. GetMixFormat

`IAudioClient::GetMixFormat` 返回 shared-mode Audio Engine 使用的 mix format。

注意：

- 它不等于硬件“唯一原生格式”
- exclusive mode 仍应使用 `IsFormatSupported`
- shared mode 下系统可能自动转换客户端格式

---

## 7. IsFormatSupported

用途：

```text
IAudioClient.IsFormatSupported
```

用于确认：

- shared / exclusive
- sample rate
- bit depth
- channel count
- channel mask

是否支持。

不要仅凭 Windows Sound 设置里显示的格式推断 API 一定能 Initialize。

---

## 8. IAudioClient2

`IAudioClient2` 在 IAudioClient 基础上增加：

- client properties
- hardware offload 查询
- buffer size limit

`AudioClientProperties` 可以设置 stream category 和 options。

---

## 9. IAudioClient3

Windows 10 增加 `IAudioClient3`。

它允许：

```text
GetSharedModeEnginePeriod
GetCurrentSharedModeEnginePeriod
InitializeSharedAudioStream
```

目标是让 shared mode 也可以使用更小的 engine period。

典型逻辑：

```text
GetSharedModeEnginePeriod(format)
     ↓
min / max / default / fundamental
     ↓
choose legal period
     ↓
InitializeSharedAudioStream
```

Period 必须：

- >= min
- <= max
- 是 fundamental period 的整数倍

---

## 10. Stream Flags

常见：

### EVENTCALLBACK

事件驱动 buffer。

### LOOPBACK

从 render endpoint 捕获系统混音。

仅 shared mode。

### NOPERSIST

不持久化 session volume 等状态。

### CROSSPROCESS

跨进程 session。

### RATEADJUST

允许通过 `IAudioClockAdjustment` 调整 sample rate。

---

## 11. AUDCLNT_STREAMOPTIONS

Windows 新版还提供：

- RAW
- MATCH_FORMAT
- AMBISONICS
- POST_VOLUME_LOOPBACK

### RAW

请求尽量绕过信号处理。

但“RAW”并不意味着可以绕过所有 endpoint-specific / always-on 处理。

### MATCH_FORMAT

请求 engine 尽量采用客户端提出的格式。

### POST_VOLUME_LOOPBACK

loopback 在应用 volume / mute 后采样，而默认 loopback tap 通常在 volume / mute 前。

---

## 12. IAudioClock

`IAudioClock` 可用于：

- stream position
- frequency / timing
- A/V sync
- glitch / latency analysis

低延迟音频程序不要只靠 `DateTime` 或普通 wall clock 推断 audio position。

---

## 13. 常见错误

- `AUDCLNT_E_DEVICE_INVALIDATED`
- `AUDCLNT_E_UNSUPPORTED_FORMAT`
- `AUDCLNT_E_EXCLUSIVE_MODE_NOT_ALLOWED`
- `AUDCLNT_E_DEVICE_IN_USE`
- `AUDCLNT_E_BUFFER_SIZE_NOT_ALIGNED`
- `AUDCLNT_E_SERVICE_NOT_RUNNING`

研究时应保留原始 HRESULT。

---

## 14. 官方入口

- WASAPI  
  https://learn.microsoft.com/windows/win32/coreaudio/wasapi
- audioclient.h  
  https://learn.microsoft.com/windows/win32/api/audioclient/
- IAudioClient3  
  https://learn.microsoft.com/windows/win32/api/audioclient/nn-audioclient-iaudioclient3
- Exclusive Mode  
  https://learn.microsoft.com/windows/win32/coreaudio/exclusive-mode-streams
- Low Latency Audio  
  https://learn.microsoft.com/windows-hardware/drivers/audio/low-latency-audio
