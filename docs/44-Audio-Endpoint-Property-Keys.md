# Audio Endpoint Property Keys：设备属性开发索引

> 状态：🟢 Public API

Windows audio endpoint 的 PropertyStore 不只有 FriendlyName。

很多调试和设备识别能力都来自 property keys。

## 1. 读取原则

传统桌面应用：

```text
IMMDevice::OpenPropertyStore
        ↓
IPropertyStore::GetValue
        ↓
PROPVARIANT
```

Microsoft 当前也建议现代应用优先考虑：

```text
Windows.Devices.Enumeration
```

读取设备属性。

## 2. 不建议随意写 PropertyStore

Microsoft Core Audio 文档明确：

> audio service 管理这些 endpoint properties，client 应读取而不是随意设置。

很多属性来自：

- driver
- INF
- AudioEndpointBuilder
- audio service

## 3. PKEY_Device_FriendlyName

用途：

- UI display name

不要作为永久唯一 ID。

## 4. PKEY_AudioEndpoint_StableId

这是非常值得开发者关注的属性。

普通：

```text
IMMDevice::GetId
```

返回的 endpoint ID 可能在：

- OS update
- driver update

后变化。

`PKEY_AudioEndpoint_StableId` 的目标则是：

> Windows 尝试跨 OS / driver 更新保留这个 opaque identifier。

适合：

- 记住用户选过的 microphone
- 记住 preferred speaker
- device re-association

但它仍应该被当作 opaque value，而不是自行解析。

## 5. PKEY_AudioEndpoint_FormFactor

描述：

- Speakers
- Headphones
- Microphone
- Headset
- HDMI
- SPDIF
- LineLevel
- Handset
- ...

可用于 UI 分类。

## 6. PKEY_AudioEndpoint_PhysicalSpeakers

描述 physical speaker configuration / channel mask。

适合：

- multichannel UI
- speaker layout diagnostics

## 7. PKEY_AudioEndpoint_FullRangeSpeakers

表示哪些 physical speaker 被认为是 full range。

与 bass management / speaker configuration 相关。

## 8. PKEY_AudioEndpoint_Disable_SysFx

历史上用于描述 shared-mode system effects enable/disable 状态。

不要简单把它当成：

> 所有 modern APO effect 的唯一总开关。

新 Windows effect model 还有：

- processing modes
- APO
- IAudioEffectsManager
- OEM effect state

## 9. PKEY_AudioEngine_DeviceFormat

描述 Audio Engine 对 endpoint 的 shared-mode device format。

这对诊断：

- sample rate
- channel count
- bit depth
- WAVEFORMATEXTENSIBLE

很有价值。

## 10. PKEY_AudioEngine_OEMFormat

OEM / INF 提供的 default device format。

它和用户当前选择 / engine runtime format 不应直接混为一谈。

## 11. PKEY_AudioEndpoint_Supports_EventDriven_Mode

可用于描述 endpoint 是否支持 event-driven mode。

低延迟 / WASAPI 研究中很有价值。

## 12. PKEY_AudioEndpoint_JackSubType

描述 output jack category GUID。

可辅助理解：

- headphones
- speaker
- line out
- digital connector

## 13. PKEY_AudioEndpoint_Association

用于关联：

- KS pin category
- audio endpoint

更偏 driver / topology diagnostics。



## 14. 现代 DeviceInformation 的 6 个音频属性

Windows.Devices.Enumeration 的官方音频设备属性目前重点公开 6 个：

- `System.Devices.AudioDevice.Microphone.SensitivityInDbfs`
- `System.Devices.AudioDevice.Microphone.SensitivityInDbfs2`
- `System.Devices.AudioDevice.Microphone.SignalToNoiseRatioInDb`
- `System.Devices.AudioDevice.SpeechProcessingSupported`
- `System.Devices.AudioDevice.RawProcessingSupported`
- `System.Devices.MicrophoneArray.Geometry`

这些属性适合在 `DeviceInformation` 枚举时通过 additionalProperties 请求。

其中多个属性同时存在 Shell / Property System 的 `PKEY_Devices_*` 形式。本仓库在 `api/audio-properties.csv` 同时记录现代 canonical name 与 PROPERTYKEY，避免把两套命名误认为两种不同能力。

## 15. Driver INF / FxPropertyStore 属性

设备属性还需要区分另一类来源：驱动安装和 APO effects 配置。

常见分组：

```text
Endpoint / engine
  PKEY_AudioEngine_OEMFormat
  PKEY_AudioEngine_OEMPeriod
  PKEY_AudioEndpoint_Default_VolumeInDb

APO placement
  PKEY_FX_StreamEffectClsid
  PKEY_FX_ModeEffectClsid
  PKEY_FX_EndpointEffectClsid

Composite APO
  PKEY_CompositeFX_StreamEffectClsid
  PKEY_CompositeFX_ModeEffectClsid
  PKEY_CompositeFX_EndpointEffectClsid

Offload / Keyword detector
  PKEY_FX_Offload_*
  PKEY_CompositeFX_Offload_*
  PKEY_*_KeywordDetector_*

Processing modes
  PKEY_SFX_ProcessingModes_Supported_For_Streaming
  PKEY_MFX_ProcessingModes_Supported_For_Streaming
  PKEY_EFX_ProcessingModes_Supported_For_Streaming
```

这些 key 很多是 **driver / INF / FxPropertyStore contract**，不能因为最终能在某个 property store 看到，就把它们当作普通应用可随意修改的设置项。

完整结构化索引：

- `api/audio-properties.csv`

## 16. 属性来源要分层

建议 dump 工具至少把属性标成：

```text
Endpoint runtime property
PnP / Device property
Modern DeviceInformation property
Driver INF policy
APO / FxPropertyStore
Observed / undocumented
```

这样能避免最常见的错误：看到一个 GUID + propID 就假设它属于同一套 public app API。

## 17. 调试工具建议

做 endpoint property dump 时，建议至少输出：

```text
PROPERTYKEY
VARTYPE
raw value
friendly symbolic name
source category
```

不要只 hardcode 5 个 property。

## 18. 官方资料

- Audio Endpoint Properties  
  https://learn.microsoft.com/windows/win32/coreaudio/audio-endpoint-properties

- Device Properties  
  https://learn.microsoft.com/windows/win32/coreaudio/device-properties

- PKEY_AudioEndpoint_StableId  
  https://learn.microsoft.com/windows/win32/coreaudio/pkey-audioendpoint-stableid

- PKEY_AudioEndpoint_FormFactor  
  https://learn.microsoft.com/windows/win32/coreaudio/pkey-audioendpoint-formfactor

- Audio device information properties  
  https://learn.microsoft.com/windows/uwp/audio-video-camera/audio-device-information-properties

- Audio INF file settings  
  https://learn.microsoft.com/windows-hardware/drivers/audio/audio-inf-file-settings
