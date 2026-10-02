# 高质量社区 / 工程资料索引

> 状态：Community / Engineering references  
> 原则：社区资料用于补充工程经验，Public API 语义最终仍以 Microsoft 文档 / SDK 为准。

---

## 1. Matthew van Eerde

Blog：

https://matthewvaneerde.wordpress.com/

GitHub：

https://github.com/mvaneerde

Matthew van Eerde 长期写 Windows 音频底层相关内容。

其公开代码 / 文章涉及：

- endpoint property enumeration
- default audio device troubleshooting
- DeviceTopology tree
- APO enumeration
- ACM enumeration
- audio diagnostics

这是 Windows Audio 研究非常有价值的工程资料来源。

---

## 2. Mark Heath / NAudio

Blog：

https://www.markheath.net/category/naudio

NAudio：

https://github.com/naudio/NAudio

值得研究：

- WASAPI
- sample rate conversion
- playback/capture abstraction
- .NET audio
- WaveOut/WinMM history
- effects / mixing

特别注意：

旧文章可能描述当时 Windows Vista / Win7 行为。

要结合文章日期和现代 Microsoft docs 阅读。

---

## 3. OBS Studio

仓库：

https://github.com/obsproject/obs-studio

Windows audio backend：

```text
plugins/win-wasapi
```

适合研究：

- WASAPI capture
- endpoint reconnect
- process/application audio capture
- device timing
- COM lifecycle
- Windows version branching

OBS 是非常好的“高负载真实产品”案例。

---

## 4. Chromium

源码：

https://chromium.googlesource.com/chromium/src/

适合搜索：

```text
WASAPI
CoreAudioUtilWin
AudioDeviceListenerWin
AudioManagerWin
```

浏览器必须处理大量真实设备兼容问题：

- hotplug
- Bluetooth
- communications
- sample rate
- browser tab capture

非常值得研究工程策略。

---

## 5. WebRTC

源码：

https://webrtc.googlesource.com/src/

适合：

- Windows audio device module
- AEC
- NS
- AGC
- drift
- echo reference
- communications capture/render

如果研究 VoIP，WebRTC 是绕不开的重要实现。

---

## 6. Wine

https://gitlab.winehq.org/wine/wine

适合研究：

- WinMM
- MMDevAPI
- WASAPI compatibility implementation
- DirectSound

注意：

> Wine 是 reimplementation，不是 Windows 源码。

---

## 7. ReactOS

https://github.com/reactos/reactos

适合：

- WinMM
- legacy multimedia
- Windows-compatible subsystem research

同样不能当作 Microsoft implementation。

---

## 8. PortAudio

https://github.com/PortAudio/portaudio

适合：

- WASAPI backend
- DirectSound backend
- WMME
- WDM-KS
- cross-platform device model

---

## 9. miniaudio

https://github.com/mackron/miniaudio

适合：

- compact Windows backend
- WASAPI
- DirectSound
- WinMM fallback
- device notification
- format conversion

---

## 10. FFmpeg

https://github.com/FFmpeg/FFmpeg

适合：

- codec
- resampling
- audio filters
- WASAPI / DirectShow device integration
- media pipeline

不要把 codec layer 和 Windows endpoint API 混在一起。

---

## 11. Stack Overflow / GitHub Issues

这类资料最大的价值：

- edge case
- HRESULT
- undocumented behavior
- real device failures

最大的风险：

- 过时
- 只有单台机器
- 复制了错误的 COM definition
- 缺 Windows Build

使用时必须：

1. 查发布日期
2. 看评论 / follow-up
3. 和 SDK header 对照
4. 自己实测

---

## 12. Source Ranking

建议：

```text
Microsoft SDK / WDK
  >
Microsoft Learn
  >
Microsoft official samples
  >
mature open-source product
  >
specialist engineering blog
  >
GitHub issue / StackOverflow
  >
anonymous snippet
```

Undocumented API 例外：

没有官方 contract 时，需要：

```text
multiple independent sources
+
actual Windows testing
```
