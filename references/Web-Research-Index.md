# Web Research Index

> WinAudioResearch 的目标不是“收藏几个教程”，而是建立 Windows 音频开发资料地图。  
> 本页维护持续检索范围，避免仓库长期只偏向某一种 API。

## 已覆盖的信息源

### Microsoft

- Microsoft Learn / Win32 Core Audio
- Windows Driver Audio docs
- Windows App / WinRT media docs
- Windows Performance Toolkit
- Windows HLK
- Media Foundation
- XAudio2
- MIDI
- Microsoft official GitHub samples
- Microsoft Docs source repositories

### Standards / Vendors

- USB-IF
- Bluetooth SIG
- Steinberg VST / ASIO
- OpenAL ecosystem

### Mature Open Source

- NAudio
- EarTrumpet
- SonicRoute
- WinAudioRoute
- CSCore
- SoundSwitch
- JUCE
- PortAudio
- miniaudio
- FFmpeg
- libsndfile
- SDL
- OpenAL Soft

### Community / Blogs

- Mark Heath audio / NAudio articles
- Windows Developer Blog historical audio articles
- GitHub Issues / discussions
- Stack Overflow / Microsoft Q&A as hypothesis sources

## 技术范围 Checklist

### Core Audio

- [x] MMDevice
- [x] Audio Session
- [x] EndpointVolume
- [x] Meter
- [x] Notifications
- [x] DeviceTopology
- [x] PropertyStore

### Streaming

- [x] WASAPI shared
- [x] WASAPI exclusive
- [x] IAudioClient2
- [x] IAudioClient3
- [x] event-driven
- [x] loopback
- [x] process loopback
- [x] IAudioClock
- [x] MMCSS

### Modern Windows Audio

- [x] AudioGraph
- [x] MediaCapture
- [x] DeviceInformation
- [x] Spatial Audio
- [x] Audio effects discovery

### Media / Codec

- [x] Media Foundation
- [x] Source Reader / Sink Writer
- [x] MFT
- [x] DMO
- [x] ACM
- [x] resampler
- [x] common Windows codecs

### Driver / Hardware

- [x] WDM
- [x] WaveRT
- [x] PortCls
- [x] KS
- [x] ACX
- [x] APO
- [x] AudioEndpointBuilder
- [x] offload
- [x] power management
- [x] HLK

### Hardware Transport

- [x] USB Audio
- [x] Bluetooth Classic
- [x] Bluetooth LE Audio
- [x] HDMI / DisplayPort
- [x] analog jack detection
- [x] microphone array
- [ ] Thunderbolt / PCIe pro audio specifics

### Pro Audio

- [x] ASIO
- [x] VST3
- [x] JUCE
- [x] PortAudio
- [ ] AAX
- [ ] CLAP
- [ ] JACK on Windows historical context

### MIDI

- [x] WinMM MIDI
- [x] WinRT MIDI
- [x] Windows MIDI Services
- [x] MIDI 2.0 / UMP

### Security / Policy

- [x] microphone privacy
- [x] PMP / PUMA
- [x] per-app endpoint policy
- [x] system default policy
- [ ] AppContainer / low integrity edge cases
- [ ] protected process edge cases

### Diagnostics

- [x] HRESULT
- [x] ETW
- [x] WPR / WPA
- [x] HLK
- [ ] dedicated audio ETW provider/event catalog
- [ ] glitch ETL analysis examples
- [ ] ProcMon / registry diagnostics map

## 下一轮检索目标

- Windows audio ETW provider catalog
- Bluetooth codec / LE Audio Windows-version matrix
- endpoint property complete dump
- AppContainer audio restrictions
- Windows service / registry map
- AEC / Voice Clarity / CAPX deeper notes
- pro audio AAX / CLAP / JACK context
- virtual cable / virtual mixer open-source driver implementations
- audio test signal / latency measurement tools
- Windows Store / MSIX audio capability differences
- .NET COM source generation for Core Audio
- Rust / Python / C++ Windows audio wrappers
- Go bindings
- Windows ARM64 audio toolchain and driver notes
