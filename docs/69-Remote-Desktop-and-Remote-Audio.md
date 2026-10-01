# Remote Desktop / RDP Audio Redirection

> 状态：🟢 Microsoft documented Remote Desktop behavior

Windows Audio 不一定只连接本机硬件。

在：

- Remote Desktop
- Azure Virtual Desktop
- Windows 365
- RemoteApp

中，audio 可以通过 RDP 重定向。

---

## 1. Audio Output Redirection

远程 session 中的 audio：

```text
Remote application
      ↓
remote Windows audio stack
      ↓
RDP audio redirection
      ↓
local client
      ↓
local speaker
```

用户看到的“remote audio”可能并不对应远程机器上的真实 physical speaker。

---

## 2. Microphone Redirection

本地 microphone：

```text
Local microphone
      ↓
RDP client
      ↓
audio input virtual channel
      ↓
remote session
      ↓
remote application
```

Microsoft Open Specifications 定义：

```text
MS-RDPEAI
Remote Desktop Protocol: Audio Input Redirection Virtual Channel Extension
```

---

## 3. Policy

管理员可以通过：

- Group Policy
- Intune
- RDP properties

控制：

- audio output redirection
- microphone redirection

所以远程 session 中：

> endpoint 存在 / 不存在

可能是 policy 结果，而不是 driver fault。

---

## 4. 用户选择

Remote Desktop client 可以允许：

- play on local device
- play on remote computer
- do not play

microphone 也可以：

- redirect
- disable

---

## 5. 对 Audio Tool 的影响

如果你的 mixer / recorder 在 remote session 中运行：

- FriendlyName 可能是 remote endpoint
- endpoint topology 与物理本地设备不同
- latency 包含 network
- format / channel capability 可能被 virtualized
- default endpoint policy 可能由 RDP session 决定

所以 diagnostics 应记录：

```text
Is remote session?
Session ID?
Endpoint name?
Device interface?
RDP audio redirection enabled?
```

---

## 6. Loopback

Remote session loopback capture 的实际行为应独立测试。

不要简单假设：

> “本地听到声音，所以远程 WASAPI loopback 一定能捕获同一位置的数据”。

RDP virtualization 可能改变 endpoint graph。

---

## 7. Latency

RDP audio latency 包含：

- remote render buffer
- encode / transport
- network
- local decode
- local playback buffer
- hardware

这与本机 WASAPI latency 完全不是同一个指标。

---

## 8. Communications

VoIP app 在 remote desktop 场景中还要同时处理：

- microphone redirection
- audio output redirection
- network latency
- application network call

形成“双层 network path”。

---

## 9. 官方资料

- Configure audio/video redirection over RDP  
  https://learn.microsoft.com/azure/virtual-desktop/redirection-configure-audio-video

- MS-RDPEAI Audio Input Redirection  
  https://learn.microsoft.com/openspecs/windows_protocols/ms-rdpeai/

- Windows App device/audio redirection  
  https://learn.microsoft.com/windows-app/device-audio-folder-redirection-teams
