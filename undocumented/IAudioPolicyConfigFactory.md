# IAudioPolicyConfigFactory

> 状态：🔴 Undocumented + ✅ SonicRoute Verified

这个名字常见于 EarTrumpet 等项目，用来描述 Windows 内部按应用音频策略能力。

## 研究中最重要的三个操作

```text
SetPersistedDefaultAudioEndpoint(
    processId,
    flow,
    role,
    deviceId)

GetPersistedDefaultAudioEndpoint(
    processId,
    flow,
    role)

ClearAllPersistedApplicationDefaultEndpoints()
```

## Role

SonicRoute 当前设置 per-app endpoint 时会同时处理：

- `eMultimedia`
- `eConsole`

这是产品实测策略，不代表所有场景都必须这样做。

## Device ID

SonicRoute 的内部策略实现会把设备 ID 转换为 AudioPolicyConfig 预期的完整 device interface path。

render 与 capture 使用不同的 device interface suffix。

这也是一个非常容易踩坑的地方：

**MMDevice 返回的 ID 与 internal policy API 最终接受的字符串形式需要按实现核对。**

## Windows 10 / 11 IID

SonicRoute 当前使用：

```text
Windows 11 21H2+
ab3d4648-e242-459f-b02f-541c70306324

Downlevel / Windows 10
2a59116d-6c4f-45e0-a74f-707e3fef9258
```

请把这些值视为研究记录，而不是公开 SDK 常量。

## 第三方参考

- EarTrumpet interface:
  https://github.com/File-New-Project/EarTrumpet/blob/master/EarTrumpet/Interop/MMDeviceAPI/IAudioPolicyConfigFactory.cs
- EarTrumpet factory selection:
  https://github.com/File-New-Project/EarTrumpet/blob/master/EarTrumpet/Interop/Helpers/AudioPolicyConfigFactory.cs
