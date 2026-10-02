# Core Audio IID / CLSID and Dependency Normalization Audit

> Baseline: **2026-10-02**  
> Scope: the interface/coclass records already indexed in the six Core Audio tables, their acquisition dependencies, audio-state monitor factories and four shared COM support functions.

## Result

This round completes the identifier/dependency target that followed the [SDK header audit](105-Core-Audio-SDK-Header-Coverage-Audit.md).

| Item | Result |
|---|---:|
| Existing IID/CLSID records checked | **63**: 62 interfaces + `MMDeviceEnumerator` |
| Previously blank identifier cells filled | **53** |
| Previously populated identifiers rechecked | **10** |
| Dependency records added | **70** |
| Repository dependency records after integration | **102** |
| Repository total after integration | **2825** |

No new public interface is inferred from a GUID alone. The audit normalizes the existing client-facing inventory and lists additional header declarations as explicit gaps.

## 1. Source snapshot and scope

Identifiers were extracted from Microsoft's `win32metadata` recompiled SDK headers at commit [`5c5efbc01d4c87f6830ec304d42777991d533154`](https://github.com/microsoft/win32metadata/commit/5c5efbc01d4c87f6830ec304d42777991d533154). This is a reproducible source snapshot, not a claim about the newest installed SDK on a contributor's machine.

The [audit manifest](../api/core-audio-audit.json) records each exact header name, SHA-256 digest, expected IID/CLSID and excluded declaration. Header URLs below are pinned to the same commit.

| Database | Pinned header | Identifiers checked |
|---|---|---:|
| [MMDevice](../api/core-mmdevice.csv) | [mmdeviceapi.h](https://github.com/microsoft/win32metadata/blob/5c5efbc01d4c87f6830ec304d42777991d533154/generation/WinSDK/RecompiledIdlHeaders/um/mmdeviceapi.h) | 10 |
| [WASAPI](../api/wasapi.csv) | [Audioclient.h](https://github.com/microsoft/win32metadata/blob/5c5efbc01d4c87f6830ec304d42777991d533154/generation/WinSDK/RecompiledIdlHeaders/um/Audioclient.h) | 16 |
| [Audio Session](../api/audio-session.csv) | [audiopolicy.h](https://github.com/microsoft/win32metadata/blob/5c5efbc01d4c87f6830ec304d42777991d533154/generation/WinSDK/RecompiledIdlHeaders/um/audiopolicy.h) | 8 |
| [EndpointVolume](../api/endpoint-volume.csv) | [endpointvolume.h](https://github.com/microsoft/win32metadata/blob/5c5efbc01d4c87f6830ec304d42777991d533154/generation/WinSDK/RecompiledIdlHeaders/um/endpointvolume.h) | 4 |
| [DeviceTopology](../api/device-topology.csv) | [devicetopology.h](https://github.com/microsoft/win32metadata/blob/5c5efbc01d4c87f6830ec304d42777991d533154/generation/WinSDK/RecompiledIdlHeaders/um/devicetopology.h) | 24 |
| [AudioStateMonitor](../api/audio-state-monitor.csv) | [audiostatemonitorapi.h](https://github.com/microsoft/win32metadata/blob/5c5efbc01d4c87f6830ec304d42777991d533154/generation/WinSDK/RecompiledIdlHeaders/um/audiostatemonitorapi.h) | 1 |

`audiostatemonitorapi.h` uses `DECLARE_INTERFACE_IID_`; the other covered interfaces use `MIDL_INTERFACE`. Coclass UUIDs use `DECLSPEC_UUID`. Checking only `MIDL_INTERFACE` would miss the monitor interface and the enumerator CLSID.

The CSV values use uppercase `8-4-4-4-12` GUID text without braces. This convention is limited to this audited inventory; unrelated property/error tables retain their existing encodings.

## 2. Identity and acquisition

An IID identifies an interface contract. A CLSID identifies a COM class. Their roles differ in activation calls:

```text
MMDeviceEnumerator CLSID
    → CoCreateInstance requests IMMDeviceEnumerator IID
    → enumerator returns IMMDevice
    → IMMDevice.Activate requests an interface IID
    → IAudioClient.GetService requests a service IID
```

Representative checked values:

| Identity | Value |
|---|---|
| `MMDeviceEnumerator` CLSID | `BCDE0395-E52F-467C-8E3D-C4579291692E` |
| `IMMDeviceEnumerator` IID | `A95664D2-9614-4F35-A746-DE8DB63617E6` |
| `IAudioClient` IID | `1CB9AD4C-DBFA-4C32-B178-C2F568A703B2` |
| `IAudioStateMonitor` IID | `63BD8738-E30D-4C77-BF5C-834E87C657E2` |

An IID does not establish that `CoCreateInstance` can create that interface directly. Keep the existing `acquisition` field when selecting `Activate`, `GetService`, `QueryInterface`, a factory or an application-provided callback. Interface availability still depends on the documented Windows version, endpoint and service context.

In MSVC C++, [`__uuidof`](https://learn.microsoft.com/cpp/cpp/uuidof-operator) accesses the SDK type's UUID attribute. This avoids writing a second hand-maintained UUID literal. C or external `IID_*`/`CLSID_*` references still need suitable GUID definitions in the build; this audit does not claim that an import library supplies every GUID symbol.

## 3. Dependency semantics

[dependencies.csv](../api/dependencies.csv) now includes all 63 covered interface/coclass records, all eight monitor factories, the existing asynchronous activation function and four COM support functions. The 70 additions comprise 58 missing interface/coclass entries, eight monitor factories and four COM functions.

For COM interfaces, `header` describes the compile-time ABI. `dll_or_runtime` describes the Windows runtime or an application-provided callback. A blank `library` means this audit asserts no direct interface import library. These methods are invoked through COM interfaces rather than looked up as function exports. Microsoft's [IAudioClient requirements and acquisition documentation](https://learn.microsoft.com/windows/win32/api/audioclient/nn-audioclient-iaudioclient) illustrates this distinction.

The native function dependencies are recorded separately:

| Function | Header | Import library | DLL / runtime evidence |
|---|---|---|---|
| `ActivateAudioInterfaceAsync` | `mmdeviceapi.h` | `Mmdevapi.lib` | `Mmdevapi.dll` |
| Eight `Create*AudioStateMonitor` functions | `audiostatemonitorapi.h` | `windows.media.mediacontrol.lib` | Windows audio-state monitor runtime; no DLL name stated in Learn Requirements |
| `CoInitializeEx`, `CoUninitialize`, `CoCreateInstance`, `CoTaskMemFree` | `combaseapi.h`; include `Objbase.h` | `Ole32.lib` | `Ole32.dll` |

Sources: [asynchronous activation](https://learn.microsoft.com/windows/win32/api/mmdeviceapi/nf-mmdeviceapi-activateaudiointerfaceasync), [render monitor factory](https://learn.microsoft.com/windows/win32/api/audiostatemonitorapi/nf-audiostatemonitorapi-createrenderaudiostatemonitor), [COM initialization](https://learn.microsoft.com/windows/win32/api/combaseapi/nf-combaseapi-coinitializeex), [COM shutdown](https://learn.microsoft.com/windows/win32/api/combaseapi/nf-combaseapi-couninitialize), [class creation](https://learn.microsoft.com/windows/win32/api/combaseapi/nf-combaseapi-cocreateinstance), [task-memory cleanup](https://learn.microsoft.com/windows/win32/api/combaseapi/nf-combaseapi-cotaskmemfree). Each factory row also links to its own Requirements page.

The support functions' historical minimum Windows versions describe those functions, not the minimum Windows version of Core Audio. An application must satisfy both sets of requirements. Memory cleanup follows the individual API's ownership contract; `CoTaskMemFree` is not a substitute for releasing an interface or returning a WASAPI buffer.

## 4. Reproducing the checks

From the repository root, using Python 3.10 or newer:

```bash
python scripts/validate_api_db.py
python scripts/validate_core_audio_audit.py
python -m unittest discover -s tests -v
```

The offline audit rejects missing or changed identifiers, incorrect declaration kinds/headers, missing dependencies, dependency header/version/status mismatches and changed native-function import requirements.

For source verification, download the six pinned headers automatically:

```bash
python scripts/validate_core_audio_audit.py --fetch-headers
```

Alternatively, supply an existing directory containing the exact unmodified source files:

```bash
python scripts/validate_core_audio_audit.py --headers-dir /path/to/sdk-headers
```

Source verification checks both the file digests and parsed declarations. It also requires every UUID declaration in each source header to be covered or explicitly excluded. The GitHub Actions workflow runs database validation, regression tests and this pinned-source comparison on synchronized snapshots and API pull requests.

Lookup examples:

```bash
python scripts/query_api.py --type symbol 1CB9AD4C-DBFA-4C32-B178-C2F568A703B2
python scripts/query_api.py --type dependency IAudioClient
python scripts/query_api.py --type dependency windows.media.mediacontrol.lib
```

## 5. Explicit coverage gaps

The pinned headers contain six further UUID declarations outside this pass:

| Declaration | Remaining work |
|---|---|
| `IMMDeviceActivator` | Activation-provider contract/acquisition review |
| `IAudioAmbisonicsControl` | Adjacent WASAPI control; member and version audit |
| `IKsControl` | Generic KS property/method/event control ABI and acquisition review |
| `IKsJackContainerId` | Jack identity interface; member and version audit |
| `IKsJackDescription3` | Newer jack-description interface; member and version audit |
| `DeviceTopology` coclass | Direct class activation review; endpoint topology acquisition remains `IMMDevice.Activate` |

These are declared gaps, not invented compatibility claims. This round does not audit Spatial Audio, APO, KS or undocumented policy GUIDs, revise every minimum-build field, or provide hardware/runtime evidence. Existing L5 domain labels retain their documented scope; no domain is promoted to L6.

Next priority: PortCls edge-method/IID/version review, followed by ACX header deltas and the remaining generic KS event/category/AVStream contracts. Core Audio follow-up work includes the six declarations above and reproducible callback/apartment/lifetime evidence.
