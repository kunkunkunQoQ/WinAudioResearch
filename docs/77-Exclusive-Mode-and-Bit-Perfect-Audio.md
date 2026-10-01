# WASAPI Exclusive、Bit-perfect 与“原样输出”

> 状态：🟢 Public API + engineering caveats

“Bit-perfect”经常被过度简化。WASAPI Exclusive 很重要，但它不是一个自动保证所有 bit 永远不变的开关。

## Shared Mode

```text
App stream
  ↓
Windows Audio Engine
  ↓
mix / conversion / effects
  ↓
endpoint
```

系统可能进行 resample、mix、volume 或 APO processing，所以 shared mode 默认不等于 bit-perfect。

## Exclusive Mode

`AUDCLNT_SHAREMODE_EXCLUSIVE` 让应用独占 endpoint。其他 system sounds / applications 无法同时使用这个 endpoint。

Exclusive 更适合：

- hard bit-exact requirement
- custom sample rate
- certain pro-audio workflows

但 driver、hardware DSP、device volume、format conversion、digital transport 等仍可能影响端到端结果。

## IsFormatSupported

Exclusive stream 前应调用 `IAudioClient::IsFormatSupported` 确认 sample rate、bit depth、channel count 和 channel mask。

Windows Sound UI 显示某个格式，不代表任意自定义 WAVEFORMAT 都能成功 Initialize。

## 用户可以禁用 Exclusive

如果用户关闭“Allow applications to take exclusive control”，应用需要处理：

`AUDCLNT_E_EXCLUSIVE_MODE_NOT_ALLOWED`

如果另一个应用已经独占：

`AUDCLNT_E_DEVICE_IN_USE`

## Windows 10+ Low-period Shared Mode

Microsoft 当前建议：如果主要目标是 low latency，先评估 `IAudioClient3` shared low-period stream，因为它保留 system mixing / interoperability，同时 latency 可接近 exclusive mode。

## RAW 与 Exclusive 不是一回事

RAW 表示 processing intent；Exclusive 表示 endpoint sharing mode。两者是不同维度。

## Volume / Format

严格 bit-perfect 还要核对：

- session volume
- endpoint volume
- hardware volume
- integer/float conversion
- sample rate
- channel conversion
- DSP/effects

例如 source 是 16-bit PCM，但 app decode 成 float 再转换回 int，未必满足严格 bit identity。

## Encoded Passthrough

Dolby/DTS passthrough 传递的是 encoded bitstream。它不是“Exclusive PCM”的同义词，需要 endpoint capability、digital output 和特定格式支持。

## 如何验证

比“听不出来”更可靠：

- known PCM pattern
- digital loop capture（如果路径允许）
- checksum / bit compare
- device sample-rate indicator
- unity gain
- effects disabled
- endpoint/driver documentation

## 官方资料

- Exclusive-Mode Streams  
  https://learn.microsoft.com/windows/win32/coreaudio/exclusive-mode-streams
- IAudioClient::IsFormatSupported  
  https://learn.microsoft.com/windows/win32/api/audioclient/nf-audioclient-iaudioclient-isformatsupported
- IAudioClient3  
  https://learn.microsoft.com/windows/win32/api/audioclient/nn-audioclient-iaudioclient3
