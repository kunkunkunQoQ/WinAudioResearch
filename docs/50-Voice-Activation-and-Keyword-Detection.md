# Voice Activation、Keyword Detection 与 Wake-on-Voice

> 状态：🟢 Public driver architecture / historical platform docs

Windows audio driver stack 还支持一个普通音频播放器很少碰到的领域：

> 低功耗、持续监听、keyword detection。

这通常用于：

- voice assistant
- wake-on-voice
- hardware keyword spotter
- DSP always-listening

## 1. KWS

KWS：

```text
Keyword Spotter
```

检测：

- activation phrase
- predefined keyword
- wake word

可以是：

- software KWS
- hardware-offloaded KWS

## 2. Wake-on-Voice

如果 keyword detector 能在低功耗状态工作并唤醒系统：

```text
Wake-on-Voice
```

这是 Modern Standby / always-listening device 的重要场景。

## 3. Hardware Keyword Spotter

硬件方案常见：

```text
Microphones
   ↓
DSP / KWS hardware
   ↓
small circular buffer
   ↓
keyword detected
   ↓
interrupt / event
   ↓
Windows
```

CPU 不需要一直高频处理 microphone data。

## 4. Burst Buffer

硬件应保存 keyword 前后的 PCM。

原因：

> keyword 被检测到时，真正触发 detection 的语音已经发生了一段时间。

所以系统需要：

- pre-roll
- keyword start/end timestamp
- buffered capture burst

## 5. Sound Detector KS Properties

Windows 文档定义过：

- KSPROPERTY_SOUNDDETECTOR_PATTERNS
- KSPROPERTY_SOUNDDETECTOR_SUPPORTEDPATTERNS
- KSPROPERTY_SOUNDDETECTOR_ARMED
- KSPROPERTY_SOUNDDETECTOR_MATCHRESULT
- KSEVENT / notification

用于 driver 与 OS 之间配置 detector。

## 6. OEM Adapter

历史 Voice Activation model 还涉及：

- Keyword Detector OEM Adapter
- COM interface
- driver opaque model data translation

新 Multiple Voice Assistant architecture 进一步支持多个 assistant / pattern。

## 7. WaveRT Enhancement

Voice Activation 不是单独一套完全脱离 audio driver 的 API。

它和：

- WaveRT
- burst capture
- accurate timestamps
- KWS pin

紧密相关。

## 8. Timestamp

driver / DSP 需要把：

```text
DSP clock
```

映射到：

```text
Windows performance counter
```

这样系统才能知道：

> keyword 对应的 PCM 实际是何时采集的。

不能简单用：

> “数据送到 Windows 的时间”

代替真实 capture time。

## 9. SYSVAD

Microsoft SYSVAD sample 包含 voice activation / keyword detector 相关参考实现。

https://github.com/microsoft/Windows-driver-samples/tree/main/audio/sysvad

## 10. 现代意义

虽然部分 Cortana 文档具有明显历史背景，但底层主题仍值得研究：

- hardware KWS
- low-power voice capture
- burst buffer
- audio timestamp
- driver / DSP communication

## 11. 官方资料

- Voice Activation  
  https://learn.microsoft.com/windows-hardware/drivers/audio/voice-activation

- Multiple Voice Assistant  
  https://learn.microsoft.com/windows-hardware/drivers/audio/voice-activation-mva

- SysVAD  
  https://github.com/microsoft/Windows-driver-samples/tree/main/audio/sysvad
