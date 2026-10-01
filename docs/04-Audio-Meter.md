# IAudioMeterInformation：Endpoint 与 Session 的实时声音活动

> 状态：🟢 Public API + ✅ SonicRoute Verified

`IAudioMeterInformation` 用于读取 peak meter。

IID：

```text
C02216F6-8C67-4B5B-9D00-D008E73E0064
```

## 1. 常用方法

```text
GetPeakValue
GetMeteringChannelCount
GetChannelsPeakValues
QueryHardwareSupport
```

`GetPeakValue` 返回：

```text
0.0 .. 1.0
```

它表示 peak，不是：

- RMS；
- LUFS；
- VU；
- dBFS 历史统计；
- “音量设置百分比”。

所以：

> volume slider = 50%  
> 不代表 meter = 0.5。

## 2. Endpoint meter

可以从 endpoint 激活 `IAudioMeterInformation`。

适合：

- 查看某设备总输出活动；
- 查看 capture endpoint 当前输入 peak；
- 做简单设备级活动指示。

## 3. Session meter

SonicRoute 会从 session 对象取得 `IAudioMeterInformation`，用于按应用显示实时声音活动。

调用链：

```text
IMMDevice
   ↓
IAudioSessionManager2
   ↓
IAudioSessionEnumerator
   ↓
IAudioSessionControl2
   ↓ QI / interface
IAudioMeterInformation
   ↓
GetPeakValue
```

这样可以做：

```text
Game.exe     ███████░
Browser.exe  ██░░░░░░
Discord.exe  ░░░░░░░░
```

## 4. 为什么要扫所有 ACTIVE render endpoint

如果：

```text
Default = Speakers
Game    → Headphones
Browser → Speakers
```

只扫描默认 endpoint，会漏掉 Game。

因此 SonicRoute 的目标是“所有当前应用声音活动”时，会枚举所有 ACTIVE render endpoint。

这是比“默认设备 meter”更昂贵，但语义更正确的做法。

## 5. 一个 PID 多 session

SonicRoute 收集同 PID 的多个 session meter，再取有效峰值中的最大值：

```text
displayPeak(pid) = max(sessionPeaksForPid)
```

这是 UI 聚合策略，不是 Windows API 规则。

其他工具可以：

- 分 session 显示；
- 按 endpoint 分组；
- 选择其他聚合算法。

## 6. 采样与重新扫描

SonicRoute 当前大约：

```text
SampleInterval ≈ 33 ms
RescanInterval ≈ 2000 ms
```

约 30 FPS 足够 UI 流畅，也能控制 CPU / Dispatcher 开销。

为什么还要 rescan？

Session 会：

- 新建；
- Expire；
- 移动到其他 endpoint；
- 因设备变化失效。

不能永远持有最初的一组 COM 对象。

## 7. Attack / Release 平滑

原始 peak 跳动很快。

SonicRoute 当前视觉平滑思路：

```text
if raw > previous:
    alpha = Attack
else:
    alpha = Release

display = previous + (raw - previous) * alpha
```

这只是 UI smoothing，不是音频分析算法。

## 8. 避免“静音也 30 FPS 刷 UI”

SonicRoute 会：

- 值没变化时不发布新快照；
- UI 关闭时停止 worker；
- 目标为空时等待；
- 重新扫描前释放旧 session handle。

这说明真正可能耗 CPU 的往往是：

```text
COM re-enumeration
+
managed allocation
+
UI dispatcher update
```

而不是单独一次 GetPeakValue。

## 9. Hardware support

`QueryHardwareSupport` 可以查询 peak meter 是否由硬件支持。

没有硬件支持时 Windows 仍可能提供软件实现，所以 hardware-support flag 不等于“GetPeakValue 是否可用”。

## 10. 官方资料

- IAudioMeterInformation  
  https://learn.microsoft.com/windows/win32/api/endpointvolume/nn-endpointvolume-iaudiometerinformation
- GetPeakValue  
  https://learn.microsoft.com/windows/win32/api/endpointvolume/nf-endpointvolume-iaudiometerinformation-getpeakvalue
- Peak Meters  
  https://learn.microsoft.com/windows/win32/coreaudio/peak-meters
