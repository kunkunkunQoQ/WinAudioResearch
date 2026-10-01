# COM Threading 与 Apartment

> 状态：🟢 Public API + ✅ SonicRoute implementation notes

COM threading 是 Windows Audio 中非常容易被忽略的稳定性问题。

## 1. STA 与 MTA

常见 apartment：

- STA：Single-Threaded Apartment
- MTA：Multi-Threaded Apartment

WPF UI 主线程通常是 STA。

后台音频 worker 则常适合明确使用 MTA。

## 2. IAudioSessionNotification

使用 session notification 时，需要特别注意：

- 正确初始化 COM；
- callback 所在线程模型；
- callback 对象生命周期；
- 按文档要求先触发 session enumeration。

“Register 成功但没有 OnSessionCreated”不一定是 Audio Service 坏了，也可能是 threading / initialization 问题。

## 3. IAudioClient 的历史线程注意事项

Microsoft 的 `IAudioClient` 文档特别备注：

> Windows 8 中，第一次使用 IAudioClient 访问设备应在 STA 线程上；从 MTA 首次调用可能出现未定义行为。

这说明：

> “接口从 Vista 开始支持”不代表每个 Windows 版本的线程行为完全相同。

## 4. GetService 对象的释放线程

Microsoft 对部分 WASAPI service interface（例如 `IAudioCaptureClient`）说明：

> Release 应发生在调用 `IAudioClient::GetService` 创建该 interface 的同一线程。

因此稳妥 ownership model：

```text
Audio worker thread
   ├─ Activate
   ├─ Initialize
   ├─ GetService
   ├─ use
   └─ Release
```

而不是把原生 COM 对象在 UI / worker 之间随意传递。

## 5. SonicRoute meter worker

当前 AudioMeterService：

- 创建后台线程；
- 设置 MTA；
- worker 内枚举 session / meter；
- worker 内读取；
- worker 内释放；
- 只把 managed snapshot 发给 UI。

```text
COM world                UI world
---------                --------
session objects
meter objects
     │
     └── float snapshot ─────→ Dispatcher
```

这样能减少 COM object 跨线程流动。

## 6. Callback 中不要做重活

无论：

- device notification；
- endpoint volume callback；
- session notification；

都建议：

```text
capture minimal data
→ enqueue
→ return quickly
```

避免：

- 枚举整个系统；
- 阻塞 UI；
- 同步等待其他 COM 线程；
- 大量文件 IO。

## 7. Managed callback 生命周期

C# 侧建议明确保留强引用：

```csharp
private MyNotificationClient _notification;
```

而不是注册一个临时对象后完全不再引用。

退出时也应成对：

```text
Register
...
Unregister
```

## 8. 调试时记录线程信息

```text
ManagedThreadId:
ApartmentState:
Operation:
COM owner thread:
Callback source:
Dispose thread:
```

很多“只在某些机器偶发”的问题，最终与 threading / ownership 有关。
