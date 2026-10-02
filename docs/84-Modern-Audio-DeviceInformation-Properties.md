# Modern Audio DeviceInformation Properties

> 状态：🟢 Public Windows API  
> Microsoft 页面最近更新：2026-05-23。

传统 Core Audio 开发者很容易只关注：

```text
IMMDevice + IPropertyStore
```

现代 Windows 还通过：

```text
Windows.Devices.Enumeration.DeviceInformation
```

暴露一批对 audio / microphone 很有价值的 property。

---

## 1. Microphone Sensitivity

### System.Devices.AudioDevice.Microphone.SensitivityInDbfs

类型：

```text
Double
```

含义：

> microphone sensitivity，以 dBFS 表示。

---

## 2. SensitivityInDbfs2

```text
System.Devices.AudioDevice.Microphone.SensitivityInDbfs2
```

类型：

```text
Double
```

从 Windows 10 1803 起可用。

Microsoft 描述：

- 在 fixed hardware gain 后测量
- 假设 software gain 为 0 dB

相比旧 sensitivity property，更适合现代 microphone calibration / voice-processing capability 描述。

---

## 3. SignalToNoiseRatioInDb

```text
System.Devices.AudioDevice.Microphone.SignalToNoiseRatioInDb
```

类型：

```text
Double
```

描述 microphone SNR。

适合：

- voice quality
- device diagnostics
- array / built-in mic capability display

不要把它当成应用运行时实时 SNR meter。

它是 device information property。

---

## 4. SpeechProcessingSupported

```text
System.Devices.AudioDevice.SpeechProcessingSupported
```

类型：

```text
Boolean
```

表示 audio device 是否支持 speech processing。

它可以帮助 app 判断：

- speech-oriented processing capability

但不等于：

> 当前 stream 一定已经启用了 AEC / NS / AGC。

真正 effect state 还应结合：

- processing mode
- IAudioEffectsManager
- stream category
- driver/APO capability

---

## 5. RawProcessingSupported

```text
System.Devices.AudioDevice.RawProcessingSupported
```

类型：

```text
Boolean
```

表示 endpoint 是否支持 raw processing。

对于：

- measurement
- custom DSP
- ML preprocessing
- pro audio

非常有价值。

---

## 6. MicrophoneArray.Geometry

```text
System.Devices.MicrophoneArray.Geometry
```

类型：

```text
byte[]
```

描述 microphone array geometry。

这对：

- beamforming
- far-field speech
- Voice Clarity
- array diagnostics

有意义。

---

## 7. 为什么 DeviceInformation Property 值得单独研究

传统 Audio Endpoint property 更多关注：

- endpoint identity
- form factor
- format
- speakers
- effects

现代 DeviceInformation property 可以进一步描述：

- microphone quality
- speech capability
- raw capability
- microphone array geometry

所以一个完整 audio diagnostics tool 最终可以同时整合：

```text
IMMDevice PropertyStore
+
DeviceInformation Properties
```

---

## 8. Property 查询

通常流程：

```text
DeviceInformation.FindAllAsync(selector, requestedProperties)
```

显式请求目标 property key。

不要假设所有 extended property 默认都会被返回。

---

## 9. Availability

不同 property：

- 可能不存在
- driver/OEM 没有声明
- 旧 Windows 不支持

正确处理：

```text
property missing
≠
false / 0
```

应该区分：

- unsupported
- not reported
- reported false/value

---

## 10. 和 StableId 的关系

这批 modern properties 和：

```text
PKEY_AudioEndpoint_StableId
```

解决不同问题。

StableId：

> endpoint identity stability。

DeviceInformation audio properties：

> endpoint/audio hardware capability / quality metadata。

---

## 11. 官方资料

- Audio device information properties  
  https://learn.microsoft.com/windows/uwp/audio-video-camera/audio-device-information-properties

- Enumerate devices  
  https://learn.microsoft.com/windows/apps/develop/devices-sensors/enumerate-devices

- Device information properties  
  https://learn.microsoft.com/windows/apps/develop/devices-sensors/device-information-properties
