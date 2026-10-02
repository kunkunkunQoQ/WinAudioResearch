# Thunderbolt / PCIe Professional Audio on Windows

> 状态：🟢 Windows low-latency concepts + third-party vendor implementation notes

Thunderbolt / PCIe audio 不是一个单独的：

```text
Windows Audio API
```

对应用来说，最终通常仍通过：

- ASIO
- WDM / WASAPI
- vendor control API

访问。

真正差异主要在：

- hardware transport
- driver architecture
- channel count
- DMA
- latency
- vendor routing/mixer

---

## 1. Thunderbolt 不是 USB-C 的同义词

很多设备都使用：

```text
USB Type-C connector
```

但：

> Type-C connector 不代表设备一定使用 Thunderbolt protocol。

专业音频设备 troubleshooting 时必须确认：

- USB
- Thunderbolt
- PCIe tunneling

实际 transport。

---

## 2. Windows 应用看到什么

一台 Thunderbolt interface 安装 vendor driver 后，可能同时暴露：

### WDM / WASAPI endpoints

给：

- browser
- games
- media player
- Windows mixer

### ASIO device

给：

- DAW
- pro audio

所以同一硬件可能存在两套 app-facing model。

---

## 3. Vendor Driver 很重要

专业 interface 往往不依赖 Windows inbox class driver 完成全部功能。

Vendor driver 可能提供：

- ASIO
- low-latency DMA
- many channels
- internal DSP mixer
- clock source selection
- sample rate
- routing
- firmware

所以“Windows 能看到 device”不等于：

> pro audio driver 已正确安装。

---

## 4. Focusrite 的公开例子

Focusrite 当前 Windows support 文档明确把 driver 粗分为：

- ASIO
- WDM

并建议 DAW 使用 native ASIO。

其部分产品：

- Thunderbolt interface
- RedNet PCIe / PCIeNX

对 Windows 的 WDM exposure 能力甚至不同。

例如 vendor 文档记录：

- 某些 RedNet PCIe 旧卡面向 ASIO
- newer PCIeNX 可通过 driver 暴露部分 WDM channels

这说明：

> PCIe 硬件存在，并不自动意味着 Windows Sound Settings 必然看到标准 endpoint。

最终取决于 vendor driver。

---

## 5. PCIe Audio

PCIe audio interface/card 常见优势：

- direct PCIe transport
- high channel count
- predictable DMA
- lower transport overhead

但真正 round-trip latency 仍取决于：

- ASIO buffer
- driver
- hardware DSP
- converter latency
- sample rate
- DAW processing

不能只用“PCIe”判断 latency。

---

## 6. Thunderbolt Audio

Thunderbolt 可以给外置 device 提供接近 PCIe-style high-bandwidth transport。

常见于：

- recording interface
- Dante interface
- high channel count converter

但 Windows compatibility 仍取决于：

- Thunderbolt controller
- BIOS/firmware
- vendor driver
- security/authorization
- cable/topology

---

## 7. ASIO vs WDM Setting

Vendor support documents常提醒：

Windows Sound Control Panel 中：

```text
16/24 bit / sample rate
```

的 WDM format设置：

> 不一定影响同一硬件的 ASIO stream。

ASIO host 可能直接使用自己的：

- sample rate
- bit depth
- buffer

配置。

所以调试 DAW 时不要只看：

```text
mmsys.cpl
```

---

## 8. Low Latency

Microsoft Low Latency Audio 文档把：

- WASAPI exclusive
- ASIO
- modern low-latency shared mode

都作为 Windows pro-audio latency path 讨论。

Windows 10+ 以后：

> shared-mode Audio Engine latency 已明显降低。

所以“专业音频 = 必须 ASIO”不是所有场景都成立。

但成熟 DAW / high-channel interface：

> native ASIO driver 仍非常常见。

---

## 9. Channel Count

Consumer WDM endpoint 常面向：

- stereo
- 5.1 / 7.1

Professional interface 可能：

- 8
- 16
- 32
- 64
- 128 channels

Vendor WDM driver 可以选择：

- 暴露多个 stereo endpoint
- 暴露 multichannel endpoint
- 只暴露少量 WDM channels
- ASIO 暴露全部 channels

这完全可能因产品而异。

---

## 10. Clocking

Pro hardware 常支持：

- internal clock
- Word Clock
- ADAT
- SPDIF
- Dante/PTP
- external sync

所以多设备 drift / sync 问题不能只靠 Windows AudioClock 解决。

Hardware clock topology 也很关键。

---

## 11. 调试清单

```text
Transport:
  Thunderbolt / PCIe / USB / Network

Driver:
  Vendor version

WDM endpoints:
  count / formats

ASIO:
  driver name / buffer / sample rate

Clock:
  internal/external

Firmware:
  version

Round-trip latency:
  measured, not marketing number
```

---

## 12. 资料

Microsoft:

- Low Latency Audio  
  https://learn.microsoft.com/windows-hardware/drivers/audio/low-latency-audio

Vendor engineering references:

- Focusrite ASIO / WDM explanation  
  https://support.focusrite.com/hc/en-gb/articles/360013509640-What-do-the-terms-ASIO-and-WDM-mean

- Focusrite Windows audio optimization  
  https://support.focusrite.com/hc/en-gb/articles/207355205-Optimising-Windows-for-audio

- RME Windows drivers  
  https://www.rme-usa.com/downloads.html

> Vendor pages describe their products, not Windows universal API behavior. Use them as ecosystem examples, not platform contracts.
