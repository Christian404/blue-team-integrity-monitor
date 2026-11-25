"""Read-only file integrity comparison for a directory you are authorized to inspect."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path


def snapshot(root):
    root = Path(root)
    if not root.is_dir() or root.is_symlink():
        raise ValueError('root must be an existing, non-symlink directory')
    files = {}
    for folder, dirs, names in os.walk(root, followlinks=False):
        dirs[:] = sorted(d for d in dirs if d not in {'.git', '__pycache__'} and not (Path(folder) / d).is_symlink())
        for name in sorted(names):
            path = Path(folder) / name
            if path.is_symlink() or not path.is_file():
                continue
            digest = hashlib.sha256()
            with path.open('rb') as stream:
                while chunk := stream.read(65536):
                    digest.update(chunk)
            files[path.relative_to(root).as_posix()] = digest.hexdigest()
    return files


def compare(before, after):
    return {'added': sorted(after.keys() - before.keys()),
            'removed': sorted(before.keys() - after.keys()),
            'modified': sorted(k for k in before.keys() & after.keys() if before[k] != after[k])}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['baseline', 'compare'])
    parser.add_argument('directory', type=Path)
    parser.add_argument('manifest', type=Path)
    args = parser.parse_args()
    try:
        # Keep the manifest outside the observed directory to avoid observing itself.
        if args.manifest.resolve().is_relative_to(args.directory.resolve()):
            raise ValueError('store the manifest outside the observed directory')
        current = snapshot(args.directory)
        if args.command == 'baseline':
            with args.manifest.open('x', encoding='utf-8') as stream:
                json.dump({'schema': 1, 'created_at': datetime.now(timezone.utc).isoformat(), 'algorithm': 'SHA-256', 'files': current}, stream, indent=2)
            print(json.dumps({'status': 'baseline_created', 'files': len(current)}))
            return 0
        data = json.loads(args.manifest.read_text(encoding='utf-8'))
        if data.get('schema') != 1 or data.get('algorithm') != 'SHA-256' or not isinstance(data.get('files'), dict):
            raise ValueError('invalid manifest schema')
        before = data['files']
        if not all(isinstance(k, str) and isinstance(v, str) and len(v) == 64 and all(c in '0123456789abcdef' for c in v) for k, v in before.items()):
            raise ValueError('invalid SHA-256 entries')
        result = compare(before, current)
        print(json.dumps({'status': 'changes_detected' if any(result.values()) else 'unchanged', **result}, ensure_ascii=False, indent=2))
        return 1 if any(result.values()) else 0
    except (OSError, ValueError, TypeError) as error:
        parser.exit(2, f'Error: {error}\n')


if __name__ == '__main__':
    raise SystemExit(main())
