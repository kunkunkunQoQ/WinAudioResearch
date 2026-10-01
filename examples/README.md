# Examples

这个目录未来只放 **最小复现**，不做第二套 WinAudioRoute。

示例原则：

- 一篇文章对应一个可以单独运行的小实验；
- 尽量不依赖第三方音频库；
- 打印 HRESULT / Windows Build；
- 不隐藏 COM 调用链；
- 不默认修改系统状态。

计划：

```text
examples/
  DeviceEnumeration/
  DefaultEndpointRead/
  SessionEnumeration/
  SessionVolume/
  EndpointVolume/
  SessionMeter/
  EndpointNotification/
  WasapiLoopback/
  UndocumentedPerAppRoute/
```

对 undocumented 实验：

- 默认只读；
- 写操作必须显式参数；
- 输出风险提示；
- 打印 IID / Build / HRESULT；
- 不把成功结果描述成官方支持。

未来每个实验建议输出：

```text
Windows Build:
Architecture:
Interface:
Endpoint:
Operation:
HRESULT:
Result:
```
