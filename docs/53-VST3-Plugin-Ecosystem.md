# VST 3 Plug-in Ecosystem on Windows

> 状态：第三方专业音频标准，官方来源为 Steinberg

VST 不是 Windows 系统音频 API。

但在 Windows 专业音频 / DAW / DSP 生态中，它非常重要，因此值得和：

- WASAPI
- ASIO
- XAudio2
- APO

放在同一张开发地图中。

## 1. VST Plug-in 是什么

VST plug-in 是由 host 加载的 audio / event processing component。

概念：

```text
DAW / Host
   ↓ audio block + events
VST Plug-in
   ↓ processed block
Host routing / mixer
```

## 2. VST 3 的数据模型

Plugin 可暴露：

- audio inputs
- audio outputs
- event inputs
- event outputs
- parameters
- automation
- state

host 决定：

- block size
- processing graph
- sample rate
- timing

## 3. Windows Packaging

当前 VST3 在 Windows 不是简单“任意 DLL 放哪都行”。

规范定义标准位置：

### User

```text
%LOCALAPPDATA%\Programs\Common\VST3
```

### Global 64-bit

```text
C:\Program Files\Common Files\VST3
```

### Global 32-bit

```text
C:\Program Files (x86)\Common Files\VST3
```

### Application-local

```text
<App>\VST3
```

Host 应按规范扫描。

## 4. VST 3 不需要传统 COM 注册

Steinberg 当前文档明确：

> VST 3 不要求像 DirectX plugin 那样做传统 registration。

Host 通过标准 folder 扫描 plug-in bundle。

## 5. VST3 SDK

当前 Steinberg SDK 包括：

- VST3 API
- helper classes
- host examples
- plugin examples
- validator
- wrappers

Windows 当前支持架构包括：

- x86
- x86_64
- arm64
- arm64EC

具体以当前 SDK README 为准。

## 6. 和 ASIO 的区别

VST：

> plugin / processing component model

ASIO：

> audio device I/O model

它们经常一起出现在 DAW，但不是一回事。

典型：

```text
ASIO Device
    ↕
DAW mixer
    ↕
VST plugins
```

## 7. 和 APO 的区别

VST：

- application host 内
- user selects plugin
- DAW / editor ecosystem

APO：

- Windows Audio Engine
- system / OEM endpoint processing
- driver package integration

不要把 VST EQ 当成系统 APO。

## 8. 和 Media Foundation MFT 的区别

MFT：

- Media Foundation pipeline
- codec / transform / media processing

VST：

- DAW / music-production plugin ecosystem

都能 DSP，但 host contract 完全不同。

## 9. Realtime Rule

VST audio processing callback 同样不适合：

- 阻塞
- disk I/O
- unpredictable allocation

因为 host audio thread 有 realtime deadline。

## 10. 官方资料

- Steinberg VST3 SDK  
  https://github.com/steinbergmedia/vst3sdk

- VST3 Documentation  
  https://github.com/steinbergmedia/vst3_doc

- VST3 Developer Portal  
  https://steinbergmedia.github.io/vst3_dev_portal/

- Plug-in Locations  
  https://steinbergmedia.github.io/vst3_dev_portal/pages/Technical+Documentation/Locations+Format/Plugin+Locations.html
