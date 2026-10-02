# Core Audio 结构体 / 枚举 / 常量目录

> 状态：🟢 Public API  
> 目的：把开发中常见的“接口之外的数据类型”集中起来。

---

## Device / Endpoint

### EDataFlow

```text
eRender
eCapture
eAll
```

### ERole

```text
eConsole
eMultimedia
eCommunications
```

### EndpointFormFactor

常见：

- RemoteNetworkDevice
- Speakers
- LineLevel
- Headphones
- Microphone
- Headset
- Handset
- DigitalAudioDisplayDevice
- SPDIF
- HDMI
- UnknownDigitalPassthrough
- EndpointFormFactor

具体 enum 以当前 SDK 为准。

### DEVICE_STATE

常见 flags：

- ACTIVE
- DISABLED
- NOTPRESENT
- UNPLUGGED

---

## Session

### AudioSessionState

```text
Inactive
Active
Expired
```

### AudioSessionDisconnectReason

- DeviceRemoval
- ServerShutdown
- FormatChanged
- SessionLogoff
- SessionDisconnected
- ExclusiveModeOverride

### AUDIO_STREAM_CATEGORY

常见：

- Other
- Communications
- Alerts
- SoundEffects
- GameEffects
- GameMedia
- GameChat
- Speech
- Movie
- Media
- FarFieldSpeech
- UniformSpeech
- VoiceTyping

---

## WASAPI

### AudioClientProperties

用于 `IAudioClient2::SetClientProperties`。

重要字段概念：

- category
- options
- offload

### AUDCLNT_SHAREMODE

```text
Shared
Exclusive
```

### AUDCLNT_STREAMFLAGS_*

常见：

- CROSSPROCESS
- LOOPBACK
- EVENTCALLBACK
- NOPERSIST
- RATEADJUST
- AUTOCONVERTPCM
- SRC_DEFAULT_QUALITY

### AUDCLNT_STREAMOPTIONS

常见：

- RAW
- MATCH_FORMAT
- AMBISONICS
- POST_VOLUME_LOOPBACK

### AUDCLNT_BUFFERFLAGS

- DATA_DISCONTINUITY
- SILENT
- TIMESTAMP_ERROR

### AUDIO_DUCKING_OPTIONS

- DEFAULT
- DO_NOT_DUCK_OTHER_STREAMS

### AUDIO_EFFECT / AUDIO_EFFECT_STATE

用于公开 effect discovery / control。

---

## Activation / Process Loopback

### AUDIOCLIENT_ACTIVATION_PARAMS

决定：

- default activation
- process loopback activation

### AUDIOCLIENT_ACTIVATION_TYPE

包括：

- DEFAULT
- PROCESS_LOOPBACK

### AUDIOCLIENT_PROCESS_LOOPBACK_PARAMS

主要：

- TargetProcessId
- ProcessLoopbackMode

### PROCESS_LOOPBACK_MODE

- INCLUDE_TARGET_PROCESS_TREE
- EXCLUDE_TARGET_PROCESS_TREE

---

## EndpointVolume

### AUDIO_VOLUME_NOTIFICATION_DATA

通知内容包括：

- event context GUID
- mute state
- master volume
- channel count
- channel volumes

---

## DeviceTopology

### PartType

```text
Connector
Subunit
```

### DataFlow

DeviceTopology 自己的：

- In
- Out

不要和 MMDevice 的 EDataFlow 混淆。

### ConnectorType

描述 connector 类型。

### KSJACK_DESCRIPTION

- ChannelMapping
- Color
- ConnectionType
- GeoLocation
- GenLocation
- PortConnection
- IsConnected

### KSJACK_DESCRIPTION2

- DeviceStateInfo
- JackCapabilities

### KSJACK_SINK_INFORMATION

面向 HDMI / DP 等数字 sink。

---

## Audio Format

### WAVEFORMATEX

关键：

- format tag
- channel count
- sample rate
- avg bytes/sec
- block align
- bits/sample

### WAVEFORMATEXTENSIBLE

额外：

- valid bits
- channel mask
- SubFormat GUID

### KSAUDIO_SPEAKER_*

speaker channel mask constants。

---

## Spatial Audio

### AudioObjectType

描述：

- static spatial location
- dynamic object

### SPATIAL_AUDIO_STREAM_OPTIONS

spatial stream options。

### SpatialAudioObjectRenderStreamActivationParams

包含：

- ObjectFormat
- StaticObjectTypeMask
- MinDynamicObjectCount
- MaxDynamicObjectCount
- Category
- EventHandle
- NotifyObject

---

## APO

### APO_REG_PROPERTIES

APO registration metadata。

### APOInitSystemEffects / 2 / 3

不同 Windows 代际的 APO initialization context。

### AUDIO_SYSTEMEFFECT

Windows 11 controllable system effect：

- id
- canSetState
- state

---

## HRESULT / Status

除了通用 COM：

- `S_OK`
- `E_INVALIDARG`
- `E_POINTER`
- `E_NOINTERFACE`

Audio 常见：

- `AUDCLNT_E_DEVICE_INVALIDATED`
- `AUDCLNT_E_SERVICE_NOT_RUNNING`
- `AUDCLNT_E_UNSUPPORTED_FORMAT`
- `AUDCLNT_E_EXCLUSIVE_MODE_NOT_ALLOWED`
- `AUDCLNT_E_DEVICE_IN_USE`
- `AUDCLNT_E_BUFFER_SIZE_NOT_ALIGNED`
- `AUDCLNT_S_NO_SINGLE_PROCESS`

详见：
[HRESULT 与诊断](13-HRESULT-and-Diagnostics.md)

---

## 原则

不要自己“凭记忆”重定义结构大小。

优先核对：

```text
Windows SDK / WDK header
```

尤其：

- ARM64
- packing
- unions
- PROPVARIANT
- WAVEFORMATEXTENSIBLE
- raw COM ABI
