# Windows 11 Voice Clarity：系统级语音增强与测试要求

> 状态：🟢 Microsoft documented platform / HLK behavior

Voice Clarity 是 Windows 11 新一代 speech / communications processing 能力之一。

研究它时不能只看：

```text
noise suppression
```

还要理解：

- AEC
- microphone/speaker causality
- timestamps
- acoustic coupling
- microphone dynamic range
- hardware gain
- APO
- HLK certification

---

## 1. Voice Clarity 不是一个普通 App Filter

Voice Clarity 更接近：

> Windows / OEM audio processing stack 中的 communications enhancement capability。

它依赖：

- system / device audio architecture
- APO
- render reference
- microphone path
- accurate timestamps

---

## 2. Causality

Microsoft Voice Clarity Causality Test 要求：

> QPC timestamp 对齐之后，每个 microphone signal 都必须相对于每个 speaker loopback signal 有正延迟。

直观：

```text
speaker signal produced
        ↓
sound travels / processing
        ↓
microphone observes signal
```

不能出现时间关系“反过来”。

---

## 3. 为什么 Causality 对 AEC 很重要

AEC 要知道：

```text
Reference[n - delay]
```

对应：

```text
Mic[n]
```

如果：

- QPC timestamp 错
- capture/render buffer timestamp 不一致
- driver 报告错误 timing

AEC 很难正确估计 echo path。

---

## 4. Microsoft Causality Test

官方 HLK test：

1. 每个 speaker channel 播放 logarithmic sine sweep
2. 其他 channel silence
3. microphone RAW capture
4. 按 QPC timestamp 对齐 speaker/mic
5. cross-correlation 计算 delay
6. 每个 speaker-mic pair 都必须满足 positive delay

测试支持：

- Windows 11 x64
- Windows 11 Arm64
- Windows 11 version 22631 及后续版本线

---

## 5. Acoustic Coupling Factor

Voice Clarity 还有：

```text
Mic Speaker Coupling Factor Test
```

目标：

> 内置 speaker 到 microphone 的声学耦合不能过强。

测试：

- 播放 / capture sweep
- timestamp alignment
- 估计 impulse response
- 计算 acoustic coupling

如果 speaker 和 microphone 物理设计耦合太强：

再好的 AEC 软件也更难处理。

---

## 6. Mic Boost

官方 Voice Clarity Mic Boost Test 要求：

> microphone capture path 不应存在不符合要求的 boost subunit。

因为 Voice Clarity algorithm 假设 microphone signal gain model 满足特定条件。

---

## 7. Mic Dynamic Range

Voice Clarity Dynamic Range Test 检查：

> 0 dB microphone signal 是否真正代表 microphone 可用 full dynamic range，不能无故损失 significant bits。

这说明：

Voice Clarity 不只是“装个 AI model”。

它对：

- hardware
- driver
- gain staging
- format

都有要求。

---

## 8. Hardware Volume Control

Voice Clarity 还有 microphone hardware volume test。

如果 endpoint 声明支持 hardware mic volume：

- 暂时禁用 third-party software APO
- raw capture
- 测多个 endpoint volume step
- 验证实际 recorded level 随 hardware volume 正确变化

---

## 9. x64 / Arm64

这些 HLK test 同时明确覆盖：

- x64
- Arm64

对 ARM Windows device 的语音 subsystem 开发非常重要。

---

## 10. 与 App AEC 的关系

应用自己使用：

- WebRTC AEC
- 自定义 NN noise suppressor

和 system Voice Clarity 不是完全同一路径。

如果系统已经在 Communications mode 做 processing，再叠加 app-level AEC/NS：

可能产生：

- double processing
- distortion
- pumping
- phase issues

所以应用需要知道：

> 当前 endpoint / stream 上到底有哪些 effect。

可以结合：

- IAudioEffectsManager
- RawProcessingSupported
- SpeechProcessingSupported

做更合理决策。

---

## 11. 研究 / 测试建议

如果研究 Voice Clarity：

记录：

```text
Windows Build
Architecture
Mic endpoint
Speaker endpoint
Driver
Processing mode
Raw support
Speech processing support
APO list
QPC timestamps
Loopback timestamp
Causality
Coupling
Latency
```

---

## 12. 官方资料

- Voice Clarity Causality Test  
  https://learn.microsoft.com/windows-hardware/test/hlk/testref/voice-clarity-system-verification-test-causality

- Voice Clarity Mic Speaker Coupling Factor Test  
  https://learn.microsoft.com/windows-hardware/test/hlk/testref/voice-clarity-system-verification-test-coupling-factor

- Voice Clarity Mic Boost Test  
  https://learn.microsoft.com/windows-hardware/test/hlk/testref/voice-clarity-system-verification-test-mic-boost

- Voice Clarity Mic Dynamic Range Test  
  https://learn.microsoft.com/windows-hardware/test/hlk/testref/voice-clarity-system-verification-test-mic-dynamic-range
