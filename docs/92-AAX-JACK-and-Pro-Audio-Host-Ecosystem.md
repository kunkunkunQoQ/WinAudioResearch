# AAX、JACK 与 Windows 专业音频 Host / Routing 生态

> 状态：第三方专业音频技术  
> 这页补充 Windows Audio API 之外、但专业音频开发经常遇到的生态。

---

# Part A — AAX

## 1. AAX 是什么

AAX：

```text
Avid Audio eXtension
```

用于创建：

- audio effects
- processing plugins
- virtual instruments

Avid 官方列出的 host/ecosystem 包括：

- Pro Tools
- VENUE | S6L
- Media Composer

---

## 2. AAX SDK

Avid 官方开发入口：

https://developer.avid.com/aax/

SDK 通过 click-through license agreement 提供。

---

## 3. Commercial AAX

Avid 当前文档说明：

商业 AAX 产品还需要：

- 联系 Avid 获取所需工具 / license
- iLok account
- AAX digital signing 流程
- commercial development 需要 iLok USB key

所以：

> AAX 不能简单当作一个“随便 include header 就发布”的开放插件格式。

具体 licensing 条款必须以当前 Avid agreement 为准。

---

## 4. AAX 不是 Windows Device API

AAX plugin：

> 在 Pro Tools / VENUE 等 host 内处理 audio。

真正设备 I/O 通常由：

- Pro Tools audio engine
- ASIO / vendor driver

处理。

所以：

```text
AAX
≠
WASAPI replacement
```

---

# Part B — JACK

## 5. JACK 是什么

JACK：

```text
JACK Audio Connection Kit
```

是低延迟 audio server / routing ecosystem。

最常见于：

- Linux
- professional audio routing

但也有 Windows build。

---

## 6. Windows JACK

JACK 官方当前 download 页面仍提供：

- Win32
- Win64

Windows build，版本线 1.9.22。

官方注明：

- Windows 7+
- 64-bit build 支持混合 32/64-bit 环境

---

## 7. JACK Model

JACK 典型：

```text
Client A output
      ↓
JACK server/router
      ↓
Client B input
      ↓
hardware backend
```

它强调：

- graph routing
- low latency
- sample-synchronous clients

---

## 8. Windows Backend

JACK 在 Windows 上最终仍需要一个 host/device backend。

常见专业环境：

- ASIO

因此：

```text
JACK graph
+
ASIO device backend
```

可能形成 Windows pro-audio routing path。

---

## 9. 为什么它和虚拟声卡不同

JACK client routing：

> 只有参与 JACK graph 的 app 才天然可见。

虚拟 Windows audio endpoint：

> 任意普通 Windows app 都可以在 Sound Settings 看到。

二者不是一回事。

---

# Part C — Professional Host Layers

## 10. Plugin Layer

- VST3
- CLAP
- AAX

解决：

> host ↔ DSP plugin ABI

## 11. Device I/O Layer

- ASIO
- WASAPI
- Core Audio (macOS)
- ALSA/JACK backend (Linux)

解决：

> host ↔ audio device

## 12. Graph / Routing Layer

- JACK
- DAW internal routing
- virtual audio driver
- network audio

解决：

> stream ↔ stream / app ↔ app routing

---

## 13. 为什么必须分层

一个“Windows EQ Plugin”问题可能实际问的是完全不同的东西：

### DAW plugin

用：

- VST3 / CLAP / AAX

### 全系统 EQ

用：

- APO
- virtual device
- system DSP path

### 单独播放器 EQ

用：

- app DSP
- XAudio2 / AudioGraph / WASAPI pipeline

不要把它们混成：

> “写一个插件”。

---

## 14. 资料

- AAX SDK  
  https://developer.avid.com/aax/

- JACK downloads  
  https://jackaudio.org/downloads/

- JACK  
  https://jackaudio.org/
