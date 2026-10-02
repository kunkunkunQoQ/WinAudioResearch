# Audio Glitch ETL 分析工作流：从“听到卡顿”到可定位证据

> 状态：🟢 Microsoft diagnostics tooling + engineering workflow

Glitch 问题最常见的无效报告：

> “声音偶尔爆一下。”

真正有价值的分析需要：

```text
repro timestamp
+
audio ETW
+
CPU scheduling
+
DPC/ISR
+
driver/APO state
```

---

## 1. 首选：Microsoft CollectAudioLogs

官方仓库：

https://github.com/microsoft/audio

采集：

```text
repro.etl
```

包含：

- Windows audio services
- audio drivers
- APO providers

并可附：

- MMDevice registry
- PnP state
- driver INF/version

---

## 2. 为什么只保留 30~60 秒

Microsoft Audio Team 说明：

Audio tracing 在 stream active 时产生大量 events。

CollectAudioLogs 是 circular trace。

所以：

> trace buffer 满后，新 event 会覆盖旧 event。

实际常见只保留：

```text
~30–60 sec
```

因此：

### Repro

问题发生后：

> 立即停止日志。

---

## 3. 不要开 TTD 来测 Glitch

Microsoft 明确提醒：

Time Travel Tracing：

- CPU intensive
- 会让 audio processing 变慢
- 自己可能制造 audible glitch

所以：

```text
Audio quality/glitch
→ normal ETW
```

而不是：

```text
TTD
```

---

## 4. WPA 第一轮看什么

### CPU Usage

关注：

- app audio thread
- audiodg.exe
- vendor process/service

### DPC / ISR

关注：

- network driver
- GPU driver
- storage
- USB
- audio driver

是否出现长时间执行。

### Thread Scheduling

检查：

- audio worker 是否没及时运行
- priority
- ready time
- preemption

### Power

检查：

- CPU frequency / core parking
- device power transition
- D-state

---

## 5. Audio-Specific Timeline

如果 ETL 中有 Windows Audio provider events：

把：

- stream start
- buffer processing
- glitch
- endpoint change
- format
- APO

和系统 timeline 对齐。

不要只看单个 event name。

---

## 6. DATA_DISCONTINUITY

如果 app 自己有 WASAPI capture diagnostics：

记录：

```text
AUDCLNT_BUFFERFLAGS_DATA_DISCONTINUITY
```

timestamp。

再到 ETL 中看同一时刻：

- scheduling
- DPC
- device reset

这样能把用户态 evidence 和系统 trace 对齐。

---

## 7. Device Invalidated

如果 glitch 同时出现：

```text
AUDCLNT_E_DEVICE_INVALIDATED
```

优先排查：

- hotplug
- driver restart
- Bluetooth profile change
- HDMI link
- format change

这不一定是“CPU 来不及”。

---

## 8. Power Transition

常见：

```text
idle
→ first audio
→ pop/drop
```

可能来自：

- endpoint D-state resume
- DSP wake
- USB selective suspend
- Bluetooth link transition

这时必须看 power timeline。

---

## 9. APO

如果 audiodg CPU spike：

检查：

- loaded APO
- effect state
- processing mode
- vendor DSP

APO realtime code如果：

- blocking
- allocates
- locks too long

可以直接破坏 audio deadline。

---

## 10. Driver DPC/ISR

HLK Troubleshooting Audio Testing 明确指出：

Zero-glitch test failure 应重点检查：

- improper driver thread priority
- long DPC / ISR
- improper hardware power management

所以：

> “DPC latency”不是社区玄学，它确实是 Windows 官方 audio glitch troubleshooting 的一部分。

---

## 11. Minimum Repro Record

```text
UTC/local time:
Windows Build:
Endpoint:
Driver:
Shared/Exclusive:
Format:
Period:
App PID:
audiodg PID:
Repro timestamp:
WASAPI HRESULT:
Discontinuity count:
ETL:
```

---

## 12. Comparison Run

至少录：

### Good trace

没有 glitch。

### Bad trace

出现 glitch。

对比：

- DPC
- CPU
- APO
- endpoint
- buffer events

通常比只看 bad trace 更容易发现异常。

---

## 13. ETL 大小

不要为了“更多数据”无限增大 circular buffer。

Audio ETW 事件量高。

更好的方法：

- 缩短 reproduction
- stop quickly
- 只开必要 providers
- 多跑几次

---

## 14. Feedback Hub

Microsoft CollectAudioLogs 的日志与 Feedback Hub：

```text
Devices and Drivers → Audio and Sound → Recreate my problem
```

大体同类。

对 OS bug：

> Feedback Hub + local diagnostics copy

是官方上报渠道之一。

---

## 15. 官方资料

- Microsoft Audio Team CollectAudioLogs  
  https://github.com/microsoft/audio

- Troubleshooting Audio Testing  
  https://learn.microsoft.com/windows-hardware/test/hlk/testref/troubleshooting-audio-testing

- Windows Performance Analyzer  
  https://learn.microsoft.com/windows-hardware/test/wpt/windows-performance-analyzer

- ETW  
  https://learn.microsoft.com/windows-hardware/test/wpt/event-tracing-for-windows
