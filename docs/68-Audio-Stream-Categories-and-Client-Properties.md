# AUDIO_STREAM_CATEGORY、AudioClientProperties 与 Stream Intent

> 状态：🟢 Public API

Windows Audio 不只关心：

- sample rate
- channel
- buffer size

应用还可以告诉系统：

> “这个 stream 是拿来做什么的？”

这个 intent 会影响：

- ducking
- processing
- offload
- driver signal-processing mode
- game / communications policy

---

## 1. AUDIO_STREAM_CATEGORY

Header：

```text
audiosessiontypes.h
```

常见 category：

- AudioCategory_Other
- AudioCategory_Communications
- AudioCategory_Alerts
- AudioCategory_SoundEffects
- AudioCategory_GameEffects
- AudioCategory_GameMedia
- AudioCategory_GameChat
- AudioCategory_Speech
- AudioCategory_Movie
- AudioCategory_Media
- AudioCategory_FarFieldSpeech
- AudioCategory_UniformSpeech
- AudioCategory_VoiceTyping

---

## 2. Communications

```text
AudioCategory_Communications
```

适合：

- VoIP
- voice call
- realtime chat

可能参与：

- ducking
- communications processing mode
- AEC / NS / AGC pipeline

---

## 3. GameChat

```text
AudioCategory_GameChat
```

和 Communications 类似，但 Microsoft 明确说明：

> GameChat 不会衰减其他 streams。

所以游戏语音不应该偷懒全部标成 Communications。

---

## 4. GameMedia / GameEffects

### GameMedia

游戏背景 music / media。

系统可以让普通 music/media app 对它拥有更高 foreground media priority。

### GameEffects

游戏实时 sound effects。

把 music 和 effects 分成不同 category 有助于 Windows 更准确理解 stream intent。

---

## 5. Media / Movie

### Media

没有 dialogue 为主的 media。

### Movie

包含 dialogue 的 media。

OEM / driver 可以按 signal processing mode 做不同优化。

---

## 6. Speech

用于 speech audio。

和 Communications 不完全相同。

---

## 7. FarFieldSpeech

用于：

> 麦克风距离说话者较远的 speech capture。

例如：

- smart speaker-like device
- meeting room
- laptop far-field mic array

它可能影响 driver / speech processing 的选择。

---

## 8. UniformSpeech

用于：

> 希望跨 Windows 设备获得更一致 speech processing 的 ML / speech application。

这个 category 对：

- speech ML
- model input consistency

非常值得关注。

---

## 9. VoiceTyping

用于：

- dictation
- voice typing

不是普通 media microphone capture。

---

## 10. Category 对 Stream Type 有限制

Microsoft 文档说明：

### Render

所有 category 可用。

### Capture

主要：

- Communications
- Speech
- Other

### Loopback

使用：

- Other

所以不能随便把任意 category 塞给任意 stream。

---

## 11. AudioClientProperties

```text
AudioClientProperties
```

成员：

```text
cbSize
bIsOffload
eCategory
Options
```

通过：

```text
IAudioClient2::SetClientProperties
```

设置。

---

## 12. bIsOffload

如果：

```text
TRUE
```

表示 client 希望使用 hardware-offloaded audio。

是否真的能 offload：

- endpoint capability
- hardware engine
- pin availability

共同决定。

Windows 10 起 hardware-offloaded stream 必须使用 event-driven mode。

---

## 13. AUDCLNT_STREAMOPTIONS

`Options` 可表达 stream characteristics。

典型：

- RAW
- MATCH_FORMAT
- AMBISONICS
- POST_VOLUME_LOOPBACK

不同 Windows Build 支持项不同，应 runtime check。

---

## 14. Category → Processing Mode

不要硬编码：

```text
Communications = one fixed DSP chain
```

更准确：

```text
app category
      ↓
Windows policy
      ↓
endpoint supported processing modes
      ↓
APO / driver / hardware behavior
```

具体 processing 取决于 endpoint。

---

## 15. 对 SonicRoute / Mixer 的意义

Mixer 看到一个 session 时，未来可以研究：

- category
- ducking
- effects
- activity

而不是只显示：

- PID
- volume

这样能帮助解释：

> 为什么某个应用一开麦，别的声音会自动变小？

---

## 16. 官方资料

- AUDIO_STREAM_CATEGORY  
  https://learn.microsoft.com/windows/win32/api/audiosessiontypes/ne-audiosessiontypes-audio_stream_category

- AudioClientProperties  
  https://learn.microsoft.com/windows/win32/api/audioclient/ns-audioclient-audioclientproperties-r1

- Audio Signal Processing Modes  
  https://learn.microsoft.com/windows-hardware/drivers/audio/audio-signal-processing-modes
