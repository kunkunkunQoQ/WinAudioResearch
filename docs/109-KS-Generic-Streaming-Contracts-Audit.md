# KS Generic Streaming Contracts Audit

> Baseline: **2026-10-02**  
> Scope: generic `ks.h` contracts used by Windows audio filters and pins outside the audio-specific `ksmedia.h` property-set checklist.

## Result

This stage turns the conceptual KS core documented in `docs/100` into a machine-readable database.

| Area | Structured coverage |
|---|---:|
| KS Core symbols / types / properties | **114** |
| KS methods | **4** |
| New relationship edges | **87** |
| Repository total after integration | **2756** |

New tables:

- `api/ks-core.csv`
- `api/methods-ks.csv`

## 1. Why this layer matters

Audio-specific property sets are only one part of Kernel Streaming. A real audio pin also depends on generic KS contracts for capability discovery, creation, runtime state, buffer framing, streaming I/O and time.

```text
KS filter
  ↓ KSPROPSETID_Pin
pin factory capability
  ↓ KSPIN_CONNECT
pin instance
  ↓ KSPROPSETID_Connection
format / state / allocator framing
  ↓
KSSTREAM_HEADER + StreamIo
  ↓
MediaSeeking / Clock / StreamAllocator
```

## 2. Pin factory coverage

`KSPROPSETID_Pin` is now represented with all 17 current enum members from the SDK header including instance counts, data flow, data ranges, interfaces, mediums, communication, physical connection, category/name and the newer format-proposal/mode-format members.

Supporting types now include `KSP_PIN`, `KSE_PIN`, `KSPIN_CINSTANCES`, `KSPIN_DATAFLOW`, `KSDATAFORMAT`, `KSDATARANGE`, `KSATTRIBUTE`, `KSPIN_COMMUNICATION`, `KSPIN_CONNECT` and `KSPIN_PHYSICALCONNECTION`.

## 3. Standard interface and connection runtime

The database now records `KSINTERFACESETID_Standard` and its Streaming, Looped Streaming and Control identifiers. `KSPROPSETID_Connection` adds all eight runtime members:

- state
- priority
- active data format
- allocator framing
- proposed format
- acquire ordering
- extended allocator framing
- scheduled start

This closes the gap between pin-factory capability discovery and a created streaming pin.

## 4. MediaSeeking

`KSPROPSETID_MediaSeeking` contributes ten properties covering capabilities, supported formats, selected time format, current/stop positions, duration, available range, preroll and time-format conversion.

The time-format GUID set is also indexed: NONE, FRAME, BYTE, SAMPLE, FIELD and MEDIA_TIME.

## 5. Clock

`KSPROPSETID_Clock` now maps logical/physical time, correlated time, resolution, state and the kernel function table. `KSEVENTSETID_Clock` adds interval and position marks.

Supporting types include `KSCLOCK_CREATE`, `KSCORRELATED_TIME`, `KSRESOLUTION` and `KSCLOCK_FUNCTIONTABLE`.

## 6. Allocator model

The allocator path is represented at both connection and allocator-object layers:

```text
KSPROPERTY_CONNECTION_ALLOCATORFRAMING(_EX)
        ↓
KSALLOCATOR_FRAMING / KSALLOCATOR_FRAMING_EX
        ↓
KSMETHODSETID_StreamAllocator
KSPROPSETID_StreamAllocator
KSEVENTSETID_StreamAllocator
```

Extended framing support includes `KS_FRAMING_RANGE`, `KS_FRAMING_RANGE_WEIGHTED`, `KS_COMPRESSION`, `KS_FRAMING_ITEM` and the standard system/user/kernel memory-type GUIDs.

## 7. Stream I/O and headers

`KSMETHODSETID_StreamIo` contributes READ and WRITE method records. The generic streaming payload is now represented by `KSSTREAM_HEADER` and its embedded `KSTIME` presentation timestamp/rate structure.

## 8. Relationship graph

The 87 new edges deliberately connect sets to members and members to their payload types. Important examples:

- Pin DATARANGES → `KSDATARANGE`
- Pin DATAINTERSECTION / PROPOSEDATAFORMAT → `KSDATAFORMAT`
- Connection ALLOCATORFRAMING → `KSALLOCATOR_FRAMING`
- Connection ALLOCATORFRAMING_EX → `KSALLOCATOR_FRAMING_EX`
- MediaSeeking POSITIONS → `KSPROPERTY_POSITIONS`
- Clock CORRELATEDTIME → `KSCORRELATED_TIME`
- StreamAllocator STATUS → `KSSTREAMALLOCATOR_STATUS`
- `KSSTREAM_HEADER` → `KSTIME`

## 9. Coverage boundary

This is a strong integrated generic streaming baseline but not a claim that all of `ks.h` is exhausted. Remaining KS work includes broader generic event/category coverage, AVStream automation/callback structures, less-audio-relevant transport/property families and per-version evidence.

That is why the domain remains **L4+ integrated** rather than being promoted prematurely to L5.

## Primary source

- Microsoft SDK/WDK recompiled `ks.h` — https://github.com/microsoft/win32metadata/blob/main/generation/WinSDK/RecompiledIdlHeaders/shared/ks.h
- KS Core Foundation overview — `docs/100-KS-Core-Foundation.md`
- KS Audio property-set audit — `docs/98-KS-Audio-Property-Set-Coverage.md`
