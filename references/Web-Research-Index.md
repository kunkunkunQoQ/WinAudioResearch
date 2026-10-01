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
- [x] AppContainer / packaged app model basics
- [ ] low-integrity / sandbox edge cases
- [ ] protected process edge cases

### Diagnostics

- [x] HRESULT
- [x] ETW
- [x] WPR / WPA
- [x] HLK
- [ ] dedicated audio ETW provider/event catalog
- [ ] glitch ETL analysis examples
- [ ] ProcMon / registry diagnostics map

## 本轮新增完成

- [x] AppContainer / MSIX / desktop packaging audio basics
- [x] AEC control / IAudioEffectsManager / system-effects property store
- [x] Deep Noise Suppression public effect identity
- [x] IAudioStateMonitor
- [x] IAudioClientDuckingControl / IAudioViewManagerService timeline
- [x] Windows SDK audio header catalog
- [x] C# / Python / Rust / Go / C++ bindings and wrappers
- [x] virtual audio device / network audio architecture
- [x] Windows audio developer tools
- [x] RDP / remote audio
- [x] WaveRT / ACX deep dives
- [x] driver INF → endpoint/effects configuration
- [x] audio testing / latency / fidelity
- [x] exclusive / bit-perfect caveats
- [x] ARM64 audio / WDK
- [x] driver signing / distribution
- [x] services / Session 0
- [x] expanded WASAPI HRESULT catalog

## 下一轮检索目标

- Windows audio ETW provider / event catalog
- glitch ETL analysis examples
- ProcMon / public-vs-internal registry diagnostics map
- Bluetooth codec / LE Audio Windows-version matrix
- endpoint property complete symbolic catalog
- low-integrity / sandbox / protected-process edge cases
- Voice Clarity / platform speech processing deeper notes
- AAX / CLAP / JACK-on-Windows context
- more open-source virtual cable / virtual mixer drivers
- audio test-signal / latency measurement tools
- .NET source-generated COM / CsWin32 audio interop
- C++/WinRT and WIL patterns for Core Audio
- Thunderbolt / PCIe professional audio specifics
- Remote Desktop / Cloud PC endpoint behavior experiments
- Windows ARM64 real-device regression matrix
