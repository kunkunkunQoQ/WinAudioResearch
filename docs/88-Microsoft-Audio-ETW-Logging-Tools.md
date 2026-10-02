# Microsoft Windows Audio Team ETW / CollectAudioLogs

> 状态：🟢 Microsoft official open-source tooling

除了 WPR / WPA 通用性能工具，Microsoft Windows Audio Team 还公开维护：

```text
microsoft/audio
```

仓库：

https://github.com/microsoft/audio

这个仓库非常值得 Windows Audio 开发者直接收藏。

---

## 1. CollectAudioLogs

Microsoft 官方描述：

> 用于收集诊断 Windows audio 问题的 audio logs。

主要面向：

- Windows Audio Team 联合诊断
- audio driver developer
- APO software vendor
- audio system troubleshooting

仓库入口：

https://github.com/microsoft/audio/tree/main/CollectAudioLogs

---

## 2. 和 Feedback Hub 的关系

CollectAudioLogs 收集的资料：

> 大部分与 Feedback Hub 在 Devices and Drivers → Audio and Sound → Recreate my problem 中采集的日志类似。

区别之一：

- CollectAudioLogs 输出目录更扁平
- 更方便开发者手工查看

---

## 3. repro.etl

采集包中最重要的文件：

```text
repro.etl
```

可以用：

```text
Windows Performance Analyzer
```

打开。

里面包含 WPR profile 指定的 ETW provider。

Microsoft 明确说它覆盖：

- Windows audio services
- 多种 audio driver provider
- APO provider

---

## 4. Circular Trace

Audio ETW 的事件量很高。

特别是：

> audio playback / capture 运行时，每个 frame/processing path 会产生大量 logging。

Microsoft 的 CollectAudioLogs 使用 circular logging。

典型结果：

```text
大约只能保留最后 30~60 秒活动
```

实际长度取决于：

- trace size
- audio activity
- provider volume

因此复现问题后应：

> 尽快停止采集。

---

## 5. Time Travel Tracing

CollectAudioLogs 还有一个普通 Feedback Hub 没有的高级功能：

```text
Time Travel Tracing (TTD)
```

可以针对：

- AudioSrv
- AudioEndpointBuilder
- AudioDG

收集 TTD。

典型文件：

```text
svchost.run / .out → AudioSrv
svchost.run / .out → AudioEndpointBuilder
audiodg.run / .out → AudioDG
```

---

## 6. TTD 不适合 Audio Quality / Glitch 测试

Microsoft 明确提醒：

Time Travel Tracing：

- CPU 开销很大
- 可能自己制造 audio glitch
- 可能产生 audible artifact

因此：

> 调查 audio quality / glitch 时，不应该首先用 TTD。

普通 audio feedback ETW log 更合适。

---

## 7. TTD 还会改变系统状态

为了 trace Windows services：

脚本可能需要暂时调整：

- security features
- Shadow Stack
- CET related service settings

并重启 service。

如果脚本中途被中断：

> 某些安全设置可能暂时保持在修改状态。

因此它是高级调试手段，不是日常用户日志功能。

---

## 8. 为什么 APO 开发者特别需要 AudioDG Trace

APO 运行在：

```text
audiodg.exe
```

中。

如果出现：

- APO crash
- deadlock
- bad processing
- AudioDG failure

AudioDG TTD / ETW 非常有价值。

---

## 9. Additional System Information

CollectAudioLogs 还能导出：

- PnP logs
- MMDevice registry information
- driver version
- driver INF
- install dates
- Event Viewer PnP data
- device state / failure

这非常重要，因为：

> 单看 repro.etl，有时不知道当前 endpoint 到底来自哪个 driver / device instance。

---

## 10. 推荐诊断流程

### Audio glitch / dropout

```text
CollectAudioLogs normal ETW
→ reproduce
→ stop within ~30 sec
→ WPA inspect
```

### Driver / endpoint installation

同时采：

```text
system information
PnP
registry
ETW
```

### APO crash / difficult service bug

在 Microsoft / vendor engineer 指导下再考虑：

```text
Time Travel Tracing
```

---

## 11. Provider Discovery

通用 ETW provider 可以用：

```text
logman query providers
```

列出 provider name / GUID。

不要依赖博客里写死的 provider GUID，优先从当前系统和官方 WPRP 中确认。

---

## 12. 和 WinAudioResearch 的关系

未来建议仓库提供：

```text
diagnostics/
  audio.wprp
  parse-audio-etl.md
  glitch-checklist.md
```

但不需要复制 Microsoft 自己已经维护的 CollectAudioLogs。

更合理：

> 链接、解释用途、补充我们自己的分析指南。

---

## 13. 官方资料

- Microsoft Windows Audio Team repository  
  https://github.com/microsoft/audio

- Windows Performance Analyzer  
  https://learn.microsoft.com/windows-hardware/test/wpt/windows-performance-analyzer

- ETW  
  https://learn.microsoft.com/windows-hardware/test/wpt/event-tracing-for-windows

- Time Travel Debugging  
  https://learn.microsoft.com/windows-hardware/drivers/debugger/time-travel-debugging-overview
