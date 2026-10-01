# Windows 版本兼容性：公开 API 与内部 ABI 要分开记录

> 状态：🟢 Public API + 🟡 Observed + 🔴 Undocumented

Windows Audio 兼容性至少要分成两套逻辑：

1. **公开 SDK 接口的最低支持系统**
2. **未公开接口在具体 Build 上的实测结果**

不能混成一句：

> “Win10/11 都支持。”

## 1. Public API：看 Minimum supported client

| 接口 | Header | 最低客户端 |
|---|---|---|
| `IMMDeviceEnumerator` | mmdeviceapi.h | Windows Vista |
| `IAudioClient` | audioclient.h | Windows Vista |
| `ISimpleAudioVolume` | audioclient.h | Windows Vista |
| `IAudioEndpointVolume` | endpointvolume.h | Windows Vista |
| `IAudioMeterInformation` | endpointvolume.h | Windows Vista |
| `IAudioSessionManager2` | audiopolicy.h | Windows 7 |
| `IAudioSessionControl2` | audiopolicy.h | Windows 7 |
| `IAudioClient3` | audioclient.h | Windows 10 |

“最低支持”也不代表所有驱动、蓝牙 profile、虚拟设备行为完全一致。

## 2. Undocumented API：只能记录实测 Build

例如 SonicRoute 当前 AudioPolicyConfig：

```text
Windows 11 21H2+ IID
AB3D4648-E242-459F-B02F-541C70306324

Downlevel IID
2A59116D-6C4F-45E0-A74F-707E3FEF9258
```

这里不能写：

> officially supported on Windows 10+

更准确的是：

> 当前项目按这些系统分支选择 internal IID；需要继续按 Build 验证。

## 3. 版本检测也可能影响 internal API

SonicRoute 在 .NET Framework 兼容工作中记录过：

- manifest compatibility 声明会影响某些版本 API 的结果；
- 如果把 Win11 判断成旧 Build，internal IID 选择可能错误；
- 表面上可能只是“路由静默失败”。

项目因此采用原生方式获取更可靠的真实 Build。

这是：

> ✅ SonicRoute Verified / implementation note

不意味着所有 .NET 应用都必须自己 P/Invoke 版本 API。

## 4. Architecture 也是兼容维度

至少记录：

```text
x64
ARM64
```

原因：

- COM interface ABI 理论上架构透明；
- 但手写结构布局、function pointer delegate、native packing 可能不是；
- 第三方驱动 / DLL 也可能限制架构。

尤其要关注：

```text
PROPVARIANT
WAVEFORMATEX / WAVEFORMATEXTENSIBLE
raw vtable function pointer
```

不能因为 x64 能跑就假设 ARM64 一定正确。

## 5. 驱动 / endpoint 类型也是变量

同一 Windows Build 下：

- Realtek HDA
- USB DAC
- Bluetooth A2DP
- Bluetooth HFP
- HDMI / DP
- virtual audio device

都可能表现不同。

建议兼容报告至少包含：

```text
Windows:
Build:
Architecture:
Runtime:
Endpoint type:
Driver:
Operation:
HRESULT:
Observed result:
```

## 6. 重新验证触发条件

出现以下情况时，应重新跑 undocumented 测试：

- Windows feature update；
- Insider major build；
- Audio Service 行为变化；
- 新增 ARM64 支持；
- Windows 音量合成器实现改变；
- 长期参考项目调整 internal IID；
- vtable 调用开始出现新 HRESULT。

## 7. 失败也要保留

不要只提交：

```text
Build 26xxx works
```

更有价值的是：

```text
Build:
Operation:
Expected:
Actual:
HRESULT:
Repro rate:
Regression from:
```

失败可以帮助判断到底是：

- IID 变化；
- ABI 变化；
- 参数格式变化；
- 权限变化；
- 单驱动问题。

## 8. 相关文档

- [API Reference Matrix](11-API-Reference-Matrix.md)
- [HRESULT & Diagnostics](13-HRESULT-and-Diagnostics.md)
- [Research Validation Checklist](16-Research-Validation-Checklist.md)
