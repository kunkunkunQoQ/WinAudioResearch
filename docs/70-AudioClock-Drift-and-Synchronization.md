# AudioClock、Device Position、Drift 与多设备同步

> 状态：🟢 Public API + engineering concepts

音频实时系统最容易低估的东西之一：

> 不同 audio device 有不同硬件时钟。

两个都标称 48 kHz 的设备，不代表实际 sample clock 完全一样。

---

## 1. IAudioClock

通过：

```text
IAudioClient::GetService(IID_IAudioClock)
```

获得。

主要：

- `GetFrequency`
- `GetPosition`
- `GetCharacteristics`

可以知道 stream/device timing。

---

## 2. Position

`GetPosition` 返回：

- device position
- correlated QPC time

这比：

```text
DateTime.Now
```

更适合音频 stream timing。

---

## 3. IAudioClock2

`IAudioClock2`：

> 提供当前 device position。

用于更明确的 device position 查询。

---

## 4. IAudioClockAdjustment

接口：

```text
IAudioClockAdjustment
```

允许 client 调整 stream sample rate。

通常和：

```text
AUDCLNT_STREAMFLAGS_RATEADJUST
```

配合。

---

## 5. 为什么两个设备会 Drift

设备 A：

```text
实际 48000.8 Hz
```

设备 B：

```text
实际 47999.2 Hz
```

短时间听不出来。

长时间：

- buffer 越积越多
- 或越来越空
- 最终 underrun / overrun

所以多设备同步必须处理 drift。

---

## 6. Capture → Render 到不同设备

例如：

```text
USB Mic
   ↓
DSP
   ↓
HDMI Speaker
```

两边 hardware clock 不同。

不能简单：

```text
每 capture 480 frame
就 render 480 frame
永远不调整
```

长期会 drift。

需要：

- buffer occupancy control
- resampling ratio adjustment
- clock correlation

---

## 7. AEC 更敏感

AEC 需要：

- capture timestamp
- render reference timestamp
- delay estimate

如果 reference 与 microphone 时钟不同：

还要处理：

- drift
- latency change
- Bluetooth variable delay

所以 Windows 11 AEC APO framework 提供 reference stream timestamp 是非常重要的。

---

## 8. A/V Sync

视频 playback 要把：

- audio clock
- presentation clock
- video timestamps

同步。

Media Foundation 有自己的 presentation clock model。

不要只用 UI timer 去同步音视频。

---

## 9. Timestamp Error

WASAPI capture packet 可能带：

```text
AUDCLNT_BUFFERFLAGS_TIMESTAMP_ERROR
```

这时当前 packet device timestamp 不可靠。

同步算法要：

- 标记
- 平滑
- 不直接当精确 anchor

---

## 10. QPC

Windows high-resolution timing：

```text
QueryPerformanceCounter
```

常用于把音频 device position 映射到系统 monotonic time。

但真正音频位置仍应优先来自 audio clock / packet timestamp。

---

## 11. 多设备同步策略

常见：

### Master Clock

选择一个 endpoint 为 master。

### Adaptive Resampling

另一个 stream 根据：

```text
buffer fill / clock drift
```

微调 resample ratio。

### Drop / Insert

简单方案偶尔：

- drop frame
- insert silence

但听感通常差于连续 drift compensation。

---

## 12. 官方资料

- IAudioClock  
  https://learn.microsoft.com/windows/win32/api/audioclient/nn-audioclient-iaudioclock

- IAudioClock2  
  https://learn.microsoft.com/windows/win32/api/audioclient/nn-audioclient-iaudioclock2

- IAudioClockAdjustment  
  https://learn.microsoft.com/windows/win32/api/audioclient/nn-audioclient-iaudioclockadjustment
