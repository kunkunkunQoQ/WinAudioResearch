# WASAPI 与 IAudioClient

> 状态：🟢 Public API

WASAPI（Windows Audio Session API）负责应用与 audio endpoint 之间的音频数据流。

## 核心入口

```text
IMMDevice
   ↓ Activate(IID_IAudioClient)
IAudioClient
   ↓ Initialize
   ↓ GetService
IAudioRenderClient / IAudioCaptureClient / ...
```

## Shared mode

共享模式下：

- 多个应用共享 endpoint；
- Windows audio engine 负责混音；
- `GetMixFormat` 可以取得 engine 用于共享模式内部处理的格式。

## Exclusive mode

独占模式下，应用直接独占 endpoint 的音频流能力，延迟和格式控制更直接，但会影响其他应用访问设备。

## Loopback

WASAPI loopback 可以捕获 render endpoint 上 audio engine 正在播放的系统混音。

典型路径：

```text
render IMMDevice
   ↓
IAudioClient.Initialize(... LOOPBACK ...)
   ↓
IAudioCaptureClient
```

## 与 SonicRoute 当前能力的区别

SonicRoute 大部分功能是在“设备控制 / session 控制 / policy”层完成，并不需要自己持续读写 PCM buffer。

只有当目标变成：

- 录制系统声音
- 自己播放 PCM
- 做 EQ / DSP
- 低延迟 capture/render
- exclusive mode

才会真正进入 WASAPI stream 编程。

## 官方资料

- About WASAPI: https://learn.microsoft.com/windows/win32/coreaudio/wasapi
- IAudioClient: https://learn.microsoft.com/windows/win32/api/audioclient/nn-audioclient-iaudioclient
- Stream Management: https://learn.microsoft.com/windows/win32/coreaudio/stream-management
- Loopback Recording: https://learn.microsoft.com/windows/win32/coreaudio/loopback-recording
