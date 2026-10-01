# Realtime Audio Threading、MMCSS 与 Buffer Deadline

> 状态：🟢 Public Windows scheduling / Core Audio documentation

音频程序最容易犯的性能错误之一是：

> “CPU 平均占用不高，所以实时线程一定没问题。”

实时音频真正关心的是：

> 每一个 buffer deadline 是否按时完成。

## 1. Buffer Deadline

假设 period：

```text
3 ms
```

那么 audio thread 每几毫秒就必须：

- wake
- read/write buffer
- finish processing
- return

即使平均 CPU 只有 5%，某一次：

- GC
- lock
- page fault
- DPC
- disk I/O

卡住 10ms，也可能产生 audible glitch。

## 2. MMCSS

Windows 提供：

```text
Multimedia Class Scheduler Service
```

它让 time-sensitive multimedia thread 获得较高 CPU scheduling priority，同时避免完全饿死低优先级任务。

## 3. 常见 MMCSS Task

Windows 默认包含：

- Audio
- Capture
- Distribution
- Games
- Playback
- Pro Audio
- Window Manager

专业低延迟线程常见：

```text
Pro Audio
```

## 4. AvSetMmThreadCharacteristics

线程可以注册：

```text
AvSetMmThreadCharacteristics
```

停止工作后：

```text
AvRevertMmThreadCharacteristics
```

不要把 multimedia priority 永久留在线程上。

## 5. Pro Audio

Microsoft exclusive-mode example 使用：

```text
TaskName = "Pro Audio"
```

来保证最小 device period 下的 buffer servicing 更可靠。

但文档同样强调：

> 如果实际场景允许，应放宽 period / priority，而不是无脑使用最高 realtime priority。

## 6. Audio / ProAudio Work Queue

Microsoft Windows 10 low-latency 文档还推荐：

- Real-Time Work Queue API
- Media Foundation work queue

把工作标记成：

- Audio
- ProAudio

让 Windows 更合理地协调 realtime audio work。

## 7. AudioGraph

AudioGraph 的 threading / quantum scheduling 更多由 Windows 自动管理。

所以 Microsoft low-latency guidance 中：

> 新应用尽量优先 AudioGraph；只有需要更低层控制或更低 latency 时再直接使用 WASAPI。

## 8. Realtime Callback 不应该做什么

尽量避免：

- lock 竞争
- async wait
- network
- disk
- console output
- UI update
- large allocation
- GC pressure
- COM enumeration
- device enumeration
- process enumeration

正确模式：

```text
control thread
→ prepare state

audio realtime thread
→ read immutable/preallocated state
→ process buffer
→ return

UI / logging thread
← lock-free/minimal event
```

## 9. C# 特别注意

C# realtime processing 不是不能做，但要注意：

- allocation
- boxing
- LINQ
- string formatting
- closures
- event churn
- GC
- array copy

SonicRoute 的 meter 线程不是 PCM realtime audio callback，所以要求没这么极端；如果未来写真正 DSP / capture-render pipeline，标准会高很多。

## 10. Timer 不是 Audio Clock

不要使用：

- DispatcherTimer
- System.Threading.Timer

推断精准 PCM position。

真正 stream timing 应使用：

- IAudioClock
- audio packet timestamp
- QPC correlation

timer 更适合 UI / housekeeping。

## 11. Multimedia Timer

旧：

```text
timeSetEvent
```

一类 multimedia timer 已被 Microsoft 标成 legacy。

现代实时音频更应研究：

- event-driven WASAPI
- MMCSS
- waitable events
- work queue

## 12. 官方资料

- Multimedia Class Scheduler Service  
  https://learn.microsoft.com/windows/win32/procthread/multimedia-class-scheduler-service

- Exclusive-Mode Streams  
  https://learn.microsoft.com/windows/win32/coreaudio/exclusive-mode-streams

- Low Latency Audio  
  https://learn.microsoft.com/windows-hardware/drivers/audio/low-latency-audio

- User-Mode Audio Components  
  https://learn.microsoft.com/windows/win32/coreaudio/user-mode-audio-components
