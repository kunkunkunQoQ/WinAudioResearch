# PortCls Reference and Coverage

> Baseline: **2026-10-02**  
> Status: 🟢 Public WDK / 🟤 Legacy for superseded models

PortCls is the system-supplied audio port-class framework implemented by **Portcls.sys**.

Microsoft describes the architecture as a **port + miniport** model:

```text
Vendor adapter driver
   ├─ MiniportWaveRT
   ├─ MiniportTopology
   └─ MiniportMidi / DMus
          │
          ▼
PortCls system port drivers
   ├─ IPortWaveRT
   ├─ IPortTopology
   └─ IPortMidi / IPortDMus
          │
          ▼
Kernel Streaming filters
```

The system port driver handles much of the generic KS/filter work; the vendor miniport supplies hardware-specific behavior.

Microsoft explicitly documents this split and notes that a bound port/miniport pair forms a KS filter.

## Structured database

- [PortCls symbols](../api/portcls.csv)
- [PortCls methods/helpers](../api/methods-portcls.csv)
- [WaveRT symbols](../api/wavert.csv)
- [WaveRT methods](../api/methods-wavert.csv)
- [Relationships](../api/relationships.csv)
- [Dependencies](../api/dependencies.csv)

Current PortCls baseline:

- **112** symbol/type/function records
- **194** helper/interface method records

This is a **header-index baseline**, not yet a claim that every method of every legacy interface is exhaustively indexed.

## 1. Generic Port / Miniport model

All PortCls port drivers expose the base:

```text
IPort
```

Important base methods:

- `IPort::Init`
- `IPort::GetDeviceProperty`
- `IPort::NewRegistryKey`

Port objects are created by:

```text
PcNewPort
```

The corresponding generic miniport base is:

```text
IMiniport
```

with:

- `GetDescription`
- `DataRangeIntersection`

The filter description returned by a miniport uses PortCls descriptors such as:

- `PCFILTER_DESCRIPTOR`
- `PCPIN_DESCRIPTOR`
- `PCNODE_DESCRIPTOR`
- `PCAUTOMATION_TABLE`

These structures bridge PortCls miniports to the KS filter / pin / node / property model.

## 2. Major port / miniport pairs

### WaveRT

```text
IPortWaveRT
      ↕
IMiniportWaveRT
      ↓
IMiniportWaveRTStream
```

WaveRT is the modern PortCls streaming model used since Windows Vista.

### Topology

```text
IPortTopology
      ↕
IMiniportTopology
```

This pair exposes the hardware mixing / connector / node topology as a KS topology filter.

### MIDI

```text
IPortMidi
      ↕
IMiniportMidi
      ↓
IMiniportMidiStream
```

### Historical wave models

The WDK still documents:

- `IPortWaveCyclic` / `IMiniportWaveCyclic`
- `IPortWavePci` / `IMiniportWavePci`

These are retained in the database as **Legacy** because they matter for historical compatibility and older driver code.

## 3. Adapter initialization

Important PortCls helpers include:

```text
PcInitializeAdapterDriver
PcAddAdapterDevice
PcNewPort
PcRegisterSubdevice
PcRegisterPhysicalConnection
```

Typical conceptual path:

```text
DriverEntry
  ↓
PcInitializeAdapterDriver
  ↓
AddDevice
  ↓
create port + miniport
  ↓
IPort::Init
  ↓
PcRegisterSubdevice
  ↓
KS filter becomes visible
```

Physical connections between wave/topology filters are registered separately so Windows can reconstruct hardware signal paths.

## 4. Property / Method / Event descriptors

PortCls translates miniport automation into KS behavior using:

- `PCPROPERTY_ITEM`
- `PCPROPERTY_REQUEST`
- `PCMETHOD_ITEM`
- `PCMETHOD_REQUEST`
- `PCEVENT_ITEM`
- `PCEVENT_REQUEST`
- `PCPFNEVENT_HANDLER`

For property requests, `PCPROPERTY_REQUEST` carries major/minor target object references so the handler can distinguish filter, pin and node targets.

This layer explains how a C++ PortCls miniport ultimately exposes KS property sets such as:

```text
KSPROPSETID_Audio
KSPROPSETID_Jack
KSPROPSETID_AudioEngine
KSPROPSETID_RTAudio
```

## 5. Hardware events

Miniports use:

```text
IPortEvents
```

to register and generate hardware-originated event notifications.

Common example:

```text
hardware volume/mute change
       ↓
IPortEvents
       ↓
KSEVENTSETID_AudioControlChange
       ↓
Windows / WDMAud client notification
```

## 6. Power / PnP

PortCls contains several generations of adapter power/PnP interfaces:

- `IAdapterPowerManagement`
- `IAdapterPowerManagement2`
- `IAdapterPowerManagement3`
- `IPortClsPower`
- `IPortClsRuntimePower`
- `IAdapterPnpManagement`
- `IPortClsPnp`
- `IMiniportPnpNotify`
- `IPowerNotify`

Related helper functions include registration/unregistration and explicit power-state requests.

This area should remain a separate audit target because methods and Windows-version requirements differ significantly across generations.

## 7. Resources / DMA / interrupts

PortCls also supplies infrastructure abstractions:

- `IResourceList`
- `IDmaChannel`
- `IDmaChannelSlave`
- `IInterruptSync`
- `IServiceGroup`
- `IServiceSink`

plus helpers such as:

- `PcNewResourceList`
- `PcNewInterruptSync`
- `PcNewServiceGroup`

These are important when reading older SysVAD/WDK samples even if a modern WaveRT implementation does not use every legacy abstraction.

## 8. Registry / dynamic subdevices

PortCls exposes:

- `IRegistryKey`
- `PcNewRegistryKey`
- `IUnregisterSubdevice`
- `IUnregisterPhysicalConnection`

These interfaces explain several patterns in dynamic audio-subdevice drivers and older WDM sample code.

## 9. ETW / diagnostics helpers

The public header includes:

- `IPortClsEtwHelper`
- `IPortWMIRegistration`

Windows 7+ `IPortWMIRegistration` coordinates miniport ETW/WMI registration with PortCls.

This will later connect into the repository-wide ETW / diagnostics catalog.

## 10. Stream-resource management

Windows 10 adds stream-resource tracking APIs:

- `IPortClsStreamResourceManager`
- `IPortClsStreamResourceManager2`
- `PCSTREAMRESOURCE_DESCRIPTOR`
- `PcAddStreamResource`
- `PcRemoveStreamResource`

These let a WaveRT driver register resources such as streaming interrupts or driver-owned realtime threads with PortCls.

## 11. WaveRT integration

WaveRT relies on both miniport and port-stream interfaces.

The miniport stream implements buffer/state/timing operations:

```text
IMiniportWaveRTStream
  ├─ AllocateAudioBuffer
  ├─ GetPosition
  ├─ GetClockRegister
  ├─ GetPositionRegister
  ├─ GetHWLatency
  ├─ SetFormat
  └─ SetState
```

The port provides memory helpers:

```text
IPortWaveRTStream
  ├─ AllocatePagesForMdl
  ├─ AllocateContiguousPagesForMdl
  ├─ MapAllocatedPages
  ├─ UnmapAllocatedPages
  └─ physical-page helpers
```

Optional DMA notification support is supplied by:

```text
IMiniportWaveRTStreamNotification
```

Modern packet-oriented interfaces include:

- `IMiniportWaveRTInputStream`
- `IMiniportWaveRTOutputStream`

Microsoft documents WaveRT as giving the audio engine direct access to the cyclic buffer, reducing repeated mapping/copy work compared with older port models.

## 12. Current coverage status

### Header-level

The repository now has a machine-readable entry for every interface/function/descriptor/enum exposed by the current Microsoft `portcls.h` reference index used for this baseline.

### Method-level

Method coverage is currently **core-focused**.

Strong areas:

- base `IPort` / `IMiniport`
- WaveRT
- MIDI
- Topology
- power
- event notifications
- WMI registration
- resource list
- exported `Pc*` helper functions

Still requiring per-interface method audit:

- DMA interfaces
- registry interface
- runtime power
- PnP-management generations
- notifications/audio-module helpers
- audio-engine node interfaces
- unregister helpers
- legacy WaveCyclic / WavePci stream details

Therefore PortCls is currently **L4 Integrated**, not yet L5 Audited.

## 13. Next PortCls audit

Next pass:

1. enumerate every `portcls.h` interface method;
2. audit minimum supported client where Microsoft documents it;
3. add IID/GUID values where useful;
4. classify Legacy vs current contracts;
5. connect PortCls APIs to KS property/event contracts;
6. connect PortCls APIs to SysVAD / official samples;
7. audit `dmusicks.h` DirectMusic port/miniport interfaces separately.

## Primary sources

- PortCls introduction  
  https://learn.microsoft.com/windows-hardware/drivers/audio/introduction-to-port-class
- portcls.h reference  
  https://learn.microsoft.com/windows-hardware/drivers/ddi/portcls/
- WaveRT port driver  
  https://learn.microsoft.com/windows-hardware/drivers/audio/understanding-the-wavert-port-driver
- WaveRT miniport driver  
  https://learn.microsoft.com/windows-hardware/drivers/audio/wavert-miniport-driver

## Related focused audits

- [PortCls Method Coverage Audit](104-PortCls-Method-Coverage-Audit.md)
- [WaveRT / RTAudio Contract Map](103-WaveRT-RTAudio-Contract-Map.md)
- [DirectMusic Kernel DDI](102-DirectMusic-Kernel-DDI.md)

The broad PortCls surface now has strong method coverage across DMA, registry, service groups, WaveCyclic/WavePci, power/PnP, audio-engine/offload, notifications, ETW, DRM and dynamic subdevice helpers. A small edge audit remains before L5.
