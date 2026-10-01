# References

## Microsoft

- Core Audio APIs  
  https://learn.microsoft.com/windows/win32/coreaudio/core-audio-apis-in-windows-vista
- Core Audio Interfaces  
  https://learn.microsoft.com/windows/win32/coreaudio/core-audio-interfaces
- MMDevice / IMMDeviceEnumerator  
  https://learn.microsoft.com/windows/win32/api/mmdeviceapi/nn-mmdeviceapi-immdeviceenumerator
- IAudioSessionManager2  
  https://learn.microsoft.com/windows/win32/api/audiopolicy/nn-audiopolicy-iaudiosessionmanager2
- IAudioEndpointVolume  
  https://learn.microsoft.com/windows/win32/api/endpointvolume/nn-endpointvolume-iaudioendpointvolume
- IAudioMeterInformation  
  https://learn.microsoft.com/windows/win32/api/endpointvolume/nn-endpointvolume-iaudiometerinformation
- WASAPI  
  https://learn.microsoft.com/windows/win32/coreaudio/wasapi
- IAudioClient  
  https://learn.microsoft.com/windows/win32/api/audioclient/nn-audioclient-iaudioclient
- Loopback Recording  
  https://learn.microsoft.com/windows/win32/coreaudio/loopback-recording

## Open source references

### SonicRoute

https://github.com/kunkunkunQoQ/SonicRoute

技术实现入口：

https://github.com/kunkunkunQoQ/SonicRoute/wiki

### WinAudioRoute

https://github.com/kunkunkunQoQ/WinAudioRoute

### EarTrumpet

https://github.com/File-New-Project/EarTrumpet

特别关注：

- `IAudioPolicyConfigFactory`
- per-app persisted endpoint
- Windows version specific internal interface implementation

## 引用原则

第三方项目只能证明“有人这样实现 / 这个行为曾经可用”，不能替代 Microsoft 对 public API 的规范。

对 undocumented API，应尽量至少保留：

- 来源链接
- commit / date
- Windows Build
- 实测结果
