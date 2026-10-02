# IAudioViewManagerService：把 HWND 与 Audio Stream 关联

> 状态：🟢 Public API

Windows Build 22621+ 在 `audioclient.h` 中提供：

```text
IAudioViewManagerService
```

它用于：

> 把一个 audio stream 与特定 HWND 关联。

---

## 1. 获取方式

从当前 stream 的：

```text
IAudioClient
```

调用：

```text
GetService(IID_IAudioViewManagerService)
```

得到接口。

---

## 2. SetAudioStreamWindow

核心方法：

```text
SetAudioStreamWindow(HWND hwnd)
```

把当前 audio stream 关联到一个窗口。

---

## 3. 官方用途

Microsoft 文档特别提到：

> 用于 Mixed Reality 场景中，正确表示音频与 app window 的空间位置关系。

所以不要误解为：

> “这是设置 Windows 音量合成器图标 / 分组的 API”。

它不是 GroupingParam 的替代。

---

## 4. 为什么多窗口 App 会需要

一个 app 可以有：

- main window
- video window
- call window
- floating player

不同 window 可能有独立 audio stream。

如果系统知道：

```text
stream ↔ HWND
```

可以在支持的体验里更正确理解 audio source location。

---

## 5. 最低系统

Microsoft 当前文档：

```text
Minimum client: Windows Build 22621
```

因此使用前应做 version / interface availability 检测。

---

## 6. 与 Audio Session Identity 区别

```text
IAudioViewManagerService
→ stream ↔ HWND

GroupingParam
→ multiple session UI grouping

Session GUID
→ stream → session identity
```

三者不能混用。

---

## 7. 接口不可用时

旧 Windows：

```text
Query/GetService → interface unavailable
```

应该安全降级。

不能因为这个接口不存在就阻止正常 audio playback。

---

## 8. 官方资料

- IAudioViewManagerService  
  https://learn.microsoft.com/windows/win32/api/audioclient/nn-audioclient-iaudioviewmanagerservice

- SetAudioStreamWindow  
  https://learn.microsoft.com/windows/win32/api/audioclient/nf-audioclient-iaudioviewmanagerservice-setaudiostreamwindow
