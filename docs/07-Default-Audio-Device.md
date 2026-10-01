# 系统默认音频设备：读取是公开的，设置要分开看

> 状态：🟢 Public API（读取） + 🔴 Undocumented（传统桌面程序设置）

Windows Core Audio 对“读取默认 endpoint”提供了公开 API：

```text
IMMDeviceEnumerator
   ↓
GetDefaultAudioEndpoint(flow, role)
   ↓
IMMDevice
```

这里必须同时指定：

- data flow：`eRender` / `eCapture`
- role：`eConsole` / `eMultimedia` / `eCommunications`

因此“默认设备”实际上是一个 **flow + role** 组合。

## 读取默认设备

这是正式公开能力。

典型用途：

- 获取当前默认扬声器
- 获取默认麦克风
- 判断 communications role 是否与 console role 相同
- 在默认设备变化后重新绑定 session / meter

参考：

https://learn.microsoft.com/windows/win32/api/mmdeviceapi/nf-mmdeviceapi-immdeviceenumerator-getdefaultaudioendpoint

## 设置默认设备

这部分不要和读取混在一起。

传统桌面工具常见的 `IPolicyConfig::SetDefaultEndpoint` / PolicyConfig 方案属于 **未公开 COM 接口**，并不是和 `GetDefaultAudioEndpoint` 对称的公开 Core Audio setter。

因此：

```text
GetDefaultAudioEndpoint
    → Public API

PolicyConfig.SetDefaultEndpoint
    → Undocumented implementation used by many desktop tools
```

## Role 的实际处理

如果程序要模拟“切换系统默认播放设备”的用户体验，通常需要明确是否同时更新：

- Console
- Multimedia
- Communications

不要只因为 UI 上显示一个“默认设备”，就假设三个 role 永远一致。

## 和按应用路由不要混淆

系统默认 endpoint：

```text
default endpoint for a role
```

按应用持久化 endpoint：

```text
persisted default endpoint for a process/app
```

两者都是“设备选择”，但底层策略不是同一个概念。

## 研究建议

涉及设置默认设备时，文档和代码中应明确标注：

- 使用了哪个 PolicyConfig IID
- 设置了哪些 role
- Windows Build
- HRESULT
- 是否有公开替代方案

这能避免把内部接口误写成 Windows SDK 的稳定能力。
