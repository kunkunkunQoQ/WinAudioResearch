# Windows Audio Debugging Toolkit：开发者应该知道的工具

> 状态：工具索引

Windows 音频排错如果只靠：

```text
Debug.WriteLine
```

很快会遇到瓶颈。

这页集中整理实用工具。

---

## 1. Windows Sound Settings / mmsys.cpl

最基础但仍重要：

```text
mmsys.cpl
```

可检查：

- default device
- communications default
- endpoint volume
- enhancements
- exclusive mode
- format
- recording level

开发时先确认系统 UI 中真实状态，避免把“用户配置问题”当 API bug。

---

## 2. Device Manager

检查：

- driver version
- device instance
- hardware ID
- disabled device
- driver provider
- install status

尤其适合 USB / virtual driver / Bluetooth。

---

## 3. KsStudio

WDK 工具：

```text
KsStudio.exe
```

检查：

- KS filters
- pins
- nodes
- topology
- properties
- format
- stream

用于区分 driver 问题和 user-mode audio API 问题。

---

## 4. Windows Performance Recorder

```text
WPR
```

采集 ETW。

适合：

- glitch
- CPU
- thread scheduling
- power
- audio graph

---

## 5. Windows Performance Analyzer

```text
WPA
```

分析 ETL timeline。

适合关联：

- app thread
- audiodg
- DPC/ISR
- CPU
- power state

---

## 6. Event Viewer

音频 driver / USB Audio / device startup failure 常能在：

```text
System Event Log
```

看到更具体原因。

USB Audio 2.0 官方文档也明确建议查看 System event log。

---

## 7. ProcMon

Microsoft Sysinternals：

```text
Process Monitor
```

可以观察：

- registry
- file
- process/thread

尤其适合研究：

- Audio PolicyConfig registry
- driver property
- app config

但它不能替代 ETW 的实时 audio timing 分析。

---

## 8. Process Explorer

可检查：

- audiodg.exe
- loaded DLL
- process tree
- handles
- CPU

如果怀疑某个 vendor APO：

可帮助观察 audiodg loaded module。

---

## 9. WinDbg

适合：

- driver crash
- user-mode crash
- COM / native stack
- dump

虚拟 audio driver / APO 开发最终很可能需要 WinDbg。

---

## 10. Driver Verifier

驱动开发可以使用：

```text
Driver Verifier
```

检查：

- memory
- IRQL
- pool
- driver misuse

但它可能显著增加系统压力，应该只在测试环境使用。

---

## 11. HLK / Audio Tests

正式 driver / hardware compatibility 还要看：

- Windows Hardware Lab Kit
- audio HLK tests

这是“我的 driver 能播放”与“符合 Windows driver quality 要求”之间的重要差距。

---

## 12. Audio Endpoint Property Dumper

建议仓库未来提供一个最小 sample：

输出：

- all endpoints
- property keys
- formats
- default roles
- session
- jack info

这是研究 Windows audio 环境最有价值的小工具之一。

---

## 13. ETW Trace + Repro Script

一个理想 issue 应附：

```text
repro steps
Windows Build
driver version
endpoint
HRESULT
ETL timestamp
app log
```

而不是：

> “Windows 音频偶尔炸了。”

---

## 14. 官方资料

- KsStudio Utility  
  https://learn.microsoft.com/windows-hardware/drivers/audio/ksstudio-utility

- Event Tracing for Windows  
  https://learn.microsoft.com/windows-hardware/test/wpt/event-tracing-for-windows

- Windows Performance Recorder  
  https://learn.microsoft.com/windows-hardware/test/wpt/windows-performance-recorder

- Windows Performance Analyzer  
  https://learn.microsoft.com/windows-hardware/test/wpt/windows-performance-analyzer

- Driver Verifier  
  https://learn.microsoft.com/windows-hardware/drivers/devtest/driver-verifier
