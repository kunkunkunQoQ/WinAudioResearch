# Windows HLK Audio Tests：Fidelity、Glitch、Latency 与 Certification

> 状态：🟢 Microsoft Hardware Lab Kit

如果做 audio driver / OEM hardware，不能只测试：

> “能播声音、能录音”。

Windows HLK 有一整套 audio quality / compatibility tests。

---

## 1. Windows HLK

Windows Hardware Lab Kit：

> Windows hardware / driver compatibility testing framework。

用于：

- Windows 11
- Windows 10
- Windows Server 2016+

参与 Windows Hardware Compatibility Program 时，需要使用对应版本 HLK。

---

## 2. Audio Test 关注什么

Microsoft audio HLK 不只测试 API 成功。

还测试：

- fidelity
- jack detection
- glitch
- communications quality
- latency
- power behavior
- APO behavior
- driver stability

---

## 3. Zero Glitch

Microsoft troubleshooting 文档特别强调：

Audio logo tests 中有多个：

```text
zero glitch
```

test case。

如果失败，优先检查：

- driver thread priority
- long DPC / ISR
- hardware power management

这说明：

> audio glitch 很多时候是 realtime scheduling / driver / power 问题，而不是用户态 buffer 算错。

---

## 4. Fidelity Setup

Audio fidelity test 需要非常严格的：

- cable
- reference hardware
- signal routing
- room setup

连接错误可能导致：

- 极低/异常 THD+N
- 假失败

所以测量结果必须和 setup 一起记录。

---

## 5. Communications Audio Fidelity

官方 manual test 评估：

### Microphone

- speech-to-noise ratio
- raw mic digital level
- clipping / saturation

### Speaker

- speaker output level

### Combined

- mic clipping while loudspeaker plays
- echo attenuation
- timestamp-unreported latency
- mouth-to-ear latency

这套测试非常适合作为自制 communications audio test lab 的参考。

---

## 6. Mouth-to-Ear Latency

定义：

```text
speaker render input
        ↓
physical air path
        ↓
microphone capture output
```

整体时间差。

它比单纯：

```text
IAudioClient buffer size
```

更接近真实 communications user experience。

---

## 7. Timestamp Latency

Microsoft test 还检查：

> microphone 和 loopback signal 之间没有被 timestamp 正确报告出来的额外 latency。

这和 Voice Clarity causality / clock accuracy直接相关。

---

## 8. Jack Detection

HLK troubleshooting 也包含 jack detection 专项。

例如 TRRS combo jack：

```text
Tip   = Left
Ring1 = Right
Ring2 = Ground
Sleeve= Microphone
```

错误：

- jack geometry
- impedance detection
- driver property

都会影响测试。

---

## 9. HDMI / DP / S/PDIF

Microsoft 要求测试前确认：

- HDMI
- DisplayPort
- S/PDIF
- headphone
- microphone

等 endpoint 都已连接且可正常 streaming。

因此 driver test environment 应覆盖：

> 全部 exposed endpoint，不只是默认 speaker。

---

## 10. Logs

HLK failure 时首先看：

```text
HLK Studio test log
```

并确保安装：

- latest HLK filters
- kit updates

因为有时 test / OS 本身已知问题会通过 filter/errata 处理。

---

## 11. Latency Performance Lab

Microsoft 还提供 communications audio latency performance lab。

工具历史上包括：

- glitch-free media test
- ETW patterns
- media engine test
- audio-specific utilities

这些更偏 OEM/system optimization。

---

## 12. 建议用于 WinAudioResearch 的测试层次

### App Library

```text
unit / integration
```

### Windows Audio Tool

```text
device/session hotplug regression
```

### Driver / Virtual Audio Device

```text
HLK
+
ETW
+
glitch / latency
+
fidelity
```

### Voice System

```text
communications fidelity
+
Voice Clarity
+
AEC / causality
```

---

## 13. 官方资料

- Windows Hardware Lab Kit  
  https://learn.microsoft.com/windows-hardware/test/hlk/

- Troubleshooting Audio Testing  
  https://learn.microsoft.com/windows-hardware/test/hlk/testref/troubleshooting-audio-testing

- Communications Audio Fidelity Test  
  https://learn.microsoft.com/windows-hardware/test/hlk/testref/8b2c652c-71c3-4f8b-a1d2-dc40cb660168

- Audio Latency Performance Exercise  
  https://learn.microsoft.com/windows-hardware/test/wpt/optimizing-windows-devices-for-multimedia-experiences-exercise-1
