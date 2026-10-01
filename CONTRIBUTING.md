# Contributing

WinAudioResearch 的目标是记录 **可验证、可追溯** 的 Windows 音频技术结论。

提交 Issue / PR 时，建议附上：

- Windows 版本与 Build
- x64 / ARM64
- .NET / C++ 运行环境
- 音频设备与驱动类型（若相关）
- 最小复现步骤
- HRESULT / 异常信息
- 结论属于 Public API、Observed、Undocumented 还是 Experiment

如果内容涉及未公开 Windows 接口，请不要只写“可以工作”，还应注明：

1. 接口来源；
2. 已验证的 Windows 版本；
3. 是否依赖固定 IID / vtable slot；
4. 是否存在公开 API 替代方案；
5. 失败时对系统状态有什么影响。

文档优先使用 Microsoft Learn / Windows SDK 作为公开接口来源。
