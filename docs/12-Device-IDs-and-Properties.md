# Device ID、FriendlyName 与 PropertyStore

> 状态：🟢 Public API + 🟡 Observed + ✅ SonicRoute Verified

Windows Audio 里的“设备 ID”并不是所有接口都通用的一种字符串。

## 1. IMMDevice::GetId

公开 MMDevice API 返回 endpoint ID string。

典型用途：

```text
IMMDevice.GetId
     ↓
save / compare / log
     ↓
IMMDeviceEnumerator.GetDevice(id)
```

Microsoft 文档允许把这个 ID 跨进程传递，再使用 `GetDevice` 重新取得 endpoint。

## 2. 不要用 FriendlyName 当 ID

FriendlyName 例如：

```text
Speakers (Realtek Audio)
Headphones
Microphone
```

它是展示字符串，不保证：

- 唯一；
- 永久稳定；
- 不随语言变化；
- 不随驱动更新变化。

更合理的模型：

```text
Id          = identity
DisplayName = UI label
```

## 3. PKEY_Device_FriendlyName

SonicRoute 当前读取：

```text
fmtid = A45C254E-DF1C-4EFD-8020-67D146A850E0
pid   = 14
```

流程：

```text
OpenPropertyStore(STGM_READ)
       ↓
GetValue(PKEY_Device_FriendlyName)
       ↓
PROPVARIANT
       ↓
VT_LPWSTR
       ↓
PropVariantClear
```

## 4. PropertyStore 不止 FriendlyName

研究时可以做 property-dump：

```text
GetCount
  ↓
for each property:
    GetAt
    GetValue
    print PROPERTYKEY + VARTYPE + value
```

它有助于研究：

- endpoint form factor；
- interface information；
- driver / device relation；
- Windows 新增 endpoint properties。

## 5. Per-App AudioPolicyConfig 的 ID

SonicRoute 的 internal per-app route 会构造内部策略 API 使用的完整 device-interface path。

概念：

```text
\\?\SWD#MMDEVAPI# + endpointId + interfaceSuffix
```

render / capture suffix 不同。

这是 undocumented 行为。

## 6. System PolicyConfig 的 ID

SonicRoute 对系统默认 endpoint 的 `IPolicyConfig::SetDefaultEndpoint` 注释记录：

> 传 `IMMDevice::GetId` 的 endpoint ID；如果错误包装成 per-app full path，曾实测得到 `E_INVALIDARG`。

这是一个很重要的案例：

> 两个函数都叫 deviceId，不代表字符串契约相同。

## 7. 持久化风险

如果程序把 endpoint ID 写进配置：

- 设备拔插后可能不存在；
- 驱动重装后可能改变；
- 设备重新枚举后可能改变；
- 虚拟设备更新后尤其可能变化。

启动时建议：

1. 用保存 ID 调 `GetDevice`；
2. 失败则重新枚举；
3. 允许用户重新匹配；
4. 不要静默用同名设备替换，除非产品明确设计如此。

## 8. 建议日志格式

```text
Flow:
State:
Id:
FriendlyName:
Default(Console):
Default(Multimedia):
Default(Communications):
```

未公开路由研究再补：

```text
FullPolicyDevicePath:
Policy operation:
HRESULT:
```

## 9. 参考

- Endpoint ID Strings  
  https://learn.microsoft.com/windows/win32/coreaudio/endpoint-id-strings
- Device Properties  
  https://learn.microsoft.com/windows/win32/coreaudio/device-properties
- IPropertyStore  
  https://learn.microsoft.com/windows/win32/api/propsys/nn-propsys-ipropertystore
