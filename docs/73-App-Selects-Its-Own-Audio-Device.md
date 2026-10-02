# 应用选择自己的输出设备：公开 API 与系统级 Per-App Routing 的区别

> 状态：🟢 Public API + 🔴 System policy distinction

这是 Windows 音频开发中最容易混淆的概念之一。

“让**自己的应用**输出到指定设备”通常有公开 API。

“让**别的应用**默认输出到指定设备”则涉及系统 per-app policy，常见实现依赖未公开接口。

---

## 1. WASAPI：自己的应用直接打开指定 Endpoint

公开做法：

```text
IMMDeviceEnumerator
   ↓
EnumAudioEndpoints / GetDevice
   ↓
IMMDevice (target endpoint)
   ↓
Activate(IAudioClient)
   ↓
Initialize
```

此时：

> 你的 stream 天然就在这个 endpoint 上。

完全不需要改系统默认设备。

---

## 2. MediaPlayer.AudioDevice

WinRT / MediaPlayer：

```text
MediaPlayer.AudioDevice
```

可以设置一个：

```text
DeviceInformation
```

作为 MediaPlayer 使用的输出设备。

最低支持：

```text
Windows 10 Anniversary Update / 14393
```

---

## 3. AudioGraphSettings.PrimaryRenderDevice

AudioGraph：

```text
AudioGraphSettings.PrimaryRenderDevice
```

可以给整个 AudioGraph 指定主要 render device。

如果为 null：

> 使用系统默认 playback device。

---

## 4. 为什么这和 SonicRoute 不一样

如果你的 app 控制：

```text
自己的 stream
```

公开 API 足够。

SonicRoute 要做的是：

```text
给任意第三方应用设置 persisted endpoint preference
```

它不是那个第三方 app 自己创建 stream。

因此 Windows public WASAPI API 没有一个简单的：

```text
SetOtherProcessDefaultEndpoint(pid, device)
```

这才是 AudioPolicyConfig 研究存在的原因。

---

## 5. 三种场景

### 场景 A：我自己的播放器

公开：

```text
MediaPlayer.AudioDevice
或
IMMDevice → IAudioClient
```

### 场景 B：我自己的 AudioGraph

公开：

```text
AudioGraphSettings.PrimaryRenderDevice
```

### 场景 C：我要让 Chrome 下一次默认走某个音箱

这属于：

```text
system per-app audio policy
```

常见桌面实现进入：

🔴 AudioPolicyConfig

---

## 6. 不要为了自己的 App 修改系统默认设备

错误设计：

```text
我要让播放器从耳机播放
→ 先把 Windows 默认设备切成耳机
→ 播放
→ 再切回去
```

问题：

- 影响别的应用
- default-role race
- 用户体验差
- 可能触发设备 callback

正确：

> 直接让自己的 audio client 打开目标 endpoint。

---

## 7. Capture 同理

自己的 app 想录指定 microphone：

- 枚举 capture endpoint
- 打开指定 endpoint
- 建 capture client

不需要把 Windows 默认 microphone 改掉。

---

## 8. Modern WinRT Device Enumeration

设备来源通常：

```text
MediaDevice.GetAudioRenderSelector
      ↓
DeviceInformation.FindAllAsync
      ↓
choose DeviceInformation
```

再赋给：

- MediaPlayer.AudioDevice
- AudioGraph settings

---

## 9. Endpoint 消失后的恢复

即使 app 指定了 endpoint：

- USB unplug
- Bluetooth disconnect
- HDMI unplug

都可能 invalidated。

需要：

```text
device change
→ release old stream
→ re-enumerate
→ choose fallback
→ reinitialize
```

---

## 10. 官方资料

- MediaPlayer.AudioDevice  
  https://learn.microsoft.com/uwp/api/windows.media.playback.mediaplayer.audiodevice

- AudioGraphSettings.PrimaryRenderDevice  
  https://learn.microsoft.com/uwp/api/windows.media.audio.audiographsettings.primaryrenderdevice

- WASAPI  
  https://learn.microsoft.com/windows/win32/coreaudio/wasapi

- IMMDevice  
  https://learn.microsoft.com/windows/win32/api/mmdeviceapi/nn-mmdeviceapi-immdevice
