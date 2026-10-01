# MMDevice：设备枚举、默认端点与属性

> 状态：🟢 Public API + ✅ SonicRoute Verified

MMDevice API 是大多数 Windows Core Audio 程序的设备入口。

## 1. 核心 COM 对象

| 对象 / 接口 | GUID | 作用 |
|---|---|---|
| MMDeviceEnumerator class | `BCDE0395-E52F-467C-8E3D-C4579291692E` | 创建设备枚举器 |
| `IMMDeviceEnumerator` | `A95664D2-9614-4F35-A746-DE8DB63617E6` | endpoint 枚举 / 默认设备 / 通知 |
| `IMMDevice` | `D666063F-1587-4E43-81F1-B948E807363F` | 单个 endpoint |
| `IMMDeviceCollection` | `0BD7A1BE-7A1A-44DB-8397-CC5392387B5E` | endpoint 集合 |
| `IPropertyStore` | `886D8EEB-8CF2-4446-8D02-CDBA1DBDCF99` | 读取 / 写入属性 |

SonicRoute 当前声明：
https://github.com/kunkunkunQoQ/SonicRoute/blob/master/SonicRoute.Core/Interop/WasapiInterfaces.cs

## 2. EDataFlow

```text
eRender  = 0  // 播放
eCapture = 1  // 录音
eAll     = 2
```

它描述 endpoint 的数据流方向。

不要和 `ERole` 混淆。

## 3. DeviceState

```text
ACTIVE      = 0x1
DISABLED    = 0x2
NOTPRESENT  = 0x4
UNPLUGGED   = 0x8
```

普通设备选择 UI 往往只关心 `ACTIVE`。

诊断工具则可以枚举 ALL，把状态一起打印，帮助区分：

- 设备存在但禁用；
- 设备不在场；
- 物理连接断开；
- 真正活跃 endpoint。

## 4. 枚举链

```text
IMMDeviceEnumerator
   ↓ EnumAudioEndpoints(eRender, ACTIVE)
IMMDeviceCollection
   ↓ GetCount
   ↓ Item(i)
IMMDevice
   ↓ GetId
   ↓ OpenPropertyStore
IPropertyStore
   ↓ PKEY_Device_FriendlyName
```

一个重要原则：

> **FriendlyName 只用于显示，不应当作为唯一身份。**

多个 endpoint 可以同名，驱动升级后名称也可能变化。

## 5. Endpoint ID

`IMMDevice::GetId` 返回 endpoint ID string。

典型用途：

- 稍后通过 `GetDevice` 重建 `IMMDevice`；
- 跨进程传递设备身份；
- 在应用配置里保存用户选择。

但持久化时应认识到：

- ID 与系统设备枚举 / 驱动有关；
- 驱动重装、系统升级等情况下可能变化；
- 它不是硬件永久序列号。

详见：
[Device IDs & Properties](12-Device-IDs-and-Properties.md)

## 6. FriendlyName 与 PROPVARIANT

SonicRoute 当前读取：

```text
PKEY_Device_FriendlyName
fmtid = A45C254E-DF1C-4EFD-8020-67D146A850E0
pid   = 14
```

流程：

```text
IMMDevice.OpenPropertyStore(STGM_READ)
        ↓
IPropertyStore.GetValue
        ↓
PROPVARIANT
        ↓
VT_LPWSTR
        ↓
PropVariantClear
```

### 一定要清理 PROPVARIANT

读完字符串不能直接把结构体丢掉。

SonicRoute 使用：

```text
PropVariantClear
```

释放底层可能持有的资源。

## 7. 默认设备：Flow + Role

公开方法：

```text
GetDefaultAudioEndpoint(EDataFlow flow, ERole role)
```

ERole：

```text
eConsole        = 0
eMultimedia     = 1
eCommunications = 2
```

所以 Windows 可以同时存在：

- 默认播放 Console；
- 默认播放 Communications；
- 默认录音 Console；
- 默认录音 Communications；

等不同组合。

SonicRoute 当前 `GetDefaultDeviceId` 读取 `eConsole`，这是产品选择，不代表所有功能都只应看 Console role。

## 8. 为什么不能只枚举默认设备

如果用户路由成：

```text
Game    → Headphones
Browser → Speakers
Discord → USB headset
```

只在默认 render endpoint 上枚举 session，会漏掉其他 endpoint。

所以“全系统应用列表”和“默认设备当前 session”是两个不同目标。

## 9. SonicRoute 的短缓存

当前 `AudioService.GetDevices` 对设备列表使用约 **3 秒 TTL**。

目的：

- 启动阶段多个 UI 同时请求时避免重复枚举；
- 快捷键连续操作时减少 COM 调用。

代价：

- 设备插拔后列表可能短暂滞后；
- 要立即精确时应强制刷新或结合 notification。

这是应用层性能权衡，不是 Windows API 规范。

## 10. 常见失败处理

### endpoint invalidated

USB 拔插、蓝牙 profile 切换、驱动重启后，旧 COM 对象可能失效。

通常正确恢复是：

```text
release old objects
→ re-enumerate
→ re-activate
```

而不是一直重试同一对象。

### 忘记释放 collection / device / property store

长期常驻工具容易因此积累 COM reference。

## 11. 官方资料

- IMMDeviceEnumerator  
  https://learn.microsoft.com/windows/win32/api/mmdeviceapi/nn-mmdeviceapi-immdeviceenumerator
- Enumerating Audio Devices  
  https://learn.microsoft.com/windows/win32/coreaudio/enumerating-audio-devices
- Device Properties  
  https://learn.microsoft.com/windows/win32/coreaudio/device-properties
- Endpoint ID Strings  
  https://learn.microsoft.com/windows/win32/coreaudio/endpoint-id-strings
