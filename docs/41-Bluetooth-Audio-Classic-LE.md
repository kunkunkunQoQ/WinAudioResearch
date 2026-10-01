# Windows Bluetooth Audio：A2DP、HFP、LE Audio 与 Sideband

> 状态：🟢 Microsoft documented driver / platform behavior

Windows 蓝牙音频至少要分成两代体系：

1. Bluetooth Classic Audio
2. Bluetooth LE Audio

它们在 endpoint、codec、capture、driver model 和 Windows 版本上的行为明显不同。

## 1. Bluetooth Classic：A2DP

A2DP 用于高质量立体声播放。

典型：

```text
Application
  ↓
Windows Audio Engine
  ↓
A2DP profile
  ↓
Bluetooth controller
  ↓
Headset / speaker
```

常见 codec：

- SBC
- aptX Classic
- AAC
- 某些 Windows 11 24H2 + 特定 Qualcomm 平台上的 aptX Adaptive

A2DP 本身只负责 host → device 的高质量播放，不负责 microphone capture。

## 2. Bluetooth Classic：HFP

HFP 用于：

- headset microphone
- 通话
- 双向语音

经典限制：

- capture 与 playback 同时使用
- 输出通常切到 mono speech mode
- 典型 8 kHz CVSD / 16 kHz mSBC

这就是很多用户看到的：

> 一打开蓝牙耳机麦克风，音乐质量突然下降。

## 3. Windows 10 与 Windows 11 Endpoint 行为不同

### Windows 10

常见为多个 endpoint：

```text
Device Stereo         → A2DP output
Device Hands-Free     → HFP output
Device Hands-Free Mic → HFP input
```

### Windows 11

Windows 会把 Classic Bluetooth endpoint 体验统一得更多。

如果设备同时支持 A2DP / HFP：

- 输出端点不再简单暴露成两个独立用户设备
- Windows 会根据场景自动切换 profile

例如：

- 普通 media playback → A2DP
- 打开 microphone → HFP
- Communications category stream → HFP

## 4. 自动 Profile 切换

Windows 11 中：

```text
media only
→ A2DP

microphone opened
→ HFP

communications output category
→ HFP
```

关闭 microphone 后，如果 media 仍在播放，系统会再切回 A2DP。

因此应用看到的 endpoint 不一定能直接告诉你“此刻物理链路正在用 A2DP 还是 HFP”。

## 5. Resampling

当 HFP 进入 8 / 16 kHz speech path，而其他应用仍输出 48 kHz 时，Windows 会根据当前 profile 需要进行 resampling。

所以：

> 一个应用请求 48 kHz，并不代表 Bluetooth air link 此刻就是 48 kHz。

## 6. Bluetooth LE Audio

Windows 11 22H2 后开始加入 LE Audio 支持。

核心协议包括：

- BAP
- TMAP
- HAP
- ASCS
- PACS

Windows driver-side LE Audio 路径使用：

- ACX
- vendor-specific audio path (VSAP)
- LE isochronous transport

## 7. LE Audio 与 Classic 共存

同一设备如果同时支持：

- Classic Audio
- LE Audio

Windows 会控制只让其中一套路径处于 active 状态。

LE active 时：

- A2DP/HFP sideband DDI 可被关闭
- 创建 LE Audio profile circuit

Classic active 时则反过来。

## 8. LE Audio 对语音体验的意义

Classic HFP 的典型问题：

- microphone 一开，输出降为 mono speech quality

LE Audio 的目标之一是改善这一限制，并支持更高质量、更现代的双向语音场景。

## 9. Sideband / Bypass

某些平台为了：

- 降功耗
- DSP offload
- 降主 CPU 占用

不会把所有 Bluetooth audio 数据都经标准 host HCI 走。

Windows 支持 sideband / bypass architecture。

典型：

```text
Audio DSP
  ↕ I2S / PCM / vendor bus
Bluetooth Controller
```

控制面仍可能通过 Windows Bluetooth stack 管理。

## 10. A2DP Sideband Offload

Windows 11 22000 起有 documented A2DP sideband offload architecture。

目标主要是：

- audio DSP 批量接收数据
- CPU / SoC 进入更低功耗
- Bluetooth controller 直接从 sideband 获得 audio data

## 11. 对应用开发者的建议

如果你做：

- 普通播放 → 不应自己手工切 A2DP/HFP
- 通信软件 → 正确设置 audio category / communications semantics
- device diagnostics → 记录 endpoint、profile 行为、format
- latency analyzer → Bluetooth transport 是重要变量
- mixer → 不要假设一个 endpoint 永远对应固定 codec / sample rate

## 12. 官方资料

- Bluetooth Classic Audio  
  https://learn.microsoft.com/windows-hardware/drivers/bluetooth/bluetooth-classic-audio

- Bluetooth LE Audio  
  https://learn.microsoft.com/windows-hardware/drivers/bluetooth/bluetooth-low-energy-audio

- Bluetooth HFP Bypass Audio Streaming  
  https://learn.microsoft.com/windows-hardware/drivers/audio/bluetooth-hfp-bypass-audio-streaming

- Audio Sideband A2DP Offload  
  https://learn.microsoft.com/windows-hardware/drivers/audio/audio-sideband-a2dp-offload

- Communications Audio Format Capabilities  
  https://learn.microsoft.com/windows/win32/coreaudio/communications-audio-format-capabilities
