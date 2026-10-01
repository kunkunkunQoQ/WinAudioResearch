# Low Latency、RAW、Offload：Windows 音频性能路径

> 状态：🟢 Public API / Driver Documentation

“低延迟”不是一个开关。

Windows 中影响 latency 的因素包括：

- API
- buffer / period
- shared / exclusive
- driver
- hardware
- processing mode
- APO
- scheduler
- power management
- offload

---

## 1. 先区分三件事

### Low latency

更短的 input/output buffer 周期。

### RAW

减少可选 signal processing。

### Hardware offload

让某些音频处理 / mixing / decode 路径由 hardware audio engine 承担。

三者不等价。

---

## 2. IAudioClient3 低周期 Shared Mode

Windows 10 起：

```text
IAudioClient3
```

允许查询 Audio Engine 支持的 period：

- minimum
- maximum
- default
- fundamental

然后：

```text
InitializeSharedAudioStream
```

请求更短 shared-mode period。

这可以在保留系统 mixing 的同时得到接近 exclusive mode 的 latency。

---

## 3. AudioGraph Low Latency

AudioGraph 提供：

```text
QuantumSizeSelectionMode
```

包括：

- SystemDefault
- LowestLatency
- ClosestToDesired

因此 C# / WinRT 应用也能用更高层 API 构建低延迟 graph。

---

## 4. Exclusive Mode

Exclusive mode 仍有价值：

- bit-exact
- 非 engine format
- 特定专业音频流程

但成本：

- endpoint 被独占
- 其他程序静音 / 无法打开
- 用户可以禁用 exclusive mode
- format / buffer 要求更严格

---

## 5. RAW Stream

`AUDCLNT_STREAMOPTIONS_RAW`：

目标是绕过大多数 signal processing。

适合：

- measurement
- custom DSP
- speech / ML preprocessing
- 音频测试

但 RAW 不保证：

> “数据绝对未经任何硬件或 endpoint-specific 处理”。

驱动 / hardware 的 always-on 行为仍需设备侧文档和实测确认。

---

## 6. Signal Processing Modes

Windows 10+ 定义：

- Raw
- Default
- Media
- Movie
- Speech
- Communications
- Notification

应用通过 audio category / properties 表达场景。

驱动通过 mode-aware APO / topology 提供相应 processing。

---

## 7. Hardware Offload

硬件 offload 允许 audio stream 在 hardware audio engine 中处理。

驱动需要暴露：

- host process pin
- loopback pin
- offload pins
- KSNODETYPE_AUDIO_ENGINE

用途通常包括：

- 降低 CPU
- 低功耗 playback
- 专用 DSP
- hardware mixing

---

## 8. Loopback 与 Offload

如果音频最终在 hardware engine 处理，driver 仍需正确暴露 loopback path。

官方驱动文档专门规定了：

- loopback pin
- host pin
- offload pin
- hardware EFX 前后的 tap 关系

因此做系统录音 / loopback 测试时，hardware offload 也可能影响观察到的路径。

---

## 9. Latency 测量

不要只测：

```text
API call duration
```

更有意义：

- render period
- capture period
- round-trip latency
- scheduling jitter
- glitch count
- actual hardware latency
- resampler / DSP delay

---

## 10. MMCSS

专业低延迟音频线程常需要合适的 realtime scheduling / MMCSS 策略。

不过不要简单把线程设成最高优先级就认为“更专业”。

错误 priority / busy loop 反而可能：

- 抢占系统
- 造成 UI 卡顿
- 造成其他 audio thread glitch

---

## 11. 官方资料

- Low Latency Audio  
  https://learn.microsoft.com/windows-hardware/drivers/audio/low-latency-audio

- IAudioClient3  
  https://learn.microsoft.com/windows/win32/api/audioclient/nn-audioclient-iaudioclient3

- Exclusive-Mode Streams  
  https://learn.microsoft.com/windows/win32/coreaudio/exclusive-mode-streams

- AUDCLNT_STREAMOPTIONS  
  https://learn.microsoft.com/windows/win32/api/audioclient/ne-audioclient-audclnt_streamoptions

- Audio Signal Processing Modes  
  https://learn.microsoft.com/windows-hardware/drivers/audio/audio-signal-processing-modes

- Hardware-Offloaded Audio Processing  
  https://learn.microsoft.com/windows-hardware/drivers/audio/hardware-offloaded-audio-processing
