# 音量与静音：Session 和 Endpoint 不要混用

> 状态：🟢 Public API + ✅ SonicRoute Verified

Windows 至少存在两类常见“音量”：

## Session volume

接口：`ISimpleAudioVolume`

适合：

- 调整某个应用/session 音量
- 静音某个应用/session

典型范围为 `0.0 .. 1.0`。

## Endpoint volume

接口：`IAudioEndpointVolume`

适合：

- 调整设备主音量
- 调整设备级静音
- 监听设备主音量 / mute 变化

例如全局麦克风静音，本质上更接近 capture endpoint 的设备级 mute，而不是某个应用 session 的 mute。

## 为什么不要混淆

```text
ISimpleAudioVolume
  → session master volume
  → 影响一个 session

IAudioEndpointVolume
  → endpoint master volume
  → 可能影响使用该设备的多个应用
```

Microsoft 也明确建议：普通共享模式音频应用通常使用 session volume；只有需要管理 endpoint master volume 的程序才应使用 EndpointVolume API。

## 回调

`IAudioEndpointVolumeCallback` 可用于监听：

- mute 变化
- master volume 变化
- channel volume 变化

长期驻留软件优先使用事件回调，再按实际驱动兼容性决定是否增加低频轮询兜底。

## 官方资料

- EndpointVolume API: https://learn.microsoft.com/windows/win32/coreaudio/endpointvolume-api
- IAudioEndpointVolume: https://learn.microsoft.com/windows/win32/api/endpointvolume/nn-endpointvolume-iaudioendpointvolume
- ISimpleAudioVolume: https://learn.microsoft.com/windows/win32/api/audioclient/nn-audioclient-isimpleaudiovolume
