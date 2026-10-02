# CLAP Audio Plugin Format

> 状态：第三方开放音频插件标准  
> 官方项目：free-audio/clap

CLAP：

```text
CLever Audio Plug-in API
```

是面向：

- DAW host
- synthesizer
- audio effect
- instrument plugin

的开放插件 ABI。

它不是 Windows 系统音频 API，但属于 Windows 专业音频开发生态的重要组成部分。

---

## 1. 官方仓库

https://github.com/free-audio/clap

License：

```text
MIT
```

核心目标：

> 定义 stable ABI，让 host 与 plugin 二进制互操作。

---

## 2. ABI Stability

CLAP 1.x：

> plugin binary 编译于一个 CLAP 1.x 版本，应能被其他兼容 CLAP 1.y host 加载。

这和 header-only C++ source compatibility 不一样。

重点是：

```text
ABI
```

---

## 3. Core Objects

两个最重要对象：

```text
clap_host
clap_plugin
```

Plugin 由 host 创建并驱动。

---

## 4. Plugin Lifecycle

```text
create
  ↓
init
  ↓
activate
  ↓
start_processing
  ↓
process...
  ↓
stop_processing
  ↓
deactivate
  ↓
destroy
```

不同方法有明确 thread contract。

---

## 5. Thread Contract

CLAP header 很强调：

- main-thread
- audio-thread
- thread-safe

例如：

```text
process()
```

运行在：

```text
audio-thread
```

这和 Windows WASAPI realtime callback 的原则一致：

> realtime processing 路径不能随意 blocking / allocation。

---

## 6. Extensions

CLAP 大量功能通过 extension 扩展。

例如：

- audio ports
- note ports
- params
- state
- GUI
- latency
- tail
- render
- thread-check
- timer support

Host / plugin 通过：

```text
get_extension
```

查询 support。

---

## 7. Parameters

CLAP parameter model 支持：

- automation
- gesture begin/end
- process-time parameter events
- non-processing flush

非常适合现代 DAW automation。

---

## 8. State

```text
CLAP_EXT_STATE
```

用于：

- project reload
- duplicate plugin
- preset
- save/load plugin state

---

## 9. Audio Ports

```text
CLAP_EXT_AUDIO_PORTS
```

插件可以描述：

- input/output ports
- mono/stereo
- 32-bit required
- optional 64-bit audio

---

## 10. Validator / Examples

官方 ecosystem 提供：

- clap-validator
- clap-host
- clap-plugins
- clap-wrapper
- language bindings

Windows build example：

https://github.com/free-audio/clap-plugins

---

## 11. CLAP vs VST3 / AAX

### CLAP

- open / MIT
- C ABI
- extension model
- modern host/plugin integration

### VST3

- Steinberg ecosystem
- mature cross-platform plugin standard

### AAX

- Avid / Pro Tools ecosystem
- commercial deployment有额外 license/signing流程

WinAudioResearch 不应该替开发者选“哪个最好”，而是记录：

- ABI
- licensing
- host support
- threading
- deployment

---

## 12. Windows Audio API 的位置

CLAP plugin 通常不会自己直接：

```text
IMMDevice / IAudioClient
```

Host（DAW）才负责：

```text
ASIO / WASAPI / device
```

Plugin 只处理 host 提供的 audio buffers。

所以：

```text
CLAP / VST3 / AAX
= plugin ABI layer

WASAPI / ASIO
= device I/O layer
```

必须区分。

---

## 13. 官方资料

- CLAP  
  https://github.com/free-audio/clap

- CLAP website  
  https://cleveraudio.org/

- Example plugins  
  https://github.com/free-audio/clap-plugins
