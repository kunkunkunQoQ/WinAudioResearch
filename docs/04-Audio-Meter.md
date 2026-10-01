# IAudioMeterInformation：实时声音活动

> 状态：🟢 Public API + ✅ SonicRoute Verified

`IAudioMeterInformation` 提供音频流的 peak meter 信息。

## GetPeakValue

```text
GetPeakValue() -> float 0.0 .. 1.0
```

Microsoft 文档说明，该值是音频流各 channel 中记录到的 peak sample 的归一化结果。

## Endpoint meter 与 Session meter

可以在 endpoint 层获取 `IAudioMeterInformation`。

在实际 Core Audio session 对象上，也可以 QueryInterface 到 `IAudioMeterInformation`，从而读取 session 的声音活动。SonicRoute 的简洁面板实时电平就是沿这条路径实现：

```text
all active render endpoints
   ↓
IAudioSessionManager2
   ↓
IAudioSessionControl2
   ↓ QueryInterface
IAudioMeterInformation
   ↓
GetPeakValue
```

## 为什么需要遍历所有 render endpoint

如果只读取默认播放设备：

- 浏览器被路由到音箱
- 游戏被路由到耳机
- 默认设备仍是另一个 endpoint

那么只枚举默认 endpoint 会漏掉其他设备上的 session。

因此需要根据产品目标决定：

- 只关心默认设备 → 枚举一个 endpoint
- 关心所有应用声音活动 → 枚举全部 ACTIVE render endpoint

## UI 平滑不是 API 的职责

原始 peak 会快速跳动。SonicRoute 在 UI 层使用 attack / release 平滑，并对发布值量化，减少无效 UI 刷新。

这是显示策略，不属于 Windows API 语义。

## 官方资料

- IAudioMeterInformation: https://learn.microsoft.com/windows/win32/api/endpointvolume/nn-endpointvolume-iaudiometerinformation
- GetPeakValue: https://learn.microsoft.com/windows/win32/api/endpointvolume/nf-endpointvolume-iaudiometerinformation-getpeakvalue
- Peak Meters: https://learn.microsoft.com/windows/win32/coreaudio/peak-meters
