# Windows 音频开发必备的 Digital Audio Fundamentals

> 这篇不是 Windows API 文档，而是为了避免“接口会调，但 PCM 理解错了”。

## 1. Sample vs Frame

### Sample

某一个 channel 在一个时间点的数值。

### Frame

同一个时间点所有 channel 的 sample。

Stereo：

```text
Frame 0 = L0 + R0
Frame 1 = L1 + R1
```

所以 WASAPI 很多 API 用：

```text
frames
```

而不是 raw sample count。

## 2. Sample Rate

例如：

```text
48000 Hz
```

表示每个 channel 每秒 48000 sample。

不是：

> “整个 stereo 一共 48000 sample”。

Stereo 实际每秒：

```text
48000 frames
96000 scalar samples
```

## 3. Bit Depth

常见：

- 16-bit signed PCM
- 24-bit PCM
- 32-bit PCM
- 32-bit float

注意：

```text
32-bit
```

不代表一定是 int32。

Shared-mode Windows audio 中 float 非常常见。

## 4. Interleaved PCM

Stereo interleaved：

```text
L R L R L R
```

5.1：

```text
frame0(ch0 ch1 ch2 ch3 ch4 ch5)
frame1(...)
```

channel meaning 应结合 channel mask。

## 5. Block Align

```text
blockAlign
= channels × containerBits / 8
```

一个 frame 占多少 bytes。

## 6. Byte Rate

```text
avgBytesPerSec
= sampleRate × blockAlign
```

WAV / WAVEFORMAT 中经常需要。

## 7. Integer PCM Range

16-bit signed：

```text
-32768 .. 32767
```

转换 float 时通常映射到约：

```text
-1.0 .. +1.0
```

处理时要避免 clipping。

## 8. Float PCM

float audio 通常可以暂时超过 1.0，但最终输出链：

- converter
- limiter
- DAC

可能 clip。

所以 DSP 内部 headroom 和最终 output normalization 是两件事。

## 9. dBFS

数字音频常见：

```text
0 dBFS = full scale
```

低于 full scale：

- -6 dBFS
- -20 dBFS
- ...

peak meter scalar 转 dB 常用：

```text
20 * log10(amplitude)
```

但 Windows UI volume scalar 不应直接等同于 PCM dBFS。

## 10. RMS vs Peak

Peak：

- 瞬时最大振幅

RMS：

- 更接近能量 / loudness 的粗略量

LUFS：

- 更复杂的 loudness 标准

`IAudioMeterInformation.GetPeakValue`：

> 只是 peak，不是 RMS / LUFS。

## 11. Clipping

多个 stream 相加：

```text
0.8 + 0.8 = 1.6
```

如果最终目标只能到 1.0：

→ clipping。

Mixer 需要：

- gain staging
- limiter
- headroom

## 12. Resampling

44.1 kHz → 48 kHz 不是简单：

> “每隔几 sample 插一个点”。

高质量 resampler 涉及：

- interpolation
- filter
- anti-aliasing
- phase / latency

Windows 可用：

- Audio Engine conversion
- Media Foundation Resampler
- AudioGraph
- third-party DSP

## 13. Channel Conversion

Stereo → mono：

不能简单只取 left。

常见需要：

```text
mix matrix
```

5.1 → stereo 更复杂。

Windows resampler / audio engine 会结合 channel mask 做 mapping。

## 14. Latency

总 latency：

```text
application
+ buffer
+ engine
+ APO
+ driver
+ hardware
+ physical output
```

只测一层 API call 不能代表 end-to-end latency。

## 15. Clock Drift

两个独立 audio device：

- USB mic
- speaker

可能有独立 hardware clock。

长期 capture + render 会逐渐 drift。

如果做：

- echo cancellation
- multi-device recording
- network sync

必须考虑 clock drift / resampling。

## 16. Glitch

Glitch 通常是：

> deadline missed / buffer starvation / discontinuity

不是单纯“CPU 太高”。

## 17. 相关仓库文档

- [Audio Formats](31-Audio-Formats-WAVEFORMAT.md)
- [Low Latency](26-Low-Latency-Raw-Offload.md)
- [Realtime Threading](56-Realtime-Audio-Threading-and-MMCSS.md)
- [Audio Meter](04-Audio-Meter.md)
