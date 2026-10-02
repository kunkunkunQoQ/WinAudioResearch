# DirectMusic Kernel DDI / dmusicks.h

> Status: 🟤 Legacy / historical WDM audio contract

DirectMusic kernel support is an important historical part of the Windows audio driver stack.

It is not the recommended architecture for new Windows 10/11 audio drivers, but it remains relevant for:

- older WDM drivers;
- historical MIDI / synthesizer hardware;
- understanding `dmusprop.h` property sets;
- archived WDK samples;
- PortCls MIDI / DMus architecture;
- compatibility research.

## Header scope

Microsoft's current `dmusicks.h` reference contains:

- `IAllocatorMXF`
- `IMasterClock`
- `IMiniportDMus`
- `IMXF`
- `IPortDMus`
- `IPositionNotify`
- `ISynthSinkDMus`
- `DMUS_KERNEL_EVENT`
- `DMUS_STREAM_TYPE`

Machine-readable tables:

- [`api/dmusicks.csv`](../api/dmusicks.csv)
- [`api/methods-dmusicks.csv`](../api/methods-dmusicks.csv)

## Port / miniport architecture

```text
PortCls
  └─ IPortDMus
       ↕
    IMiniportDMus
       ↓ NewStream
      IMXF
```

`IPortDMus` is implemented by the PortCls DMus port driver.

`IMiniportDMus` is implemented by the vendor miniport.

Together they form a DirectMusic KS filter.

## MXF transport

`IMXF` is the DirectMusic MIDI transport interface.

Important methods:

- `ConnectOutput`
- `DisconnectOutput`
- `PutMessage`
- `SetState`

Messages are packaged as `DMUS_KERNEL_EVENT` structures.

Conceptually:

```text
DMUS_KERNEL_EVENT
       ↓
      IMXF
       ↓
another IMXF / allocator / sink
```

`PutMessage` eventually recycles the event back into the allocator.

## Allocator

The DMus port driver creates one allocator for each stream and exposes:

`IAllocatorMXF`

Additional methods:

- `GetMessage`
- `GetBuffer`
- `GetBufferSize`
- `PutBuffer`

`GetMessage` supplies reusable `DMUS_KERNEL_EVENT` structures.

`GetBuffer` is used when event data is too large to fit in the inline storage of `DMUS_KERNEL_EVENT`.

## Master clock

`IMasterClock::GetTime` returns the system DirectMusic master reference time in 100-ns units.

DirectMusic stream events are timestamped against this clock.

The miniport receives the master clock when a stream is created.

## Kernel software synthesizer path

A DMus stream can expose `ISynthSinkDMus`.

```text
MIDI input
   ↓
IMXF
   ↓
kernel synth
   ↓
ISynthSinkDMus::Render
   ↓
DMus port-driver wave sink
   ↓
PCM wave output
```

`ISynthSinkDMus` also provides:

- reference-time → sample-time conversion;
- sample-time → reference-time conversion;
- master-clock synchronization.

This was designed so synth output could be synchronized with other timed media.

## Windows compatibility note

Microsoft documents DMus as a historical PortCls miniport type.

WaveCyclic, WavePci, Topology, MIDI and DMus existed before WaveRT. WaveRT arrived with Windows Vista.

For Windows Vista and later, Microsoft notes that kernel-mode software synthesizers are not supported as a modern driver direction, although the historical DDI remains documented.

Therefore WinAudioResearch marks the kernel DirectMusic surface as **Legacy**, not Undocumented.

## Official samples

Microsoft's archived audio sample list includes:

- `Dmusuart` — DirectMusic UART driver sample;
- `ddksynth` — DirectMusic software synthesizer sample.

These are now indexed in `api/samples.csv`.

## Relationship to modern Windows MIDI

Do not confuse:

```text
dmusicks.h / DirectMusic kernel DDI
```

with:

```text
Windows MIDI Services / Windows.Devices.Midi2
```

They belong to different Windows audio generations.

The repository preserves both because the goal is full Windows audio coverage, not only current application APIs.

## Primary sources

- DirectMusic DDI Overview
  https://learn.microsoft.com/windows-hardware/drivers/audio/directmusic-ddi-overview
- dmusicks.h
  https://learn.microsoft.com/windows-hardware/drivers/ddi/dmusicks/
- DMus Port Driver
  https://learn.microsoft.com/windows-hardware/drivers/audio/dmus-port-driver
- DMus Miniport Driver
  https://learn.microsoft.com/windows-hardware/drivers/audio/dmus-miniport-driver
- Sample Audio Drivers
  https://learn.microsoft.com/windows-hardware/drivers/audio/sample-audio-drivers
