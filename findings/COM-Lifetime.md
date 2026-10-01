# COM 生命周期与资源释放

> 状态：🟡 Implementation notes + ✅ SonicRoute Verified

Windows 音频程序长时间运行后出现内存增长，很多时候不是“GC 不工作”，而是 COM 生命周期没有处理好。

## 两种对象要分清

### RCW

C# `[ComImport]` 对象通常由 Runtime Callable Wrapper 包装。

项目中可能使用：

```csharp
Marshal.ReleaseComObject(value);
```

### 原始 interface pointer

手工 `QueryInterface` / WinRT factory 得到的 `IntPtr`：

```csharp
Marshal.Release(ptr);
```

不要把它当 RCW。

## HSTRING 也不是 COM object

```text
WindowsCreateString
        ↓
use
        ↓
WindowsDeleteString
```

## 枚举刷新

如果每次刷新 session / device 列表都不断创建新 RCW，而旧对象长期被集合、事件订阅或 closure 持有，常驻程序的内存和 COM reference 都会积累。

SonicRoute 的 meter 实现会在重新扫描前先释放旧 session handle，再重新枚举。

## Callback 生命周期

注册：

```text
Register...Callback
```

通常就应设计对应的：

```text
Unregister...Callback
```

否则 callback 对象和底层 COM 对象可能形成长期引用关系。

## 不要机械调用 FinalReleaseComObject

“看到 COM 就强制 FinalRelease”同样危险。

如果同一 RCW 仍被其他代码使用，强制释放会造成不可预测异常。

原则是：明确 ownership，再释放。
