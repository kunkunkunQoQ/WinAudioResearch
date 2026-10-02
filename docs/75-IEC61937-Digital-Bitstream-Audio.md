# IEC 61937、HDMI / S/PDIF 与 Compressed Bitstream Audio

> 状态：🟢 Public Windows audio format documentation

数字音频输出不一定总是 PCM。

HDMI / DisplayPort / S/PDIF 还可能传输：

- Dolby Digital
- DTS
- Dolby Digital Plus
- Dolby TrueHD
- DTS-HD
- 其他 IEC 61937 payload

---

## 1. PCM vs Encoded Bitstream

### PCM

Windows / app 已经 decode：

```text
compressed source
→ decoder
→ PCM
→ endpoint
```

### Bitstream / Passthrough

应用保留 encoded audio：

```text
encoded frames
→ IEC 61937 packaging
→ HDMI / S/PDIF
→ AVR / TV decode
```

---

## 2. 为什么 WAVEFORMATEXTENSIBLE 不够

普通 `WAVEFORMATEXTENSIBLE` 主要描述一个 audio format。

IEC 61937 场景同时需要描述：

- encoded stream transport characteristics
- decoded audio characteristics

因此 Windows 7 增加：

```text
WAVEFORMATEXTENSIBLE_IEC61937
```

---

## 3. WAVEFORMATEXTENSIBLE_IEC61937

它扩展 WAVEFORMATEXTENSIBLE，用于表达：

- encoded format
- effective decoded channel count
- sample size
- data rate

这对 UI / capability 判断非常重要。

---

## 4. SubFormat GUID

Windows SDK / ksmedia.h 定义多种 compressed audio subformat GUID。

这些 GUID 用于：

- WAVEFORMATEXTENSIBLE.SubFormat
- IEC61937 extended structure

表示具体 codec / transport format。

---

## 5. HDMI / DisplayPort Capability

CEA sink 不一定支持所有 compressed format。

所以：

> 不能看到 HDMI endpoint 就盲目发送所有 Dolby/DTS bitstream。

必须确认：

- sink capability
- driver
- format support

---

## 6. IsFormatSupported

WASAPI：

```text
IAudioClient::IsFormatSupported
```

是判断目标 endpoint 是否接受 format 的重要入口。

不要只看设备品牌规格表。

---

## 7. Exclusive Mode

Compressed bitstream / passthrough 场景常与：

```text
exclusive mode
```

相关。

因为 shared Audio Engine 的常规模式是 PCM mix。

具体 encoded transport 应按：

- codec
- endpoint
- OS
- driver

实现。

---

## 8. S/PDIF 限制

S/PDIF 带宽比 HDMI 更有限。

典型：

- stereo PCM
- Dolby Digital
- DTS core

高码率无损多声道通常更依赖 HDMI。

---

## 9. HDMI + Protected Content

bitstream 还可能涉及：

- HDCP
- PUMA
- Protected Media Path

特别是商业 DRM content。

---

## 10. 调试

建议记录：

```text
Endpoint
Connection type
Sink
Format GUID
Encoded channels
Decoded channels
Sample rate
Exclusive/shared
IsFormatSupported result
HRESULT
```

---

## 11. 官方资料

- Representing Formats for IEC 61937 Transmissions  
  https://learn.microsoft.com/windows/win32/coreaudio/representing-formats-for-iec-61937-transmissions

- Subformat GUIDs for Compressed Audio Formats  
  https://learn.microsoft.com/windows-hardware/drivers/audio/subformat-guids-for-compressed-audio-formats

- WAVEFORMATEXTENSIBLE  
  https://learn.microsoft.com/windows-hardware/drivers/ddi/ksmedia/ns-ksmedia-waveformatextensible
