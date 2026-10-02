# Windows Built-in Audio Codecs：版本变化与部署注意事项

> 状态：🟢 Microsoft documented media capability  
> 这页记录“Windows 自带什么 codec”这类会随 OS 版本变化的信息。

---

## 1. 不要假设系统永远自带同一组 Codec

Windows media codec availability 会因为：

- OS version
- edition
- N/KN media feature
- OEM preload
- optional feature
- Store codec extension

变化。

所以应用不能只说：

> “Windows 10/11 都有这个 codec。”

---

## 2. Windows 11 24H2：AC-3 变化

Microsoft 当前 Supported codecs 文档明确：

> 从 Windows 11 version 24H2 开始，AC-3 codec 不再随 Windows 内置。

但：

> 很多 device manufacturer 仍可能预安装 AC-3 codec。

因此：

```text
Windows 11 24H2
```

并不自动等于：

```text
AC-3 unavailable
```

而是：

```text
not inbox by default
```

应用应做 capability detection。

---

## 3. D / E

Microsoft codec capability table 常标：

- D = Decode
- E = Encode

不要只看到格式名就假设双向能力都有。

例如某 codec 可能：

- 只 decode
- 不能 encode

---

## 4. Container != Codec

例：

```text
MP4
```

是 container。

其中可以装：

- AAC
- ALAC
- AC-3
- video codec

所以：

> “支持 MP4”

不能直接推导：

> “支持里面所有 audio codec”。

---

## 5. Media Foundation

Windows built-in codecs 通常通过：

- Media Foundation
- Media Extension
- system codec components

暴露。

使用：

```text
Source Reader
MFT enumeration
```

可以判断实际 runtime capability。

---

## 6. Capability Detection

推荐：

1. 尝试枚举 MFT
2. 查询 input/output media type
3. 对实际 file/source 尝试创建 decoder
4. 正确处理 codec unavailable

而不是：

```text
if WindowsVersion >= X then codec exists
```

---

## 7. N / KN Editions

部分 Windows edition 可能缺少某些 media components。

部署专业 media app 时，应把：

- standard Windows
- N edition
- clean install
- OEM image

都纳入测试。

---

## 8. Store Extensions

某些格式由：

- Microsoft Store codec extension
- OEM codec pack

补充。

这也意味着：

> 用户 A 的 Windows 11 和用户 B 的 Windows 11，media capability 可能不同。

---

## 9. 对 Audio Player 的建议

应用最好把错误写成：

```text
Decoder for AC-3 is unavailable on this system.
```

而不是：

```text
File is broken.
```

---

## 10. 和 WASAPI 的关系

WASAPI 不 decode AC-3 / AAC / MP3。

典型：

```text
Media Foundation codec
        ↓
PCM
        ↓
WASAPI
```

或：

```text
encoded bitstream
→ IEC61937
→ compatible digital endpoint
```

这是两种不同路线。

---

## 11. 官方资料

- Supported codecs  
  https://learn.microsoft.com/windows/uwp/audio-video-camera/supported-codecs

- Supported Media Formats in Media Foundation  
  https://learn.microsoft.com/windows/win32/medfound/supported-media-formats-in-media-foundation

- Media Foundation  
  https://learn.microsoft.com/windows/win32/medfound/microsoft-media-foundation-sdk
