# Windows Audio HLK、Driver Testing 与 Certification

> 状态：🟢 Public Windows Hardware testing documentation

如果你写的是：

- audio driver
- virtual audio endpoint
- OEM audio device
- USB / HDMI / Bluetooth audio stack

“应用里能响”远远不够。

Microsoft 有 Windows Hardware Lab Kit：

```text
HLK
```

用于 hardware / driver compatibility testing。

## 1. Windows HLK

HLK 用于：

- Windows hardware compatibility
- driver tests
- system tests
- certification submission

适用于：

- Windows 10
- Windows 11
- Windows Server

## 2. Device.Audio Tests

Audio 相关 test 会覆盖：

- endpoint streaming
- jack detection
- glitch
- fidelity
- device behavior
- HDMI / DisplayPort
- system fundamentals

## 3. Zero Glitch

Microsoft audio logo tests 中包含 zero-glitch validation。

如果失败：

不能简单说：

> “Windows 太严格”。

应该排查：

- driver
- buffer
- DPC / ISR
- hardware
- power transition
- APO
- format change

## 4. Fidelity

Fidelity test 可能涉及：

- THD+N
- cable setup
- analog loop path
- device setup

因此 test environment 配错也会造成 false-looking failure。

## 5. Jack Detection

HLK 还会验证：

- jack presence
- connected / disconnected
- endpoint state

所以：

```text
KSPROPERTY_JACK_DESCRIPTION
```

不只是“给 Windows UI 好看”。

它会参与真实 compatibility behavior。

## 6. HDMI / DisplayPort

HLK troubleshooting 文档特别提醒：

测试前要确保：

- HDMI endpoint connected
- DisplayPort endpoint connected
- SPDIF endpoint connected
- playback / capture 能实际 streaming

这说明 digital endpoint 也是完整 audio test matrix 的一部分。

## 7. HLK Filter / Errata

如果：

- HLK test 本身有已知问题
- OS test 有 false failure

Microsoft 会发布：

- HLK filters
- errata

所以不能因为一次 test failure 就立刻改 driver。

应先核对：

- target build
- current HLK version
- filters
- errata

## 8. Audio Driver 开发流程建议

```text
Driver builds
   ↓
Basic endpoint test
   ↓
WASAPI streaming
   ↓
format / role / jack test
   ↓
ETW / glitch test
   ↓
HLK
   ↓
cross-build regression
```

## 9. Virtual Audio Driver 也应该测什么

至少：

- render/capture
- default role
- session creation
- exclusive/shared
- event-driven
- format negotiation
- sleep/resume
- service restart
- uninstall/reinstall
- ARM64/x64
- HLK applicable tests

## 10. 官方资料

- Windows Hardware Lab Kit  
  https://learn.microsoft.com/windows-hardware/test/hlk/

- Troubleshooting Audio Testing  
  https://learn.microsoft.com/windows-hardware/test/hlk/testref/troubleshooting-audio-testing

- Audio Driver Samples  
  https://learn.microsoft.com/windows-hardware/drivers/samples/audio-driver-samples
