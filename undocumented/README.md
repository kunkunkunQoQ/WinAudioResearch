# Undocumented Windows Audio

这个目录专门记录 Windows 音频系统中的 **未公开 / 未稳定文档化接口**。

> 🔴 这里的接口不应被理解为 Microsoft 支持的公共 SDK。

目前重点：

- `Windows.Media.Internal.AudioPolicyConfig`
- `IAudioPolicyConfigFactory`
- `SetPersistedDefaultAudioEndpoint`
- `GetPersistedDefaultAudioEndpoint`
- `ClearAllPersistedApplicationDefaultEndpoints`

## 为什么单独放目录

如果把内部接口和公开 Core Audio 混在同一层，很容易产生两个问题：

1. 使用者误以为它们拥有同样的兼容性保证；
2. Windows 更新后接口失效时，无法快速定位风险来源。

因此本仓库要求：

- 公开接口 → `docs/`
- 内部接口 → `undocumented/`
- 项目实测 → `findings/`

## 参考项目

EarTrumpet 是研究 Windows per-app audio routing 时的重要公开参考：

https://github.com/File-New-Project/EarTrumpet

SonicRoute 当前实现：

https://github.com/kunkunkunQoQ/SonicRoute/blob/master/SonicRoute.Core/Interop/AudioPolicyConfig.cs
