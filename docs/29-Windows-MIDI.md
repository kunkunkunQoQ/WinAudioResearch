# Windows MIDI：Legacy MIDI 与 Windows MIDI Services

> 状态：🟢 Public APIs + Microsoft official project

Windows MIDI 目前需要区分两代体系：

1. 传统 WinMM / WinRT MIDI 1.0
2. Windows MIDI Services（下一代 MIDI 1.0 + MIDI 2.0 / UMP）

---

## 1. 传统 MIDI Services

Win32 legacy API 主要：

- midiIn*
- midiOut*
- midiStream*
- MIDIHDR
- HMIDIIN
- HMIDIOUT

Microsoft 文档入口：

https://learn.microsoft.com/windows/win32/multimedia/midi-services

---

## 2. Windows Runtime MIDI

Windows 10 还提供过：

```text
Windows.Devices.Midi
```

适合 UWP / WinRT app。

它主要围绕 MIDI 1.0 设备与 message model。

---

## 3. Windows MIDI Services

Microsoft 当前官方项目：

https://github.com/microsoft/MIDI

项目定位：

> next-generation MIDI API for Windows

覆盖：

- MIDI 1.0
- MIDI 2.0
- MIDI-CI
- UMP
- new USB MIDI 2.0 driver
- transports
- tools
- diagnostics

---

## 4. UMP

MIDI 2.0 核心之一是：

```text
Universal MIDI Packet (UMP)
```

它使用 32-bit word packet structure，而不是传统 MIDI 1.0 byte stream 的简单模型。

---

## 5. 为什么新项目应该关注 Windows MIDI Services

相比传统 WinMM MIDI：

- 更现代 API
- MIDI 2.0
- UMP
- better timestamp / transport architecture
- service-based architecture
- modern device / endpoint abstraction

如果项目生命周期较长，不应只研究 `midiOutShortMsg`。

---

## 6. 兼容 MIDI 1.0

Windows MIDI Services 并不是“只支持 MIDI 2.0”。

Microsoft 项目明确包含：

- MIDI 1.0
- MIDI 2.0

并提供兼容 / transport 层。

---

## 7. Driver / Transport

新体系不只有 app SDK。

还包含：

- USB MIDI 2.0 class driver
- service
- transports
- plugins
- diagnostics tools

这和传统简单的 `midiOutOpen` 模型完全不同。

---

## 8. 开发资料

官方入口：

https://aka.ms/midi

官方 GitHub：

https://github.com/microsoft/MIDI

---

## 9. Legacy API 仍然为什么存在

因为：

- 大量 DAW / tools
- 旧 hardware
- 旧 plugin / MIDI device
- compatibility

所以研究仓库应该同时保留：

```text
Legacy MIDI 1.0
+
Modern Windows MIDI Services
```

而不是简单标记“旧 API = 不需要”。

---

## 10. 参考

- Windows MIDI Services  
  https://github.com/microsoft/MIDI

- Docs  
  https://aka.ms/midi

- Legacy MIDI Services  
  https://learn.microsoft.com/windows/win32/multimedia/midi-services
