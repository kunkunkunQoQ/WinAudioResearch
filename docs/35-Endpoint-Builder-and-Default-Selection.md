# AudioEndpointBuilder 与 Windows 默认音频设备选择

> 状态：🟢 Public Driver Documentation + 🟡 Windows implementation behavior

为什么插入一个 USB 耳机后，Windows 有时自动把它设成默认设备，有时不会？

答案不只是：

> “谁最后插入谁默认”。

Windows 有 AudioEndpointBuilder 和默认 endpoint ranking / policy。

---

## 1. AudioEndpointBuilder

Windows 服务：

```text
AudioEndpointBuilder
```

负责：

- 发现底层 audio device
- 分析 KS topology
- 创建 software audio endpoints
- endpoint form factor
- endpoint properties
- active / disabled state
- 默认选择所需信息

---

## 2. Endpoint vs PnP Device

一个物理 / PnP audio adapter：

可能产生多个：

- speaker endpoint
- headphone endpoint
- microphone endpoint
- digital endpoint
- communications endpoint

所以：

```text
PnP device
≠
IMMDevice endpoint 1:1
```

---

## 3. 默认设备选择优先级

Microsoft 官方默认 endpoint selection 文档描述的流程包括：

1. 找应用特定 preferred default endpoint
2. 找用户设置的 system preferred default
3. 否则按 endpoint ranking / heuristic

这意味着 Windows 10 起 per-app preference 也参与默认 endpoint 选择逻辑。

---

## 4. Ranking Factors

Windows 10 文档列出的因素包括：

- Jack detection capability
- Form factor
- KSNodeType
- Bus type
- General location
- Geometric location
- Subtype-specific factor

Windows 给这些 factor 加权，形成 endpoint rank。

---

## 5. Jack Detection

支持 jack detection 的 endpoint 往往具有更高优先级。

USB / Bluetooth endpoint 在 Windows heuristic 中也被视为具备相应动态连接信息。

---

## 6. Form Factor

常见：

- Headphones
- Headset
- Speakers
- Microphone
- LineLevel
- HDMI / DigitalAudioDisplayDevice
- SPDIF

不同 role 的优先级不同。

例如：

- communications 更偏好 headset / handset
- console playback 可能偏好 headphones / speakers

---

## 7. Console vs Communications

Windows 对：

- console
- communications

使用不同 ranking 逻辑。

这再次说明：

> “默认设备”不是一个全局 string。

---

## 8. PKEY_AudioDevice_NeverSetAsDefaultEndpoint

驱动 / endpoint 可以参与“不要自动成为默认设备”的策略。

这类 property 对虚拟设备特别重要。

否则安装一个虚拟 endpoint 可能意外抢走用户默认设备。

---

## 9. EnableEndpointByDefault

`PKEY_AudioDevice_EnableEndpointByDefault` 可影响某些 endpoint 默认创建为 enabled / disabled 的行为。

这是驱动 / endpoint 配置层，不是普通应用 UI 设置。

---

## 10. 和 undocumented IPolicyConfig 的关系

EndpointBuilder / ranking 解释的是：

> Windows 自己如何决定默认 endpoint。

`IPolicyConfig.SetDefaultEndpoint` 则是桌面工具常用于：

> 强制写入用户默认选择。

两者不是同一个层次。

---

## 11. 官方资料

- Default Audio Endpoint Selection  
  https://learn.microsoft.com/windows-hardware/drivers/audio/default-audio-endpoint-selection

- Audio Endpoint Builder Algorithm  
  https://learn.microsoft.com/windows-hardware/drivers/audio/audio-endpoint-builder-algorithm

- PKEY_AudioDevice_EnableEndpointByDefault  
  https://learn.microsoft.com/windows-hardware/drivers/audio/pkey-audiodevice-enableendpointbydefault

- EndpointFormFactor  
  https://learn.microsoft.com/windows/win32/api/mmdeviceapi/ne-mmdeviceapi-endpointformfactor
