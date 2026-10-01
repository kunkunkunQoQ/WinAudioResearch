# Community Articles / Blogs / Learning Resources

> 状态：社区资料索引  
> 原则：教程非常有价值，但公开 API 语义仍以 Microsoft 文档 / SDK 为准。

## 1. Mark Heath / NAudio

主页分类：

https://www.markheath.net/category/naudio

长期积累大量 Windows / .NET 音频文章。

高价值主题包括：

- WASAPI
- device enumeration
- loopback capture
- resampling
- Media Foundation
- ASIO
- waveform
- MIDI
- codecs

### 30 Days of NAudio Documentation

https://markheath.net/post/30-days-naudio-docs

覆盖：

- playback
- output devices
- WasapiOut
- recording
- loopback
- codecs
- MFT
- ACM
- MIDI

### Automatic Sample Rate Conversion with WASAPI

https://www.markheath.net/post/2022/4/30/wasapi-sample-rate-conversion

适合了解：

- WASAPI format negotiation
- AUTOCONVERTPCM
- SRC
- NAudio 如何处理 format mismatch

### What's up with WASAPI?

https://www.markheath.net/post/2008/6/2/what-up-with-wasapi

具有历史价值，可看到 Vista Core Audio 出现时：

- WinMM
- DirectSound
- Kernel Streaming
- WASAPI

之间的定位变化。

注意文章年代较早，不能把当年的限制直接套到现代 Windows 11。

## 2. Windows Developer Blog

Windows Developer Blog 历史文章中有：

- MIDI enhancements
- low latency
- AudioGraph
- UWP audio
- Bluetooth MIDI

例如：

https://blogs.windows.com/windowsdeveloper/2016/09/21/midi-enhancements-in-windows-10/

这类内容适合理解：

> 某个 Windows 版本为什么引入一个 API。

但具体接口签名仍应回 Microsoft Learn / SDK。

## 3. Steinberg Developer Resources

VST3：

https://steinbergmedia.github.io/vst3_dev_portal/

VST API docs：

https://steinbergmedia.github.io/vst3_doc/

适合：

- plugin architecture
- realtime rules
- plugin location
- hosting
- build
- validation

## 4. JUCE Tutorials

JUCE 官方：

https://juce.com/

https://github.com/juce-framework/JUCE

适合：

- plugin development
- realtime audio callback
- device abstraction
- MIDI
- DSP

## 5. PortAudio Docs

https://www.portaudio.com/docs/

适合：

- callback stream model
- blocking stream
- host API
- device enumeration
- cross-platform architecture

## 6. USB-IF

USB Audio Class 真正 protocol specification：

https://www.usb.org/documents

Windows Learn 解释 Windows driver behavior；

USB-IF spec 解释：

- descriptor
- endpoint
- clock
- class request

两者都需要看。

## 7. Bluetooth SIG

Bluetooth profile / codec / LE Audio 标准：

https://www.bluetooth.com/specifications/

Windows Learn 解释 Windows implementation；

Bluetooth SIG 解释：

- A2DP
- HFP
- BAP
- TMAP
- PACS
- ASCS

协议本身。

## 8. Khronos / OpenAL

OpenAL ecosystem 可从：

https://www.openal.org/

和 OpenAL Soft：

https://github.com/kcat/openal-soft

研究：

- positional audio
- HRTF
- 3D source/listener model

## 9. Stack Overflow / Q&A

这类资料适合：

- HRESULT 搜索
- obscure COM interop problem
- exact device issue
- driver-specific behavior

但建议使用方式：

```text
community answer
→ extract hypothesis
→ verify Microsoft docs / source / experiment
```

不要把单个回答升级成稳定 Windows contract。

## 10. Reddit / forums

适合研究：

- 用户痛点
- driver compatibility
- Bluetooth quirks
- DAC / ASIO experience
- Windows Update regression

不适合直接作为：

- API ABI
- IID
- system guarantee

的唯一来源。

## 11. 来源评级建议

### A — Specification / official contract

- Windows SDK / WDK
- Microsoft Learn
- USB-IF
- Bluetooth SIG
- Steinberg VST/ASIO official

### B — Official sample / first-party implementation

- microsoft/Windows-classic-samples
- microsoft/Windows-driver-samples
- microsoft/MIDI

### C — Mature third-party code

- NAudio
- EarTrumpet
- JUCE
- PortAudio

### D — Community article / issue

- blog
- Stack Overflow
- GitHub issue

### E — Anecdotal

- forum
- Reddit
- user report

仓库记录最好明确来源等级。
