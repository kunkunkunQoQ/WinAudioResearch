# RDP / Remote Desktop Audio Redirection

> 状态：🟢 Microsoft documented platform behavior

Remote Desktop 会引入一层“虚拟音频环境”。

应用开发时，如果只按本机 endpoint 思考，进入 RDP / AVD / Windows 365 后可能得到完全不同的设备和 session 行为。

---

## 1. Remote Audio Output

RDP 可以把远端 Windows 的声音：

- 播放到本地设备
- 播放在远端
- 完全禁用

因此远端应用看到的 audio endpoint 可能是：

```text
Remote Audio
```

而不是远端机器真实的 Realtek / USB / HDMI endpoint。

---

## 2. Microphone Redirection

本地 microphone 可以被重定向到远端 session。

远端 Windows 会看到一个 capture endpoint。

链路：

```text
Local Microphone
   ↓
RDP transport
   ↓
Remote virtual capture endpoint
   ↓
Remote application
```

---

## 3. WTS Session 与 Audio Session

`IAudioSessionEvents::OnSessionDisconnected` 的原因枚举专门包含：

- SessionLogoff
- SessionDisconnected

这说明 Audio Session 生命周期和 Windows Terminal Services session 有直接关系。

RDP disconnect 时：

> audio session 可能被系统断开，而不是简单进入 Inactive。

---

## 4. 设备身份会变化

本地：

```text
USB Headset
```

通过 RDP 后，远端应用通常不会看到原始 USB device identity。

所以不要假设：

- IMMDevice ID
- StableId
- FriendlyName
- driver

可以跨 RDP session 和本地机器一一对应。

---

## 5. Format / Latency

RDP audio 会增加：

- encode/decode
- network transport
- jitter buffer
- resampling

因此：

> WASAPI buffer period 并不代表用户耳朵听到的完整 remote latency。

---

## 6. 应用要不要特殊处理 RDP

普通 playback app：

- 通常直接使用系统提供的 default endpoint 即可。

专业 / low latency app：

- 应检测 session environment
- 不应把远程 endpoint latency 当真实 local hardware latency

诊断工具：

- 建议标记当前 Windows session 是否 remote
- 记录 endpoint driver / transport

---

## 7. RDP Audio Redirection Policy

管理员可以通过：

- Group Policy
- Intune
- RDP properties

控制：

- audio output redirection
- microphone capture redirection

因此某个 capture endpoint 不存在，可能是 policy，而不是 microphone API bug。

---

## 8. OnSessionDisconnected 恢复

当 disconnect reason 是：

- WTS logoff
- WTS disconnected
- server shutdown
- device removal
- format changed
- exclusive override

应用应该：

1. 释放旧 IAudioClient
2. 释放 GetService 得到的接口
3. 等待环境恢复 / endpoint 重新出现
4. 重新枚举
5. 重新 Activate

---

## 9. 测试矩阵

如果应用支持 remote desktop，至少测试：

```text
Local desktop
RDP connect
RDP disconnect
RDP reconnect
Microphone redirected
Microphone blocked
Audio played locally
Audio disabled
User logoff
```

---

## 10. 官方资料

- Configure audio and video redirection over RDP  
  https://learn.microsoft.com/azure/virtual-desktop/redirection-configure-audio-video

- IAudioSessionEvents::OnSessionDisconnected  
  https://learn.microsoft.com/windows/win32/api/audiopolicy/nf-audiopolicy-iaudiosessionevents-onsessiondisconnected
