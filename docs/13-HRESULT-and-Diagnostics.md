# HRESULT 与 Windows Audio 诊断

> 状态：🟢 Public API + ✅ SonicRoute practice

Windows Audio 研究代码最不应该写成：

```text
try { ... } catch { }
```

至少在 debug / research 层，应该保留 HRESULT。

## 1. 建议统一日志格式

```text
Operation: ISimpleAudioVolume.SetMasterVolume
HRESULT:  0xXXXXXXXX
Decimal:  ...
PID:      ...
Endpoint: ...
Windows:  ...
Build:    ...
```

Undocumented API 再加：

```text
IID:
CLSID / ActivatableClass:
VtableSlot:
Arguments:
```

## 2. HRESULT 判断

COM 常见规则：

```text
hr >= 0 → success / success-status
hr <  0 → failure
```

不要只判断：

```text
hr == 0
```

因为成功状态不一定只有 `S_OK`。

## 3. 常见错误类别

### E_INVALIDARG

常见原因：

- 音量超范围；
- channel index 越界；
- internal policy 收到错误格式 device ID；
- undocumented ABI 参数语义不正确。

### AUDCLNT_E_DEVICE_INVALIDATED

endpoint 被：

- 拔出；
- 禁用；
- 重新配置；
- 驱动重启；
- 资源改变。

常见恢复：

```text
release old graph
→ re-enumerate
→ reactivate
```

### AUDCLNT_E_SERVICE_NOT_RUNNING

Windows Audio service 没有运行。

这和“设备不存在”不是同一个问题。

## 4. 成功状态也可能携带重要信息

`IAudioSessionControl2::GetProcessId` 可以返回：

```text
AUDCLNT_S_NO_SINGLE_PROCESS
```

它仍是成功状态，但表示 session 涉及多个进程。

如果代码写成：

```text
if (hr != 0) fail;
```

就会错误处理这种返回值。

## 5. SonicRoute 的实用模式

当前不少底层接口使用：

```csharp
[PreserveSig]
int Method(...)
```

失败时保留：

```text
HRESULT=0xXXXXXXXX (decimal)
```

这对排查 AudioPolicyConfig 特别重要。

## 6. 研究日志

Public API：

```text
Windows Build
Architecture
Endpoint
Operation
HRESULT
Observed behavior
```

Undocumented API 再补：

```text
Interface IID
Activation route
Vtable slot
Parameter interpretation
Before state
After state
Persistence after restart
```

## 7. 不要吞失败后继续更新 UI

错误模式：

```text
call internal API
catch
update UI as if success
```

更稳妥：

- 底层返回明确 result；
- UI 只在确认成功后更新；
- 失败保留 HRESULT；
- 下一次操作前重新同步系统真实状态。

## 8. 参考

- System Error Codes  
  https://learn.microsoft.com/windows/win32/debug/system-error-codes
- COM Error Handling  
  https://learn.microsoft.com/windows/win32/com/error-handling-in-com
