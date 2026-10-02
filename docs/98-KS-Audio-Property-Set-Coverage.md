# Kernel Streaming Audio Property Set Coverage

> Baseline: **2026-10-02**  
> Scope: audio-specific property sets listed by Microsoft under **Audio Drivers Property Sets**.

## Family-level coverage

Microsoft currently lists **27 audio driver property-set families**. All 27 now have at least a family-level record in `api/ks-audio.csv`.

| Property set | Family present |
|---|---|
| `KSPROPSETID_AC3` | ✅ |
| `KSPROPSETID_Acoustic_Echo_Cancel` | ✅ |
| `KSPROPSETID_Audio` | ✅ |
| `KSPROPSETID_AudioEngine` | ✅ |
| `KSPROPSETID_AudioGfx` | ✅ |
| `KSPROPSETID_AudioLoopback` | ✅ |
| `KSPROPSETID_AudioModule` | ✅ |
| `KSPROPSETID_BtAudioModule` | ✅ |
| `KSPROPSETID_DirectSound3DBuffer` | ✅ |
| `KSPROPSETID_DirectSound3DListener` | ✅ |
| `KSPROPSETID_DrmAudioStream` | ✅ |
| `KSPROPSETID_FMRXControl` | ✅ |
| `KSPROPSETID_FMRXTopology` | ✅ |
| `KSPROPSETID_Hrtf3d` | ✅ |
| `KSPROPSETID_Itd3d` | ✅ |
| `KSPROPSETID_Jack` | ✅ |
| `KSPROPSETID_RTAudio` | ✅ |
| `KSPROPSETID_SoundDetector` | ✅ |
| `KSPROPSETID_SoundDetector2` | ✅ |
| `KSPROPSETID_Synth` | ✅ |
| `KSPROPSETID_SynthClock` | ✅ |
| `KSPROPSETID_Synth_Dls` | ✅ |
| `KSPROPSETID_Sysaudio` | ✅ |
| `KSPROPSETID_Sysaudio_Pin` | ✅ |
| `KSPROPSETID_TelephonyControl` | ✅ |
| `KSPROPSETID_TelephonyTopology` | ✅ |
| `KSPROPSETID_TopologyNode` | ✅ |

**Family coverage: 27 / 27.**

This is deliberately different from saying **all members are complete**.

## Newly expanded in this audit

### WaveRT / RTAudio

`KSPROPSETID_RTAudio` now includes the documented property family for:

- buffer allocation;
- notification buffer support;
- hardware clock / position registers;
- hardware latency;
- packet count;
- capture read packets;
- render write packets;
- presentation position;
- register / unregister notification events.

Microsoft documents these RTAudio properties as pin-targeted, get-only requests at the property-set contract level.

### Legacy WDM audio families

The database now also indexes:

- AC-3 control properties;
- hardware AEC controls;
- DRM stream content ID;
- DirectSound 3D buffer/listener properties;
- HRTF / ITD 3D properties;
- DirectMusic Synth / SynthClock / DLS;
- SysAudio / SysAudio_Pin virtual-device controls.

These are retained because WinAudioResearch is a **Windows audio history + compatibility + implementation** database, not only a modern API list.

### FM receiver

The two remaining Microsoft-listed families are now represented:

- `KSPROPSETID_FMRXControl`
- `KSPROPSETID_FMRXTopology`

including receiver state, render endpoint, antenna endpoint and volume entries. These are primarily Windows 10 Mobile-era contracts and are marked Legacy.

## Member-level status

Areas with relatively strong property/member coverage:

- `KSPROPSETID_Audio`
- `KSPROPSETID_AudioEngine`
- `KSPROPSETID_RTAudio`
- `KSPROPSETID_Jack`
- SoundDetector / SoundDetector2
- DirectSound 3D / HRTF / ITD
- Synth / SynthClock / Synth_Dls
- Telephony
- SysAudio core set

Areas that still require deeper member/type auditing:

- `KSPROPSETID_BtAudioModule`
- some AudioModule supporting structures;
- AC-3 supporting enums/structures;
- DirectSound 3D supporting structures;
- RTAudio support structures;
- SysAudio enum members beyond the commonly documented property pages;
- exact FMRX structure/type metadata;
- old WDM property sets outside Microsoft's current audio-specific list.

## Next KS audit boundary

The next stage should expand beyond the 27-family checklist into related KS contracts that audio drivers rely on but that are not all listed as audio-specific property sets:

- `KSPROPSETID_General`
- connection / stream property sets;
- data ranges / interfaces / mediums;
- KSEVENT families;
- WaveRT structures;
- pin creation attributes;
- audio signal-processing mode properties.

## Primary sources

- Audio Drivers Property Sets  
  https://learn.microsoft.com/windows-hardware/drivers/audio/audio-drivers-property-sets
- RTAudio property set  
  https://learn.microsoft.com/windows-hardware/drivers/audio/kspropsetid-rtaudio
- Audio endpoints, properties and events  
  https://learn.microsoft.com/windows-hardware/drivers/audio/audio-endpoints--properties-and-events
- KS Audio database  
  ../api/ks-audio.csv
