# Undocumented / Reverse Engineering 资料索引

> 状态：🔴 Undocumented / Community Research  
> 这页只做“研究导航”，不把社区实现自动描述成 Microsoft 规范。

Windows Audio 有一些非常实用、但官方没有公开稳定 setter / contract 的机制。

典型：

- system default endpoint setter
- per-app persisted endpoint routing
- internal AudioPolicyConfig
- internal registry layout

这些内容必须和 Public API 严格分层。

---

## 1. EarTrumpet

https://github.com/File-New-Project/EarTrumpet

价值：

- 长期维护
- Windows audio mixer 实战
- per-app routing
- internal audio policy
- Windows version branching

重点搜索：

```text
IAudioPolicyConfigFactory
AudioPolicyConfigFactory
SetPersistedDefaultAudioEndpoint
```

---

## 2. SonicRoute

https://github.com/kunkunkunQoQ/SonicRoute

当前已验证 / 记录：

- Win10 / Win11 internal IID split
- HSTRING
- RoGetActivationFactory
- manual vtable call
- per-app input/output route
- system default PolicyConfig
- route persistence
- device ID conversion

WinAudioResearch 对这些内容重新按：

- Public
- Observed
- Undocumented
- Experiment

分级。

---

## 3. PolicyConfig 社区 Headers

GitHub 上大量项目声明：

```text
IPolicyConfig
PolicyConfigClient
SetDefaultEndpoint
```

常见 IID / CLSID 被多个项目重复使用。

研究时应该做：

1. 比较多个独立实现
2. 看 Windows 版本
3. 确认 vtable method order
4. 实测 role
5. 记录 HRESULT

不能只复制第一个 StackOverflow answer。

---

## 4. Registry Audio Policy

社区和项目源码常观察：

```text
HKCU\Software\Microsoft\Internet Explorer\LowRegistry\Audio\PolicyConfig
```

与：

- per-app volume
- routing
- property store

相关。

但这是内部 implementation detail。

不要：

- 直接假定 schema 永远不变
- 把 key 当 public persistence API
- 整树删除却不提示用户

---

## 5. Windows Settings 本身也是观察对象

遇到 internal API 不确定时，可以做 black-box 对照：

1. Windows Settings 手工修改
2. ProcMon 记录 registry / COM activity
3. app 查询 public observable state
4. 比较 internal API 写入后的结果

这种方法适合 reverse engineering，但仍不能把结论升级为 official contract。

---

## 6. symbol / binary research

更深入时，研究者可能使用：

- public symbols
- WinDbg
- IDA / Ghidra
- COM metadata
- WinRT metadata
- activation factory tracing

但应尊重：

- license
- applicable law
- redistribution rules
- security boundaries

本仓库更关注 interoperability / compatibility research，而不是绕过安全机制。

---

## 7. ReactOS / Wine

研究历史 Windows multimedia API 时，有时可以参考：

- Wine
- ReactOS

它们可以帮助理解：

- WinMM
- DirectSound
- legacy multimedia semantics

但：

> 它们不是 Windows 实现源码。

只能作为独立 reimplementation reference。

---

## 8. Chromium / Firefox / WebRTC

大型浏览器也包含非常成熟的 Windows audio backend。

适合研究：

- WASAPI capture/render
- communications
- device change
- WebRTC AEC integration
- latency
- Bluetooth behavior

但它们的 abstraction 很大，需要区分：

> 浏览器自己的策略

和：

> Windows API 本身。

---

## 9. OBS Studio

OBS 是研究 Windows audio capture 很有价值的开源项目。

适合：

- WASAPI output capture
- process/application capture
- device reconnect
- timestamp / sync
- monitoring

同样应回到 Microsoft public contract 验证底层语义。

---

## 10. Chromium Audio

Chromium source：

https://chromium.googlesource.com/chromium/src/

搜索：

```text
WASAPI
AudioDeviceListenerWin
CoreAudioUtilWin
```

可研究 browser 如何处理真实 Windows audio device edge cases。

---

## 11. WebRTC

https://webrtc.googlesource.com/src/

适合：

- AEC
- NS
- AGC
- audio device module
- Windows capture/render
- drift / latency

---

## 12. OBS Studio

https://github.com/obsproject/obs-studio

适合：

- capture
- loopback
- audio monitoring
- timestamp / sync
- reconnect

---

## 13. Community Sources 的证据等级

建议：

### Level A

Microsoft public documentation / header

### Level B

Microsoft sample

### Level C

多个长期成熟第三方项目一致

### Level D

单个项目 / issue / blog

### Level E

个人 reverse engineering / speculation

Undocumented 结论至少尽量达到：

```text
C + 实机验证
```

---

## 14. 记录格式

每条 internal finding 建议记录：

```text
Source:
Commit:
Windows Build:
Architecture:
IID / CLSID:
ABI:
Input:
HRESULT:
Observed output:
Regression status:
```

---

## 15. 本仓库当前 internal 专区

- [Undocumented 入口](../undocumented/README.md)
- [AudioPolicyConfig](../undocumented/AudioPolicyConfig.md)
- [IAudioPolicyConfigFactory](../undocumented/IAudioPolicyConfigFactory.md)
- [System PolicyConfig](../undocumented/System-PolicyConfig.md)
- [PolicyConfig Role vs DataFlow](../findings/PolicyConfig-Role-vs-DataFlow.md)
- [Per-App Routing Persistence](../findings/Per-App-Routing-Persistence.md)
