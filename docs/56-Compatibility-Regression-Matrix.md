# Windows Audio Compatibility / Regression Matrix 规范

> 目标：长期记录 Windows Build、架构、设备、driver 与 undocumented API 行为。

如果 WinAudioResearch 只写：

> “Windows 11 可用”

很快会失去价值。

真正有用的是：

> 哪个 Build、哪个驱动、哪个接口、什么结果。

---

## 1. Public API Matrix

建议字段：

| Field | Example |
|---|---|
| OS | Windows 11 |
| Build | 26100.x |
| Arch | x64 |
| Device | USB DAC |
| Driver | usbaudio2.sys |
| API | IAudioClient3 |
| Operation | InitializeSharedAudioStream |
| Result | Success |
| HRESULT | 0x00000000 |
| Notes | 2.5 ms period |

---

## 2. Undocumented Matrix

增加：

| Field | Example |
|---|---|
| Activatable class | Windows.Media.Internal.AudioPolicyConfig |
| IID | ... |
| Vtable slot | 25 |
| Role | Multimedia |
| Flow | Render |
| Device ID format | full interface path |
| Persistence | survives app restart |
| Regression | no |

---

## 3. Endpoint Matrix

记录：

- IMMDevice ID
- StableId
- FriendlyName
- FormFactor
- transport
- driver
- default roles
- event-driven support
- device format
- jack capability

---

## 4. Transport Matrix

类型：

- HDA
- USB Audio 1
- USB Audio 2
- Bluetooth A2DP
- Bluetooth HFP
- Bluetooth LE Audio
- HDMI
- DisplayPort
- Virtual
- Remote / RDP

行为可能不同。

---

## 5. Architecture Matrix

至少：

- x64
- ARM64

需要特别验证：

- PROPVARIANT layout
- raw vtable delegate
- native DLL
- COM marshalling
- driver availability

---

## 6. Windows Branch

建议不要只写：

```text
Windows 11
```

应该写：

```text
version
build
KB / patch level
channel
```

例如：

- 23H2
- 24H2
- Insider Dev
- Server 2025

---

## 7. Driver Version

同一 Windows Build 不同 driver：

- Realtek OEM
- Microsoft inbox
- NVIDIA HDMI
- AMD HDMI
- Intel SST
- vendor USB ASIO

结果可能不同。

所以 driver version 是重要变量。

---

## 8. Repro Rate

不要只写：

```text
failed once
```

记录：

```text
0/20
1/20
20/20
```

可以快速区分：

- deterministic incompatibility
- race
- hotplug timing
- driver flakiness

---

## 9. Regression

字段：

```text
LastKnownGood:
FirstKnownBad:
FixedIn:
```

这对 Windows update 后 internal API 失效特别重要。

---

## 10. 建议目录

未来可以增加：

```text
compatibility/
  public-api.csv
  undocumented-api.csv
  devices/
  windows-builds/
```

CSV 适合：

- diff
- filter
- CI
- 自动生成 Markdown matrix

---

## 11. Issue Template

遇到 regression：

```text
### Environment
Windows:
Build:
Arch:
Driver:
Device:

### API
Interface:
Method:
IID:
HRESULT:

### Steps

### Expected

### Actual

### Last Known Good

### Logs
```

---

## 12. 目标

让 WinAudioResearch 最终不只是：

> 文档收藏夹

而是：

> Windows Audio 行为数据库。
