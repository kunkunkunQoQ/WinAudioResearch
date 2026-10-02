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

The method database now contains **194 PortCls helper/interface method records** and covers the major current and historical groups.

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

The broad high-value groups above have now been filled, including:

- DMA + subordinate DMA;
- interrupt synchronization;
- DRM port interfaces;
- power generations 1–3 and runtime power;
- PnP rebalance interfaces;
- audio-module notifications;
- PortCls ETW helper;
- hardware audio-engine and stream audio-engine methods;
- signal-processing modes;
- dynamic pin names/counts;
- WaveCyclic and WavePci paths;
- dynamic subdevice/physical-connection removal.

The database is still intentionally kept at **L4** rather than L5 because the final audit must verify:

- `IMiniportStreamAudioEngineNode2` and any newer additions;
- a few obscure helper interfaces/macros such as legacy prefetch controls;
- exact IID/GUID fields where useful;
- per-method minimum Windows client and IRQL where Microsoft documents them;
- cross-check against the current installed WDK, not Learn pages alone;
- methods inherited from base interfaces are not double-counted as missing.

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

It should be promoted to **L5 Audited** only after the remaining edge items are compared against the current WDK header and IID/version metadata is normalized.

## Primary sources

- portcls.h
  https://learn.microsoft.com/windows-hardware/drivers/ddi/portcls/
- Introduction to Port Class
  https://learn.microsoft.com/windows-hardware/drivers/audio/introduction-to-port-class
- Audio Helper Object Interfaces
  https://learn.microsoft.com/windows-hardware/drivers/audio/audio-helper-object-interfaces
- Sample Audio Drivers
  https://learn.microsoft.com/windows-hardware/drivers/audio/sample-audio-drivers
