# Audio Driver INF → Endpoint / APO / Format 配置链

> 状态：🟢 Public WDK

一个 endpoint 的大量默认行为在 driver installation / INF 阶段就已经配置。

```text
Driver INF
  ↓
device / interface properties
  ↓
AudioEndpointBuilder
  ↓
Endpoint PropertyStore / Effects Store
  ↓
IMMDevice / Windows Sound UI / Audio Engine
```

## Device Format

`PKEY_AudioEngine_OEMFormat` 由 OEM / INF 提供 default stream format。用户随后可以在 Windows Sound Control Panel 修改当前 format，因此要区分 OEM default、current device format 和 WASAPI mix format。

`PKEY_AudioEngine_DeviceFormat` 描述 Audio Engine shared-mode device format。

## Event-driven support

`PKEY_AudioEndpoint_Supports_EventDriven_Mode` 可由 OEM / driver 配置，用来描述 endpoint 的 event-driven capability。

## Form Factor 与默认选择

Driver / endpoint config 可以告诉 Windows endpoint 是 Speakers、Headphones、Microphone、Headset、HDMI、SPDIF 等。这会影响 Windows UI 和默认 endpoint ranking。

## Default Software Volume

`PKEY_AudioEndpoint_Default_VolumeInDb` 可配置没有 hardware volume node 的 endpoint 的初始软件音量。

## APO Registration

常见 effects properties：

- `PKEY_FX_StreamEffectClsid`
- `PKEY_FX_ModeEffectClsid`
- `PKEY_FX_EndpointEffectClsid`

Windows 新版还支持 composite FX，使同一 SFX/MFX/EFX placement 可包含多个 effect。

APO 还应声明支持的 processing modes，例如 DEFAULT、MEDIA、MOVIE、COMMUNICATIONS、SPEECH、RAW。

## Endpoint Extension UI

`PKEY_AudioEndpoint_ControlPanelPageProvider` 可关联 endpoint configuration/property page provider。

## 为什么不应直接改内部 Registry

ProcMon 可能看到 endpoint property、effects store、policy store 的实际 registry 位置，但 storage location 不等于 public API contract。Driver / HSA 应优先使用 INF、documented property API、HSA API 与 APO framework。

## 对 Virtual Audio Driver 的意义

虚拟 endpoint 需要认真定义：

- form factor
- friendly name
- default format
- supported formats
- default volume
- effects
- roles
- jack / topology
- endpoint properties

“能出声”并不等于符合 Windows audio UX。

## 官方资料

- Audio Endpoint Properties  
  https://learn.microsoft.com/windows/win32/coreaudio/audio-endpoint-properties
- PKEY_AudioEngine_OEMFormat  
  https://learn.microsoft.com/windows-hardware/drivers/audio/pkey-audioengine-oemformat
- Implementing APOs  
  https://learn.microsoft.com/windows-hardware/drivers/audio/implementing-audio-processing-objects
- Composite Endpoint FX  
  https://learn.microsoft.com/windows-hardware/drivers/audio/pkey-compositefx-endpointeffectclsid
- Default Volume in dB  
  https://learn.microsoft.com/windows-hardware/drivers/audio/pkey-audioendpoint-default-volumeindb
