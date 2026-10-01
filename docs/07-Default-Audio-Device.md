# 系统默认音频设备：公开读取 vs 内部设置

> 状态：🟢 Public API（读取） + 🔴 Undocumented（常见桌面设置方式） + ✅ SonicRoute Verified

“读取默认设备”和“设置默认设备”并不是一对完全对称的公开接口。

## 1. 读取默认 endpoint：公开 API

```text
IMMDeviceEnumerator
   ↓
GetDefaultAudioEndpoint(flow, role)
   ↓
IMMDevice
```

参数：

- `EDataFlow`
- `ERole`

例如：

```text
(eRender, eConsole)
(eRender, eMultimedia)
(eRender, eCommunications)
(eCapture, eConsole)
(eCapture, eMultimedia)
(eCapture, eCommunications)
```

## 2. 默认设备不是一个值

更准确的模型是：

```text
DefaultEndpoint[flow][role]
```

通讯软件常关心 Communications role，而普通媒体播放更常关注 Console / Multimedia。

## 3. 设置默认 endpoint：常见实现依赖 IPolicyConfig

SonicRoute 当前使用未公开 COM class：

```text
CLSID_PolicyConfigClient
870AF99C-171D-4F9E-AF0D-E63DF40C2BC9
```

接口 IID：

```text
F8679F50-850A-41CF-9C72-430F290290C8
```

方法表中包含：

```text
SetDefaultEndpoint
```

但：

> `IPolicyConfig` 并不是 Microsoft 为普通 Win32 应用公开承诺稳定的 Core Audio API。

详见：
[System PolicyConfig](../undocumented/System-PolicyConfig.md)

## 4. 一个真实的 SonicRoute 研究问题

SonicRoute 当前源码把 `SetDefaultEndpoint` 第二参数声明为：

```text
EDataFlow
```

多个其他公开实现使用：

```text
ERole
```

因为两个 enum 恰好都使用 0 / 1 / 2，ABI 上可能看起来正常，但语义完全不同。

单独记录：

[PolicyConfig：ERole / EDataFlow 参数语义复核](../findings/PolicyConfig-Role-vs-DataFlow.md)

当前应继续标记为“需要独立实测确认”，而不是只凭社区 header 直接定性。

## 5. Device ID 也不同

SonicRoute 当前注释记录：

- `IPolicyConfig.SetDefaultEndpoint` 使用 `IMMDevice.GetId()` 返回的 endpoint ID；
- per-app AudioPolicyConfig 会包装成内部策略需要的完整 device-interface path。

所以不能因为两个 API 都有 `deviceId` 参数，就默认格式一样。

## 6. 如何正确验证“默认设备切换”

不要只看 Windows UI。

建议调用前后都读取：

```text
Render  / Console
Render  / Multimedia
Render  / Communications
Capture / Console
Capture / Multimedia
Capture / Communications
```

并记录：

- endpoint ID；
- notification；
- HRESULT；
- 实际改变了哪个 role。

## 7. 默认设备变化通知

`IMMNotificationClient::OnDefaultDeviceChanged` 会提供：

- flow；
- role；
- new endpoint ID。

这比高频轮询默认设备更适合作为主机制。

## 8. 边界速查

```text
GetDefaultAudioEndpoint
    🟢 Public

OnDefaultDeviceChanged
    🟢 Public

SetDefaultEndpoint via IPolicyConfig
    🔴 Undocumented

SetPersistedDefaultAudioEndpoint
    🔴 Undocumented
```

## 9. 官方资料

- GetDefaultAudioEndpoint  
  https://learn.microsoft.com/windows/win32/api/mmdeviceapi/nf-mmdeviceapi-immdeviceenumerator-getdefaultaudioendpoint
- EDataFlow  
  https://learn.microsoft.com/windows/win32/api/mmdeviceapi/ne-mmdeviceapi-edataflow
- ERole  
  https://learn.microsoft.com/windows/win32/api/mmdeviceapi/ne-mmdeviceapi-erole
- IMMNotificationClient  
  https://learn.microsoft.com/windows/win32/api/mmdeviceapi/nn-mmdeviceapi-immnotificationclient
