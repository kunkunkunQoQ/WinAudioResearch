# SonicRoute PolicyConfig：ERole / EDataFlow 参数语义需要复核

> 状态：🧪 Experiment / code audit  
> 这是一条研究记录，不在这里直接修改 SonicRoute。

## 发现

SonicRoute 当前：

```text
SonicRoute.Core/Interop/PolicyConfigClient.cs
```

把 `IPolicyConfig.SetDefaultEndpoint` 声明为：

```csharp
int SetDefaultEndpoint(
    [MarshalAs(UnmanagedType.LPWStr)] string wszDeviceId,
    EDataFlow dataFlow);
```

调用方传入：

```csharp
SetDefaultEndpoint(deviceId, flow)
```

源码：

https://github.com/kunkunkunQoQ/SonicRoute/blob/master/SonicRoute.Core/Interop/PolicyConfigClient.cs

## 为什么值得复核

公开的 MMDevice 枚举定义：

```text
EDataFlow:
eRender  = 0
eCapture = 1
eAll     = 2

ERole:
eConsole        = 0
eMultimedia     = 1
eCommunications = 2
```

而多个长期使用 PolicyConfig 的公开项目，把未公开的 `IPolicyConfig::SetDefaultEndpoint` 第二参数声明为：

```cpp
SetDefaultEndpoint(PCWSTR deviceId, ERole role)
```

例如：

https://github.com/matzman666/OpenVR-AdvancedSettings/blob/master/src/tabcontrollers/audiomanager/IPolicyConfig.h

## 为什么它可能“看起来能工作”

两组 enum 的底层整数刚好都是 0 / 1 / 2。

因此 ABI 层面：

```text
EDataFlow.eRender  (0) -> ERole.eConsole        (0)
EDataFlow.eCapture (1) -> ERole.eMultimedia     (1)
EDataFlow.eAll     (2) -> ERole.eCommunications (2)
```

调用未必会因为参数大小或值域直接失败。

但参数的 **语义不同**。

## 可能造成的结果

如果 common PolicyConfig 定义在当前 Windows 上仍成立，那么现有调用更可能表示：

- 切输出设备时，仅设置 Console role；
- 切输入设备时，设置的是 Multimedia role；
- 并不是通过第二参数告诉 PolicyConfig “这是 render / capture”。

render / capture 实际上已经包含在传入的 endpoint device ID 本身。

## 如何验证

不要只看 UI 是否“切过去了”，应分别检查三个 role：

```text
GetDefaultAudioEndpoint(eRender, eConsole)
GetDefaultAudioEndpoint(eRender, eMultimedia)
GetDefaultAudioEndpoint(eRender, eCommunications)

GetDefaultAudioEndpoint(eCapture, eConsole)
GetDefaultAudioEndpoint(eCapture, eMultimedia)
GetDefaultAudioEndpoint(eCapture, eCommunications)
```

测试建议记录：

- Windows Build
- 操作前六个 flow/role 组合
- 调用 SetDefaultEndpoint 后六个组合
- HRESULT
- Windows 设置 UI 中的变化

## 当前结论

这条记录目前应标为 **“需要独立实测确认”**，而不是直接写成 SonicRoute bug。

原因是 `IPolicyConfig` 本身属于未公开接口；对 undocumented ABI 的判断不能只靠某一个第三方 header。

但它已经足够说明一个重要原则：

> 未公开 COM 接口即使调用“不崩”，也不代表参数语义声明正确。

## Microsoft enum references

- EDataFlow: https://learn.microsoft.com/windows/win32/api/mmdeviceapi/ne-mmdeviceapi-edataflow
- ERole: https://learn.microsoft.com/windows/win32/api/mmdeviceapi/ne-mmdeviceapi-erole
