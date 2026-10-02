# Microsoft 官方 Windows Audio Samples / Tools

> 这页专门整理“文档看完以后应该去哪里看真实代码”。

---

## 1. Windows Classic Samples

仓库：

https://github.com/microsoft/Windows-classic-samples

### WASAPIRendering

https://github.com/microsoft/Windows-classic-samples/tree/main/Samples/WASAPIRendering

适合：

- shared render
- event-driven
- IAudioClient
- IAudioRenderClient

### ApplicationLoopback

https://github.com/microsoft/Windows-classic-samples/tree/main/Samples/ApplicationLoopback

适合：

- process loopback
- ActivateAudioInterfaceAsync
- process tree include/exclude

### Win7Samples/multimedia/audio

https://github.com/microsoft/Windows-classic-samples/tree/main/Samples/Win7Samples/multimedia/audio

其中有大量经典 WASAPI 示例：

- CaptureSharedEventDriven
- CaptureSharedTimerDriven
- RenderSharedEventDriven
- RenderSharedTimerDriven
- RenderExclusiveEventDriven
- RenderExclusiveTimerDriven
- DuckingCaptureSample

虽然目录名历史较老，但对理解 WASAPI 调用链仍然非常有价值。

---

## 2. Windows Universal Samples

仓库：

https://github.com/microsoft/Windows-universal-samples

### AudioCreation / AudioGraph

https://github.com/microsoft/Windows-universal-samples/tree/main/Samples/AudioCreation

包含：

- file playback
- microphone capture
- frame input/output
- submix
- effects
- low latency

### WindowsAudioSession

https://github.com/microsoft/Windows-universal-samples/tree/main/Samples/WindowsAudioSession

演示 UWP 环境的 WASAPI 相关场景。

### MIDI

https://github.com/microsoft/Windows-universal-samples/tree/main/Samples/MIDI

---

## 3. Windows Driver Samples

仓库：

https://github.com/microsoft/Windows-driver-samples

### SysVAD

https://github.com/microsoft/Windows-driver-samples/tree/main/audio/sysvad

Windows audio driver 学习的核心 sample。

覆盖：

- WDM
- WaveRT
- virtual audio
- APO
- offload
- topology

### SysVAD 结构化子项目

API database 现在单独索引：

- **TabletAudioSample** — WaveRT / offload / 多 endpoint
- **EndpointsCommon** — endpoint / topology 共用代码
- **SwapAPO** — SFX / MFX / APO INF 注册
- **KeywordDetectorAdapter** — voice activation / keyword detector

这些条目不仅作为链接存在，也已经通过 `api/relationships.csv` 关联到 WaveRT、APO、SoundDetector 等 contract。

### Simple Audio Sample

https://github.com/microsoft/Windows-driver-samples/tree/main/audio/simpleaudiosample

比 SysVAD 更适合第一次读 audio driver。

### ACX Samples

https://github.com/microsoft/Windows-driver-samples/tree/main/audio/Acx

新 ACX driver model。

---

## 3.1 历史 DirectMusic Driver Samples

Microsoft 旧 WDK sample 列表仍记录：

- **Dmusuart** — DirectMusic UART driver
- **ddksynth** — DirectMusic software synthesizer

它们对应仓库的 `api/dmusicks.csv` / `api/methods-dmusicks.csv`。这些样例属于 Legacy 研究资料，不建议作为现代 Windows 11 新驱动架构模板。

## 4. Windows MIDI Services

https://github.com/microsoft/MIDI

这个仓库本身就是：

- SDK
- service
- tools
- driver
- samples
- docs

的综合参考。

---

## 5. Microsoft Docs 源码仓库

很多 Microsoft Learn Win32 文档本身公开在：

https://github.com/MicrosoftDocs/win32

它有一个很实用的价值：

> Learn 页面有时重定向 / 页面 UI 不方便搜索时，可以直接在 docs repo 中 grep 接口名。

---

## 6. Windows Driver Docs 源码

https://github.com/MicrosoftDocs/windows-driver-docs

适合搜索：

- APO
- WaveRT
- AudioEndpointBuilder
- KS
- driver property
- ACX

---

## 7. Windows SDK Header 是最终重要参考之一

当你在写 COM interop 时，不应该只复制博客中的 C# declaration。

优先核对：

- mmdeviceapi.h
- audioclient.h
- audiopolicy.h
- endpointvolume.h
- devicetopology.h
- spatialaudioclient.h
- ksmedia.h
- propsys.h

因为：

> 文档解释语义，Header 定义 ABI。

---

## 8. WDK Header

驱动 / APO / KS：

- audioenginebaseapo.h
- ks.h
- ksmedia.h
- portcls.h
- ACX headers

应以当前 Windows SDK / WDK 为准。

---

## 9. 推荐学习顺序

### 应用层

```text
WASAPIRendering
→ Capture sample
→ Loopback
→ AudioGraph
```

### 驱动层

```text
Windows Audio Architecture
→ Simple Audio Sample
→ SysVAD
→ ACX
→ APO
```

### MIDI

```text
microsoft/MIDI docs
→ samples
→ transports / SDK
```
