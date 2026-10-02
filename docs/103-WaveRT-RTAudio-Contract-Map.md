# WaveRT / KSPROPSETID_RTAudio Contract Map

> Status: 🟢 Public WDK

WaveRT has two closely related public surfaces:

1. PortCls miniport interfaces in `portcls.h`;
2. Kernel Streaming WaveRT properties and structures in `ksmedia.h`.

Understanding only one side leaves the model incomplete.

## Main relationship

```text
user-mode Audio Engine
        ↓ KS property request
KSPROPSETID_RTAudio
        ↓
WaveRT PortCls port driver
        ↓
IMiniportWaveRT / IMiniportWaveRTStream
        ↓
hardware DMA engine
```

## Buffer allocation

Property side:

- `KSPROPERTY_RTAUDIO_BUFFER`
- `KSPROPERTY_RTAUDIO_BUFFER_WITH_NOTIFICATION`

Supporting structures:

- `KSRTAUDIO_BUFFER_PROPERTY`
- `KSRTAUDIO_BUFFER`
- `KSRTAUDIO_BUFFER_PROPERTY_WITH_NOTIFICATION`

Miniport side:

- `IMiniportWaveRTStream::AllocateAudioBuffer`
- `IMiniportWaveRTStreamNotification::AllocateBufferWithNotification`

Port-side memory services:

- `IPortWaveRTStream::AllocatePagesForMdl`
- `AllocateContiguousPagesForMdl`
- `MapAllocatedPages`
- `UnmapAllocatedPages`
- physical-page helpers

## Position and clock

Properties:

- `KSPROPERTY_RTAUDIO_POSITIONREGISTER`
- `KSPROPERTY_RTAUDIO_CLOCKREGISTER`

Structures:

- `KSRTAUDIO_HWREGISTER_PROPERTY`
- `KSRTAUDIO_HWREGISTER`

Miniport methods:

- `GetPositionRegister`
- `GetClockRegister`

WaveRT can expose a hardware register directly to the audio client through a mapped virtual address.

This lets the client monitor stream position with lower overhead than repeatedly calling into the driver.

## Hardware latency

```text
KSPROPERTY_RTAUDIO_HWLATENCY
        ↓
KSRTAUDIO_HWLATENCY
        ↓
FifoSize
ChipsetDelay
CodecDelay
```

Miniport implementation:

`IMiniportWaveRTStream::GetHWLatency`

## Notification streaming

Request structure:

`KSRTAUDIO_NOTIFICATION_EVENT_PROPERTY`

Property flow:

```text
KSPROPERTY_RTAUDIO_BUFFER_WITH_NOTIFICATION
       ↓
REGISTER_NOTIFICATION_EVENT
       ↓
DMA progress
       ↓
kernel event
       ↓
audio engine thread wakes
```

Miniport interface:

`IMiniportWaveRTStreamNotification`

with:

- `RegisterNotificationEvent`
- `UnregisterNotificationEvent`

## Packet-based WaveRT

Windows 10 introduced packet-oriented methods and property contracts.

Capture:

```text
KSPROPERTY_RTAUDIO_GETREADPACKET
      ↔
KSRTAUDIO_GETREADPACKET_INFO
      ↔
IMiniportWaveRTInputStream::GetReadPacket
```

Render:

```text
KSPROPERTY_RTAUDIO_SETWRITEPACKET
      ↔
KSRTAUDIO_SETWRITEPACKET_INFO
      ↔
IMiniportWaveRTOutputStream::SetWritePacket
```

Packet synchronization also uses:

- `KSPROPERTY_RTAUDIO_PACKETCOUNT`
- `KSPROPERTY_RTAUDIO_PRESENTATION_POSITION`
- `KSPROPERTY_RTAUDIO_PACKETVREGISTER`

## 32-bit compatibility structures

`ksmedia.h` still exposes 32-bit compatibility layouts:

- `KSRTAUDIO_BUFFER32`
- `KSRTAUDIO_BUFFER_PROPERTY32`
- `KSRTAUDIO_BUFFER_PROPERTY_WITH_NOTIFICATION32`
- `KSRTAUDIO_HWREGISTER32`
- `KSRTAUDIO_HWREGISTER_PROPERTY32`
- `KSRTAUDIO_NOTIFICATION_EVENT_PROPERTY32`

These are useful when understanding IOCTL/property ABI layouts across 32/64-bit clients.

## Why this mapping matters

A driver-facing API database should not list:

`IMiniportWaveRTStream::GetHWLatency`

and:

`KSPROPERTY_RTAUDIO_HWLATENCY`

as unrelated items.

They are two views of the same contract path.

WinAudioResearch records those links in `api/relationships.csv`.

## Structured files

- [`api/wavert.csv`](../api/wavert.csv)
- [`api/methods-wavert.csv`](../api/methods-wavert.csv)
- [`api/ks-audio.csv`](../api/ks-audio.csv)
- [`api/relationships.csv`](../api/relationships.csv)

## Primary sources

- Understanding the WaveRT Port Driver
  https://learn.microsoft.com/windows-hardware/drivers/audio/understanding-the-wavert-port-driver
- KSPROPSETID_RTAudio
  https://learn.microsoft.com/windows-hardware/drivers/audio/kspropsetid-rtaudio
- ksmedia.h
  https://learn.microsoft.com/windows-hardware/drivers/ddi/ksmedia/
- portcls.h
  https://learn.microsoft.com/windows-hardware/drivers/ddi/portcls/
