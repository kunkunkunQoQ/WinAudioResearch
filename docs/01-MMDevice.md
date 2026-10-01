# MMDevice：设备枚举与端点

> 状态：🟢 Public API + ✅ SonicRoute Verified

MMDevice API 是 Windows Core Audio 最常见的入口。

## 核心对象

```text
MMDeviceEnumeratorComObject
        ↓
IMMDeviceEnumerator
        ├─ EnumAudioEndpoints
        ├─ GetDefaultAudioEndpoint
        ├─ GetDevice
        └─ RegisterEndpointNotificationCallback
```

## EDataFlow

常见方向：

- `eRender`：播放设备
- `eCapture`：录音设备
- `eAll`：全部

## ERole

Windows 默认设备不是一个单独概念，而是按 role 区分：

- `eConsole`
- `eMultimedia`
- `eCommunications`

因此“系统默认设备”在代码里经常需要明确：**哪个 flow + 哪个 role**。

## IMMDevice

`IMMDevice` 常用方法：

- `Activate`：获得设备相关 COM 接口
- `OpenPropertyStore`：读取设备属性
- `GetId`：endpoint ID
- `GetState`：设备状态

Friendly Name 通常从 `IPropertyStore` 读取 `PKEY_Device_FriendlyName`。

## 实战注意

### 1. 不要只枚举默认设备

如果目标是分析“系统里所有正在出声的应用”，只打开默认 render endpoint 会漏掉被手动路由到其他设备的应用。

SonicRoute 的实时声音活动实现因此会枚举所有 ACTIVE render endpoint，再逐个枚举 session。

### 2. endpoint ID 是系统接口标识，不是 UI 名称

不要把 Friendly Name 当唯一键。多个设备可以显示同名。

### 3. 设备可能随时失效

蓝牙切换、USB 拔插、驱动重启都可能让已有 COM 对象失效。持久运行程序必须考虑重新枚举。

## 官方资料

- IMMDeviceEnumerator: https://learn.microsoft.com/windows/win32/api/mmdeviceapi/nn-mmdeviceapi-immdeviceenumerator
- Enumerating Audio Devices: https://learn.microsoft.com/windows/win32/coreaudio/enumerating-audio-devices
- Device Properties: https://learn.microsoft.com/windows/win32/coreaudio/device-properties
