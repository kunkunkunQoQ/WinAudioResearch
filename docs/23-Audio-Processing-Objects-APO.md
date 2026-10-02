# Audio Processing Objects (APO)：Windows 音频 DSP 扩展机制

> 状态：🟢 Public Driver / System API  
> 主要面向 OEM / IHV / ISV 音频处理、驱动包和系统效果开发。

APO（Audio Processing Object）是 Windows 音频栈中的用户态 DSP 扩展机制。

它不是普通应用里“随便加载的 VST”。

APO 运行在 Windows Audio Engine 的处理图中，用于实现：

- EQ
- loudness
- reverb
- tremolo
- AEC
- AGC
- noise suppression
- vendor-specific audio effects

---

## 1. APO 位于哪里

简化 render 路径：

```text
Application streams
      ↓
Stream Effects (SFX)
      ↓
mix / mode processing
      ↓
Mode Effects (MFX)
      ↓
Endpoint Effects (EFX)
      ↓
Driver / Hardware
```

capture 路径方向相反。

Microsoft 把常见 APO placement 分成：

- SFX: Stream Effect
- MFX: Mode Effect
- EFX: Endpoint Effect

---

## 2. SFX

SFX 面向单个 stream。

特点：

- 每个 stream 可以有自己的 effect instance
- render 常位于 mix 之前
- capture 常位于 tee 之后
- 适合和单 stream 特征有关的处理

某些 Windows 版本在 RAW mode 下不会加载 SFX。

---

## 3. MFX

MFX 面向同一个 signal processing mode 下的一组 stream。

例如：

- Communications
- Media
- Speech

它适合：

- 模式相关 processing
- 不需要每 stream 独立状态的 DSP

---

## 4. EFX

EFX 面向 endpoint。

适合：

- speaker tuning
- device-specific EQ
- endpoint-wide processing
- hardware-specific compensation

---

## 5. APO 是 COM object

Microsoft 官方要求自定义 APO 实现为 user-mode in-process COM object。

关键接口：

- `IAudioProcessingObject`
- `IAudioProcessingObjectConfiguration`
- `IAudioProcessingObjectRT`
- `IAudioSystemEffects`

核心 realtime 方法：

```text
IAudioProcessingObjectRT::APOProcess
```

---

## 6. Real-time 限制

APO 的实时处理线程要求非常严格。

Realtime path 不应该：

- 阻塞
- 等 mutex / disk I/O
- 分配 pageable memory
- 调用可能 page fault 的代码
- 执行不可预测的长耗时操作

APO 不应该给 audio graph 引入明显额外 latency。

---

## 7. Audio Signal Processing Modes

Windows 定义多种 signal processing mode。

常见：

- RAW
- DEFAULT
- MEDIA
- MOVIE
- SPEECH
- COMMUNICATIONS
- NOTIFICATION

驱动决定 endpoint 支持哪些 mode。

应用选择 stream category，系统再根据 driver capability 映射到 mode。

---

## 8. RAW 并不等于“世界上绝对零处理”

RAW 的目标是：

> 尽量不给 stream 添加常规可选 signal processing。

但 endpoint-specific always-on processing、driver 或 hardware 必需处理仍可能存在。

这点对测量 / EQ / 音频分析软件尤其重要。

---

## 9. Windows 11 CAPX

Windows 11 对新 APO 引入了更多标准化 API / framework：

- Settings Framework
- Notifications Framework
- Logging Framework
- Threading Framework
- AEC support
- reference loopback
- effects discovery / control

Windows 11 Build 22000 起的新 APO 开发要求更强调这些框架。

---

## 10. IAudioEffectsManager

应用侧可以通过：

```text
IAudioEffectsManager
```

查询与控制关联 stream 的可控 audio effects。

能力包括：

- `GetAudioEffects`
- `SetAudioEffectState`
- effects changed notification

这让应用不必靠直接读取 OEM registry 来判断所有效果状态。

---

## 11. APO 与 SonicRoute / Sonveta 类项目的关系

普通 SonicRoute 这种：

- 音量管理
- session routing
- endpoint switch

不需要 APO。

如果要做真正“系统音频链上的 EQ / DSP / noise processing”，则可能涉及：

- APO
- virtual audio device
- WASAPI processing chain
- driver / AudioGraph / custom capture-render pipeline

它们复杂度完全不同。

---

## 12. Microsoft 示例

SysVAD 中包含 Swap APO 等参考实现：

https://github.com/microsoft/Windows-driver-samples/tree/main/audio/sysvad

---

## 13. 官方资料

- Windows Audio Processing Objects  
  https://learn.microsoft.com/windows-hardware/drivers/audio/windows-audio-processing-objects

- Audio Processing Object Architecture  
  https://learn.microsoft.com/windows-hardware/drivers/audio/audio-processing-object-architecture

- Implementing Audio Processing Objects  
  https://learn.microsoft.com/windows-hardware/drivers/audio/implementing-audio-processing-objects

- Windows 11 APIs for APO  
  https://learn.microsoft.com/windows-hardware/drivers/audio/windows-11-apis-for-audio-processing-objects

- Audio Signal Processing Modes  
  https://learn.microsoft.com/windows-hardware/drivers/audio/audio-signal-processing-modes

- IAudioEffectsManager  
  https://learn.microsoft.com/windows/win32/api/audioclient/nn-audioclient-iaudioeffectsmanager

## Structured audit

The machine-readable APO/CAPX/INF audit is maintained separately:

- [APO / CAPX / Media-Class INF Coverage Audit](106-APO-CAPX-Media-Class-INF-Coverage-Audit.md)
- [APO symbol database](../api/apo.csv)
- [APO method database](../api/methods-apo.csv)
- [Audio INF database](../api/audio-inf.csv)

The audit includes Windows 11 logging, realtime work queues, notification framework, AEC auxiliary inputs, CAPX effect property stores, SFX/MFX/EFX registration and deployment class differences.
