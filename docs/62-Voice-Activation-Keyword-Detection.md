# Voice Activation、Keyword Detection 与 Wake-on-Voice

> 状态：🟢 Public Driver / Platform Documentation

“Hey ...” 这类 voice activation 是 Windows 音频栈中很特殊的一类场景。

它的核心不是持续让普通桌面应用 24/7 录 microphone，而是：

- keyword spotter
- low-power capture path
- hardware / software detection
- privacy / power policy

---

## 1. Keyword Spotter

KWS：

```text
Keyword Spotter
```

监听短关键词，例如：

```text
"Hey Contoso"
```

检测到后，系统再启动更完整的 voice assistant experience。

---

## 2. Software Keyword Spotter

Windows 可以提供 software keyword spotting。

这仍需要：

- microphone input
- system policy
- voice activation framework

不是普通 app 自己在 background 开无限循环 capture 的同义词。

---

## 3. Hardware Keyword Detection

部分 SoC / DSP 支持低功耗 keyword detector。

好处：

- 主 CPU 休眠
- DSP 持续监听
- 低 power

---

## 4. Wake-on-Voice

如果 keyword 可以把设备从低功耗状态唤醒：

```text
Wake-on-Voice
```

这涉及：

- hardware
- driver
- power framework
- SoC support
- OEM integration

不是普通 app-only feature。

---

## 5. Multiple Voice Assistant

Microsoft 的 MVA framework 支持多个 voice assistant 场景。

官方文档明确：

> 实现 voice activation 通常是 SoC vendor / OEM 级别的重要工程项目。

---

## 6. SysVAD KeywordDetectorAdapter

SysVAD sample 包含：

```text
KeywordDetectorAdapter
```

用于展示 audio driver keyword detector integration。

---

## 7. Privacy

Voice activation 仍然和：

- microphone privacy
- user consent
- app capability

相关。

“低功耗硬件检测”不等于应用可以绕过 Windows privacy policy。

---

## 8. 与普通 Speech Recognition 区别

### Speech Recognition

应用已经 active：

```text
microphone
→ speech recognition
```

### Voice Activation

系统在更广的 lifecycle / power state：

```text
keyword
→ activate assistant
→ start full speech pipeline
```

---

## 9. DSP / AEC / Beamforming

语音助手设备还常结合：

- microphone array
- beamforming
- AEC
- noise suppression
- far-field speech mode

这些是独立技术模块，不应把 keyword spotting 当成完整 voice pipeline。

---

## 10. 官方资料

- Multiple Voice Assistant  
  https://learn.microsoft.com/windows-hardware/drivers/audio/voice-activation-mva

- Sample Audio Drivers / KeywordDetectorAdapter  
  https://learn.microsoft.com/windows-hardware/drivers/audio/sample-audio-drivers
