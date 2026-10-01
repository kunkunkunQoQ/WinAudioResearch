# Windows Audio Glossary

## Endpoint
一个音频播放或录音端点，例如扬声器、耳机、麦克风、HDMI、蓝牙或虚拟设备。常见对象：`IMMDevice`。

## Render
音频输出方向：`EDataFlow.eRender`。

## Capture
音频输入方向：`EDataFlow.eCapture`。

## Role
默认 endpoint 的使用角色：Console / Multimedia / Communications。它与 Render / Capture 不是一个维度。

## Audio Session
Windows Audio Engine 用于组织相关共享模式 stream 的逻辑控制对象。**不等于 process**。

## WASAPI
Windows Audio Session API，用于真正的 render / capture stream 数据传输。

## Shared Mode
多个应用通过 Windows Audio Engine 共享 endpoint。

## Exclusive Mode
应用独占 endpoint stream。

## RCW
Runtime Callable Wrapper，.NET 对 COM object 的 managed wrapper。

## HRESULT
COM 常见状态值。通常 `>= 0` 为成功 / 成功状态，`< 0` 为失败。

## HSTRING
Windows Runtime 字符串类型，不是普通 LPWSTR。

## PROPVARIANT
Windows Property System 的 variant 数据结构；读取后通常需要 `PropVariantClear`。

## Endpoint Volume
设备层主音量，常见接口：`IAudioEndpointVolume`。

## Session Volume
Audio Session 层主音量，常见接口：`ISimpleAudioVolume`。

## Peak Meter
瞬时 peak 活动值，常见接口：`IAudioMeterInformation`。

## PolicyConfig
Windows 内部音频策略相关接口的常见称呼，不应自动理解为公开稳定 SDK。

## Persisted Endpoint
为某应用保存的首选 endpoint policy。

## Device Invalidated
已有 endpoint / stream 因设备拔插、禁用、驱动重新配置等原因失效，通常需要重新枚举并重建对象。
