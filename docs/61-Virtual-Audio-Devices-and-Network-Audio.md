# Virtual Audio Device、Virtual Cable 与 Network Audio

> 状态：🟢 官方 driver architecture + 第三方实现参考

“虚拟扬声器 / 虚拟麦克风”与“应用内部做音频处理”不是一回事。

真正出现在 Windows：

- Sound Settings
- MMDevice
- WASAPI
- 默认设备列表

中的虚拟 endpoint，通常需要 audio driver / virtual audio device。

---

## 1. 普通应用不能凭空创建 IMMDevice Endpoint

一个普通 C# / C++ user-mode process 无法仅靠：

```text
IMMDeviceEnumerator
```

注册一个真正系统级 speaker / microphone。

Endpoint 通常来自：

```text
audio driver / device interface
       ↓
AudioEndpointBuilder
       ↓
software audio endpoint
       ↓
IMMDevice
```

---

## 2. Microsoft SysVAD

官方最重要的 virtual audio driver sample：

https://github.com/microsoft/Windows-driver-samples/tree/main/audio/sysvad

SysVAD：

> System Virtual Audio Device

展示：

- virtual render endpoint
- virtual capture endpoint
- WaveRT
- topology
- formats
- APO
- offload
- endpoint configuration

如果目标是真正开发虚拟声卡，SysVAD 是第一优先参考。

---

## 3. Simple Audio Sample

如果 SysVAD 太复杂：

https://github.com/microsoft/Windows-driver-samples/tree/main/audio/simpleaudiosample

更适合先理解：

- speaker
- microphone array
- WDM audio driver structure

---

## 4. ACX Virtual / Sample Drivers

Microsoft 新 driver framework：

```text
ACX
```

官方 samples：

https://github.com/microsoft/Windows-driver-samples/tree/main/audio/Acx

新项目应同时评估：

- legacy WDM/PortCls/WaveRT
- ACX

而不是默认复制旧 driver sample。

---

## 5. Virtual Cable 的基本概念

常见 virtual cable：

```text
Virtual Input Endpoint
          ↓
internal ring / transport
          ↓
Virtual Output Endpoint
```

用户把 app 输出到 virtual speaker，然后另一个 app 从对应 virtual capture endpoint 读取。

真正实现方式取决于 driver architecture。

---

## 6. Virtual Mixer

更复杂的 virtual mixer：

```text
App A ─┐
App B ─┼─→ Virtual Mixer → Hardware
App C ─┘
                ↓
           Virtual Capture
```

需要考虑：

- multiple streams
- format conversion
- clocks
- buffering
- volume
- channel mapping
- latency
- device restart

这已经不是简单的“复制 PCM”。

---

## 7. Scream

开源项目：

https://github.com/duncanthrax/scream

Scream 定位：

> Windows virtual network sound card

它提供：

```text
Windows virtual audio driver
        ↓
PCM
        ↓
network multicast / unicast
        ↓
receiver
        ↓
remote playback
```

适合研究：

- virtual endpoint
- driver → network transport
- PCM packet format
- receiver implementation

---

## 8. Network Audio 与 Virtual Device 的边界

你也可以不用 virtual driver：

```text
WASAPI loopback
   ↓
network
   ↓
remote player
```

这种方式：

- 不创建新的 Windows endpoint
- 更容易开发
- 但用户无法把单个应用“直接选择到一个网络 speaker endpoint”

是否需要 virtual device，取决于产品体验。

---

## 9. Process Loopback 也不是 Virtual Device

Process Loopback：

```text
capture selected process audio
```

它不会：

- 创建新 speaker
- 创建新 microphone
- 出现在 Sound Settings
- 被其他 app 当 endpoint 选择

所以不要把：

```text
process loopback
```

写成：

```text
virtual sound card
```

---

## 10. Driver Signing

真正安装 kernel/audio driver 需要考虑：

- test signing
- production signing
- Windows Hardware compatibility
- HLK
- architecture
- Secure Boot
- installer

“代码能编译”只是第一步。

---

## 11. x64 / ARM64

虚拟 audio driver 要按目标架构构建。

不能像 AnyCPU .NET 一样假设：

> 一个 kernel driver binary 同时原生支持 x64 和 ARM64。

---

## 12. Clock 与 Drift

虚拟设备最容易被低估的是：

> 谁定义 audio clock？

如果 virtual endpoint 与真实 hardware / network receiver 不共享 clock：

- buffer 会逐渐过满
- 或逐渐 underrun

需要：

- clock recovery
- resampling
- adaptive buffering

---

## 13. Latency

总 latency：

```text
app
+ virtual driver buffer
+ user/kernel transition
+ transport
+ receiver buffer
+ hardware
```

网络 jitter 还会引入额外 buffer。

---

## 14. 安全边界

虚拟 microphone 可以被其他应用当 microphone 使用。

产品必须清晰处理：

- privacy
- mute
- device naming
- default-device behavior
- uninstall cleanup

---

## 15. 官方资料

- SysVAD  
  https://github.com/microsoft/Windows-driver-samples/tree/main/audio/sysvad

- Audio Driver Samples  
  https://learn.microsoft.com/windows-hardware/drivers/samples/audio-driver-samples

- ACX Audio Class Extensions  
  https://learn.microsoft.com/windows-hardware/drivers/audio/acx-audio-class-extensions-overview

- Windows Audio Architecture  
  https://learn.microsoft.com/windows-hardware/drivers/audio/windows-audio-architecture
