# 按应用音频路由：它不属于普通 Audio Session API

> 状态：🔴 Undocumented + ✅ SonicRoute Verified

Windows 设置可以为应用指定输出 / 输入设备，但传统公开 Core Audio API 并没有提供一个简单的“给 PID 设置默认 endpoint”的稳定 Win32 方法。

SonicRoute 实际使用的是 Windows 内部 AudioPolicyConfig 机制。

## 实际调用关系

```text
Windows.Media.Internal.AudioPolicyConfig
              ↓ RoGetActivationFactory
      IAudioPolicyConfigFactory
              ↓
SetPersistedDefaultAudioEndpoint
GetPersistedDefaultAudioEndpoint
```

## 它和 Audio Session 的关系

Audio Session API 主要用于：

- 找到正在存在的 session
- 读取 PID / state
- 调 session volume / mute
- 监听 session

而 per-app routing 是一种 **持久化应用音频策略**。

换句话说：

```text
IAudioSessionManager2
    ≠ per-app routing API
```

## “Persisted” 的意义

路由规则并不只存在于当前某个 session COM 对象里，而是 Windows 保存的一条应用默认 endpoint 策略。

这也是为什么它能表现得类似 Windows 设置里的“应用音量和设备首选项”。

## 风险

由于相关接口未作为稳定公开 SDK 提供：

- IID 可能随系统版本变化；
- vtable 位置可能变化；
- 激活类是 internal；
- 行为可能被 Windows 更新调整；
- 不能把“当前可用”描述成 Microsoft 保证兼容。

本仓库会把这类内容统一放在 `undocumented/`。

## 参考

- SonicRoute implementation: https://github.com/kunkunkunQoQ/SonicRoute/blob/master/SonicRoute.Core/Interop/AudioPolicyConfig.cs
- EarTrumpet IAudioPolicyConfigFactory: https://github.com/File-New-Project/EarTrumpet/blob/master/EarTrumpet/Interop/MMDeviceAPI/IAudioPolicyConfigFactory.cs
- EarTrumpet helper: https://github.com/File-New-Project/EarTrumpet/blob/master/EarTrumpet/Interop/Helpers/AudioPolicyConfigFactory.cs
