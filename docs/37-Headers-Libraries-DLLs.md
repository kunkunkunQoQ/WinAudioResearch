# Windows Audio Header / Library / DLL 对照表

> 这页用于写 P/Invoke、C++ linking、COM interop 时快速查找组件归属。

---

## 1. MMDevice

### Header

```text
mmdeviceapi.h
```

典型：

- IMMDevice
- IMMDeviceCollection
- IMMDeviceEnumerator
- IMMNotificationClient
- ActivateAudioInterfaceAsync

相关 library / DLL：

```text
Mmdevapi.lib
Mmdevapi.dll
```

---

## 2. WASAPI

### Headers

```text
audioclient.h
audiopolicy.h
audiosessiontypes.h
```

典型：

- IAudioClient
- IAudioClient2
- IAudioClient3
- IAudioRenderClient
- IAudioCaptureClient
- IAudioClock
- ISimpleAudioVolume
- IAudioSessionManager2
- IAudioSessionControl2

---

## 3. EndpointVolume

### Header

```text
endpointvolume.h
```

典型：

- IAudioEndpointVolume
- IAudioEndpointVolumeCallback
- IAudioMeterInformation

---

## 4. DeviceTopology

### Header

```text
devicetopology.h
```

典型：

- IDeviceTopology
- IConnector
- IPart
- IPartsList
- control interfaces

---

## 5. Property System

### Headers

```text
propsys.h
propkey.h
functiondiscoverykeys_devpkey.h
```

相关：

- IPropertyStore
- PROPERTYKEY
- PROPVARIANT
- PKEY_Device_FriendlyName

清理：

```text
PropVariantClear
```

来自：

```text
ole32.dll
```

---

## 6. WinRT / HSTRING

SonicRoute internal AudioPolicyConfig 使用：

```text
combase.dll
```

函数：

- RoGetActivationFactory
- WindowsCreateString
- WindowsDeleteString
- WindowsGetStringRawBuffer

注意：

> 这里列出的是 WinRT 基础 ABI，不代表 internal AudioPolicyConfig 本身是公开 API。

---

## 7. Spatial Audio

### Header

```text
spatialaudioclient.h
```

典型：

- ISpatialAudioClient
- ISpatialAudioObject
- ISpatialAudioObjectRenderStream

---

## 8. Audio Client Activation Params

### Header

```text
audioclientactivationparams.h
```

典型：

- AUDIOCLIENT_ACTIVATION_PARAMS
- AUDIOCLIENT_PROCESS_LOOPBACK_PARAMS
- AUDIOCLIENT_ACTIVATION_TYPE
- PROCESS_LOOPBACK_MODE

---

## 9. Wave / Audio Formats

### Headers

```text
mmeapi.h
mmreg.h
ksmedia.h
```

典型：

- WAVEFORMATEX
- WAVEFORMATEXTENSIBLE
- speaker channel masks

---

## 10. XAudio2

### Headers

```text
xaudio2.h
x3daudio.h
xapo.h
xapobase.h
xapofx.h
xaudio2fx.h
hrtfapoapi.h
```

---

## 11. Media Foundation

常见 headers：

```text
mfapi.h
mfidl.h
mfreadwrite.h
mferror.h
```

常见 libraries：

```text
mfplat.lib
mf.lib
mfreadwrite.lib
mfuuid.lib
```

具体接口仍应查对应 Microsoft Learn Requirements 表。

---

## 12. Driver / KS / APO

常见：

```text
ks.h
ksmedia.h
portcls.h
audioenginebaseapo.h
```

ACX：

- acxcircuit.h
- acxdevice.h
- acxdriver.h
- acxelements.h
- acxpin.h
- acxstreams.h
- ...

---

## 13. 不要只靠 DLL 名判断 API 稳定性

例如：

```text
combase.dll
```

里可以承载公开 WinRT ABI，也可以被用来激活内部 class。

所以：

> “函数存在于 Windows 系统 DLL” != “这是公开稳定 API”。

判断公开性应看：

- Microsoft Learn
- Windows SDK / WDK public header
- documented contract
