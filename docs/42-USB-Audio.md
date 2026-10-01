# Windows USB Audio：UAC1、UAC2、inbox driver 与调试

> 状态：🟢 Microsoft documented driver behavior

USB Audio 对 Windows 应用通常表现成普通 audio endpoint，但底层实际上有 USB Audio Class、class driver、KS / WaveRT 等完整链路。

## 1. USB Audio Class 1.0

Windows 很早就提供：

```text
usbaudio.sys
```

支持 USB Audio Class 1.x 设备。

典型设备：

- USB speaker
- USB microphone
- headset
- simple USB DAC

## 2. USB Audio Class 2.0

从 Windows 10 1703 起，Windows 提供 inbox UAC2 driver：

```text
usbaudio2.sys
usbaudio2.inf
```

它实现为 WaveRT audio port class miniport。

## 3. 为什么有些 USB DAC 仍安装厂商 Driver

Windows inbox UAC2 driver 存在，但如果：

- 厂商 driver 已安装
- Windows Update 提供 partner driver

Windows 可以优先使用厂商 driver。

厂商 driver 可能提供：

- 自定义控制面板
- ASIO
- proprietary DSP
- 特殊 mixer
- firmware control

## 4. UAC2 常见 PCM 支持

Microsoft inbox UAC2 driver 支持典型 Type I：

- PCM 8..32 bits/sample
- PCM8
- IEEE float

也支持一些 Type III compressed / digital transport format。

实际 endpoint 可用格式仍取决于：

- device descriptor
- alternate setting
- driver
- Windows audio engine

## 5. Shared Mode Channel 限制

Microsoft UAC2 文档说明：

> shared mode 对超过 8 channel 的任意 channel count 有 Windows audio stack 限制。

如果做专业多通道 USB interface：

- exclusive mode
- ASIO
- vendor driver

可能成为实际路径。

## 6. USB Descriptor 很关键

UAC device 会通过 descriptors 描述：

- terminals
- feature units
- clock source
- channels
- sample rates
- alternate settings
- format capabilities

如果 descriptors 不合法，Windows 可能：

- 忽略 format
- endpoint 无法启动
- driver event log 报错

## 7. Clocking

USB Audio 设备常涉及：

- asynchronous
- adaptive
- synchronous

clock model。

应用层通常不直接操作 USB clock descriptor，但出现：

- drift
- crackle
- resampling
- sync

问题时，要意识到 USB transport clock 是变量之一。

## 8. Jack Description

Windows 10 1703+ UAC2 inbox driver 支持从 registry / descriptors 关联 jack description。

这会影响：

- Windows UI
- connector description
- DeviceTopology / jack info

## 9. 调试

如果 USB Audio 2.0 driver 无法启动：

- 查看 System Event Log
- 收集 Windows audio logs
- 核对 descriptors
- 核对 interface class / subclass / protocol
- 测试 inbox vs vendor driver

## 10. 应用层看到什么

对普通 Core Audio 应用：

```text
USB hardware
→ USB Audio class driver
→ KS / WaveRT
→ AudioEndpointBuilder
→ IMMDevice
→ WASAPI / Session API
```

所以应用通常不需要知道 USB protocol。

只有做：

- device diagnostics
- driver
- firmware
- pro audio
- low latency
- hardware control

才需要深入 USB Audio Class。

## 11. 官方资料

- USB Audio 2.0 Drivers  
  https://learn.microsoft.com/windows-hardware/drivers/audio/usb-2-0-audio-drivers

- USB Audio Class System Driver  
  https://learn.microsoft.com/windows-hardware/drivers/audio/usb-audio-class-system-driver--usbaudio-sys-

- USB-IF Audio Device Class Specifications  
  https://www.usb.org/documents
