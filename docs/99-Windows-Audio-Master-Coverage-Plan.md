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

### F. Driver packaging and installation

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

### G. Hardware and transport families

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

### H. Formats, codecs and transport payloads

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

### I. Realtime, performance and latency

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

### J. Diagnostics, testing and observability

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

### K. Security, privacy and app model

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

### L. Language bindings and developer tooling

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

### M. Open source and implementation studies

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

### N. Undocumented / observed Windows Audio

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

- KS generic connection/general/interface/event contracts
- WaveRT supporting structs and callbacks
- PortCls interfaces beyond current WaveRT core
- ACX per-header delta audit
- APO interfaces + registration/property contracts

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

1. Finish generic KS contracts used by audio: General / Connection / interface sets / event sets.
2. Expand WaveRT supporting structures and PortCls interfaces.
3. Audit all current ACX WDK header pages against the database.
4. Audit Core Audio SDK headers beyond interface-level coverage.
5. Build complete PKEY / DEVPKEY and processing-mode GUID catalogs.
6. Expand HRESULT / error catalog.
7. Build official sample index by technology and API.
8. Build source-provenance metadata and per-domain audit pages.
9. Add minimal runnable experiments only after the reference layer is stable.
