# Windows Audio 已知坑点

这里记录比接口签名更容易浪费时间的问题。

## 1. 只枚举默认 endpoint

**现象：** 某些正在播放的应用完全找不到。

**原因：** 应用可能已被路由到其他 render endpoint。

**处理：** 如果目标是“全系统 session”，枚举全部 ACTIVE render endpoint。

---

## 2. 把 PID 当 session 唯一键

**现象：** 同一应用音量 / meter 行为不完整。

**原因：** 一个 PID 可以出现多个 audio session。

**处理：** 先定义产品层聚合规则，再决定取 max peak、统一音量还是分别展示。

---

## 3. RegisterSessionNotification 后没有新会话回调

**检查：**

- 是否先调用过 session enumerator `GetCount`
- callback thread 是否正确初始化 COM / MTA
- callback 对象是否仍有生命周期引用

Microsoft 对前两项有明确文档要求。

---

## 4. 把 EndpointVolume 当应用音量

`IAudioEndpointVolume` 是 endpoint master control。

应用/session 音量通常应使用 `ISimpleAudioVolume`。

---

## 5. 设备切换后继续持有旧 COM 对象

USB 拔插、蓝牙 profile 变化、默认设备切换都可能使旧对象失效。

长期程序必须允许重新枚举和重建对象。

---

## 6. 把 internal AudioPolicyConfig 当稳定 API

它目前可以实现非常有用的 per-app routing，但没有公开 SDK 兼容承诺。

必须记录 Windows Build，并准备降级。

---

## 7. 忽略 HRESULT

如果所有 COM 调用都只写成“失败就 catch”，最终只会得到一个模糊的“音频偶尔失效”。

研究仓库中的实验应尽可能打印：

```text
HRESULT=0xXXXXXXXX
```

并保留当时系统 Build。
