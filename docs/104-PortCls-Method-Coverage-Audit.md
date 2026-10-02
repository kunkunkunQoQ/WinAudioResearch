# PortCls Method Coverage Audit

> Baseline: **2026-10-02**

This audit tracks method-level coverage after the initial `portcls.h` symbol inventory.

## What is already indexed

The symbol database contains the current PortCls header-level baseline:

- port and miniport interfaces;
- helper objects;
- exported `Pc*` functions;
- property/method/event descriptors;
- resource/power enums.

The method database now expands the most important interface groups.

## Strong method coverage

### Generic base interfaces

- `IPort`
- `IMiniport`

### WaveRT

- `IMiniportWaveRT`
- `IMiniportWaveRTStream`
- `IMiniportWaveRTStreamNotification`
- `IMiniportWaveRTInputStream`
- `IMiniportWaveRTOutputStream`
- `IPortWaveRTStream`
- `IPortClsStreamResourceManager`
- `IPortClsStreamResourceManager2` core additions

### MIDI / Topology

- `IPortMidi`
- `IMiniportMidi`
- `IMiniportTopology` core

### Helper objects

- `IDmaChannel`
- `IRegistryKey`
- `IResourceList`
- `IServiceGroup`
- `IServiceSink`
- `IPortEvents`
- `IPortWMIRegistration`
- `IPortClsVersion`

### Legacy WaveCyclic

- `IPortWaveCyclic`
- `IMiniportWaveCyclic`
- `IMiniportWaveCyclicStream`

### Dynamic topology

- `IUnregisterPhysicalConnection`

## Why legacy interfaces remain

`WaveCyclic` and `WavePci` are not recommended for new Vista+ driver design, but they remain important for:

- historical Windows audio architecture;
- old vendor drivers;
- archived WDK samples;
- DRM and DirectSound compatibility;
- understanding why WaveRT changed the buffering model.

Microsoft explicitly documents that WaveRT first appears with Windows Vista, while WaveCyclic/WavePci existed on Windows XP and later.

## Known gaps after this pass

The database is intentionally not marked fully audited yet.

Remaining high-value method groups:

- `IDmaChannelSlave` full method set;
- `IInterruptSync` full method set;
- `IDrmPort` / `IDrmPort2`;
- `IAdapterPowerManagement2/3`;
- `IAdapterPnpManagement`;
- `IPortClsPnp`;
- `IPortClsRuntimePower`;
- `IPortClsNotifications`;
- `IPortClsEtwHelper`;
- audio-engine node interfaces;
- `IPinCount` / `IPinName`;
- `IUnregisterSubdevice`;
- WavePci complete stream/path methods;
- legacy DRM stream interfaces outside `portcls.h`.

## Next audit rule

For each interface:

1. enumerate every method from Microsoft Learn / current WDK;
2. store minimum supported client only when explicitly verified;
3. classify legacy/current;
4. add IRQL notes where operationally important;
5. add relationship edges to KS property/event sets;
6. add official sample references where a sample demonstrates the contract.

## Official sample mapping

The repository now separately indexes key SysVAD pieces:

- TabletAudioSample;
- EndpointsCommon;
- SwapAPO;
- KeywordDetectorAdapter.

Historical DirectMusic examples are also indexed:

- Dmusuart;
- ddksynth.

## Maturity

PortCls remains **L4 Integrated**.

It should be promoted to **L5 Audited** only after the remaining method groups above have been exhaustively compared against the current official header/reference.

## Primary sources

- portcls.h
  https://learn.microsoft.com/windows-hardware/drivers/ddi/portcls/
- Introduction to Port Class
  https://learn.microsoft.com/windows-hardware/drivers/audio/introduction-to-port-class
- Audio Helper Object Interfaces
  https://learn.microsoft.com/windows-hardware/drivers/audio/audio-helper-object-interfaces
- Sample Audio Drivers
  https://learn.microsoft.com/windows-hardware/drivers/audio/sample-audio-drivers
