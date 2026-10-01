# Windows Audio Developer Tools：调试、检查、驱动与性能工具

> 状态：🟢 Microsoft / Windows developer tools

音频开发不能只靠 Visual Studio debugger。

很多问题需要：

- endpoint inspection
- KS topology
- driver state
- ETW
- performance trace
- device install state

---

## 1. KsStudio

Windows Driver Kit 工具。

用途：

- 枚举 Kernel Streaming filters
- 查看 filter factories
- 查看 pin / node
- 查看 properties
- 查看 events
- 构建 KS filter graph
- 测试 streaming

它可以比 MMDevice / WASAPI 更低层地查看：

> driver 实际暴露了什么。

特别适合：

- audio driver
- virtual audio
- jack/topology
- format negotiation
- KS property debugging

---

## 2. Sound Settings

现代：

```text
Settings → System → Sound
```

用于确认：

- endpoint 是否存在
- default device
- app routing
- input/output
- format
- enhancements

它是产品行为验证的重要“用户视角”。

---

## 3. mmsys.cpl

经典 Sound Control Panel：

```text
mmsys.cpl
```

适合检查：

- Playback
- Recording
- default role
- disabled devices
- exclusive mode
- enhancements
- advanced format

在研究不同 Windows 版本时仍很有价值。

---

## 4. Device Manager

用于：

- driver version
- hardware IDs
- device status
- uninstall / reinstall
- events
- power management

Endpoint 问题有时根源其实在：

> PnP device / driver。

---

## 5. PnPUtil

Microsoft 当前推荐的 built-in driver / PnP CLI：

```text
pnputil.exe
```

可以：

- enumerate drivers
- add driver package
- delete driver package
- enumerate devices
- restart / disable / enable supported device
- scan devices

新自动化脚本应优先 PnPUtil，而不是默认依赖 DevCon。

---

## 6. DevCon

DevCon 是较旧的命令行 device management tool。

仍常出现在：

- old driver scripts
- samples
- test environments

但 Microsoft 当前更推荐 PnPUtil 处理大部分现代场景。

---

## 7. Event Viewer

重要日志来源：

- driver install
- USB audio driver
- service errors
- device start failure
- kernel PnP

USB Audio 2.0 文档就明确建议：

> driver 无法启动时检查 System Event Log。

---

## 8. WPR

Windows Performance Recorder：

- CPU
- scheduling
- DPC / ISR
- power
- ETW
- audio scenario

用于录制 ETL。

---

## 9. WPA

Windows Performance Analyzer：

分析：

- timeline
- CPU
- thread scheduling
- power state
- ETW providers
- latency correlation

Audio glitch 调试非常重要。

---

## 10. WinDbg

驱动 / kernel / crash 调试：

- bugcheck
- driver
- kernel object
- stack
- memory

写 virtual audio driver 时必须熟悉至少基础 WinDbg。

---

## 11. ProcMon

Microsoft Sysinternals Process Monitor：

适合研究：

- registry
- file access
- process activity

例如：

- HSA settings
- audio policy storage
- driver install files

注意：

> ProcMon 看到某个 registry key 被系统使用，不代表那个 key 是公开 API contract。

---

## 12. Process Explorer

适合：

- process
- DLL
- handle
- audiodg
- service host

分析 OEM APO / DLL 是否加载时很有帮助。

---

## 13. HLK

Windows Hardware Lab Kit：

- audio driver compatibility
- zero glitch
- fidelity
- jack
- endpoint
- power
- driver tests

驱动产品发布前的重要环节。

---

## 14. PowerShell

可以作为：

- diagnostics glue
- PnP query
- file / event log collection
- build automation

但 Windows Core Audio 并没有一个完整、官方等价于 WASAPI 的 PowerShell cmdlet 集合。

---

## 15. 自建最小诊断工具

WinAudioResearch 最终很适合加入一个：

```text
AudioProbe
```

输出：

- Windows Build
- endpoints
- StableId
- default roles
- session
- format
- effects
- AudioStateMonitor
- HRESULT

这样文档与实际机器数据可以一一对应。

---

## 16. 官方资料

- KsStudio  
  https://learn.microsoft.com/windows-hardware/drivers/stream/ksstudio-utility

- PnPUtil  
  https://learn.microsoft.com/windows-hardware/drivers/devtest/pnputil

- Windows Performance Toolkit  
  https://learn.microsoft.com/windows-hardware/test/wpt/

- Windows HLK  
  https://learn.microsoft.com/windows-hardware/test/hlk/

- Sysinternals  
  https://learn.microsoft.com/sysinternals/
