# KS Core Foundation：General、Connection、Interfaces 与 Audio Events

> 状态：🟢 Public WDK / 🟤 Legacy（按具体 contract 标记）

Audio-specific property sets 只是 Kernel Streaming 的一部分。

音频 miniport / filter 还依赖一组 **generic KS contracts** 来描述 pin factory、pin instance、stream connection、data format、streaming interface 与 event notification。

这些 contract 定义在 `ks.h` / `ksmedia.h`，很多并不是“Audio”命名，但实际是理解 Windows audio driver 的基础。

## 1. KSPROPSETID_General

`KSPROPSETID_General` 用于查询 KS filter / pin 的通用特征。

当前公开 property：

~~~text
KSPROPERTY_GENERAL_COMPONENTID
~~~

官方：
https://learn.microsoft.com/windows-hardware/drivers/stream/kspropsetid-general

## 2. KSPROPSETID_Connection

Pin factory 描述的是“能够创建什么”。真正创建 pin instance 之后，stream connection 的状态与格式主要由 `KSPROPSETID_Connection` 管理。

当前结构库已正式落地到 `api/ks-core.csv`：

- `KSPROPERTY_CONNECTION_ALLOCATORFRAMING`
- `KSPROPERTY_CONNECTION_ALLOCATORFRAMING_EX`
- `KSPROPERTY_CONNECTION_ACQUIREORDERING`
- `KSPROPERTY_CONNECTION_DATAFORMAT`
- `KSPROPERTY_CONNECTION_PRIORITY`
- `KSPROPERTY_CONNECTION_PROPOSEDATAFORMAT`
- `KSPROPERTY_CONNECTION_STARTAT`
- `KSPROPERTY_CONNECTION_STATE`

~~~text
Pin Factory
   ↓ create
Pin Instance
   ↓
KSPROPSETID_Connection
   ├─ current format
   ├─ proposed format
   ├─ allocator framing
   ├─ priority
   └─ stream state
~~~

官方：
https://learn.microsoft.com/windows-hardware/drivers/stream/kspropsetid-connection

## 3. Data format negotiation

KS 中需要区分 `KSDATARANGE`（pin factory 能支持的范围）和 `KSDATAFORMAT`（一个具体格式）。

Pin factory 常用：

- `KSPROPERTY_PIN_DATARANGES`
- `KSPROPERTY_PIN_CONSTRAINEDDATARANGES`
- `KSPROPERTY_PIN_PROPOSEDATAFORMAT`
- `KSPROPERTY_PIN_DATAINTERSECTION`

Pin instance 创建后则可以使用：

- `KSPROPERTY_CONNECTION_PROPOSEDATAFORMAT`
- `KSPROPERTY_CONNECTION_DATAFORMAT`

~~~text
factory capability negotiation
             ↓
        create pin
             ↓
connection runtime format
~~~

这也是 ACX `ACXDATAFORMAT` 与底层 KS format model 之间的重要背景。

官方：
https://learn.microsoft.com/windows-hardware/drivers/stream/ks-data-formats-and-data-ranges

## 4. Standard streaming interface

`KSINTERFACESETID_Standard` 包含：

- `KSINTERFACE_STANDARD_STREAMING`
- `KSINTERFACE_STANDARD_LOOPED_STREAMING`
- `KSINTERFACE_STANDARD_CONTROL`

Microsoft 文档明确说明 `KSINTERFACE_STANDARD_STREAMING` 被大多数 KS audio filters 使用，而且所有 audio miniports 都支持它。

Streaming data 使用 `KSSTREAM_HEADER` 传递 buffer、timing、flags 等信息。

Looped Streaming 属于历史 DirectSound / XP-era contract；Vista 及以后系统组件已不再使用相关 LoopedStreaming event set。

官方：
- https://learn.microsoft.com/windows-hardware/drivers/stream/kernel-streaming-interface-sets
- https://learn.microsoft.com/windows-hardware/drivers/stream/ksinterface-standard-streaming

## 5. Audio-related KS event sets

Microsoft 的 Audio Drivers Event Sets 当前列出：

~~~text
KSEVENTSETID_AudioControlChange
KSEVENTSETID_LoopedStreaming
KSEVENTSETID_PinCapsChange
KSEVENTSETID_SoundDetector
KSEVENTSETID_VolumeLimit
~~~

`KSEVENTSETID_PinCapsChange` 在 Windows 7+ 用于 format capability / jack information 变化通知；`KSEVENTSETID_SoundDetector` 用于 keyword/sound detector match；`KSEVENTSETID_VolumeLimit` 从 Windows 8.1 起用于 safe-volume warning workflow。

`KSEVENTSETID_LoopedStreaming` 是历史 contract。Microsoft 文档明确说明它只用于旧系统内部组件，并且 Vista+ 已没有系统组件使用。

官方：
https://learn.microsoft.com/windows-hardware/drivers/audio/audio-drivers-event-sets

## 6. 为什么这些需要纳入 WinAudioResearch

如果数据库只整理 `KSPROPSETID_Audio` / `AudioEngine` / `Jack`，会漏掉 audio driver 真正运行时依赖的通用 KS 层。

更完整的模型应该是：

~~~text
KS Filter
  ├─ General
  ├─ Topology
  ├─ Pin factory
  │    ├─ interfaces
  │    ├─ mediums
  │    └─ data ranges
  │
  └─ Pin instance
       ├─ Connection
       ├─ stream format
       ├─ KSSTREAM_HEADER
       ├─ RTAudio / WaveRT
       └─ events
~~~

本阶段之后，MediaSeeking、Clock、StreamIo、StreamAllocator、allocator framing 与 `KSSTREAM_HEADER` 也已经进入结构化数据库。完整审计见 [KS Generic Streaming Contracts Audit](109-KS-Generic-Streaming-Contracts-Audit.md)。后续重点转向剩余 generic event infrastructure、category/node GUIDs，以及 AVStream callback / automation 边界。
