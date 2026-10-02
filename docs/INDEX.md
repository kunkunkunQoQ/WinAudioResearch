# WinAudioResearch 文档总索引

> 这是仓库的**主题式导航**。  
> 文件名前的数字最初用于阅读顺序；随着资料规模扩大和多批专题并行补充，数字已不再保证唯一。  
> **请以文件名与主题分类为准，不要把数字前缀当作稳定 ID。**

---

## API Database / 机器可读接口库

长文档之外，仓库维护独立的结构化 API 数据库：

- [API Database overview](../api/README.md)
- [Coverage](../api/COVERAGE.md)
- [Machine-readable catalog](../api/catalog.json)
- [MMDevice](../api/core-mmdevice.csv)
- [WASAPI](../api/wasapi.csv)
- [Audio Session](../api/audio-session.csv)
- [EndpointVolume](../api/endpoint-volume.csv)
- [DeviceTopology](../api/device-topology.csv)
- [Spatial Audio](../api/spatial-audio.csv)
- [Media Foundation](../api/media-foundation.csv)
- [XAudio2](../api/xaudio2.csv)
- [MIDI](../api/midi.csv)
- [APO](../api/apo.csv)
- [WinRT Audio](../api/winrt-audio.csv)
- [Audio properties](../api/audio-properties.csv)
- [HRESULT](../api/hresults.csv)
- [Undocumented](../api/undocumented.csv)
- [WaveRT](../api/wavert.csv)
- [ACX](../api/acx.csv)
- [KS Audio](../api/ks-audio.csv)
- [Audio Formats](../api/audio-formats.csv)
- [Windows Capabilities](../api/windows-capabilities.csv)
- [Build Dependencies](../api/dependencies.csv)
- [Official Samples](../api/samples.csv)

查询工具：

```bash
python scripts/query_api.py IAudioClient
python scripts/query_api.py --status Undocumented
```

---

## 1. 从这里开始

- [Windows Audio 架构与接口地图](00-Windows-Audio-Architecture.md)
- [Glossary / 术语表](17-Glossary.md)
- [Windows Audio API 选择指南](33-API-Decision-Guide.md)
- [Digital Audio Fundamentals for Windows Developers](57-Digital-Audio-Fundamentals-for-Windows-Developers.md)
- [Microsoft 官方 Windows Audio 文档总索引](18-Microsoft-Official-Documentation-Index.md)
- [API Reference Matrix](11-API-Reference-Matrix.md)
- [Windows SDK Audio Header Catalog](66-Windows-SDK-Audio-Header-Catalog.md)
- [Core Audio / WASAPI Interface Catalog](64-Core-Audio-Interface-Catalog.md)
- [Core Audio Structures / Enums Catalog](66-Core-Audio-Structures-Enums-Catalog.md)

---

## 2. Device / Endpoint / MMDevice

- [MMDevice：设备枚举、默认端点与属性](01-MMDevice.md)
- [设备变化与通知机制](05-Device-Notifications.md)
- [系统默认音频设备](07-Default-Audio-Device.md)
- [Device IDs & Properties](12-Device-IDs-and-Properties.md)
- [DeviceTopology](20-DeviceTopology.md)
- [AudioEndpointBuilder / 默认设备选择](35-Endpoint-Builder-and-Default-Selection.md)
- [Modern Device Enumeration / MediaCapture](36-Modern-Device-Enumeration-and-MediaCapture.md)
- [Audio Endpoint Property Keys](44-Audio-Endpoint-Property-Keys.md)
- [Jacks / Connectors / Microphone Arrays](49-Jacks-Connectors-and-Microphone-Arrays.md)
- [Audio Jacks / Connectors / Detection](53-Audio-Jacks-Connectors-Detection.md)
- [MediaDevice Default Device Events](61-MediaDevice-Default-Device-Events.md)
- [App Selects Its Own Audio Device](73-App-Selects-Its-Own-Audio-Device.md)
- [EndpointVolume Advanced](76-EndpointVolume-Advanced.md)
- [Modern Core Audio API Timeline](67-Modern-Core-Audio-API-Timeline.md)

---

## 3. Audio Session / Mixer / Volume / Policy

- [Audio Session：应用音频会话](02-Audio-Sessions.md)
- [Windows 音量与静音](03-Volume-and-Mute.md)
- [IAudioMeterInformation / Audio Meter](04-Audio-Meter.md)
- [按应用音频路由](06-Per-App-Audio-Routing.md)
- [Session Enumeration Edge Cases](15-Session-Enumeration-Edge-Cases.md)
- [Audio Session Persistence / Ducking](40-Audio-Session-Persistence-and-Ducking.md)
- [Stream Categories / Ducking / AudioStateMonitor](50-Stream-Categories-Ducking-AudioStateMonitor.md)
- [Audio State Monitor](63-Audio-State-Monitor.md)
- [Audio Stream Categories / Client Properties](68-Audio-Stream-Categories-and-Client-Properties.md)
- [Audio Session Identity / Grouping](71-Audio-Session-Identity-and-Grouping.md)
- [Audio Session Disconnect / Recovery](59-Audio-Session-Disconnect-Recovery.md)
- [Audio Device Lifecycle / Recovery](73-Audio-Device-Lifecycle-and-Recovery.md)

---

## 4. WASAPI / IAudioClient / Render / Capture

- [WASAPI 与 IAudioClient](08-WASAPI.md)
- [WASAPI 深入](19-WASAPI-Advanced.md)
- [Low Latency / RAW / Offload](26-Low-Latency-Raw-Offload.md)
- [Loopback / Process Audio Capture](27-Loopback-and-Process-Audio-Capture.md)
- [WASAPI Buffer Flags / Glitches](60-WASAPI-Buffer-Flags-and-Glitches.md)
- [WASAPI Auto Convert / Resampling](69-WASAPI-Auto-Convert-Resampling.md)
- [AudioClock / Drift / Synchronization](70-AudioClock-Drift-and-Synchronization.md)
- [Exclusive Mode / Bit-perfect Audio](77-Exclusive-Mode-and-Bit-Perfect-Audio.md)
- [WASAPI HRESULT Troubleshooting Catalog](82-WASAPI-HRESULT-Troubleshooting-Catalog.md)
- [Realtime Audio Threading / MMCSS](56-Realtime-Audio-Threading-and-MMCSS.md)
- [Audio Testing / Measurement](76-Audio-Testing-and-Measurement.md)

---

## 5. Audio Effects / APO / Voice Processing

- [Audio Processing Objects (APO)](23-Audio-Processing-Objects-APO.md)
- [Audio Effects / Processing Modes](34-Audio-Effects-and-Processing-Modes.md)
- [Voice AEC / Noise Suppression / AGC](49-Voice-AEC-Noise-Suppression.md)
- [Microphone / Communications Audio](55-Microphone-Communications-Audio.md)
- [Windows 11 AEC / Effects APIs](64-Windows11-AEC-and-Effects-APIs.md)
- [APO Interface Catalog](65-APO-Interface-Catalog.md)
- [Audio Effects Property Store / Device Modules](68-Audio-Effects-PropertyStore-and-DeviceModules.md)
- [Deep Noise Suppression / Modern Speech Effects](72-Deep-Noise-Suppression-and-Modern-Speech-Effects.md)
- [IAudioEffectsManager](74-IAudioEffectsManager.md)
- [Voice Activation / Keyword Detection](50-Voice-Activation-and-Keyword-Detection.md)
- [Voice Activation / Keyword Detection — supplementary](62-Voice-Activation-Keyword-Detection.md)

---

## 6. High-Level Audio / Media APIs

- [AudioGraph / Windows.Media.Audio](21-AudioGraph-and-WinRT-Audio.md)
- [Media Foundation Audio](24-Media-Foundation-Audio.md)
- [XAudio2](28-XAudio2.md)
- [Windows MIDI / MIDI 2.0](29-Windows-MIDI.md)
- [Legacy Windows Audio APIs](30-Legacy-Windows-Audio-APIs.md)
- [ACM / DMO / MFT / Codecs](46-ACM-DMO-MFT-Codecs.md)
- [VST3 Plug-in Ecosystem](53-VST3-Plugin-Ecosystem.md)
- [Language Bindings / Wrappers](60-Language-Bindings-and-Wrappers.md)

---

## 7. Spatial / Formats / Digital Transport

- [Spatial Audio / Windows Sonic](22-Spatial-Audio.md)
- [WAVEFORMATEX / WAVEFORMATEXTENSIBLE / Channel Mask](31-Audio-Formats-WAVEFORMAT.md)
- [HDMI / DisplayPort / Digital Audio](43-HDMI-DisplayPort-Digital-Audio.md)
- [IEC61937 / Digital Bitstream Audio](75-IEC61937-Digital-Bitstream-Audio.md)
- [Digital Audio Fundamentals](57-Digital-Audio-Fundamentals-for-Windows-Developers.md)

---

## 8. Hardware / Drivers / Transport

- [Audio Driver Stack：WDM / WaveRT / KS / ACX](25-Audio-Driver-Stack-WDM-WaveRT-ACX-KS.md)
- [Bluetooth Classic / LE Audio](41-Bluetooth-Audio-Classic-LE.md)
- [USB Audio / UAC1 / UAC2](42-USB-Audio.md)
- [HDMI / DisplayPort / Digital Audio](43-HDMI-DisplayPort-Digital-Audio.md)
- [Audio Power Management](47-Audio-Power-Management.md)
- [ASIO / Pro Audio](48-ASIO-and-Pro-Audio.md)
- [Audio Device Modules / HSA](51-Audio-Device-Modules-and-HSA.md)
- [Virtual Audio Device Development](51-Virtual-Audio-Device-Development.md)
- [Kernel Streaming / AVStream / KSStudio](52-Kernel-Streaming-AVStream-KSStudio.md)
- [Audio HLK Testing / Certification](54-Audio-HLK-Testing-and-Certification.md)
- [Virtual Audio Devices / Network Audio](61-Virtual-Audio-Devices-and-Network-Audio.md)
- [WaveRT Deep Dive](70-WaveRT-Deep-Dive.md)
- [ACX Deep Dive](71-ACX-Deep-Dive.md)
- [Kernel Streaming Deep Dive](74-Kernel-Streaming-Deep-Dive.md)
- [ACX Public Header Coverage Audit](97-ACX-Public-Header-Coverage-Audit.md)
- [KS Audio Property Set Coverage](98-KS-Audio-Property-Set-Coverage.md)
- [Audio Driver INF / Endpoint Configuration](75-Audio-Driver-INF-and-Endpoint-Configuration.md)
- [Windows ARM64 Audio Development](79-Windows-ARM64-Audio-Development.md)
- [Driver Signing / Distribution](80-Driver-Signing-and-Distribution.md)
- [Services / Session 0 / Windows Audio](81-Services-Session0-and-Windows-Audio.md)

---

## 9. Privacy / Security / Remote / Protected Audio

- [Microphone Privacy / Protected Audio](52-Microphone-Privacy-and-Protected-Audio.md)
- [Microphone Privacy / Permissions](58-Microphone-Privacy-Permissions.md)
- [Protected Audio / PUMA](67-Protected-Audio-PUMA.md)
- [RDP / Remote Desktop Audio](57-RDP-Remote-Desktop-Audio.md)
- [Remote Desktop / Remote Audio](69-Remote-Desktop-and-Remote-Audio.md)
- [App Model / MSIX / AppContainer Audio](65-AppModel-MSIX-AppContainer-Audio.md)

---

## 10. Diagnostics / Compatibility / Testing

- [Windows Version Compatibility](10-Windows-Version-Compatibility.md)
- [HRESULT & Diagnostics](13-HRESULT-and-Diagnostics.md)
- [COM Threading & Apartments](14-COM-Threading-and-Apartments.md)
- [Research Validation Checklist](16-Research-Validation-Checklist.md)
- [Microsoft Official Audio Samples / Tools](32-Microsoft-Audio-Samples-and-Tools.md)
- [Headers / Libraries / DLLs](37-Headers-Libraries-DLLs.md)
- [ETW / WPR / WPA Diagnostics](45-Audio-ETW-WPR-WPA-Diagnostics.md)
- [Windows Audio Debugging Toolkit](54-Windows-Audio-Debugging-Toolkit.md)
- [Compatibility / Regression Matrix](56-Compatibility-Regression-Matrix.md)
- [Windows Audio Developer Tools](62-Windows-Audio-Developer-Tools.md)
- [Windows Audio Version Capability Matrix](78-Windows-Audio-Version-Capability-Matrix.md)
- [Audio Testing / Measurement](76-Audio-Testing-and-Measurement.md)
- [WASAPI HRESULT Troubleshooting Catalog](82-WASAPI-HRESULT-Troubleshooting-Catalog.md)

---

## 11. Ecosystem / Open Source / Learning Resources

- [Third-Party Windows Audio Ecosystem](38-Third-Party-Audio-Ecosystem.md)
- [Open-source Windows Audio Codebases](58-Open-Source-Windows-Audio-Codebases.md)
- [Community Articles / Learning Resources](59-Community-Articles-and-Learning-Resources.md)
- [Community Engineering Resources](63-Community-Engineering-Resources.md)
- [Language Bindings / Wrappers](60-Language-Bindings-and-Wrappers.md)
- [Undocumented / Reverse Engineering Index](55-Undocumented-and-Reverse-Engineering-Index.md)

External source hubs:

- [../resources/README.md](../resources/README.md)
- [../references/README.md](../references/README.md)
- [../references/Web-Research-Index.md](../references/Web-Research-Index.md)

---

## 12. Undocumented Windows Audio

These documents are intentionally separated from the public API catalog.

- [Undocumented overview](../undocumented/README.md)
- [AudioPolicyConfig](../undocumented/AudioPolicyConfig.md)
- [IAudioPolicyConfigFactory](../undocumented/IAudioPolicyConfigFactory.md)
- [System PolicyConfig / SetDefaultEndpoint](../undocumented/System-PolicyConfig.md)

Related research findings:

- [PolicyConfig Role vs DataFlow](../findings/PolicyConfig-Role-vs-DataFlow.md)
- [Per-App Routing Persistence](../findings/Per-App-Routing-Persistence.md)

---

## 13. SonicRoute 实战研究

- [SonicRoute 已验证结论](../findings/SonicRoute.md)
- [COM 生命周期](../findings/COM-Lifetime.md)
- [Known Pitfalls](../findings/Known-Pitfalls.md)
- [PolicyConfig 参数语义复核](../findings/PolicyConfig-Role-vs-DataFlow.md)
- [Per-App Routing Persistence](../findings/Per-App-Routing-Persistence.md)

---

## 14. 维护约定

以后新增文档：

1. 文件名优先使用可读主题名；
2. 数字前缀仅作为历史排序提示，不作为唯一标识；
3. 必须加入本页某个主题分类；
4. Public / Observed / Undocumented 状态必须明确；
5. Public API 优先引用 Microsoft Learn / Windows SDK / WDK；
6. 第三方和 reverse-engineering 来源不得覆盖成“官方事实”；
7. Windows Build 敏感的结论要记录版本；
8. 重叠文章可以保留，但必须通过本索引明确各自定位。


---

## 15. 近期扩展专题（83–98）

这些文章是根据 2026 年最新 Microsoft 文档与专业音频生态继续补充的专题，后续会继续并入上面的主题分类。

- [Bluetooth Codec / Windows Version Matrix](83-Bluetooth-Codec-Windows-Version-Matrix.md)
- [Modern Audio DeviceInformation Properties](84-Modern-Audio-DeviceInformation-Properties.md)
- [Windows 11 Voice Clarity](85-Voice-Clarity-Windows-11.md)
- [Audio HLK Fidelity / Glitch / Latency Tests](86-Audio-HLK-Fidelity-Glitch-Latency-Tests.md)
- [Windows Built-in Audio Codecs Version Notes](87-Windows-Built-in-Audio-Codecs-Version-Notes.md)
- [Microsoft Audio ETW / CollectAudioLogs](88-Microsoft-Audio-ETW-Logging-Tools.md)
- [Modern .NET Win32 / COM Interop](89-Modern-DotNet-Win32-COM-Interop.md)
- [Modern C++ COM Patterns：WIL / WRL / C++/WinRT](90-Modern-Cpp-COM-Patterns-WIL-WRL-CppWinRT.md)
- [CLAP Audio Plug-in Format](91-CLAP-Audio-Plugin-Format.md)
- [AAX / JACK / Pro Audio Host Ecosystem](92-AAX-JACK-and-Pro-Audio-Host-Ecosystem.md)


- [ProcMon / Audio Registry Diagnostics](93-ProcMon-and-Audio-Registry-Diagnostics.md)
- [AppContainer / Low Integrity / Protected Capture Boundaries](94-AppContainer-Low-Integrity-and-Protected-Capture-Boundaries.md)
- [Audio Glitch ETL Analysis Workflow](95-Audio-Glitch-ETL-Analysis-Workflow.md)
- [Thunderbolt / PCIe Pro Audio on Windows](96-Thunderbolt-PCIe-Pro-Audio-on-Windows.md)
