# Process Monitor 与 Windows Audio Registry 诊断地图

> 状态：🟢 Microsoft diagnostic tool + 🟡/🔴 observed/internal registry implementation  
> 核心原则：**Registry 可以用于诊断 Windows 实现，但内部 key 不是公共 Audio API。**

---

## 1. Process Monitor

Microsoft Sysinternals：

https://learn.microsoft.com/sysinternals/downloads/procmon

Process Monitor 可以实时观察：

- Registry
- File system
- Process / thread
- DLL
- stack
- user/session

它特别适合回答：

> “Windows Settings / SonicRoute / EarTrumpet 改了一个音频设置以后，系统到底读写了什么？”

---

## 2. ProcMon 不是 ETW Audio Analyzer 的替代品

ProcMon 擅长：

- registry writes
- file loads
- process activity
- DLL / stack

不擅长：

- sample deadline
- audio frame timing
- glitch timestamp
- Audio Engine realtime scheduling

所以：

### 配置 / Policy 问题

```text
ProcMon
```

### Glitch / Latency / Realtime

```text
ETW + WPR/WPA
```

---

## 3. MMDevice Registry

Windows 会在 registry 中保存 audio endpoint 相关实现数据。

常见研究路径：

```text
HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\MMDevices\Audio
```

可以观察：

- render/capture endpoint
- endpoint properties
- FxProperties
- device state related data

但是：

> 应用不应该把这个 registry layout 当成 MMDevice public API。

---

## 4. Microsoft 官方原则

Microsoft 的 Audio Endpoint Properties 文档明确：

> Audio service 管理 endpoint property values；client 可以读取，但不应该直接设置这些 endpoint properties。

公开读取优先：

- Windows.Devices.Enumeration
- IMMDevice / IPropertyStore（desktop existing code）

而不是直接操作 registry backing store。

---

## 5. FxProperties

某些 endpoint registry 下可观察到：

```text
FxProperties
```

与：

- APO
- system effects configuration

相关。

研究价值很高。

但 modern Windows 11 已增加：

- IAudioEffectsManager
- IAudioSystemEffectsPropertyStore
- IAudioSystemEffects3

因此：

> 不应该为了查询现代 effect state 默认先 reverse FxProperties。

优先 public API，registry 仅作为 diagnostics / reverse engineering。

---

## 6. Per-App Audio Policy Registry

SonicRoute 当前研究过：

```text
HKCU\Software\Microsoft\Internet Explorer\LowRegistry\Audio\PolicyConfig
```

以及：

```text
PropertyStore
```

与：

- session/app audio policy
- persisted route

相关。

这属于：

🔴 Windows internal implementation detail。

---

## 7. ProcMon 实验方法

例如研究“Windows Settings 为 app 改输出设备”：

### Step 1

清空 ProcMon capture。

### Step 2

Filters：

```text
Process Name is SystemSettings.exe
OR
Path contains \Audio\
OR
Path contains PolicyConfig
OR
Path contains MMDevices
```

### Step 3

只执行一个动作：

```text
App X → Speaker Y
```

### Step 4

停止 capture。

### Step 5

分析：

- RegQueryValue
- RegSetValue
- RegCreateKey
- COM/server activity

### Step 6

再用 public API 查询系统可观察状态。

---

## 8. A/B Diff 比“盯一万条事件”更有效

建议：

```text
Capture A: before operation
Capture B: one exact operation
Capture C: reset operation
```

比较：

- path
- value name
- process
- stack

更容易发现真正相关的写入。

---

## 9. Stack 很重要

ProcMon 支持 operation stack。

如果某个：

```text
RegSetValue
```

来自：

- audiosrv
- SystemSettings
- third-party APO
- vendor service

其语义完全不同。

不能只看 registry path。

---

## 10. Microsoft CollectAudioLogs 也会导出 Registry

Microsoft Windows Audio Team 的：

```text
CollectAudioLogs
```

会收集：

- MMDevice registry keys
- PnP information
- driver INF/version/state

这进一步说明 registry 对**诊断**很有价值。

但工具的用途仍是：

> interpret system state

而不是建议 app 直接写内部 registry。

---

## 11. 安全原则

### 可以

- read for diagnostics
- compare before/after
- document observed implementation
- record Windows Build

### 谨慎

- write internal key
- delete subtree
- ship registry schema as stable contract

### 不要

- 把内部 key 描述成 Microsoft official API
- 跨 Windows version 无条件套同一 schema

---

## 12. 记录格式

```text
Windows Build:
Operation:
Process:
Registry path:
Value:
Before:
After:
Public observable state:
Reboot persistence:
Source:
```

---

## 13. 官方资料

- Process Monitor  
  https://learn.microsoft.com/sysinternals/downloads/procmon

- Audio Endpoint Properties  
  https://learn.microsoft.com/windows/win32/coreaudio/audio-endpoint-properties

- Microsoft Audio Team tools  
  https://github.com/microsoft/audio
