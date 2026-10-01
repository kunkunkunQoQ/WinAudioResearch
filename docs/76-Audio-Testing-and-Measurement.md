# Windows Audio Testing：Latency、Glitch、Fidelity、AEC 与 Measurement

> 状态：🟢 Microsoft HLK / engineering concepts

“听起来没问题”不是严谨 audio validation。Windows audio testing 至少可以分成 functional、latency、glitch、fidelity、communications、power、format 和 endpoint lifecycle。

## Functional

最基础：

- device enumerates
- stream opens
- render/capture works
- volume/mute works
- hotplug works

这只能证明基本功能。

## Glitch

Audio glitch 通常表示 realtime deadline missed、buffer starvation 或 discontinuity。来源可能是 DPC/ISR、driver、page fault、thread blocking、APO CPU spike、device wake 或 buffer period 太短。应结合 ETW、WPR、WPA 分析。

## Latency

至少区分：

- software/buffer latency
- Audio Engine / scheduling latency
- driver/hardware latency
- acoustic latency

`IAudioClient::GetStreamLatency` 不能代表完整 speaker→air→microphone 的 mouth-to-ear latency。

## Communications Fidelity

Microsoft HLK communications tests 会验证类似：

- raw microphone speech-to-noise ratio
- microphone digital signal level
- clipping
- loudspeaker output level
- AEC echo attenuation
- microphone ↔ loopback latency
- mouth-to-ear latency

这说明 communications quality 必须看完整 acoustic chain。

## THD+N / SNR

THD+N 和 SNR 更适合评估：

- DAC / ADC
- analog codec
- speaker / microphone path

纯数字 WASAPI loopback不能替代完整 hardware fidelity measurement。

## Test Signals

常见：

- sine
- sweep
- impulse
- pink noise
- speech
- silence
- multitone

不同 signal 分别适合 frequency response、distortion、latency、noise 等测试。

## Digital / Hardware / Acoustic Loopback

### Digital loopback

适合测试 PCM correctness、mixer、sample rate、channel order 和 timing。

### Cable loopback

line out → line in，可用于 round-trip driver/ADC/DAC latency。

### Acoustic loopback

speaker → air → microphone。必须固定距离、角度、环境噪声、volume 与设备位置。

## 测试元数据

每次结果建议记录：

```text
Windows Build
Driver
Endpoint
Format
Shared / Exclusive
Period
Processing Mode
APO state
Volume
Hardware
Test setup
Tool version
```

## 官方资料

- Troubleshooting Audio Testing  
  https://learn.microsoft.com/windows-hardware/test/hlk/testref/troubleshooting-audio-testing
- Communications Audio Fidelity Test  
  https://learn.microsoft.com/windows-hardware/test/hlk/testref/8b2c652c-71c3-4f8b-a1d2-dc40cb660168
- Windows Performance Toolkit  
  https://learn.microsoft.com/windows-hardware/test/wpt/
