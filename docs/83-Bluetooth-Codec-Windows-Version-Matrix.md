# Bluetooth Audio Codec / Windows Version Matrix

> 状态：🟢 Microsoft documented platform behavior  
> 本页专门记录 Windows Bluetooth Classic Audio codec 与 profile 的版本支持，避免把“设备支持某 codec”误写成“Windows 一定会使用”。

---

## 1. A2DP Codec 支持矩阵

根据 Microsoft 当前 Bluetooth Classic Audio 文档：

| Codec | Windows 10 | Windows 11 | 备注 |
|---|---|---|---|
| SBC | 1507+ | 21H2+ | A2DP 基础 codec |
| aptX Classic | 1507+ | 21H2+ | 需要 host 与 audio device 双方支持 |
| AAC | 不支持 | 21H2+ | Windows 11 加入 |
| aptX Adaptive (lossless) | 不支持 | 24H2+ | 仅部分具有兼容 Qualcomm Bluetooth radio 的 Windows 设备 |

Windows 会从其支持列表中选择：

> host 与 audio device 共同支持的第一个 codec。

所以：

```text
Headset supports AAC
```

并不等于：

```text
Windows 10 will use AAC
```

---

## 2. A2DP 只负责输出

A2DP：

```text
Host
  ↓
high-quality stereo playback
  ↓
Bluetooth audio device
```

它不提供 microphone capture。

一旦应用需要使用耳机 microphone，Classic Bluetooth 需要使用：

```text
HFP
```

---

## 3. HFP

Hands-Free Profile 支持：

- monaural playback
- monaural capture
- simultaneous communication path

Windows 支持：

### Narrowband

```text
8 kHz
CVSD
```

### Wideband

```text
16 kHz
mSBC
```

Microsoft 当前文档记录：

- Windows 10 1703+ 支持 wideband HFP
- Windows 11 21H2+ 支持，22H2 改进 compatibility

---

## 4. 为什么打开 Mic 后音质会变化

Classic Bluetooth headset 常见：

### Mic 未使用

```text
A2DP
→ stereo
→ higher-quality media playback
```

### Mic 打开

```text
HFP
→ mono playback
+
mono capture
```

因此用户常感知：

- stereo → mono
- bandwidth 下降
- music quality 明显降低

这是 Classic Bluetooth profile architecture，不是单纯 Windows volume bug。

---

## 5. Windows 10 vs Windows 11 Endpoint UX

Windows 10 常暴露：

```text
Headphones (Stereo)
Headset (Hands-Free)
Headset Microphone
```

Windows 11 更倾向统一 device experience，并根据实际 stream/category 自动 profile switch。

因此：

> 不应仅根据 FriendlyName 推断当前 Bluetooth radio 实际正在跑 A2DP 还是 HFP。

---

## 6. Communications Category

应用创建：

```text
AudioCategory_Communications
```

等 communications stream 时，Windows policy 可以影响：

- Bluetooth profile
- HFP selection
- speech processing
- ducking

所以 media player 和 VoIP app 在相同 Bluetooth headset 上可能出现完全不同的 transport behavior。

---

## 7. LE Audio

Bluetooth LE Audio 不使用传统 A2DP/HFP 数据面。

主要涉及：

- BAP
- TMAP
- PACS
- ASCS
- LE Isochronous channels
- LC3 family

Windows LE Audio 走的是更新的 driver / ACX / vendor-specific path。

因此不要把：

```text
LE Audio = 新版 A2DP
```

理解成同一 stack。

---

## 8. Codec Diagnostics 的限制

Windows public app API 并没有始终提供一个简单、跨所有设备版本稳定的：

```text
GetCurrentBluetoothCodec()
```

普通应用更多从：

- endpoint behavior
- format
- driver/device info
- Bluetooth diagnostics

间接判断。

做 codec 显示工具时要避免未经验证地从：

- sample rate
- FriendlyName

反推 codec。

---

## 9. 测试矩阵

建议：

```text
Windows 10 22H2
Windows 11 21H2
Windows 11 22H2
Windows 11 23H2
Windows 11 24H2

SBC-only headset
AAC headset
aptX Classic headset
aptX Adaptive compatible platform

Playback only
Playback + microphone
Communications category
Media category
```

---

## 10. 官方资料

- Bluetooth Classic Audio  
  https://learn.microsoft.com/windows-hardware/drivers/bluetooth/bluetooth-classic-audio

- Bluetooth LE Audio  
  https://learn.microsoft.com/windows-hardware/drivers/bluetooth/bluetooth-low-energy-audio

- Communications Audio Format Capabilities  
  https://learn.microsoft.com/windows/win32/coreaudio/communications-audio-format-capabilities
