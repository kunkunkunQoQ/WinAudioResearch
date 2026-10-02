# Audio Jack、Connector 与 Presence Detection

> 状态：🟢 Public API / Driver Documentation

Windows Audio UI 能显示：

- Front panel green jack
- Rear microphone
- Headphones plugged in
- HDMI sink

背后不只是 FriendlyName。

Driver 可以提供 jack / connector metadata。

---

## 1. DeviceTopology Jack API

常用：

```text
IKsJackDescription
IKsJackDescription2
IKsJackSinkInformation
```

这些接口从 user-mode DeviceTopology 访问 driver KS jack properties。

---

## 2. KSJACK_DESCRIPTION

字段包括：

- ChannelMapping
- Color
- ConnectionType
- GeoLocation
- GenLocation
- PortConnection
- IsConnected

因此一个 app 可以知道：

> “这是后面板绿色 3.5mm jack，并且现在有设备插入。”

---

## 3. ChannelMapping

例如 5.1 analog speaker 可能需要 3 个 stereo jack：

- Front L/R
- Center/LFE
- Rear L/R

每个 `KSJACK_DESCRIPTION` 可以记录自己的 channel mapping。

---

## 4. IsConnected

如果 hardware 支持 jack presence detection：

```text
IsConnected
```

反映当前是否插入设备。

如果 driver 不支持 detection：

> 文档规定它通常应报告 TRUE，而不是“未知”。

所以：

```text
IsConnected = TRUE
```

不一定等于 driver 真的有 presence sensor。

---

## 5. IKsJackDescription2

Windows 7+ 增加：

```text
IKsJackDescription2
```

提供：

- presence detection capability
- dynamic format change capability

这能帮助你区分：

> 一直 TRUE 是真的插着

还是：

> driver 根本不支持 presence detection。

---

## 6. KSPROPERTY_JACK_DESCRIPTION

Driver 侧：

```text
KSPROPERTY_JACK_DESCRIPTION
```

是 filter property，通常针对 bridge pin。

返回：

```text
KSMULTIPLE_ITEM
+
KSJACK_DESCRIPTION[]
```

---

## 7. IKsJackSinkInformation

适合 digital display sink。

例如：

- HDMI
- DisplayPort

可得到：

- connection type
- manufacturer/product ID
- sink description
- audio latency
- HDCP capability

---

## 8. 为什么 Mixer 工具不一定需要 Jack API

普通 volume mixer 的用户真正关心：

- endpoint name
- default role
- volume

没有必要一上来遍历 hardware topology。

Jack API 更适合：

- diagnostics
- driver tool
- OEM control panel
- audio device visualizer
- troubleshooting

---

## 9. Realtek / OEM Control Panel

很多 OEM audio control app 能显示：

- 哪个 jack 插入了什么
- jack retasking

部分信息就来自：

- HD Audio codec pin config
- driver KS properties
- vendor-specific extensions

并不都是 Core Audio FriendlyName。

---

## 10. 官方资料

- IKsJackDescription  
  https://learn.microsoft.com/windows/win32/api/devicetopology/nn-devicetopology-iksjackdescription

- IKsJackDescription2  
  https://learn.microsoft.com/windows/win32/api/devicetopology/nn-devicetopology-iksjackdescription2

- Jack Description Property  
  https://learn.microsoft.com/windows-hardware/drivers/audio/jack-description-property

- KSJACK_DESCRIPTION  
  https://learn.microsoft.com/windows-hardware/drivers/audio/ksjack-description

- KSPROPERTY_JACK_DESCRIPTION  
  https://learn.microsoft.com/windows-hardware/drivers/audio/ksproperty-jack-description
