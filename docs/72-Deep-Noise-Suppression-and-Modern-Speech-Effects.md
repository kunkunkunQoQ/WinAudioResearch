# Deep Noise Suppression 与现代 Windows Speech Effects

> 状态：🟢 Public Windows 11 effects model

Windows 11 24H2 开始，Microsoft 的公开 audio effect model 中加入：

```text
AUDIO_EFFECT_TYPE_DEEP_NOISE_SUPPRESSION
```

它和传统 Noise Suppression 并不是同一个 effect ID。

---

## 1. Noise Suppression

传统：

```text
AUDIO_EFFECT_TYPE_NOISE_SUPPRESSION
```

可以理解为：

> 较轻量的 noise suppression effect identity。

---

## 2. Deep Noise Suppression

Windows 11 24H2：

```text
AUDIO_EFFECT_TYPE_DEEP_NOISE_SUPPRESSION
```

Microsoft 描述为：

> 更高级、AI / machine-learning based 的 noise suppression。

---

## 3. 谁真正实现算法

Effect identity 是 Windows public contract。

但具体 DSP 可能来自：

- Windows platform
- OEM APO
- audio hardware vendor

不能看到 effect GUID 就假设：

> 所有 PC 算法和声音完全一样。

---

## 4. IAudioEffectsManager

应用可以：

```text
IAudioClient::GetService
        ↓
IAudioEffectsManager
        ↓
GetAudioEffects
```

查看当前 stream 的 effect list。

---

## 5. 检查 Deep Noise Suppression

遍历：

```text
AUDIO_EFFECT[]
```

查：

```text
id == AUDIO_EFFECT_TYPE_DEEP_NOISE_SUPPRESSION
```

再看：

- state
- canSetState

---

## 6. SetAudioEffectState

如果：

```text
canSetState == TRUE
```

可以尝试：

```text
SetAudioEffectState
```

需要准备：

- AUDCLNT_E_EFFECT_NOT_AVAILABLE
- AUDCLNT_E_EFFECT_STATE_READ_ONLY

因为 effect availability 会动态变化。

---

## 7. IAudioSystemEffects3

如果 APO 希望暴露可以动态 on/off 的 effect，需要实现相应 modern APO effect discovery/control interface。

这让 Windows / app 不必猜 OEM 私有设置。

---

## 8. Communications / Speech Category

是否出现某个 speech effect，可能与：

- endpoint
- category
- processing mode
- driver
- APO

相关。

所以正确研究流程：

```text
endpoint
+ AudioClientProperties category
+ processing mode
+ effects list
```

一起记录。

---

## 9. Raw Mode

如果目标是 ML 自己处理 microphone：

- RAW
- UniformSpeech
- custom capture

之间应按实际目标比较。

不要一边请求 system deep NS，一边又说要“绝对原始 microphone”。

---

## 10. AEC + NS + AGC

Voice pipeline 常见：

```text
AEC
→ Noise Suppression
→ AGC
→ app
```

但真实顺序 / placement 取决于：

- SFX/MFX/EFX
- DSP
- endpoint design

不能把这个简图当成所有机器的固定 pipeline。

---

## 11. 官方资料

- Audio Signal Processing Modes  
  https://learn.microsoft.com/windows-hardware/drivers/audio/audio-signal-processing-modes

- IAudioEffectsManager  
  https://learn.microsoft.com/windows/win32/api/audioclient/nn-audioclient-iaudioeffectsmanager

- Windows 11 APIs for APO  
  https://learn.microsoft.com/windows-hardware/drivers/audio/windows-11-apis-for-audio-processing-objects
