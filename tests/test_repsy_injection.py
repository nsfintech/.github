"""Exercise the actual inline publishing script without publishing packages."""
import os
from pathlib import Path
import subprocess
import tempfile
import textwrap
import tomllib
import unittest

WORKFLOW = Path(__file__).resolve().parents[1] / ".github/workflows/repsy-publish.yml"
SCRIPT = textwrap.dedent(WORKFLOW.read_text().split("<<'PERLEOF'\n", 1)[1].split("          PERLEOF", 1)[0])


class InjectionTests(unittest.TestCase):
    def inject(self, source, name="example"):
        with tempfile.TemporaryDirectory() as directory:
            script = Path(directory) / "inject.pl"
            manifest = Path(directory) / "Cargo.toml"
            script.write_text(SCRIPT)
            manifest.write_text(source)
            result = subprocess.run(
                ["perl", "-0pi", str(script), str(manifest)],
                env={**os.environ, "PERL_INJECT_CRATE": name, "PERL_INJECT_VER": "1.0.0-rc.14"},
                capture_output=True, text=True, check=True,
            )
            return manifest.read_text(), result.stderr

    def test_arrays_before_internal_dependency(self):
        source = '''[workspace.dependencies]
tokio = { version = "1", features = ["full"] }
serde = { version = "1", features = [
    "derive",
] }
example = { path = "crates/example", features = ["async"], default-features = false }
[profile.release]
lto = "thin"
'''
        output, log = self.inject(source)
        data = tomllib.loads(output)
        self.assertEqual(data["workspace"]["dependencies"]["example"], {
            "path": "crates/example", "features": ["async"], "default-features": False,
            "version": "=1.0.0-rc.14", "registry": "repsy",
        })
        self.assertEqual(data["profile"]["release"], {"lto": "thin"})
        self.assertIn("@repsy", log)

    def test_dependency_first_and_sequential_injection(self):
        source = '[workspace.dependencies]\nexample = { path = "a" }\nother = { path = "b" }\n'
        output, _ = self.inject(source)
        output, _ = self.inject(output, "other")
        for value in tomllib.loads(output)["workspace"]["dependencies"].values():
            self.assertEqual(value["version"], "=1.0.0-rc.14")
            self.assertEqual(value["registry"], "repsy")

    def test_missing_dependency_and_section_boundaries(self):
        for header in ('[dependencies]', '  [target."cfg(unix)".dependencies] # comment'):
            source = f'[workspace.dependencies]\ntokio = "1"\n{header}\nexample = {{ path = "outside" }}\n'
            output, log = self.inject(source)
            self.assertEqual(output, source)
            self.assertIn("::notice::", log)


if __name__ == "__main__":
    unittest.main()
