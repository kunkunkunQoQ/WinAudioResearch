# Audio Device Lifecycle：插拔、Invalidated、Service Restart 与恢复策略

> 状态：🟢 Public API + 🟡 Engineering practice

Windows 音频长期驻留程序不能假设：

> 启动时拿到的 COM object 可以用到进程退出。

Endpoint 是动态资源。

---

## 1. 哪些事情会改变 Endpoint

- USB unplug/replug
- Bluetooth disconnect/reconnect
- A2DP ↔ HFP profile switch
- HDMI monitor hotplug
- DisplayPort dock reconnect
- driver update
- driver restart
- device disable/enable
- Windows Audio Service restart
- default role change
- sleep/resume
- Remote Desktop session change

---

## 2. IMMNotificationClient

主通知入口：

- OnDeviceStateChanged
- OnDeviceAdded
- OnDeviceRemoved
- OnDefaultDeviceChanged
- OnPropertyValueChanged

长期应用应优先：

```text
notifications
+
re-enumeration
```

而不是无限 polling。

---

## 3. Device Invalidated

WASAPI 常见：

```text
AUDCLNT_E_DEVICE_INVALIDATED
```

意思不是：

> “重试 GetBuffer 100 次”。

通常意味着：

```text
old endpoint graph is no longer valid
```

恢复：

1. Stop
2. release stream services
3. release IAudioClient
4. release old endpoint refs
5. re-enumerate
6. re-select endpoint
7. Initialize new stream
8. Start

---

## 4. Default Device Change

如果 app 的语义是：

> 始终跟随 default device

那 default role change 后应：

- stop old stream
- activate new default endpoint
- rebuild graph

不要只改 UI label。

---

## 5. Explicit Device Selection

如果用户明确选：

> USB DAC X

default change 不一定应该让 app 跟着切。

应用必须区分：

```text
follow system default
vs
pinned endpoint
```

---

## 6. Endpoint ID 失效

保存的：

```text
IMMDevice.GetId
```

未来可能失效。

恢复策略：

- try GetDevice
- if missing → enumerate
- compare StableId if available
- ask / fallback according to product policy

不要只靠 FriendlyName 自动匹配。

---

## 7. StableId

较新 Windows 提供：

```text
PKEY_AudioEndpoint_StableId
```

Windows 尝试跨：

- OS update
- driver update

保持 identity。

比单纯 endpoint ID 更适合“记住用户选择”。

仍应当作 opaque identifier。

---

## 8. Session Lifecycle

即使 endpoint 不变：

- session can appear
- inactive
- expire
- process exits
- new session replaces old

所以 session COM object 也不是永久句柄。

---

## 9. Bluetooth Profile Change

Windows 11 unified Bluetooth endpoint 下：

- endpoint UI identity 可能不明显变化
- 实际 profile / format path 可能从 A2DP 切 HFP

因此 communications app 不能只监听 DeviceAdded/Removed。

还要处理：

- format
- stream invalidation
- processing behavior

---

## 10. Sleep / Resume

Resume 后：

- device may be re-enumerated
- driver state rebuilt
- first stream init fail
- endpoint state change

应用应该能重新同步系统状态。

---

## 11. Service Restart

如果：

```text
audiosrv
```

重启，旧 COM / audio graph 状态可能失效。

正常 app 不应通过“自己重启 audiosrv”作为刷新手段，但要能承受 service restart。

---

## 12. UI Snapshot vs COM Object

推荐：

```text
Audio worker / service
  owns COM

UI
  receives immutable managed snapshots
```

这样 UI 不会长期持有易失效的 native object。

---

## 13. Retry

不要写：

```text
catch
sleep 10ms
retry forever
```

更合理：

- classify HRESULT
- device invalidated → rebuild
- service stopped → wait for service/system recovery
- invalid arg → logic bug / wrong ID
- access denied → permission/capability

---

## 14. SonicRoute 的意义

SonicRoute 中：

- 短期设备 cache
- session re-enumeration
- meter rescan
- COM release

本质都是在处理：

> Windows audio object 是动态系统资源，而不是静态数据库。

---

## 15. 相关文档

- [Device Notifications](05-Device-Notifications.md)
- [HRESULT](13-HRESULT-and-Diagnostics.md)
- [Endpoint StableId](44-Audio-Endpoint-Property-Keys.md)
- [Bluetooth](41-Bluetooth-Audio-Classic-LE.md)
