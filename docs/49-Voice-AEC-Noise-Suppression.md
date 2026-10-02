# Voice Processing：AEC、Noise Suppression、AGC 与 Communications Audio

> 状态：🟢 Public API / Driver Documentation

实时语音不是“打开麦克风然后读 PCM”这么简单。

Windows 的语音处理链可能涉及：

- Acoustic Echo Cancellation (AEC)
- Noise Suppression (NS)
- Automatic Gain Control (AGC)
- Beamforming
- Communications signal processing mode
- APO
- render reference stream

---

## 1. AEC 为什么需要两个输入

AEC 的目标是消除：

```text
扬声器播放的远端声音
        ↓
被麦克风再次录进去
        ↓
远端用户听到自己的回声
```

因此 AEC 不只需要 microphone input。

它还需要：

```text
reference render stream
```

简化：

```text
Mic Capture --------┐
                    ├─→ AEC → cleaned capture
Render Reference ---┘
```

---

## 2. Windows 11 APO AEC Framework

Microsoft 在 Windows 11 APO framework 中增加了更明确的 AEC 支持。

AEC APO 可以向系统声明自己是 AEC processor。

Audio Engine 会为它：

- 配置额外 reference input
- 当 render endpoint 变化时切换 reference stream
- 提供 microphone / reference timestamps
- 允许 APO 控制 input format

这比 vendor 自己私下构造 reference tap 更标准化。

---

## 3. AEC 通常在哪里

常见于：

```text
Capture path
  ↓
AEC / NS / AGC APO
  ↓
communications app
```

而不是：

```text
普通 render EQ
```

---

## 4. Communications Category 很重要

Microsoft 建议 communications app 将 stream 标记为：

```text
AudioCategory_Communications
```

这样 Windows 可以：

- 使用正确 signal-processing mode
- 选择更适合通信的 format
- 应用 ducking policy
- 启用 voice-oriented effects
- 针对 Bluetooth profile 做正确选择

如果只是用默认 Media category，然后自己期待系统“自动知道这是 VoIP”，行为可能不符合预期。

---

## 5. Audio Format Capability Detection

通信场景中，应用可能需要知道：

- microphone sample rate
- render sample rate
- playback 是否仍支持 stereo
- microphone 使用时 output format 是否降级

Bluetooth HFP 场景尤其明显。

Microsoft 提供专门的 communications format capability guidance。

---

## 6. Noise Suppression

Noise Suppression 的目标是去除：

- fan
- keyboard
- background environment noise

但它不是 AEC。

AEC 去除的是：

```text
known render reference leaking into mic
```

NS 去除的是：

```text
unwanted environmental noise
```

两个算法可能同时存在。

---

## 7. Deep Noise Suppression

Windows 11 24H2 起，Microsoft 增加：

```text
AUDIO_EFFECT_TYPE_DEEP_NOISE_SUPPRESSION
```

用于标识更高强度、AI/ML 类的 noise suppression effect。

它仍然通过 APO/effect framework 暴露，不代表所有 Windows 11 24H2 机器都必然有可用实现。

实际 availability 取决于：

- driver
- OEM APO
- hardware / NPU / DSP
- endpoint capability

---

## 8. AGC

Automatic Gain Control 自动调 microphone gain / digital level。

优点：

- voice level 更稳定

风险：

- 环境噪声被一起拉高
- 与用户手工 microphone gain 冲突
- measurement / recording 场景不适合

所以 RAW / measurement app 通常不希望 AGC。

---

## 9. RAW Mode 与 Voice Processing

RAW mode 的目标是绕过常规 processing。

对 capture measurement / custom ML pipeline：

```text
RAW
```

往往比 Communications 更合适。

对 VoIP：

```text
Communications
```

通常更适合，因为系统 / OEM voice effects 能参与。

---

## 10. 历史 AEC System Filter

Windows 早期还有：

```text
Aec.sys
```

AEC system filter。

它属于旧式 Windows audio processing 路径，常见于：

- DirectSoundCapture
- legacy filter graph

新开发不应把它当现代 APO AEC framework 的唯一入口。

---

## 11. KSNODETYPE_ACOUSTIC_ECHO_CANCEL

驱动 topology 还定义：

```text
KSNODETYPE_ACOUSTIC_ECHO_CANCEL
```

表示 AEC control node。

这属于 KS / driver topology 层。

---

## 12. 自己实现 AEC 前需要知道什么

如果完全自己做：

```text
mic
+
render reference
+
clock sync
+
latency compensation
+
drift correction
+
adaptive filter
```

真正难点往往不是算法名字，而是：

- 两路时钟对齐
- reference delay
- Bluetooth latency
- resampling
- endpoint switching
- sample drop / glitch

所以通信软件不要低估“自己写一个 AEC”的工程复杂度。

---

## 13. 官方资料

- Windows 11 APIs for Audio Processing Objects  
  https://learn.microsoft.com/windows-hardware/drivers/audio/windows-11-apis-for-audio-processing-objects

- Audio Signal Processing Modes  
  https://learn.microsoft.com/windows-hardware/drivers/audio/audio-signal-processing-modes

- Communications Audio Format Capabilities  
  https://learn.microsoft.com/windows/win32/coreaudio/communications-audio-format-capabilities

- AEC System Filter  
  https://learn.microsoft.com/windows-hardware/drivers/audio/aec-system-filter

- KSNODETYPE_ACOUSTIC_ECHO_CANCEL  
  https://learn.microsoft.com/windows-hardware/drivers/audio/ksnodetype-acoustic-echo-cancel
