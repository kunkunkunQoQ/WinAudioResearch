# WASAPI Loopback 与 Process Loopback Capture

> 状态：🟢 Public API

Windows 至少有两类非常值得区分的 loopback capture：

1. Endpoint / system loopback
2. Process loopback

---

## 1. Endpoint Loopback

经典 WASAPI loopback：

```text
Render Endpoint
      ↓
Windows Audio Engine mix
      ↓
AUDCLNT_STREAMFLAGS_LOOPBACK
      ↓
IAudioCaptureClient
```

步骤：

1. 选一个 render endpoint
2. Activate `IAudioClient`
3. shared mode Initialize
4. 设置 `AUDCLNT_STREAMFLAGS_LOOPBACK`
5. `GetService(IAudioCaptureClient)`
6. 读取 samples

---

## 2. 只能 Shared Mode

Loopback flag 只能用于：

```text
AUDCLNT_SHAREMODE_SHARED
```

不能用于 exclusive-mode capture。

---

## 3. Event-driven Loopback 的版本历史

Windows 10 1703 之前：

- event-driven loopback capture 有历史限制
- 常见 workaround 是借助 render event signal capture thread

Windows 10 1703+：

- 正式支持 event-driven loopback client

所以旧代码中一些复杂 workaround 不一定仍是现代 Windows 必需。

---

## 4. Hardware loopback device != WASAPI loopback

一些声卡会暴露：

- Stereo Mix
- What U Hear
- Waveout Mix

这些是 driver / hardware endpoint。

WASAPI loopback 则：

- 不依赖存在一个叫“Stereo Mix”的设备
- Windows 可以从 audio engine 复制 system mix

所以用户没有 Stereo Mix，不代表程序不能做系统声音捕获。

---

## 5. Process Loopback

较新的 API 可以捕获：

```text
target PID + child process tree
```

或反向：

```text
everything EXCEPT target PID tree
```

这通过：

```text
ActivateAudioInterfaceAsync
+
AUDIOCLIENT_ACTIVATION_PARAMS
+
AUDIOCLIENT_PROCESS_LOOPBACK_PARAMS
```

实现。

---

## 6. AUDIOCLIENT_ACTIVATION_TYPE_PROCESS_LOOPBACK

activation type：

```text
AUDIOCLIENT_ACTIVATION_TYPE_PROCESS_LOOPBACK
```

再提供：

```text
TargetProcessId
ProcessLoopbackMode
```

---

## 7. Include / Exclude

`PROCESS_LOOPBACK_MODE`：

### INCLUDE_TARGET_PROCESS_TREE

只捕获：

- target process
- child processes

### EXCLUDE_TARGET_PROCESS_TREE

捕获系统其他音频，但排除：

- target process
- child processes

---

## 8. Process Loopback 的一个大优势

传统 system loopback 绑定某个 render endpoint。

Process loopback 官方 sample 描述的设计是：

> 捕获目标 process tree 的 render audio，不需要为每一个物理 endpoint 单独创建 capture client。

这对：

- 单应用录音
- streaming
- game capture
- per-app analyzer

非常有价值。

---

## 9. Windows 要求

`AUDIOCLIENT_PROCESS_LOOPBACK_PARAMS` 官方要求从 Windows 10 Build 20348 开始支持。

实际部署时应以：

- API availability
- SDK header
- OS Build

共同判断。

---

## 10. 权限与隐私

音频 capture 可能涉及：

- microphone privacy
- protected media
- app permissions
- session / service environment

不能把“接口存在”当作“所有进程所有场景都能无条件捕获”。

---

## 11. DRM / Protected Content

Microsoft loopback 文档指出，受保护内容可能受到 trusted audio path / DRM 限制。

因此系统录音软件应准备：

- silence
- access failure
- partial capture

而不是认为一定是 API bug。

---

## 12. 官方 Sample

Microsoft Application Loopback：

https://github.com/microsoft/Windows-classic-samples/tree/main/Samples/ApplicationLoopback

文档：

https://learn.microsoft.com/samples/microsoft/windows-classic-samples/applicationloopbackaudio-sample/

---

## 13. 官方资料

- Loopback Recording  
  https://learn.microsoft.com/windows/win32/coreaudio/loopback-recording

- ActivateAudioInterfaceAsync  
  https://learn.microsoft.com/windows/win32/api/mmdeviceapi/nf-mmdeviceapi-activateaudiointerfaceasync

- audioclientactivationparams.h  
  https://learn.microsoft.com/windows/win32/api/audioclientactivationparams/

- AUDIOCLIENT_PROCESS_LOOPBACK_PARAMS  
  https://learn.microsoft.com/windows/win32/api/audioclientactivationparams/ns-audioclientactivationparams-audioclient_process_loopback_params

- PROCESS_LOOPBACK_MODE  
  https://learn.microsoft.com/windows/win32/api/audioclientactivationparams/ne-audioclientactivationparams-process_loopback_mode
