# Media Foundation Audio：解码、编码、文件与媒体管线

> 状态：🟢 Public API

Media Foundation（MF）是 Windows 的现代媒体处理框架之一。

它不仅处理视频，也覆盖大量音频场景：

- decode
- encode
- transcode
- file container
- media source
- media sink
- resample
- playback pipeline

---

## 1. 它和 WASAPI 的区别

### WASAPI

更接近：

```text
PCM stream
↔ endpoint
```

关注：

- audio buffer
- endpoint
- period
- latency
- shared / exclusive

### Media Foundation

更接近：

```text
media file / source
    ↓
demux / decode / transform
    ↓
PCM / compressed stream
    ↓
sink / playback / file
```

所以：

> WASAPI 解决“音频怎么进出设备”，Media Foundation 更擅长“媒体数据怎么读取、转换、编码”。

---

## 2. Source Reader

`Source Reader` 是非常实用的 MF 高层接口。

适合：

- 打开 MP3 / AAC / MP4 / M4A 等
- 选择 audio stream
- decode 成 PCM
- 逐 sample 读取
- 不需要搭建完整 Media Session pipeline

概念：

```text
File / URL / MediaSource
      ↓
IMFSourceReader
      ↓
decoded samples
```

---

## 3. Sink Writer

Sink Writer 适合：

- 把 PCM 编码成 AAC / WMA 等
- 写 MP4 / ASF 等 container
- 简化 encoding pipeline

概念：

```text
PCM samples
    ↓
IMFSinkWriter
    ↓
encoder / mux
    ↓
file
```

---

## 4. Transform (MFT)

Media Foundation Transform 可用于：

- decoder
- encoder
- resampler
- color converter
- effect / processing

音频中常见：

- AAC decoder / encoder
- MP3 decoder
- audio resampler

---

## 5. Supported Media Formats

Microsoft 官方维护：

https://learn.microsoft.com/windows/win32/medfound/supported-media-formats-in-media-foundation

其中包括常见：

- MP3
- AAC / ADTS
- WMA
- WAV
- MPEG-4 / M4A / MP4
- ASF

支持范围会随 Windows 版本和安装组件变化。

---

## 6. 音频文件 != 音频设备

一个常见设计错误：

> 用 WASAPI 直接“播放 MP3”。

WASAPI 不负责 MP3 解码。

正确分层通常是：

```text
MP3
 ↓
Media Foundation / decoder
 ↓
PCM
 ↓
WASAPI / AudioGraph / XAudio2
 ↓
Endpoint
```

---

## 7. Resampling

如果文件是：

```text
44.1 kHz / stereo
```

设备 engine format 是：

```text
48 kHz / stereo
```

可选择：

- shared WASAPI 让 engine conversion
- Media Foundation resampler
- AudioGraph conversion
- 自己 DSP resampler

具体选择取决于：

- quality
- latency
- CPU
- control requirement

---

## 8. SilentPlayer 这类程序

如果要：

- 打开 MP4
- 只选音频轨
- decode
- 送入 playback

Media Foundation Source Reader 是很合适的系统方案。

它比“按扩展名判断格式”更稳妥，因为 container / codec 应由实际内容决定。

---

## 9. Media Session

Media Foundation 还有完整的 Media Session pipeline。

适合：

- 完整播放架构
- topology
- source → transform → sink
- timing / presentation clock

但对“只想读解码后 sample”的程序，Source Reader 往往更简单。

---

## 10. 官方资料

- Microsoft Media Foundation SDK  
  https://learn.microsoft.com/windows/win32/medfound/microsoft-media-foundation-sdk

- Source Reader  
  https://learn.microsoft.com/windows/win32/medfound/source-reader

- Sink Writer  
  https://learn.microsoft.com/windows/win32/medfound/sink-writer

- Supported Media Formats  
  https://learn.microsoft.com/windows/win32/medfound/supported-media-formats-in-media-foundation
