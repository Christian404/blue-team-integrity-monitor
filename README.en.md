# HACKER | Blue Team Integrity Monitor

[Português](README.md) · English

An offline Python tool that creates a SHA-256 baseline and reports added, removed and modified files in an authorized directory. It reads monitored files without modifying them and installs no agent, service or persistence.

Requires Python 3.10+ and no third-party packages. Create a directory named `samples` containing disposable test files. Keep the baseline manifest outside the monitored directory.

```bash
python integrity.py baseline samples baseline.json
python integrity.py compare samples baseline.json
python -m unittest discover -s tests -v
```

Exit codes: **0** means a baseline was created or no changes were found; **1** means changes were found; **2** means an input, access or manifest error. An existing baseline is never overwritten.

Tests cover SHA-256 output, relative paths, added/changed/deleted files, empty/missing directories, CLI exit codes and manifest protection. Local execution evidence is recorded in `evidence/validacao.json`. Check Actions for the separate remote CI outcome.

## Limitations and investigation

A changed hash is a signal, not proof of malware. Legitimate maintenance produces changes too. Build the baseline from a trusted state and protect it separately: an attacker-controlled manifest invalidates the comparison. Manifests are not signed. Changes reverted between scans are not detected. Files changing during a scan do not form an atomic snapshot. Symlinks, `.git` and `__pycache__` directories are skipped. This local exercise is not a replacement for Wazuh FIM or an EDR product.

Review asset ownership, approved changes and maintenance windows before taking action. Preserve evidence and assess impact before rolling back. No employer data is included.

Author: Gabriel Christian de Oliveira. Prepared with AI assistance; reviewed 25/11/2026. Current commits use the requested `HACKER:` prefix and retain real authorship and dates.
