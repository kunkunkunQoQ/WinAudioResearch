# Protected User Mode Audio (PUMA) 与受保护音频

> 状态：🟢 Public Windows media / Core Audio documentation

PUMA（Protected User Mode Audio）是 Windows 受保护媒体路径的一部分。

它的存在提醒音频开发者：

> 并不是所有“正在播放的系统声音”都应该被普通 capture / loopback 无条件复制。

---

## 1. PUMA 是什么

Windows Vista 引入 PUMA：

```text
Protected User Mode Audio
```

它运行在 Protected Environment 中，为受保护媒体提供：

- trusted audio path
- output protection
- copy protection policy
- digital output restrictions

---

## 2. 为什么需要它

DRM 内容可能要求：

- 禁止数字复制
- 只允许受信任 driver
- HDMI 必须启用 HDCP
- S/PDIF 设置 SCMS
- 禁止特定输出

因此“能播放”不等于“允许任意录制”。

---

## 3. Windows 7 的扩展

Windows 7 对 PUMA 增加：

- S/PDIF SCMS control
- HDMI HDCP control
- 允许某些应用在 Protected Environment 外访问 output protection control

---

## 4. 与 WASAPI Loopback 的关系

Loopback capture 文档长期提醒：

> protected content 可能受到 DRM / trusted audio path 限制。

所以出现：

```text
系统在播放
但 loopback silence
```

不能立刻判断是 capture implementation bug。

还要考虑：

- protected content
- output protection
- policy

---

## 5. HDMI / S/PDIF

PUMA 与数字输出特别相关：

### HDMI

可能需要：

```text
HDCP
```

### S/PDIF

可能涉及：

```text
SCMS
```

这也是为什么数字音频 endpoint 和普通 analog speaker 的内容保护行为可能不同。

---

## 6. Trusted Audio Driver

受保护内容要求底层 audio driver 满足相关 Windows 内容保护要求。

因此：

- driver signing
- certification
- protected media path

会影响真正可用的输出。

---

## 7. Media Foundation

Protected Environment 和 Media Foundation 有紧密关系。

做：

- DRM playback
- protected video/audio
- streaming service client

时，不应该只研究 WASAPI。

还要看：

- Media Foundation Protected Media Path
- Output Trust Authority

---

## 8. 对录屏 / 录音工具的意义

录音工具应该正确处理：

- no data
- protected data unavailable
- partial capture

不要尝试绕过 DRM 或受保护媒体路径。

正确目标是：

> 遵守 Windows content protection policy。

---

## 9. 调试建议

如果某内容无法 capture：

先对比：

```text
normal WAV/YouTube/non-DRM
vs
protected streaming content
```

再确认：

- endpoint
- HDMI / HDCP
- application
- loopback path

避免把内容保护问题误诊为 WASAPI bug。

---

## 10. 官方资料

- Protected User Mode Audio (PUMA)  
  https://learn.microsoft.com/windows/win32/coreaudio/protected-user-mode-audio--puma-

- Protected Media Path  
  https://learn.microsoft.com/windows/win32/medfound/protected-media-path

- Loopback Recording  
  https://learn.microsoft.com/windows/win32/coreaudio/loopback-recording
