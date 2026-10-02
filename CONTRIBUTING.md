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

修改 `api/` 后，从仓库根目录运行：

```bash
python scripts/validate_api_db.py
python scripts/validate_core_audio_audit.py
python -m unittest discover -s tests -v
```

Core Audio IID/CLSID 的来源与范围记录在 [core-audio-audit.json](api/core-audio-audit.json)。修改这些标识或扩展审计范围时，应先核对固定 commit 的 SDK 头文件，更新来源证据与明确的遗漏说明，再运行 `python scripts/validate_core_audio_audit.py --fetch-headers`。SDK 头文件保留原始字节用于哈希比对，不应转换换行或编码。

原生函数的 import library / DLL 以对应 Microsoft Learn Requirements 为准。COM 接口方法、应用实现的回调与可导入函数应分别记录；不能从接口所在头文件推断 DLL 导出关系。完整规则见 [Core Audio 标识与依赖审计](docs/110-Core-Audio-Identifiers-and-Dependencies-Audit.md)。
