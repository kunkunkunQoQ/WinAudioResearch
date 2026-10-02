# Windows Audio Master Coverage Plan

> Goal: build WinAudioResearch into a **large, source-traceable Windows audio knowledge base** covering application APIs, system policy, media frameworks, drivers, transports, formats, diagnostics, compatibility, legacy APIs and undocumented behavior.

Baseline: **2026-10-02**

## 1. Repository mission

WinAudioResearch is not intended to be one more API wrapper.

The target is a research repository where a Windows audio developer can answer all of these questions from one place:

- Which API or DDI should I use?
- Which header / DLL / package provides it?
- Which Windows versions support it?
- What object or service creates it?
- What other interfaces / property sets / drivers does it depend on?
- What is public, legacy, observed or undocumented?
- What does the data path look like from app to hardware?
- Which official sample demonstrates it?
- Which HRESULTs / events / callbacks matter?
- What changes across Windows releases?
- What is the historical predecessor of a modern API?
- How do USB / Bluetooth / HDMI / onboard codecs map into the Windows stack?
- How can I diagnose glitches, latency, endpoint creation and driver failures?

The repository therefore treats **documentation, structured metadata, relationships and verification evidence** as equally important.

---

## 2. Coverage model

Every major domain should eventually have the following artifacts.

| Artifact | Purpose |
|---|---|
| Concept document | architecture, concepts, usage boundaries |
| Symbol database | interfaces, classes, structs, enums, GUIDs, property keys |
| Method/member database | methods, callbacks, DDIs, events |
| Relationship graph | activation, containment, mapping and dependency paths |
| Version matrix | minimum Windows / build / deprecation / replacement |
| Dependency table | header, library, DLL, runtime, package |
| Error catalog | HRESULT / NTSTATUS / driver-specific failure modes |
| Samples index | Microsoft samples and high-quality open-source implementations |
| Diagnostics | ETW providers, tools, commands, logs and test workflow |
| Compatibility evidence | real devices, Windows builds, x64 / ARM64 |
| Source provenance | official / open-source / observed / reverse-engineered |

A domain is not “complete” merely because its main interface names exist in a CSV.

---

## 3. Maturity levels

Use a stricter maturity scale for large-repository planning.

### L0 — Not indexed

No dedicated coverage.

### L1 — Concept mapped

There is a long-form overview and source list.

### L2 — Symbol indexed

Major interfaces/types/keys/GUIDs are machine-readable.

### L3 — Member indexed

Methods, callbacks, events or properties are represented.

### L4 — Integrated

Relationships, dependencies, versions, errors and samples are connected.

### L5 — Audited

Compared against current official headers/reference pages and known omissions are explicitly listed.

### L6 — Verified

Important behavior is backed by reproducible experiments or real-device/build evidence.

A large knowledge base should prefer an honest **L3 with explicit gaps** over a false “100%”.

---

## 4. Master domain map

### A. Application-facing Windows Audio APIs

Target coverage:

1. MMDevice / endpoint enumeration
2. WASAPI / IAudioClient generations
3. Audio Sessions / ducking / grouping / persistence
4. EndpointVolume
5. DeviceTopology
6. Audio state monitoring
7. Process loopback
8. IAudioEffectsManager and modern effects APIs
9. Spatial Audio / Windows Sonic
10. Windows.Devices.Enumeration
11. AudioGraph / Windows.Media.Audio
12. MediaCapture / capture devices
13. MediaPlayer / app-selected audio device

Primary structured tables already exist for most of this layer.

Microsoft describes the classic Core Audio set as MMDevice, WASAPI, DeviceTopology and EndpointVolume; modern Windows also exposes higher-level WinRT/media APIs.

### B. Media, game and content frameworks

Target coverage:

- Media Foundation
- Source Reader / Sink Writer
- Media Session / SAR
- Media Foundation Transforms
- built-in audio codecs
- XAudio2
- XAPO
- Windows MIDI Services / MIDI 2.0
- WinMM MIDI
- waveOut / waveIn
- DirectSound
- DirectMusic
- DirectShow audio context
- ACM / DMO

Historical APIs remain important for compatibility and understanding old software.

### C. Audio policy, identity and endpoint construction

Target coverage:

- AudioEndpointBuilder
- endpoint IDs / container IDs / stable IDs
- endpoint property stores
- DeviceInformation properties
- default roles
- communications policy
- session policy / ducking
- per-app persisted endpoints
- device association
- endpoint creation algorithm
- internal PolicyConfig / AudioPolicyConfig research

Public and undocumented policy mechanisms must remain clearly separated.

### D. Audio Engine and processing

Target coverage:

- audiodg / Audio Engine
- shared-mode mix engine
- processing modes
- system effects
- APO lifecycle
- SFX / MFX / EFX
- CompositeFX
- hardware offload
- RAW mode
- Voice Clarity
- AEC / noise suppression / AGC
- audio modules
- keyword detection

### E. Driver frameworks

Target coverage:

#### ACX

- device / driver initialization
- circuit / factory circuit
- pin / jack / microphone array
- stream / RT packets / stream bridges
- data formats
- elements
- AudioEngine / StreamAudioEngine
- AudioModule
- events / requests
- targets
- manager / templates
- ObjectBag
- versioning/function availability

Continue per-header completeness audit.

#### PortCls / WaveRT

- PortCls object model
- miniport interfaces
- WaveRT buffer models
- notification streams
- packet streams
- hardware position/timing
- power management
- DRM / protected streams

#### Kernel Streaming

- audio-specific property sets
- generic KS property sets used by audio
- pin interfaces / mediums
- data ranges / format negotiation
- connection state
- event sets
- methods
- topology / nodes
- jack properties
- WaveRT RTAudio property set
- historical DirectSound / DirectMusic / SysAudio contracts

### F. Official driver-reference checklist

Microsoft's Audio Devices DDI Reference is a useful top-level completeness checklist. WinAudioResearch should explicitly cover:

- Audio Drivers Enumerations
- Audio Drivers Property Sets
- Audio Drivers Event Sets
- Audio Topology Nodes
- Audio Drivers Structures
- Audio Drivers Interfaces
- Bluetooth HFP DDI Reference
- High Definition Audio DDI Reference
- DRM Functions
- Audio Device Messages for MIDI
- Legacy Audio Device Messages
- Media-Class INF Extensions
- Port Class Audio Driver Reference

This checklist is broader than ACX / KS alone and should be used as a recurring WDK audit boundary.

### G. Driver packaging and installation

Target coverage:

- audio INF directives
- endpoint configuration
- APO registration
- componentized audio drivers
- extension INF
- SoftwareComponent / HSA
- driver signing
- HLK requirements
- driver distribution
- ARM64 driver concerns
- registry/property-store contracts

### H. Hardware and transport families

Dedicated knowledge tracks:

- USB Audio Class 1 / 2
- Bluetooth A2DP
- Bluetooth HFP/HSP
- Bluetooth LE Audio
- HDMI / DisplayPort audio
- Intel/AMD/NVIDIA display audio context
- HD Audio / codec topology
- I2S / SoC audio
- DSP / codec / amplifier multi-circuit architectures
- jack detection
- microphone arrays
- cellular/telephony audio
- remote/RDP audio
- virtual audio devices
- network audio

For each transport, document both **protocol context** and **how Windows exposes it**.

### I. Formats, codecs and transport payloads

Target coverage:

- WAVEFORMATEX
- WAVEFORMATEXTENSIBLE
- speaker/channel masks
- KSDATAFORMAT / KSDATARANGE
- media subtype GUIDs
- PCM / IEEE float
- IEC 61937
- AC-3 / E-AC-3
- AAC
- MP3
- FLAC
- ALAC where relevant
- Opus where Windows support exists
- Bluetooth codec mapping
- spatial/object audio formats
- codec MFTs
- container/media compatibility

### J. Realtime, performance and latency

Target coverage:

- MMCSS / Pro Audio category
- WASAPI shared/exclusive latency
- IAudioClient3 engine periods
- event-driven streams
- WaveRT latency
- hardware offload
- glitch causes
- buffer sizing
- scheduling
- QPC / audio clocks
- drift and synchronization
- power-state interaction
- CPU / memory cost patterns

### K. Diagnostics, testing and observability

Target coverage:

- ETW audio providers
- WPR / WPA
- CollectAudioLogs
- ProcMon
- Event Viewer
- KsStudio
- Device Manager / PnP diagnostics
- Driver Verifier
- HLK audio tests
- Audio Glitch tracing
- latency/fidelity measurements
- crash/hang analysis
- useful registry inspection
- HRESULT / NTSTATUS catalog

### L. Security, privacy and app model

Target coverage:

- microphone privacy
- Windows capabilities
- AppContainer
- MSIX
- low integrity
- protected audio / PUMA
- protected capture
- services / Session 0
- user-session boundaries
- RDP security boundaries
- enterprise policies

### M. Language bindings and developer tooling

Target coverage:

- C / C++
- C++/WinRT
- WRL
- WIL
- C#
- CsWin32
- COM interop patterns
- Rust windows-rs
- Python wrappers where technically meaningful
- .NET NativeAOT constraints
- x64 / ARM64 ABI notes

### N. Open source and implementation studies

Maintain curated studies of:

- Microsoft Windows-driver-samples
- SysVAD
- ACX samples
- EarTrumpet
- NAudio
- Windows MIDI repository
- FFmpeg Windows audio backends
- OBS Windows capture/audio code
- Chromium/Firefox audio backends where useful
- game engines / middleware
- other high-quality public Windows audio implementations

Open-source implementation is **cross-reference**, not the definition of the Windows contract.

### O. Undocumented / observed Windows Audio

Keep physically and semantically separated.

Research targets:

- system default endpoint setters
- per-app persisted endpoint internals
- AudioPolicyConfig
- internal COM / WinRT classes
- build-specific IIDs
- vtable layout changes
- registry behavior
- undocumented audiosrv / EndpointBuilder behavior

Required evidence:

- exact Windows build
- architecture
- IID / CLSID / class name
- parameters
- HRESULT
- before / after state
- persistence behavior
- public alternative, if any

---

## 5. Data-source hierarchy

Use this precedence when resolving conflicts:

1. current Windows SDK / WDK headers
2. Microsoft Learn reference pages
3. Microsoft official samples
4. Windows release / driver guidance
5. Microsoft GitHub repositories
6. established open-source implementations
7. reproducible WinAudioResearch / SonicRoute experiments
8. community reports
9. reverse engineering

Lower-level sources may reveal behavior not documented above them, but must not silently overwrite the meaning of a public contract.

---

## 6. Repository structure target

```text
README.md                  project entrance
api/                       machine-readable API database
coverage/                  domain coverage matrices
docs/                      long-form technical knowledge
findings/                  reproducible observations
undocumented/              internal / ABI-sensitive research
resources/                 source hubs and external materials
references/                provenance and web research index
samples/                   future minimal experiments
scripts/                   queries / validation / generators
```

Future optional directories:

```text
experiments/
compatibility/
traces/
schemas/
```

Do not add them until there is real content.

---

## 7. Structured database expansion plan

The next database families should be added in this order.

### Priority 1 — Complete the lower layers

- Core Audio adjacent SDK declarations and callback/apartment/lifetime evidence after completed IID/CLSID dependency normalization
- remaining generic KS event/category/AVStream boundaries after completed Pin/Connection/Allocator/Clock integration
- PortCls final edge-method/IID/version audit
- ACX per-header delta audit
- APO runtime/build evidence after completed L5 header audit

### Priority 2 — Complete application runtime

- modern Core Audio headers beyond the classic four
- IAudioEffectsManager / IAudioStateMonitor
- Process Loopback support types
- WinRT audio members
- Media Foundation audio objects / attributes
- XAudio2 / XAPO complete type + HRESULT inventory

### Priority 3 — Properties / formats / errors

- PKEY / DEVPKEY catalogs
- processing-mode GUIDs
- audio subtype GUIDs
- KS node/pin/category GUIDs
- AUDCLNT HRESULTs
- Media Foundation errors
- XAudio2 errors
- driver NTSTATUS entries when audio-specific

### Priority 4 — Hardware / compatibility

- USB / Bluetooth / HDMI capability matrix
- Windows version behavior
- ARM64 notes
- real device evidence

---

## 8. Long-form documentation plan

Avoid creating one article per tiny symbol.

Prefer a layered structure:

- architecture overview;
- domain deep dive;
- focused implementation topic;
- coverage audit;
- troubleshooting guide.

Each article should link back to the structured database instead of duplicating huge interface tables.

---

## 9. Coverage dashboards

Maintain two kinds of coverage.

### Domain coverage

Example:

```text
WASAPI             L4
ACX                L5
KS Audio           L4
Bluetooth Audio    L2
USB Audio          L2
Diagnostics        L2
Undocumented       L3
```

### Contract coverage

Examples:

- ACX public headers covered / audited
- KS audio property-set families covered
- Core Audio header symbols covered
- APO interfaces covered
- official samples indexed

Never convert these into a misleading single “Windows Audio = 83% complete” number.

---

## 10. Validation rules

Every structured record should eventually answer:

```text
What is it?
Where is it declared?
Is it public?
How is it acquired?
What Windows version?
What does it connect to?
Where is the official source?
When was it verified?
```

For unstable/undocumented records also require:

```text
Which exact build?
Which architecture?
How was it observed?
What can break?
```

---

## 11. Milestones

### Milestone A — Core Windows Audio reference

Goal:

- Core Audio
- WASAPI
- sessions
- endpoint/device
- modern effect APIs
- Spatial Audio
- major WinRT audio APIs

### Milestone B — Driver reference

Goal:

- ACX audited
- WaveRT strong
- PortCls expanded
- KS property/event/interface foundations
- APO + INF strong

### Milestone C — Hardware/transport reference

Goal:

- USB
- Bluetooth Classic/LE
- HDMI/DP
- HD Audio / SoC
- jack / mic arrays / telephony

### Milestone D — Formats / codecs / media

Goal:

- subtype GUID catalog
- Windows codec support
- MF transform map
- IEC61937
- legacy ACM/DMO

### Milestone E — Diagnostics / compatibility

Goal:

- ETW workflows
- WPR profiles
- HLK
- Driver Verifier
- version matrices
- x64 / ARM64
- reproducible hardware evidence

### Milestone F — Research-grade cross-reference

Goal:

A developer can start from a task, API symbol, device behavior, error code or driver concept and navigate across:

```text
concept
→ public API/DDI
→ header/runtime
→ related property/event
→ Windows version
→ official sample
→ diagnostics
→ known implementation
→ observed compatibility evidence
```

That is the long-term definition of “large Windows audio knowledge base”.

---

## 12. Immediate next rounds

APO public-header coverage is L5 and the main generic KS streaming contracts are now machine-readable. [Audit 110](110-Core-Audio-Identifiers-and-Dependencies-Audit.md) has completed normalization of the 63 indexed Core Audio IID/CLSID records and their dependencies, with six adjacent SDK declarations explicitly deferred. The next reference round returns to the remaining driver audits.

1. Finish the remaining PortCls edge-method/IID/version audit.
2. Continue ACX current-WDK per-header delta audit.
3. Fill remaining generic KS event/category and AVStream callback boundaries.
4. Audit adjacent Core Audio SDK declarations and callback/apartment/lifetime boundaries.
5. Expand PKEY / DEVPKEY and codec/subtype GUID catalogs.
6. Expand AUDCLNT / Media Foundation / XAudio2 HRESULT catalogs.
7. Build API relationship path tests and source-provenance metadata.
8. Add L6 runtime evidence only where reproducible builds/hardware are available.
9. Add minimal runnable experiments after the reference layer is stable.
