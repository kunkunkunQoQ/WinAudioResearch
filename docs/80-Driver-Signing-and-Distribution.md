# Windows Audio Driver Signing / Distribution

> 状态：🟢 Public Windows driver policy

如果项目包含：

- virtual speaker
- virtual microphone
- APO driver package
- ACX / WDM audio driver

发布流程必须包含 driver signing。

## 1. 为什么必须签名

64-bit Windows kernel-mode code 有强制签名要求。

Windows 10 1607 起，新 kernel-mode driver 的正式加载通常要求由 Microsoft Dev Portal 签名。

所以：

> 本地 test mode 能装

不等于：

> 普通用户 Windows 可以直接装。

## 2. Development / Test Signing

开发阶段可以：

- test certificate
- test signing mode
- test machine

用于：

- debug
- driver bring-up
- local validation

不要把 test-signed driver 当成正式发行包。

## 3. Production Signing

正式路径涉及：

- Windows Hardware Developer Program
- EV certificate for dashboard identity/setup
- submission
- Microsoft signature

具体要求会更新，应以 Hardware Dev Center 当前规则为准。

## 4. HLK-tested Signing

Microsoft 推荐生产路径：

```text
Driver
  ↓
HLK tests
  ↓
Hardware submission
  ↓
Dashboard signed
```

优势：

- hardware compatibility validation
- reliability
- security
- power
- serviceability
- performance

都进入正式测试流程。

## 5. Attestation Signing

Attestation signing 更适合某些 testing / special scenarios。

Microsoft 当前明确区分：

- HLK-tested production path
- attestation testing scenarios

不能因为 attestation 流程更短就默认它等价于所有 retail distribution。

## 6. Catalog

PnP driver package 常包含：

- INF
- SYS/DLL
- CAT

Microsoft 返回 signed catalog 后，安装系统据此验证 package integrity / publisher。

## 7. Secure Boot

现实用户机器通常开启：

```text
Secure Boot
```

不要设计依赖：

- disable Secure Boot
- enable test mode

才能使用的正式产品。

## 8. Driver Install

常用：

```text
PnPUtil
```

进行：

- add driver
- install
- delete package
- enumerate driver/device

自动化 installer 不应仅依赖老 DevCon sample。

## 9. Uninstall

Virtual audio driver 必须测试：

- app uninstall
- driver package removal
- reboot
- endpoint cleanup
- default device recovery

最糟糕的产品体验之一是：

> 卸载软件后仍留下 broken default audio endpoint。

## 10. Update

升级需要考虑：

- driver version
- package ranking
- endpoint identity
- settings migration
- StableId
- default role

不能简单覆盖 .sys。

## 11. Architecture

发布矩阵可能包括：

- x64
- ARM64

各自需要正确 driver binary / catalog / package。

## 12. 官方资料

- Driver Signing Policy  
  https://learn.microsoft.com/windows-hardware/drivers/install/kernel-mode-code-signing-policy--windows-vista-and-later-

- Driver Signing Options  
  https://learn.microsoft.com/windows-hardware/drivers/dashboard/driver-signing-offerings

- Driver Signing Tutorial  
  https://learn.microsoft.com/windows-hardware/drivers/install/windows-driver-signing-tutorial

- HLK  
  https://learn.microsoft.com/windows-hardware/test/hlk/
