# Audio Jacks、Connector、Jack Detection 与 Microphone Array

> 状态：🟢 Public Core Audio / WDK

Windows 不只知道“这是麦克风”或“这是耳机”。

底层 driver / topology 还可以描述：

- jack 颜色
- 物理位置
- connector 类型
- 是否插入
- channel mapping
- microphone array geometry

这些信息会影响：

- Windows UI
- endpoint creation
- diagnostics
- DeviceTopology

## 1. KSPROPERTY_JACK_DESCRIPTION

driver 可以通过：

```text
KSPROPERTY_JACK_DESCRIPTION
```

描述物理 jack。

返回：

```text
KSMULTIPLE_ITEM
+
KSJACK_DESCRIPTION[]
```

每个 jack 可描述：

- ChannelMapping
- Color
- ConnectionType
- GeoLocation
- GenLocation
- PortConnection
- IsConnected

## 2. Jack Presence Detection

如果 hardware 支持插孔检测：

```text
IsConnected
```

应准确反映是否插入设备。

如果不支持 presence detect：

```text
IsConnected = TRUE
```

因此：

> TRUE 不一定意味着硬件真的能检测到插入状态。

## 3. IKsJackDescription

用户态 DeviceTopology 提供：

```text
IKsJackDescription
```

应用可以通过 `IPart::Activate` 获取。

常用：

- GetJackCount
- GetJackDescription

这相当于给应用一个更方便的 Core Audio 包装，去访问底层 KS jack information。

## 4. IKsJackDescription2

Windows 7+ 增加：

```text
IKsJackDescription2
```

可以拿到：

- jack detection capability
- device state
- dynamic format change capability

## 5. KSJACK_SINK_INFORMATION

用于数字 display audio sink，例如：

- HDMI
- DisplayPort

可记录：

- connection type
- manufacturer ID
- product ID
- sink latency
- HDCP capability
- description

## 6. 为什么 Jack 信息很有用

例如 PC 后面板有：

- green
- pink
- blue
- black
- orange

应用可以用：

- color
- geo location
- connector type

帮用户区分真实物理 jack。

## 7. Microphone Array Geometry

Windows 还支持：

```text
KSPROPERTY_AUDIO_MIC_ARRAY_GEOMETRY
```

返回：

```text
KSAUDIO_MIC_ARRAY_GEOMETRY
```

内容包括：

- linear / planar / 3D
- microphone count
- frequency range
- microphone x/y/z coordinates
- working volume angle

## 8. 为什么 mic geometry 重要

对：

- beamforming
- source localization
- AEC
- speech capture

来说，只知道：

```text
2 microphones
```

远远不够。

算法需要知道：

> 两个 microphone 实际在设备上的空间位置。

## 9. ACX

ACX 也有：

```text
ACX_MIC_ARRAY_GEOMETRY
```

用于新 driver model 中描述 array geometry。

## 10. DeviceTopology 与 KS 的关系

```text
Driver / KS property
      ↓
AudioEndpointBuilder
      ↓
DeviceTopology
      ↓
IKsJackDescription
```

这是一条很典型的“driver metadata 进入用户态 API”的链路。

## 11. 官方资料

- Jack Description Property  
  https://learn.microsoft.com/windows-hardware/drivers/audio/jack-description-property

- IKsJackDescription  
  https://learn.microsoft.com/windows/win32/api/devicetopology/nn-devicetopology-iksjackdescription

- IKsJackDescription2  
  https://learn.microsoft.com/windows/win32/api/devicetopology/nn-devicetopology-iksjackdescription2

- KSPROPERTY_JACK_DESCRIPTION  
  https://learn.microsoft.com/windows-hardware/drivers/audio/ksproperty-jack-description

- Microphone Array Geometry Property  
  https://learn.microsoft.com/windows-hardware/drivers/audio/microphone-array-geometry-property

- KSPROPERTY_AUDIO_MIC_ARRAY_GEOMETRY  
  https://learn.microsoft.com/windows-hardware/drivers/audio/ksproperty-audio-mic-array-geometry
