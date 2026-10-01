# Windows 11：AEC、Audio Effects Manager 与 System Effects Property Store

> 状态：🟢 Public Windows 11 APIs

Windows 11 为 audio effects / APO ecosystem 增加了一批非常重要的公开 API。

这些接口说明：

> 现代 Windows 已经不再只能靠 registry / OEM private API 去查询所有 audio effects。

---

## 1. IAudioEffectsManager

Header：

```text
audioclient.h
```

最低：

```text
Windows Build 22000
```

从：

```text
IAudioClient::GetService
```

取得。

能力：

- GetAudioEffects
- SetAudioEffectState
- RegisterAudioEffectsChangedNotificationCallback
- UnregisterAudioEffectsChangedNotificationCallback

---

## 2. AUDIO_EFFECT

结构：

```text
GUID id
BOOL canSetState
AUDIO_EFFECT_STATE state
```

effect GUID 由 Windows / KS 定义。

这让应用可以知道：

- 当前有哪些 effect
- 是否可修改
- 当前 on/off 状态

---

## 3. Deep Noise Suppression

Microsoft 当前文档示例明确展示：

```text
AUDIO_EFFECT_TYPE_DEEP_NOISE_SUPPRESSION
```

应用可以：

- 查询 effect 是否存在
- 判断 canSetState
- 尝试 SetAudioEffectState

需要处理：

- AUDCLNT_E_EFFECT_NOT_AVAILABLE
- AUDCLNT_E_EFFECT_STATE_READ_ONLY

---

## 4. IAcousticEchoCancellationControl

Header：

```text
audioclient.h
```

最低公开要求：

```text
Windows Build 22621
```

它允许 capture stream：

> 指定哪一个 render endpoint 用作 AEC reference stream。

---

## 5. 获取 AEC Control

流程：

```text
IMMDevice
  ↓ Activate IAudioClient
IAudioClient
  ↓ Initialize
  ↓ GetService(IID_IAcousticEchoCancellationControl)
IAcousticEchoCancellationControl
```

如果：

```text
GetService → E_NOINTERFACE
```

可能表示：

- endpoint 没有可控 AEC
- 或 AEC 存在但不允许 app 指定 reference endpoint

不能简单解释成：

> “Windows 没有 AEC”。

---

## 6. SetEchoCancellationRenderEndpoint

参数：

```text
endpointId
```

传：

```text
NULL
```

则让 Windows 自己选择 AEC reference render endpoint。

无效 endpoint：

```text
E_INVALIDARG
```

---

## 7. IAudioSystemEffectsPropertyStore

Header：

```text
mmdeviceapi.h
```

最低：

```text
Windows Build 22000
```

主要面向：

- OEM
- HSA
- audio-device configuration app

需要 restricted capability：

```text
audioDeviceConfiguration
```

---

## 8. 三种 Property Store

```text
DEFAULT
USER
VOLATILE
```

### DEFAULT

由 INF / default config 填充。

不保证跨 OS upgrade 保留。

### USER

用户 effect setting。

Windows 会在 upgrade / migration 中保留。

### VOLATILE

endpoint 每次进入 active 时清理。

适合 transient state。

---

## 9. 权限

普通非管理员 client：

- property store 写权限受限

管理员 client 可请求更高 STGM access。

此外 HSA API 还涉及 package restricted capability。

---

## 10. Notification

`IAudioSystemEffectsPropertyStore` 可以：

```text
RegisterPropertyChangeNotification
```

收到 property key 变化。

需要注意：

> 直接手改 registry 不会触发这个 notification；通过 IPropertyStore::SetValue 才会产生对应通知。

---

## 11. Windows 11 APO CAPX

Windows 11 对 APO 新增一组框架：

- AEC
- reference loopback
- settings
- notifications
- logging
- threading
- effects discovery / control

这使 modern APO ecosystem 更标准化。

---

## 12. Media Foundation 24H2 Integration

Windows 11 24H2 的 Media Foundation service interfaces 还加入：

- MF_ACOUSTIC_ECHO_CANCELLATION_CONTROL_SERVICE
- MF_AUDIO_EFFECTS_MANAGER_SERVICE

说明这些 audio effect controls 正逐渐进入更广的 Windows media pipeline。

---

## 13. 官方资料

- IAudioEffectsManager  
  https://learn.microsoft.com/windows/win32/api/audioclient/nn-audioclient-iaudioeffectsmanager

- IAcousticEchoCancellationControl  
  https://learn.microsoft.com/windows/win32/api/audioclient/nn-audioclient-iacousticechocancellationcontrol

- IAudioSystemEffectsPropertyStore  
  https://learn.microsoft.com/windows/win32/api/mmdeviceapi/nn-mmdeviceapi-iaudiosystemeffectspropertystore

- Windows 11 APIs for APO  
  https://learn.microsoft.com/windows-hardware/drivers/audio/windows-11-apis-for-audio-processing-objects
