# Audio Device Modules、DSP Configuration 与 Hardware Support App

> 状态：🟢 Public Windows driver / WinRT API

很多 OEM audio control app 并不是直接去读写一个“神秘 registry key”。

Windows 10 1703+ 提供 Audio Device Module 通信机制，用于让 app 与：

- driver module
- DSP module
- audio hardware processing block

通信。

## 1. Audio Module 是什么

Microsoft 定义：

> 相对独立、原子化的音频处理逻辑单元。

可能存在于：

- audio driver
- hardware DSP
- APO
- smart amplifier
- vendor processing block

## 2. AudioDeviceModulesManager

WinRT：

```text
Windows.Media.Devices.AudioDeviceModulesManager
```

可以：

- 获取 module collection
- query module
- send command
- receive result
- listen for changes

## 3. 为什么需要它

OEM 系统可能有：

- DSP EQ
- beamformer
- amplifier
- noise processor
- proprietary effect

用户需要一个 control app。

传统做法容易变成：

- private IOCTL
- private registry
- private service

Audio Device Modules 给出一套更标准化的 communication model。

## 4. Restricted Capability

应用需要：

```text
audioDeviceConfiguration
```

restricted capability。

这不是普通商店 app 默认就能随意使用的能力。

## 5. Targeting

module 可以关联到：

- KS wave filter
- initialized KS pin / stream

普通 HSA 通常访问 filter-level module。

stream-targeted module 更偏：

- APO
- active stream processing

## 6. Driver 侧

driver 通过新的 KS property set 暴露 module。

Windows 再把它映射给：

```text
Windows.Media.Devices
```

client。

## 7. Notification

driver module 状态变化后可以触发系统 notification，再映射成 app callback。

这适合：

- DSP parameter changed
- hardware state changed
- effect setting changed

## 8. 和 APO 的关系

Audio Module 不等于 APO。

但：

> APO 可以是 module 的一个例子。

更一般地，module 也可以是：

- driver logic
- hardware DSP block

## 9. HSA

Hardware Support App 常见职责：

- endpoint configuration
- OEM audio settings
- module control
- diagnostics
- firmware / DSP configuration

## 10. 官方资料

- Configure and Query Audio Device Modules  
  https://learn.microsoft.com/windows-hardware/drivers/audio/configure-and-query-audiodevicemodules

- Implementing Audio Module Communication  
  https://learn.microsoft.com/windows-hardware/drivers/audio/implementing-audio-module-communication

- AudioDeviceModulesManager  
  https://learn.microsoft.com/uwp/api/windows.media.devices.audiodevicemodulesmanager
