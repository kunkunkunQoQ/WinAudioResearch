# HDMI / DisplayPort / Digital Audio Endpoint

> 状态：🟢 Public driver / Core Audio documentation

HDMI / DisplayPort 音频 endpoint 和普通 analog speaker 最大区别之一是：

> audio sink capability 来自显示设备 / digital sink，而不是固定板载 codec。

## 1. 常见链路

```text
Application
  ↓
Windows Audio Engine
  ↓
GPU / display audio driver
  ↓
HDMI / DisplayPort
  ↓
Monitor / TV / AVR
```

所以 audio endpoint 可能随着：

- 显示器连接
- DP MST
- HDMI hotplug
- GPU driver reset
- docking station

动态出现 / 消失。

## 2. Endpoint Form Factor

Windows endpoint properties 中可看到：

```text
EndpointFormFactor.HDMI
```

这只是 UI / endpoint physical type 的一部分。

## 3. KSJACK_SINK_INFORMATION

Windows driver API 提供：

```text
KSJACK_SINK_INFORMATION
```

用于描述 display-related digital audio sink，例如：

- HDMI
- DisplayPort

字段包括：

- connection type
- manufacturer ID
- product ID
- audio latency
- HDCP capability
- sink description

## 4. Audio Latency

Digital sink 自己可能声明：

```text
AudioLatency
```

所以“WASAPI buffer latency”不是整个端到端 HDMI latency。

完整路径还包括：

- Windows buffer
- driver
- GPU transport
- display / AVR DSP
- speaker processing

## 5. Hot Plug

HDMI audio endpoint 生命周期通常和 display connection 强相关。

程序应正确处理：

```text
OnDeviceAdded
OnDeviceRemoved
OnDefaultDeviceChanged
DEVICE_INVALIDATED
```

而不是长期缓存一个 IMMDevice / IAudioClient。

## 6. Format Capability

数字 sink 可能支持：

- stereo PCM
- multichannel PCM
- encoded bitstream
- Dolby / DTS transport

具体能力取决于：

- display / AVR
- GPU audio driver
- EDID / sink information
- Windows audio policy

## 7. HDCP / Protected Content

某些受保护媒体路径会要求：

- HDCP
- protected output

因此“普通 loopback 能听见”不代表所有 DRM / protected stream 都允许被 capture。

## 8. S/PDIF

S/PDIF 同样属于 digital audio endpoint，但与 HDMI/DP 的 capability signaling 不完全相同。

常见用途：

- PCM stereo
- encoded passthrough

## 9. Endpoint Debugging 建议

记录：

```text
Endpoint ID
StableId
FriendlyName
FormFactor
DeviceFormat
PhysicalSpeakers
Default roles
GPU driver
Display model
HDMI / DP connection
```

## 10. 官方资料

- KSJACK_SINK_INFORMATION  
  https://learn.microsoft.com/windows-hardware/drivers/ddi/ksmedia/ns-ksmedia-_tagksjack_sink_information

- PKEY_AudioEndpoint_FormFactor  
  https://learn.microsoft.com/windows/win32/coreaudio/pkey-audioendpoint-formfactor

- Protected User Mode Audio (PUMA)  
  https://learn.microsoft.com/windows/win32/coreaudio/protected-user-mode-audio--puma-

- Protected Media Path  
  https://learn.microsoft.com/windows/win32/medfound/protected-media-path
