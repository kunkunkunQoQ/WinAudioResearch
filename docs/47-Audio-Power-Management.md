# Windows Audio Power Management

> 状态：🟢 Public driver documentation

Audio driver / hardware 不只是“播放时工作，停止时什么都不管”。

Modern Windows 特别重视：

- idle power
- D-state
- DSP offload
- Modern Standby
- Bluetooth / audio offload

## 1. Device Power State

典型：

```text
D0 = fully on
D1/D2 = intermediate
D3 = low/off state
```

正确 audio driver 应在没有工作时允许 hardware 进入更低功耗。

## 2. PortCls Idle Power

PortCls 支持 registry power settings：

- ConservationIdleTime
- PerformanceIdleTime
- IdlePowerState

可分别针对：

- battery
- AC

定义 idle behavior。

## 3. Modern Standby

在 Modern Standby 平台：

audio device 应在无需求时进入低功耗状态。

但以下场景可能重新唤醒：

- notification sound
- voice activation
- background audio
- communications
- keyword detection

## 4. Audio Offload

硬件 offload 允许：

- DSP / hardware engine 持续播放
- CPU / main SoC 更长时间休眠

典型目标：

- music playback
- long-duration media
- low power

## 5. Bluetooth Sideband

Bluetooth A2DP / HFP sideband 也可以利用 DSP path：

```text
system memory
→ burst to DSP
→ sideband to Bluetooth controller
```

减少 host CPU 持续介入。

## 6. ACX Power Management

ACX 使用 WDF / KMDF power behavior。

驱动应正确实现：

- power-up
- startup
- power-down
- surprise removal
- idle management
- D3Hot / D3Cold

## 7. Power Bug 的表现

常见：

- laptop standby 掉电异常
- audio device 一直 D0
- 播放结束后仍高功耗
- resume 后 endpoint 消失
- device invalidated
- first sound after idle 延迟 / pop

## 8. ETW / WPA

Microsoft 推荐使用：

```text
ETW + Xperf/WPR + WPA
```

验证 D-state transitions。

## 9. 应用层也会影响功耗

即使 driver 正确，应用如果：

- 永远保持 WASAPI stream open
- 高频 polling
- 维持 capture
- 不释放 IAudioClient

也可能让 audio device 无法 idle。

所以常驻 audio tool 应明确：

> 没有必要时不要保持真正 active audio stream。

## 10. SonicRoute 类工具

仅做：

- session enumeration
- volume
- notifications

通常不需要长期创建 active PCM stream。

实时 meter 可以通过 session meter，而不是为了 meter 自己启动 loopback capture。

这能显著减少功耗 / audio graph 干扰。

## 11. 官方资料

- PortCls Registry Power Settings  
  https://learn.microsoft.com/windows-hardware/drivers/audio/portcls-registry-power-settings

- Audio subsystem power management for Modern Standby  
  https://learn.microsoft.com/windows-hardware/design/device-experiences/audio-subsystem-power-management-for-modern-standby-platforms

- ACX Power Management  
  https://learn.microsoft.com/windows-hardware/drivers/audio/acx-power-management

- Hardware-Offloaded Audio Processing  
  https://learn.microsoft.com/windows-hardware/drivers/audio/hardware-offloaded-audio-processing
