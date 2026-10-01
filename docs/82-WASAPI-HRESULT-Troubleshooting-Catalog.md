# WASAPI HRESULT / Troubleshooting Catalog

> 状态：🟢 Public API  
> 用途：把“失败”快速分类成 lifecycle、format、buffer、CPU、service、permission 等问题。

## 初始化状态

### AUDCLNT_E_NOT_INITIALIZED

需要先成功：

```text
IAudioClient::Initialize
```

再调用依赖 initialized stream 的 service/method。

### AUDCLNT_E_ALREADY_INITIALIZED

同一个 IAudioClient 已经 Initialize。

通常应该：

- 创建新的 client object
- 或释放后重新 Activate

而不是重复 Initialize 同一实例。

## Endpoint

### AUDCLNT_E_DEVICE_INVALIDATED

endpoint：

- unplugged
- disabled
- removed
- reconfigured

正确方向：

```text
release → re-enumerate → reactivate
```

### AUDCLNT_E_WRONG_ENDPOINT_TYPE

典型：

- capture endpoint 上请求 IAudioRenderClient
- render endpoint 上请求 IAudioCaptureClient
- loopback flag 用在 capture endpoint

说明 API target 用错，不是“设备暂时忙”。

### AUDCLNT_E_DEVICE_IN_USE

常见：

- endpoint 已被 exclusive stream 占用
- shared endpoint 被使用时你请求 exclusive

## Service

### AUDCLNT_E_SERVICE_NOT_RUNNING

Windows Audio service 未运行。

不要误报成：

> “找不到声卡”。

## Resources

### AUDCLNT_E_RESOURCES_INVALIDATED

可能：

- stream suspended
- exclusive/offload disconnected
- packaged app quiesced
- protected output stream closed

和 DEVICE_INVALIDATED 类似但语义更偏：

> 当前 stream resources 已失效。

通常需要重建 stream。

## Buffer

### AUDCLNT_E_BUFFER_ERROR

GetBuffer 无法取得 packet / buffer。

Capture 在特定情况下可以等待下一次 processing pass；重复失败时应考虑 Stop/Reset/rebuild。

### AUDCLNT_E_BUFFER_TOO_LARGE

Render 请求 frames 超过：

```text
bufferSize - currentPadding
```

这是 buffer math bug。

### AUDCLNT_E_BUFFER_SIZE_ERROR

常见于：

- exclusive
- event-driven

但请求 / release packet size 不符合 endpoint buffer size 要求。

### AUDCLNT_E_OUT_OF_ORDER

GetBuffer / ReleaseBuffer 调用配对顺序错误。

例如：

```text
GetBuffer
GetBuffer   ← wrong
ReleaseBuffer
```

### AUDCLNT_E_INVALID_SIZE

ReleaseBuffer 写入 frames 超过上一轮 GetBuffer 请求数量。

## CPU

### AUDCLNT_E_CPUUSAGE_EXCEEDED

Audio Engine 检测 processing pass 多次超过允许 CPU budget。

这说明：

- realtime callback 太慢
- period 太短
- DSP 太重
- scheduling 有问题

不要仅增加 try/catch。

## Exclusive

### AUDCLNT_E_EXCLUSIVE_MODE_NOT_ALLOWED

用户 / policy 不允许 app 独占 endpoint。

应：

- fallback shared
- 或明确告诉用户

而不是强制改系统设置。

## Format

### Unsupported format

使用：

```text
IsFormatSupported
```

检查。

不要把 unsupported format 当成 driver crash。

## Success Status 也要处理

### AUDCLNT_S_BUFFER_EMPTY

Capture GetBuffer：

> 当前没有数据。

这是 success status，不是 exception。

代码不应写：

```text
hr != S_OK → failure
```

更一般应使用：

```text
SUCCEEDED(hr)
FAILED(hr)
```

## 日志建议

```text
HRESULT hex
HRESULT signed decimal
API
Windows Build
Endpoint ID
StableId
Flow
Role
Shared/Exclusive
Format
Period
Stream flags
Category
Device state
```

## 官方资料

- IAudioClient  
  https://learn.microsoft.com/windows/win32/api/audioclient/nn-audioclient-iaudioclient
- InitializeSharedAudioStream  
  https://learn.microsoft.com/windows/win32/api/audioclient/nf-audioclient-iaudioclient3-initializesharedaudiostream
- IAudioRenderClient::GetBuffer  
  https://learn.microsoft.com/windows/win32/api/audioclient/nf-audioclient-iaudiorenderclient-getbuffer
- IAudioCaptureClient::GetBuffer  
  https://learn.microsoft.com/windows/win32/api/audioclient/nf-audioclient-iaudiocaptureclient-getbuffer
