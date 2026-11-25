from pathlib import Path
import hashlib
import subprocess
import sys
import tempfile
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from integrity import snapshot, compare


class IntegrityTests(unittest.TestCase):
    def test_sha256_and_relative_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); (root/'sample.txt').write_bytes(b'evidence')
            self.assertEqual(snapshot(root), {'sample.txt': hashlib.sha256(b'evidence').hexdigest()})

    def test_added_modified_removed(self):
        self.assertEqual(compare({'a':'old','b':'old'}, {'a':'new','c':'new'}), {'added':['c'],'removed':['b'],'modified':['a']})

    def test_unchanged(self):
        self.assertFalse(any(compare({'a':'same'}, {'a':'same'}).values()))

    def test_empty_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(snapshot(tmp), {})

    def test_missing_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError): snapshot(Path(tmp)/'absent')

    def test_cli_exit_codes_and_manifest_protection(self):
        script = str(Path(__file__).resolve().parents[1]/'integrity.py')
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)/'observed';root.mkdir();manifest=Path(tmp)/'baseline.json';(root/'a').write_text('one')
            def run(*args):return subprocess.run([sys.executable,script,*map(str,args)],capture_output=True)
            self.assertEqual(run('baseline',root,manifest).returncode,0)
            self.assertEqual(run('compare',root,manifest).returncode,0)
            (root/'a').write_text('two')
            self.assertEqual(run('compare',root,manifest).returncode,1)
            self.assertEqual(run('baseline',root,manifest).returncode,2)
            self.assertEqual(run('baseline',root,root/'manifest.json').returncode,2)


if __name__ == '__main__': unittest.main()
