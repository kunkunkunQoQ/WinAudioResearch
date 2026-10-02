# Virtual Audio Device：虚拟扬声器、虚拟麦克风到底怎么做

> 状态：🟢 Microsoft driver documentation + engineering guidance

很多项目都会出现这个需求：

> 我想创建一个 Windows 里真正可选的虚拟扬声器 / 虚拟麦克风。

关键结论：

> 普通 user-mode C# / C++ 应用不能只靠 MMDevice / WASAPI “创建一个真正 audio endpoint”。

真正 endpoint 通常来自 audio driver。

---

## 1. Windows 里的虚拟 Audio Endpoint

目标效果：

```text
Windows Sound Settings
    ↓
Virtual Speaker
Virtual Microphone
```

它需要系统看到：

- audio device interface
- KS / WaveRT / ACX circuit
- topology
- format
- endpoint property

然后 AudioEndpointBuilder 创建对应 software endpoint。

---

## 2. Microsoft 官方起点：SysVAD

Microsoft：

```text
System Virtual Audio Device Driver Sample (SysVAD)
```

是研究虚拟音频设备最重要的官方样例。

它展示：

- multiple endpoints
- WaveRT
- audio offload
- topology
- virtual hardware abstraction
- APO integration

官方 sample：

https://github.com/microsoft/Windows-driver-samples/tree/main/audio/sysvad

---

## 3. Simple Audio Sample

如果 SysVAD 太复杂：

https://github.com/microsoft/Windows-driver-samples/tree/main/audio/simpleaudiosample

更适合第一次理解：

- speaker
- microphone
- WDM audio driver structure

---

## 4. ACX 路线

Microsoft 新的 Audio Class Extensions：

```text
ACX
```

可以用于新 audio driver framework。

概念：

- ACXDEVICE
- ACXCIRCUIT
- ACXSTREAM
- ACXPIN
- ACXELEMENT

但目前并不是所有旧 WDM / PortCls 场景都自动“应该迁移到 ACX”。

---

## 5. 虚拟播放设备做 DSP

常见架构：

```text
App outputs to Virtual Speaker
          ↓
Virtual Audio Driver
          ↓
user/kernel DSP path
          ↓
Real Speaker
```

难点：

- sample transport
- format conversion
- clock / latency
- default device behavior
- session visibility
- power
- driver signing
- uninstall / upgrade
- crash recovery

所以“做一个虚拟设备”远比“做一个 audio mixer UI”复杂。

---

## 6. 虚拟麦克风

典型：

```text
App-generated PCM
      ↓
Virtual Mic Driver
      ↓
Discord / browser / game capture
```

如果目标是让第三方 app 把它当 microphone：

> 必须提供真正 capture endpoint。

普通“把声音播放到 real microphone”不是同一概念。

---

## 7. User-mode pipeline 的替代方案

如果你不需要真正 endpoint，只需要：

- 自己程序内处理
- capture + DSP + render
- system loopback analyzer

可以不用 driver。

例如：

```text
WASAPI Capture
   ↓
DSP
   ↓
WASAPI Render
```

但第三方 app 不会看到一个新的 microphone / speaker。

---

## 8. Driver Signing

真正发布 audio driver 还涉及：

- INF
- package
- signing
- Windows Hardware Program / attestation / certification
- Secure Boot compatible signing

这不是一般 EXE 分发流程。

---

## 9. 安装与卸载

必须考虑：

- endpoint 残留
- default device 被切走
- driver update
- reboot requirement
- device instance cleanup
- rollback

虚拟设备程序如果 uninstall 后把用户默认 speaker 留在不存在 endpoint 上，体验会非常差。

---

## 10. 测试

至少测试：

- x64
- ARM64
- Windows 10/11
- shared mode
- exclusive mode
- default role
- session enumeration
- system loopback
- suspend/resume
- driver restart
- install/update/uninstall

---

## 11. 官方资料

- Sample Audio Drivers  
  https://learn.microsoft.com/windows-hardware/drivers/audio/sample-audio-drivers

- SysVAD Virtual Audio Device Driver Sample  
  https://learn.microsoft.com/samples/microsoft/windows-driver-samples/sysvad-virtual-audio-device-driver-sample/

- Audio Driver Samples  
  https://learn.microsoft.com/windows-hardware/drivers/samples/audio-driver-samples

- ACX Overview  
  https://learn.microsoft.com/windows-hardware/drivers/audio/acx-audio-class-extensions-overview
