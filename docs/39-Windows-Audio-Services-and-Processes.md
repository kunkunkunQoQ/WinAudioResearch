# Windows Audio 系统进程、服务与组件

> 状态：🟢 Microsoft documented architecture

当 Windows 音频出问题时，只看你的应用线程通常不够。

理解下面几个系统组件非常重要：

- audiodg.exe
- audioeng.dll
- audiosrv.dll
- AudioEndpointBuilder
- MMDevice / endpoint abstraction
- audio driver

---

## 1. Audio Device Graph — audiodg.exe

Microsoft 当前 Windows Audio Architecture 文档描述：

```text
Audio Device Graph = audiodg.exe
```

它加载：

```text
Audio Engine = audioeng.dll
```

---

## 2. Audio Engine 做什么

Audio Engine 负责：

- shared-mode stream mixing
- stream processing
- format conversion
- volume processing
- APO loading / processing
- 向 driver 传输 audio data

一个简化路径：

```text
Application
   ↓
WASAPI shared stream
   ↓
Audio Engine / audiodg
   ↓
APO
   ↓
driver
   ↓
hardware
```

---

## 3. 为什么 audiodg.exe 独立出来

音频 processing 与应用进程分开有很多好处：

- 隔离 audio engine
- 隔离部分 APO processing
- 一个普通应用崩溃不应直接拖垮整个 engine
- 系统可以统一管理 shared-mode streams

但 OEM APO 出问题时，用户有时会观察到：

- audiodg CPU 高
- audiodg crash
- 音频断续

这时不能只怀疑应用本身。

---

## 4. Audio Service — audiosrv.dll

Microsoft 文档说明 Audio Service：

- setup / control audio streams
- implement background audio policy
- implement ducking policy
- manage audio related policy

因此：

> Windows Audio 不只是驱动 + WASAPI。

还有 service policy 层。

---

## 5. AUDCLNT_E_SERVICE_NOT_RUNNING

如果 Windows Audio Service 未运行，WASAPI 调用可能返回：

```text
AUDCLNT_E_SERVICE_NOT_RUNNING
```

这和：

- device not found
- device invalidated
- unsupported format

完全不同。

诊断工具应把它单独显示。

---

## 6. Audio Endpoint Builder

Microsoft 当前文档写作：

```text
Audio Endpoint Builder
(audioendpointbuilder.exe)
```

负责：

- discover new audio devices
- create software audio endpoints

它把底层 driver / topology 转换成应用看到的 endpoint abstraction。

---

## 7. Endpoint Builder 和 IMMDevice

`IMMDevice` 是应用看到的 endpoint object。

但它背后可能来自：

- HDA codec
- USB audio
- Bluetooth
- HDMI
- virtual audio driver
- software endpoint

所以：

> `IMMDevice` 是系统构造的 endpoint abstraction，不等同于“一个物理设备”。

---

## 8. Driver

音频 driver 最终负责和硬件 / virtual endpoint 通信。

常见：

- WDM
- WaveRT
- PortCls
- ACX

上层程序一般不直接和 miniport driver 交互。

---

## 9. Exclusive Mode

Exclusive stream 会绕过 shared-mode mixing 的一些路径，但仍不是：

> “应用直接写声卡 DMA，没有任何 Windows 组件”。

driver / endpoint / hardware 仍然存在。

---

## 10. APO 为什么经常和 audiodg 一起被讨论

APO 是 user-mode signal-processing object。

Audio Engine 会加载 APO。

因此：

- enhancement
- OEM EQ
- noise processing
- spatial processing

可能会影响 audiodg 的 CPU / latency / crash behavior。

---

## 11. 服务重启为什么能“修好音频”

当：

- endpoint state 卡住
- audio graph 出错
- driver reset
- policy state 异常

重启 Audio Service 有时会重建部分系统 audio state。

但它不是应用应该默认使用的“正常刷新 API”。

一个应用需要恢复 device invalidated 时，优先：

```text
release
→ re-enumerate
→ reactivate
```

而不是自动重启 Windows Audio Service。

---

## 12. 诊断建议

遇到音频异常记录：

```text
Windows Build
Audio service running?
Endpoint state
Default endpoint
Driver version
audiodg CPU / crash
APO / enhancement state
HRESULT
```

---

## 13. 官方资料

- Windows Audio Architecture  
  https://learn.microsoft.com/windows-hardware/drivers/audio/windows-audio-architecture

- Audio Endpoint Builder Algorithm  
  https://learn.microsoft.com/windows-hardware/drivers/audio/audio-endpoint-builder-algorithm

- Windows Audio Processing Objects  
  https://learn.microsoft.com/windows-hardware/drivers/audio/windows-audio-processing-objects
