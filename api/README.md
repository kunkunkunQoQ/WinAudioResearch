# WinAudioResearch API Database

这个目录是 WinAudioResearch 的**机器可读 API 数据库**。

它和 `docs/` 的关系：

```text
docs/
  → 解释原理、调用链、坑、版本差异、实战经验

api/
  → 快速检索 symbol / header / version / IID / status / official docs
```

## Database status

Last verified baseline:

```text
2026-10-02
```

Current catalog: **1694 structured records** — 835 symbol/type/property/error records, 525 method records, 130 WinRT/MIDI members, 20 capability records, 20 dependencies, 14 official samples and 150 API relationships.

来源优先级：

1. Windows SDK / WDK public headers
2. Microsoft Learn
3. Microsoft official samples
4. SonicRoute / mature OSS implementation
5. Community / reverse engineering

## Stability

| value | meaning |
|---|---|
| Public | Microsoft documented public API / type |
| Public-WDK | public WDK / driver-facing contract |
| Public-WinRT | public Windows Runtime API |
| Legacy | documented but legacy / superseded |
| Undocumented | internal / unsupported implementation detail |
| Observed | behavior verified in real systems but not a public compatibility contract |
| Experimental | still under validation |

## Common columns

CSV tables use a common core schema:

| column | meaning |
|---|---|
| symbol | API/interface/type/function name |
| kind | interface / function / enum / struct / class / constant |
| family | MMDevice / WASAPI / Session / Spatial / etc |
| header_or_namespace | SDK header or WinRT namespace |
| status | stability classification |
| min_client | minimum Windows client when verified |
| iid_or_guid | IID / CLSID / GUID when useful and verified |
| acquisition | how an app normally obtains/creates the object |
| purpose | short description |
| docs_url | primary Microsoft documentation |
| verified | last repository verification date |
| notes | important caveats |

Blank field means:

> not yet verified / not applicable

not:

> does not exist.

## Files

### Symbol / type databases

- [core-mmdevice.csv](core-mmdevice.csv)
- [wasapi.csv](wasapi.csv)
- [audio-session.csv](audio-session.csv)
- [endpoint-volume.csv](endpoint-volume.csv)
- [device-topology.csv](device-topology.csv)
- [spatial-audio.csv](spatial-audio.csv)
- [winrt-audio.csv](winrt-audio.csv)
- [media-foundation.csv](media-foundation.csv)
- [xaudio2.csv](xaudio2.csv)
- [midi.csv](midi.csv)
- [apo.csv](apo.csv)
- [wavert.csv](wavert.csv)
- [acx.csv](acx.csv)
- [ks-audio.csv](ks-audio.csv)
- [driver-platform.csv](driver-platform.csv)
- [audio-formats.csv](audio-formats.csv)
- [audio-properties.csv](audio-properties.csv)
- [hresults.csv](hresults.csv)
- [undocumented.csv](undocumented.csv)

### Method databases

- [methods-mmdevice.csv](methods-mmdevice.csv)
- [methods-wasapi.csv](methods-wasapi.csv)
- [methods-session.csv](methods-session.csv)
- [methods-endpointvolume.csv](methods-endpointvolume.csv)
- [methods-devicetopology.csv](methods-devicetopology.csv)
- [methods-spatial.csv](methods-spatial.csv)
- [methods-media-foundation.csv](methods-media-foundation.csv)
- [methods-xaudio2.csv](methods-xaudio2.csv)
- [methods-acx.csv](methods-acx.csv)
- [methods-apo.csv](methods-apo.csv)
- [methods-wavert.csv](methods-wavert.csv)

### Members / capabilities / dependencies / samples

- [members-winrt-audio.csv](members-winrt-audio.csv)
- [members-midi.csv](members-midi.csv)
- [windows-capabilities.csv](windows-capabilities.csv)
- [dependencies.csv](dependencies.csv)
- [samples.csv](samples.csv)

### Relationship graph

- [relationships.csv](relationships.csv) — Activate / GetService / QueryInterface / callback / create / contains edges

### Database metadata

- [catalog.json](catalog.json) — table inventory + record counts
- [schema.json](schema.json) — common symbol-record schema
- [COVERAGE.md](COVERAGE.md) — current coverage and next targets

### Tooling

From repository root:

```bash
python scripts/query_api.py IAudioClient
python scripts/query_api.py --status Undocumented
python scripts/query_api.py --family WASAPI
python scripts/query_api.py --type member AudioGraph
python scripts/query_api.py --type relationship IAudioClient

python scripts/query_relations.py IMMDevice --depth 2
python scripts/query_relations.py IAudioClient --direction both --depth 2
python scripts/query_relations.py IMMDevice --depth 3 --dot > graph.dot

python scripts/validate_api_db.py
```

The GitHub Actions workflow `.github/workflows/validate-api-db.yml` automatically validates database changes.

## Query examples

### Find everything introduced after Windows 10

Filter:

```text
min_client
```

for:

- Windows 10
- Build 20348
- Build 22000
- Build 22621
- later

### Find every undocumented API

Use:

```text
api/undocumented.csv
```

and cross-check:

```text
undocumented/
findings/
```

### Find the correct header

Search:

```text
header_or_namespace
```

Examples:

```text
mmdeviceapi.h
audioclient.h
audiopolicy.h
endpointvolume.h
devicetopology.h
spatialaudioclient.h
```

## Contribution rule

A database row should not be changed from:

```text
Undocumented → Public
```

unless a stable Microsoft public contract / SDK entry exists.

For version-sensitive rows, prefer an explicit build number over vague text such as:

```text
new Windows 11
```
