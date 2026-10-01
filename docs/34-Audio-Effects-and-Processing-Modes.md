# Audio Effects、Stream Category 与 Signal Processing Modes

> 状态：🟢 Public API / Driver Documentation

Windows 音频处理中经常混淆三个概念：

1. Stream Category
2. Signal Processing Mode
3. Audio Effect / APO

---

## 1. Stream Category

应用告诉系统：

> “这个 stream 是干什么的？”

常见 category：

- Media
- Movie
- Communications
- Speech
- GameChat
- GameMedia
- GameEffects
- Alerts
- SoundEffects
- Other

这会影响：

- policy
- ducking
- processing
- driver mode selection

---

## 2. Signal Processing Mode

driver / endpoint 支持的 processing mode：

- Raw
- Default
- Media
- Movie
- Speech
- Communications
- Notification

应用选 category，Windows 再匹配合适 mode。

不是：

```text
category == mode
```

一一硬编码对应。

---

## 3. RAW

RAW mode 的目标：

- 减少 signal processing
- 给 measurement / custom DSP 更干净的 path

官方要求 raw capture 不应加入：

- AEC
- AGC
- noise suppression

等 time-varying / adaptive processing。

允许的处理更受限制。

---

## 4. Communications

Communications mode 常用于：

- VoIP
- voice chat
- Teams / Skype 类场景

可能关联：

- AEC
- AGC
- noise suppression
- voice optimization

具体是否启用取决于：

- driver
- APO
- hardware
- system capabilities

---

## 5. Media / Movie

适合：

- music
- video
- movie playback

OEM 可根据设备实现：

- speaker EQ
- bass enhancement
- virtual surround
- loudness

---

## 6. Speech

面向 speech capture / recognition。

和 Communications 不完全相同。

---

## 7. APO Placement

Effect 可以位于：

- SFX
- MFX
- EFX

因此“系统有一个 EQ”这个说法不够精确。

应该问：

- 对哪个 stream？
- 哪个 mode？
- 哪个 endpoint？
- effect 在哪个 stage？

---

## 8. IAudioEffectsManager

新版 Windows 提供：

```text
IAudioEffectsManager
```

用于查询关联 stream 的 effects：

- GetAudioEffects
- SetAudioEffectState
- effect changed callback

这比直接 reverse registry 更适合公开 API 场景。

---

## 9. Windows 11 APO Effects Discovery

Windows 11 CAPX 进一步标准化：

- effect discovery
- effect enable / disable
- notification
- settings
- logging
- threading

APO 可以通过 `IAudioSystemEffects3` 暴露可控 system effects。

---

## 10. “关闭音效”为什么不总是等于 bit-perfect

即使：

- 关 Enhancements
- 用 RAW
- volume = 100%

仍可能存在：

- format conversion
- hardware processing
- endpoint always-on DSP
- driver-specific processing

真正 bit-exact 需要端到端验证，而不是只看一个 UI 开关。

---

## 11. 官方资料

- Audio Signal Processing Modes  
  https://learn.microsoft.com/windows-hardware/drivers/audio/audio-signal-processing-modes

- Audio Processing Object Architecture  
  https://learn.microsoft.com/windows-hardware/drivers/audio/audio-processing-object-architecture

- IAudioEffectsManager  
  https://learn.microsoft.com/windows/win32/api/audioclient/nn-audioclient-iaudioeffectsmanager

- Windows 11 APIs for APO  
  https://learn.microsoft.com/windows-hardware/drivers/audio/windows-11-apis-for-audio-processing-objects
