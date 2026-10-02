import csv
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.validate_core_audio_audit import validate_audit


class CoreAudioAuditTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "api").mkdir()
        self.headers = self.root / "headers"
        self.headers.mkdir()
        self.guid = "1CB9AD4C-DBFA-4C32-B178-C2F568A703B2"
        self.source = f'MIDL_INTERFACE("{self.guid.lower()}")\n IAudioClient : public IUnknown {{}};\n'
        self.header_path = self.headers / "Audioclient.h"
        self.header_path.write_bytes(self.source.encode())
        self.symbols = [{"symbol": "IAudioClient", "kind": "interface", "family": "WASAPI", "header_or_namespace": "audioclient.h", "status": "Public", "min_client": "Windows Vista", "iid_or_guid": self.guid}]
        self.deps = [{"symbol": "IAudioClient", "family": "WASAPI", "header": "audioclient.h", "status": "Public", "min_client": "Windows Vista", "library": "", "dll_or_runtime": "COM runtime"}, {"symbol": "ActivateAudioInterfaceAsync", "family": "MMDevice", "header": "mmdeviceapi.h", "status": "Public", "min_client": "Windows 8", "library": "Mmdevapi.lib", "dll_or_runtime": "Mmdevapi.dll"}]
        self.manifest = {"version": 1, "verified": "2026-10-02", "source_repository": "https://github.com/microsoft/win32metadata", "source_commit": "a" * 40, "groups": [{"table": "api/wasapi.csv", "header": "Audioclient.h", "header_sha256": hashlib.sha256(self.source.encode()).hexdigest(), "interfaces": {"IAudioClient": self.guid}, "classes": {}, "excluded_declarations": {}}], "function_dependencies": {"ActivateAudioInterfaceAsync": {"family": "MMDevice", "library": "Mmdevapi.lib", "dll_or_runtime": "Mmdevapi.dll"}}}
        self.save()

    def save(self):
        for name, rows in (("wasapi.csv", self.symbols), ("dependencies.csv", self.deps)):
            with (self.root / "api" / name).open("w", newline="", encoding="utf-8") as stream:
                writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
                writer.writeheader()
                writer.writerows(rows)
        (self.root / "api/core-audio-audit.json").write_text(json.dumps(self.manifest), encoding="utf-8")

    def check_error(self, fragment, with_headers=False):
        errors, _ = validate_audit(self.root, self.headers if with_headers else None)
        self.assertTrue(any(fragment in error for error in errors), errors)

    def test_valid_snapshot_offline_and_from_headers(self):
        self.assertEqual(validate_audit(self.root), ([], 1))
        self.assertEqual(validate_audit(self.root, self.headers), ([], 1))

    def test_wrong_but_well_formed_guid_is_rejected(self):
        self.symbols[0]["iid_or_guid"] = "00000000-0000-0000-0000-000000000000"
        self.save()
        self.check_error("IID/CLSID differs")

    def test_blank_guid_is_rejected(self):
        self.symbols[0]["iid_or_guid"] = ""
        self.save()
        self.check_error("IID/CLSID differs")

    def test_missing_dependency_is_rejected(self):
        self.deps = self.deps[1:]
        self.save()
        self.check_error("missing dependency record")

    def test_wrong_function_import_library_is_rejected(self):
        self.deps[1]["library"] = "Ole32.lib"
        self.save()
        self.check_error("dependency library differs")

    def test_wrong_source_declaration_is_rejected(self):
        changed = self.source.replace(self.guid.lower(), "00000000-0000-0000-0000-000000000000")
        self.header_path.write_bytes(changed.encode())
        self.manifest["groups"][0]["header_sha256"] = hashlib.sha256(changed.encode()).hexdigest()
        self.save()
        self.check_error("source declaration differs", with_headers=True)

    def test_changed_source_bytes_are_rejected(self):
        self.header_path.write_bytes((self.source + "// changed snapshot\n").encode())
        self.check_error("source header hash differs", with_headers=True)

    def test_new_header_interface_requires_explicit_coverage_decision(self):
        changed = self.source + 'DECLARE_INTERFACE_IID_(IExtra, IUnknown, "A95664D2-9614-4F35-A746-DE8DB63617E6") {};\n'
        self.header_path.write_bytes(changed.encode())
        self.manifest["groups"][0]["header_sha256"] = hashlib.sha256(changed.encode()).hexdigest()
        self.save()
        self.check_error("source declaration not classified: IExtra", with_headers=True)

    def test_coclass_and_non_midl_interface_declarations(self):
        from scripts.validate_core_audio_audit import parse_declarations
        parsed = parse_declarations('class DECLSPEC_UUID("BCDE0395-E52F-467C-8E3D-C4579291692E") MMDeviceEnumerator;\nDECLARE_INTERFACE_IID_(IAudioStateMonitor, IUnknown, "63BD8738-E30D-4C77-BF5C-834E87C657E2") {};')
        self.assertEqual(parsed["MMDeviceEnumerator"], ("BCDE0395-E52F-467C-8E3D-C4579291692E", "class"))
        self.assertEqual(parsed["IAudioStateMonitor"], ("63BD8738-E30D-4C77-BF5C-834E87C657E2", "interface"))


if __name__ == "__main__":
    unittest.main()
