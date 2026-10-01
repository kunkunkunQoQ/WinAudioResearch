# Microphone / Communications Audio：AEC、AGC、NS 与格式能力

> 状态：🟢 Public Windows audio architecture / driver concepts

“录麦克风”有两类完全不同的目标：

### Raw / Measurement

希望：

- 尽量少处理
- 原始波形
- 自己做 DSP

### Communications / Speech

希望：

- AEC
- AGC
- noise suppression
- voice optimization

如果不先区分这两个场景，很容易选错 API / processing mode。

## 1. AEC

Acoustic Echo Cancellation：

目标：

> 防止 speaker 播出的远端声音重新被 microphone 录进去。

典型 VoIP：

```text
remote voice
→ speaker
→ room
→ microphone
→ AEC removes echo
```

## 2. AGC

Automatic Gain Control：

自动调节 capture gain / signal level。

优点：

- 语音更稳定

缺点：

- 不适合 measurement / music raw capture

## 3. Noise Suppression

用于降低：

- fan
- keyboard
- ambient noise

具体算法可能运行在：

- APO
- DSP
- hardware
- app

## 4. Processing Mode

Speech / Communications mode 可以允许不同 effect chain。

Raw mode 则用于：

- custom processing
- measurement
- ML capture

并限制一些 adaptive system effects。

## 5. Bluetooth Communications

Classic Bluetooth microphone 通常进入 HFP。

所以：

- mono
- 8 / 16 kHz
- playback quality change

可能不是应用 bug，而是 profile behavior。

## 6. LE Audio

LE Audio 支持更现代的 communications profile 和 stereo voice 能力。

开发 diagnostics 时应区分：

- Classic HFP
- LE TMAP/HAP

## 7. Communications Audio Format Capabilities

Windows 提供 communications format capability 相关 API / behavior。

设备可能根据：

- Bluetooth profile
- driver
- endpoint

支持不同：

- channel count
- sample rate
- format

## 8. Microphone Array

如果硬件是 array：

- mic coordinates
- working volume
- array type

会影响 beamforming / speech processing。

详见：

[Audio Jacks、Connector 与 Microphone Array](49-Jacks-Connectors-and-Microphone-Arrays.md)

## 9. Raw Capture 不是简单“关音量增强”

要更接近 raw：

- 选择正确 processing mode
- 检查 APO
- 检查 driver
- 检查 hardware DSP
- 检查 format conversion

## 10. 官方资料

- Audio Signal Processing Modes  
  https://learn.microsoft.com/windows-hardware/drivers/audio/audio-signal-processing-modes

- Communications Audio Format Capabilities  
  https://learn.microsoft.com/windows/win32/coreaudio/communications-audio-format-capabilities

- Windows Audio Processing Objects  
  https://learn.microsoft.com/windows-hardware/drivers/audio/windows-audio-processing-objects

- Microphone Array Geometry Property  
  https://learn.microsoft.com/windows-hardware/drivers/audio/microphone-array-geometry-property
