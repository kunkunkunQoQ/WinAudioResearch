# IAudioEffectsManager：应用侧查询与控制 Audio Effects

> 状态：🟢 Public API  
> Windows Build 22000+。

Windows 11 给普通 audio client 增加了一套更现代的 effect discovery / control API：

```text
IAudioEffectsManager
```

它和“实现 APO”不是一回事。

---

## 1. 获取方式

从已建立 stream 的：

```text
IAudioClient
```

通过：

```text
GetService
```

取得 `IAudioEffectsManager`。

---

## 2. GetAudioEffects

返回当前 stream 关联的 effect 列表。

每个：

```text
AUDIO_EFFECT
```

包含：

- effect GUID
- state
- canSetState

---

## 3. SetAudioEffectState

可请求：

```text
ON
OFF
```

但前提：

- effect 存在
- effect state 可修改

否则可能返回：

```text
AUDCLNT_E_EFFECT_NOT_AVAILABLE
AUDCLNT_E_EFFECT_STATE_READ_ONLY
```

---

## 4. Effects Changed Notification

接口：

```text
IAudioEffectsChangedNotificationClient
```

应用可以注册 callback。

当：

- effect list 变化
- state 变化
- effect resource availability 变化

时得到通知。

---

## 5. 为什么 effect 会动态变化

可能因为：

- endpoint 切换
- processing mode 改变
- microphone / communications state
- OEM DSP resource
- user setting
- hardware capability

所以不要在 stream 初始化时读一次后永久缓存。

---

## 6. Deep Noise Suppression

Microsoft 官方示例展示：

```text
AUDIO_EFFECT_TYPE_DEEP_NOISE_SUPPRESSION
```

应用可通过 IAudioEffectsManager：

- 找到 effect
- 检查 canSetState
- 请求启用 / 禁用

Windows 11 24H2 增加 Deep Noise Suppression effect identifier。

但不是每台机器都会有实际 implementation。

---

## 7. 它不等于“系统总 EQ API”

IAudioEffectsManager 是：

> associated stream 的 effect manager。

不是：

> 全系统统一的任意 DSP 插件管理器。

OEM endpoint effect、system effect、processing mode 都可能影响最终 list。

---

## 8. 和 IAudioSystemEffects3 区别

### Application

```text
IAudioEffectsManager
```

用于：

- discover
- query
- request state

### APO Implementation

```text
IAudioSystemEffects3
```

用于：

- APO 暴露 controllable system effects
- effect implementation / vendor side

---

## 9. 和 AudioSystemEffectsPropertyStore 区别

`IAudioEffectsManager`：

> 当前 stream 的 effect state/control。

`IAudioSystemEffectsPropertyStore`：

> endpoint effect configuration store，主要面向 OEM/HSA，且需要 restricted capability。

---

## 10. 官方资料

- IAudioEffectsManager  
  https://learn.microsoft.com/windows/win32/api/audioclient/nn-audioclient-iaudioeffectsmanager

- SetAudioEffectState  
  https://learn.microsoft.com/windows/win32/api/audioclient/nf-audioclient-iaudioeffectsmanager-setaudioeffectstate

- Windows 11 APIs for APO  
  https://learn.microsoft.com/windows-hardware/drivers/audio/windows-11-apis-for-audio-processing-objects
