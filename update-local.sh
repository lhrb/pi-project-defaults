#!/usr/bin/env bash
set -euo pipefail

cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
mkdir -p "$HOME/.pi/agent"
cp -a .pi/{agents,prompts,skills} "$HOME/.pi/agent/"
