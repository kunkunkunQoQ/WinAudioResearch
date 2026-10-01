# Windows Audio ETW / WPR / WPA 诊断

> 状态：🟢 Public Windows diagnostics infrastructure

当问题是：

- crackle
- glitch
- dropout
- random latency spike
- device D-state
- audiodg CPU spike
- driver power issue

普通日志往往不够。

Windows 的标准诊断方向之一是：

```text
ETW
→ WPR / Xperf
→ ETL
→ WPA
```

## 1. ETW

Event Tracing for Windows 可以动态收集：

- kernel events
- user-mode providers
- scheduling
- CPU
- power
- driver activity
- audio-specific traces

优点：

- 可运行时启停
- 不需要重启进程
- 可做时序关联

## 2. WPR

Windows Performance Recorder 用来采集 trace。

适合：

- reproducible scenario
- CPU / scheduling
- latency / glitch
- power

## 3. WPA

Windows Performance Analyzer 用于分析：

- timeline
- CPU usage
- thread scheduling
- D-state
- ETW provider events

## 4. Audio Glitch 分析

真正 audio glitch 往往不是：

> “GetBuffer 慢了一次”。

可能来自：

- thread 被抢占
- DPC / ISR
- driver delay
- page fault
- CPU power transition
- APO overload
- hardware timeout
- buffer period 太短

所以要把：

```text
audio event
+
CPU scheduler
+
DPC/ISR
+
driver / power trace
```

放在同一个 ETL timeline 看。

## 5. Power Trace

Microsoft 对 Modern Standby audio power management 提供 Xperf / WPA 示例。

可追踪：

```text
D0
D1
D2
D3
```

设备状态变化。

如果设备在应该 idle 时一直 D0：

- 可能有 open stream
- driver idle management 有问题
- hardware / DSP 仍在工作

## 6. PortCls Power Settings

PortCls driver 可以配置：

- ConservationIdleTime
- PerformanceIdleTime
- IdlePowerState

这会影响 audio hardware 的 idle power behavior。

## 7. 采样日志应该记录

```text
Windows Build
endpoint
driver version
buffer period
shared/exclusive
format
app PID
audiodg PID
repro timestamp
WPR profile
ETL file
```

## 8. 不要用 Task Manager 单独判断 glitch

Task Manager 能告诉你：

- CPU 高

但不能精确告诉你：

- 哪个 realtime audio deadline missed
- 是 DPC 还是 thread starvation
- device 是否从 D3 恢复太慢
- driver ISR 是否阻塞

ETW 才适合这种时序诊断。

## 9. 推荐研究方向

未来仓库可继续补：

- custom WPRP profile
- audio provider GUID
- glitch event parser
- audiodg stack
- DPC/ISR correlation
- MMCSS / Pro Audio task
- page fault / hard fault correlation

## 10. 官方资料

- Event Tracing for Windows  
  https://learn.microsoft.com/windows-hardware/test/wpt/event-tracing-for-windows

- Windows Performance Recorder  
  https://learn.microsoft.com/windows-hardware/test/wpt/windows-performance-recorder

- Windows Performance Analyzer  
  https://learn.microsoft.com/windows-hardware/test/wpt/windows-performance-analyzer

- Audio subsystem power management for Modern Standby  
  https://learn.microsoft.com/windows-hardware/design/device-experiences/audio-subsystem-power-management-for-modern-standby-platforms

- PortCls Registry Power Settings  
  https://learn.microsoft.com/windows-hardware/drivers/audio/portcls-registry-power-settings
