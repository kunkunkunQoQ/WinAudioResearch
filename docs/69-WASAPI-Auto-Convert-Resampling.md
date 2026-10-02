# WASAPI 自动 PCM 转换、Sample Rate Conversion 与 Format Negotiation

> 状态：🟢 Public API

很多旧 WASAPI 教程都会说：

> shared mode 的输入格式必须完全等于 MixFormat，否则你自己 resample。

现代 Windows 还提供：

```text
AUDCLNT_STREAMFLAGS_AUTOCONVERTPCM
```

帮助 shared-mode client 做格式转换。

---

## 1. Audio Engine Mix Format

```text
IAudioClient::GetMixFormat
```

返回 shared-mode audio engine 的 mix format。

这是最稳妥的 shared-mode format baseline。

---

## 2. AUTOCONVERTPCM

Flag：

```text
AUDCLNT_STREAMFLAGS_AUTOCONVERTPCM
```

允许 Windows 插入：

- channel matrixer
- sample rate converter

把 client 提供的 uncompressed PCM 转成 audio engine mix format。

---

## 3. SRC_DEFAULT_QUALITY

配合：

```text
AUDCLNT_STREAMFLAGS_SRC_DEFAULT_QUALITY
```

Windows 使用比默认更高质量、但开销更高的 sample rate converter。

官方建议：

- 最终给人听 → 可以考虑高质量 SRC
- silence / meter 等 → 不一定需要额外成本

---

## 4. 不是所有格式都自动支持

AUTOCONVERTPCM 不是：

> 任意 codec 自动 decode。

它面向：

```text
uncompressed PCM
```

例如：

- PCM
- float PCM

MP3 / AAC 仍然需要：

- Media Foundation
- FFmpeg
- codec

先 decode。

---

## 5. Shared vs Exclusive

### Shared

Audio Engine 可以：

- resample
- matrix
- mix

### Exclusive

应用更接近硬件 format contract。

通常需要：

```text
IsFormatSupported
```

确认 endpoint 支持。

---

## 6. 为什么 Sample Rate Conversion 有成本

Resampling 需要：

- filtering
- interpolation
- state
- CPU / DSP

高质量 converter 会增加：

- CPU
- latency

所以实时应用要在：

```text
quality
latency
CPU
```

之间取舍。

---

## 7. Capture

Capture 也可能希望得到特定格式。

如果 device native/mix format 和 app 想要不同：

选择：

- Audio Engine conversion
- Media Foundation resampler
- custom DSP

不要在读取 buffer 后直接把 48k 数据“按 44.1k 播”，那只是改变解释速度，不是 resampling。

---

## 8. Channel Conversion

AUTOCONVERTPCM 也可以插入：

```text
channel matrixer
```

例如：

- mono → stereo
- 5.1 → stereo

具体 mapping 会依据：

- channel mask
- speaker config

所以 WAVEFORMATEXTENSIBLE channel mask 很重要。

---

## 9. NAudio 历史参考

NAudio 作者 Mark Heath 曾长期讨论 WASAPI resampling。

较新的 Windows / NAudio 路径开始更多依赖：

```text
AUTOCONVERTPCM
```

这也是一个很好的例子：

> 老教程的限制可能随着 Windows API 演进而改变。

---

## 10. 官方资料

- AUDCLNT_STREAMFLAGS constants  
  https://learn.microsoft.com/windows/win32/coreaudio/audclnt-streamflags-xxx-constants

- GetMixFormat  
  https://learn.microsoft.com/windows/win32/api/audioclient/nf-audioclient-iaudioclient-getmixformat

- IsFormatSupported  
  https://learn.microsoft.com/windows/win32/api/audioclient/nf-audioclient-iaudioclient-isformatsupported

Community historical reference:

- Mark Heath: Automatic Sample Rate Conversion with WASAPI  
  https://www.markheath.net/post/2022/4/30/wasapi-sample-rate-conversion
