# WASAPI Buffer Flags、Discontinuity、Silence 与 Timestamp Error

> 状态：🟢 Public API

低层 capture / render 代码不能只处理：

```text
byte* data
numberOfFrames
```

WASAPI buffer 还带有状态 flags。

---

## 1. AUDCLNT_BUFFERFLAGS

核心：

```text
AUDCLNT_BUFFERFLAGS_DATA_DISCONTINUITY
AUDCLNT_BUFFERFLAGS_SILENT
AUDCLNT_BUFFERFLAGS_TIMESTAMP_ERROR
```

---

## 2. DATA_DISCONTINUITY

表示：

> 当前 packet 和前一个 packet 的 device position 不连续。

可能原因：

- stream state transition
- timing glitch
- capture missed data
- system scheduling delay

音频 recorder / analyzer 应：

- 记录 glitch
- 维护 timeline
- 必要时插入 silence / discontinuity marker

不要假装 packet 永远无缝连续。

---

## 3. SILENT

表示：

> 这个 packet 应被当成 silence。

实际 data pointer 中的内容不应被当作有效音频。

Capture client 在收到 SILENT flag 时，可以：

- 生成 zero PCM
- 保持时间线继续前进

---

## 4. TIMESTAMP_ERROR

表示：

> device stream position 的 timestamp 不可靠。

如果你的程序依赖：

- A/V sync
- long-term clock correlation
- multi-device sync

必须记录并处理。

---

## 5. Capture Timeline

理想 recorder 不应只：

```text
append each buffer
```

还应跟踪：

- device position
- QPC timestamp
- frame count
- discontinuity
- timestamp error

---

## 6. Render ReleaseBuffer

Render side 的 `ReleaseBuffer` 也可用：

```text
AUDCLNT_BUFFERFLAGS_SILENT
```

告诉 Audio Engine：

> 这段 buffer 是 silence，不需要客户端真的填 0。

---

## 7. Glitch != 一定是 Driver Bug

DATA_DISCONTINUITY 可能来自：

- client missed deadline
- CPU overload
- thread starvation
- DPC/ISR
- device reset
- power transition
- buffer 太小

因此应结合：

- ETW
- WPA
- app timing
- driver

分析。

---

## 8. 统计指标

建议实时程序记录：

```text
TotalFrames
Packets
DataDiscontinuities
TimestampErrors
SilentPackets
MaxCallbackDelay
AverageCallbackInterval
DeviceInvalidations
```

这比“我听起来偶尔卡”更可比较。

---

## 9. 与 Audio Clock

`IAudioClock` 可以提供 stream/device position。

结合 packet timestamp 可以：

- 估算 drift
- 监测 discontinuity
- 做 A/V sync

---

## 10. 官方资料

- AUDCLNT_BUFFERFLAGS  
  https://learn.microsoft.com/windows/win32/api/audioclient/ne-audioclient-_audclnt_bufferflags

- IAudioCaptureClient::GetBuffer  
  https://learn.microsoft.com/windows/win32/api/audioclient/nf-audioclient-iaudiocaptureclient-getbuffer

- IAudioRenderClient::ReleaseBuffer  
  https://learn.microsoft.com/windows/win32/api/audioclient/nf-audioclient-iaudiorenderclient-releasebuffer
