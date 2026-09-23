#!/usr/bin/env bash
# powrobots-collect — run all collectors sequentially
# Called by the systemd service. Logs to journald.
set -euo pipefail

cd /home/ubuntu/powrobots
export PYTHONPATH=/home/ubuntu

echo "=== powrobots collect all === $(date -u +%Y-%m-%dT%H:%M:%SZ)"
python3 -m powrobots.cli collect all
echo "=== done === $(date -u +%Y-%m-%dT%H:%M:%SZ)"
