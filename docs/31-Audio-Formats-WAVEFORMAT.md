# Windows Audio Formats：WAVEFORMATEX / WAVEFORMATEXTENSIBLE / Channel Mask

> 状态：🟢 Public API

只会调用 `IAudioClient` 还不够。

Windows 音频流的基本语言之一是：

```text
WAVEFORMATEX
WAVEFORMATEXTENSIBLE
```

---

## 1. WAVEFORMATEX

结构核心：

```text
wFormatTag
nChannels
nSamplesPerSec
nAvgBytesPerSec
nBlockAlign
wBitsPerSample
cbSize
```

---

## 2. PCM 计算

例如：

```text
48 kHz
2 channels
16 bit
```

则：

```text
nBlockAlign = channels * bitsPerSample / 8
            = 2 * 16 / 8
            = 4

nAvgBytesPerSec = sampleRate * blockAlign
                = 48000 * 4
                = 192000
```

这些值写错会造成：

- Initialize fail
- file playback speed wrong
- buffer interpretation wrong

---

## 3. WAVEFORMATEXTENSIBLE

当：

- >2 channels
- multichannel speaker mapping
- higher bit depth
- 需要明确 SubFormat

应使用 `WAVEFORMATEXTENSIBLE`。

额外字段：

- valid bits / samples per block
- channel mask
- SubFormat GUID

---

## 4. Container Bits vs Valid Bits

例：

```text
24-bit valid PCM
stored in 32-bit container
```

可以表达为：

- wBitsPerSample = 32
- wValidBitsPerSample = 24

这和简单写“24 bit”有本质区别。

---

## 5. Channel Mask

`dwChannelMask` 描述每个 channel 对应的 speaker position。

例如：

- FRONT_LEFT
- FRONT_RIGHT
- FRONT_CENTER
- LOW_FREQUENCY
- BACK_LEFT
- BACK_RIGHT

多声道不能只知道：

```text
channels = 6
```

还必须知道 6 个 channel 分别是谁。

---

## 6. SubFormat

常见：

- PCM
- IEEE_FLOAT

WAVEFORMATEXTENSIBLE 用 GUID 描述 general sample format。

---

## 7. Float PCM

Windows shared audio engine 很常见：

```text
32-bit float PCM
```

不要把：

```text
32 bit
```

自动理解为：

```text
32-bit signed integer
```

必须看 format tag / SubFormat。

---

## 8. Interleaved

传统 WASAPI PCM buffer 通常是 interleaved：

```text
L0 R0 L1 R1 L2 R2 ...
```

如果多声道：

```text
frame0[channel0..N]
frame1[channel0..N]
...
```

因此 buffer size 应以：

```text
frames * blockAlign
```

计算，而不是“sample 数 * 随便一个 byte size”。

---

## 9. Format Negotiation

Shared WASAPI：

- engine 可以做 conversion
- GetMixFormat 是重要参考

Exclusive：

- 更需要严格 `IsFormatSupported`

AudioGraph / Media Foundation：

- 可以在更高层帮助进行 format conversion

---

## 10. 文件格式和 PCM 格式不是一回事

```text
MP3 / AAC / FLAC
```

是 compressed codec / file-media concept。

```text
48kHz stereo float PCM
```

是 decoded stream format。

不要把：

> “支持 MP3”

理解成：

> “WASAPI Initialize 传 MP3 format”。

通常必须先 decode 成 PCM。

---

## 11. 官方资料

- WAVEFORMATEX  
  https://learn.microsoft.com/windows/win32/api/mmeapi/ns-mmeapi-waveformatex

- WAVEFORMATEXTENSIBLE  
  https://learn.microsoft.com/windows-hardware/drivers/ddi/ksmedia/ns-ksmedia-waveformatextensible

- Channel Mask  
  https://learn.microsoft.com/windows-hardware/drivers/audio/channel-mask

- Devices and Data Types  
  https://learn.microsoft.com/windows/win32/multimedia/devices-and-data-types
