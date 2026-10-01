# 设备变化与通知机制

> 状态：🟢 Public API

长期运行的 Windows 音频程序不能假设设备列表固定不变。

## IMMNotificationClient

通过：

```text
IMMDeviceEnumerator
   ↓ RegisterEndpointNotificationCallback
IMMNotificationClient
```

可以收到：

- `OnDeviceAdded`
- `OnDeviceRemoved`
- `OnDeviceStateChanged`
- `OnDefaultDeviceChanged`
- `OnPropertyValueChanged`

## 推荐策略

收到事件后，不要在 callback 内执行大量 UI 或复杂 COM 工作。

更稳妥的做法是：

1. 记录变化；
2. 将刷新请求投递到自己的工作队列；
3. 合并短时间内重复事件；
4. 重新枚举需要的 endpoint；
5. 释放旧 COM 对象。

## 为什么事件比高频轮询更合适

设备变化本身是低频事件。高频枚举所有 endpoint 会产生不必要的 COM 调用和对象创建。

不过驱动生态复杂，实际产品是否增加低频兜底应基于实测，而不是默认所有驱动都完美触发通知。

## 官方资料

- IMMNotificationClient: https://learn.microsoft.com/windows/win32/api/mmdeviceapi/nn-mmdeviceapi-immnotificationclient
- Device Events: https://learn.microsoft.com/windows/win32/coreaudio/device-events
