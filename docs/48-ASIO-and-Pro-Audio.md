# ASIO 与 Windows Pro Audio

> 状态：第三方专业音频标准 + Microsoft documented comparison

ASIO（Audio Stream Input/Output）不是 Microsoft Windows Audio API。

它由 Steinberg 定义，并成为 Windows 专业音频生态的重要接口。

## 1. ASIO 的目标

ASIO 主要关注：

- low latency
- multichannel
- direct hardware capability
- professional recording
- DAW / audio interface

典型：

```text
DAW
  ↓
ASIO Host API
  ↓
Vendor ASIO Driver
  ↓
Audio Interface
```

## 2. 为什么它在专业音频常见

传统共享 Windows audio path 要经过：

- Audio Engine
- shared mixing
- system processing

ASIO driver 通常提供更直接的低延迟路径。

## 3. WASAPI Exclusive vs ASIO

两者都可以用于低延迟 / 独占场景，但不是同一个 API。

### WASAPI Exclusive

Microsoft API：

- Windows SDK
- endpoint-based
- IAudioClient
- Windows-native

### ASIO

Steinberg API：

- 需要 ASIO-capable driver
- host 直接和 ASIO driver 通信
- pro audio interface 常见

## 4. Windows 10+ Shared Low Latency

Microsoft 当前 Low Latency Audio 文档特别强调：

Windows 10+ 已显著降低 shared-mode Audio Engine latency。

结合：

- IAudioClient3
- AudioGraph

可以在不独占设备的情况下获得更低延迟。

所以现代选择不应简单写成：

```text
Low latency = ASIO only
```

## 5. ASIO SDK

ASIO SDK 包含：

- interface definition
- host sample
- driver sample
- Windows COM helper
- driver registration code

核心文件常见：

- asio.h
- iasiodrv.h
- asiodrivers.*
- asiolist.*
- host sample
- sample driver

## 6. Licensing

ASIO SDK 的 licensing / trademark 要单独核对。

不要因为某个 GitHub mirror 存在，就默认：

- 任意商业使用
- 任意复制
- 任意使用 ASIO logo

都自动允许。

应以 Steinberg 当前官方 SDK license / usage guideline 为准。

## 7. ASIO 和 Core Audio Session

ASIO stream 通常不会自然映射成你预期的 Windows shared Audio Session UI。

因此：

- Windows volume mixer
- ISimpleAudioVolume
- per-app session meter

未必能像普通 shared WASAPI app 一样控制 / 展示它。

这对 mixer 开发非常重要。

## 8. 多通道

专业 interface 可能提供：

- 8
- 16
- 32
- 更多 channel

ASIO 往往比普通 Windows shared consumer path 更贴近这些硬件 channel。

## 9. Sample Rate / Buffer

ASIO host 通常直接处理：

- buffer size
- sample rate
- channel
- callbacks

因此 DAW 可以针对 interface driver 做非常细的 latency tuning。

## 10. Windows Audio Research 中的定位

WinAudioResearch 应把 ASIO 放在：

```text
Professional / third-party Windows audio ecosystem
```

而不是归入：

```text
Microsoft Core Audio API
```

## 11. 资料

- Microsoft Low Latency Audio  
  https://learn.microsoft.com/windows-hardware/drivers/audio/low-latency-audio

- Steinberg  
  https://www.steinberg.net/

- Steinberg GitHub Organization  
  https://github.com/steinbergmedia

- ASIO SDK licensing / SDK should be checked from Steinberg's current distribution.
