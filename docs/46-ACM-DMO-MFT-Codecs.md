# Windows Codec / Transform 历史：ACM → DMO → MFT

> 状态：🟢 Public APIs，包含 Legacy 技术

Windows 音频 codec / transform 开发经历了多代体系。

理解历史可以帮助你读老项目和系统 codec wrapper。

## 1. ACM — Audio Compression Manager

ACM 是经典 Windows multimedia API。

它管理：

- compressor / decompressor
- format converter
- filter driver

API 包括：

- acmDriver*
- acmFormat*
- acmStream*
- acmFilter*

Microsoft 当前明确把 ACM 标记为：

> legacy，强烈建议新代码不要优先使用。

## 2. ACM 怎么工作

ACM 可以把 audio format conversion 插入传统 waveform audio 流程。

例如：

```text
PCM
→ ACM codec
→ ADPCM / compressed
```

或反向 decode。

## 3. DMO — DirectX Media Object

DMO 是 COM-based transform。

核心接口：

```text
IMediaObject
```

用途：

- codec
- DSP
- effect
- format conversion

DMO 比 DirectShow filter model 更简单。

## 4. DMO 已被 MFT 取代

Microsoft 当前文档明确：

> DMOs 已由 Media Foundation Transforms (MFTs) supersede。

新 codec / processing plugin 更应该考虑：

```text
IMFTransform
```

## 5. MFT — Media Foundation Transform

MFT 是 Media Foundation 的通用 transform model。

用途：

- decoder
- encoder
- resampler
- DSP
- converter

核心：

```text
IMFTransform
```

## 6. Audio Resampler DSP

Windows 自带 Audio Resampler：

```text
CLSID_CResamplerMediaObject
```

可同时支持：

- IMFTransform
- IMediaObject

能力：

- sample rate conversion
- channel count conversion
- channel mapping matrix

这正体现了 DMO → MFT 的兼容过渡。

## 7. MP3 / AAC / Dolby

Media Foundation 提供多个系统 codec / MFT。

例如：

- MP3 decoder
- MP3 encoder
- AAC decoder / encoder
- Dolby decoder / encoder
- WMA family

实际 availability 要按：

- Windows version
- edition
- optional media components

确认。

## 8. Media Foundation 不等于支持所有系统 ACM codec

Microsoft 支持格式文档明确：

> Media Foundation 会 wrapper 一部分 ACM codec，但不会自动支持任意第三方 ACM codec。

所以：

```text
ACM codec installed
```

不代表：

```text
Media Foundation can automatically use it
```

## 9. MFT Enumeration

可以通过 Media Foundation API 枚举：

- audio decoder
- audio encoder
- audio effect

按：

- category
- input subtype
- output subtype

选择 transform。

## 10. Async MFT

Windows 7+ 支持 asynchronous MFT model。

适合：

- hardware codec
- parallel pipeline
- async processing

## 11. 推荐技术选择

新代码：

```text
Media Foundation / MFT
```

兼容旧软件 / codec：

```text
ACM / DMO
```

研究历史：

三者都应该理解。

## 12. 官方资料

- Audio Compression Manager  
  https://learn.microsoft.com/windows/win32/multimedia/audio-compression-manager

- ACM Reference  
  https://learn.microsoft.com/windows/win32/multimedia/audio-compression-manager-reference

- DirectX Media Objects  
  https://learn.microsoft.com/windows/win32/directshow/directx-media-objects

- About MFTs  
  https://learn.microsoft.com/windows/win32/medfound/about-mfts

- Audio Resampler DSP  
  https://learn.microsoft.com/windows/win32/medfound/audioresampler

- Supported Media Formats in Media Foundation  
  https://learn.microsoft.com/windows/win32/medfound/supported-media-formats-in-media-foundation
