# Stream Categories、Ducking 与 AudioStateMonitor

> 状态：🟢 Public API

Windows 不只关心“哪个应用在播放”。

应用还可以告诉系统：

> 这个 stream 是什么用途？

这就是 `AUDIO_STREAM_CATEGORY` / WinRT audio category 的作用。

---

## 1. AUDIO_STREAM_CATEGORY

当前 Win32 enum 包含：

- Other
- ForegroundOnlyMedia（deprecated）
- BackgroundCapableMedia（deprecated）
- Communications
- Alerts
- SoundEffects
- GameEffects
- GameMedia
- GameChat
- Speech
- Movie
- Media
- FarFieldSpeech
- UniformSpeech
- VoiceTyping

不同类别会影响：

- ducking
- signal processing mode
- latency
- policy
- Bluetooth profile
- communications behavior

---

## 2. Category != Processing Mode

应用选择：

```text
AUDIO_STREAM_CATEGORY
```

driver / Windows 选择：

```text
Signal Processing Mode
```

不是简单 1:1。

例如 Communications category 通常映射到 Communications processing mode，但最终取决于 endpoint / driver support。

---

## 3. GameChat 的特殊意义

`AudioCategory_GameChat` 与 Communications 类似，但 Microsoft 文档特别指出：

> GameChat 不会像普通 Communications stream 一样导致其他 stream 自动被 duck。

这对游戏很重要：

- voice chat
- game music
- game effects

可以并存。

---

## 4. Ducking

Windows 可以在 communications stream active 时自动降低其他 stream 音量。

这由系统 policy 管理。

经典控制：

- `IAudioVolumeDuckNotification`
- `IAudioSessionControl2::SetDuckingPreference`

---

## 5. 新 IAudioClientDuckingControl

Windows 10 Build 20348+ 提供：

```text
IAudioClientDuckingControl
```

通过：

```text
IAudioClient::GetService
```

取得。

调用：

```text
SetDuckingOptionsForCurrentStream
```

可以让当前 render stream 表达：

> 不要因为我的 stream 活跃而 duck 其他应用。

---

## 6. AUDIO_DUCKING_OPTIONS

当前：

```text
AUDIO_DUCKING_OPTIONS_DEFAULT
AUDIO_DUCKING_OPTIONS_DO_NOT_DUCK_OTHER_STREAMS
```

注意：

> 它只控制“当前 stream 是否导致别人被 duck”。

如果另一个 communications app 仍然触发 ducking，你的 app audio 仍可能被系统降低。

---

## 7. AudioStateMonitor

WinRT：

```text
Windows.Media.Audio.AudioStateMonitor
```

可以监控一类 stream 当前是否被系统：

- Active
- Lowered
- Muted

可按：

- capture/render
- category
- device role
- device ID

创建 monitor。

---

## 8. 为什么 AudioStateMonitor 有价值

普通 mixer 只能看到：

- volume setting

但某些时候 stream 实际输出被系统 policy 调低。

例如：

- alarm
- communications ducking
- app background state

AudioStateMonitor 可以帮助应用区分：

> 用户设置的 volume

与：

> 系统 policy 当前降低 / mute 的 effective state。

---

## 9. SoundLevelChanged

典型模式：

```text
AudioStateMonitor
   ↓ SoundLevelChanged
read SoundLevel
   ↓
Active / Muted / Lowered
```

应用可以：

- pause playback
- update UI
- stop capture
- avoid recording silence

---

## 10. Teams 类 app 不一定使用系统 Ducking

Microsoft 文档特别提醒：

某些 communications app 会自己管理混音，而不触发系统级 ducking。

因此：

> “Teams 正在通话但系统没有 duck 音乐”

不一定是 Windows bug。

---

## 11. 官方资料

- AUDIO_STREAM_CATEGORY  
  https://learn.microsoft.com/windows/win32/api/audiosessiontypes/ne-audiosessiontypes-audio_stream_category

- Audio Signal Processing Modes  
  https://learn.microsoft.com/windows-hardware/drivers/audio/audio-signal-processing-modes

- IAudioClientDuckingControl  
  https://learn.microsoft.com/windows/win32/api/audioclient/nn-audioclient-iaudioclientduckingcontrol

- AUDIO_DUCKING_OPTIONS  
  https://learn.microsoft.com/windows/win32/api/audioclient/ne-audioclient-audio_ducking_options

- AudioStateMonitor  
  https://learn.microsoft.com/uwp/api/windows.media.audio.audiostatemonitor

- Detect and respond to audio state changes  
  https://learn.microsoft.com/windows/apps/develop/media-authoring-processing/detect-and-respond-to-audio-state-changes
