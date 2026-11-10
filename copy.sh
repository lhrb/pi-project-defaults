#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 || ! -d "$1" ]]; then
    printf 'Usage: %s EXISTING_PROJECT_DIRECTORY\n' "$0" >&2
    exit 1
fi

source_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
destination=$(cd -- "$1" && pwd)
files=(architecture.md AGENTS.md .pi/settings.json .pi/agents .pi/prompts .pi/skills)

# Check every target before copying anything. Never merge or overwrite defaults.
for file in "${files[@]}"; do
    target="$destination/$file"
    if [[ -e "$target" || -L "$target" ]]; then
        printf 'Refusing to overwrite: %s\n' "$target" >&2
        exit 1
    fi
    if [[ ! -e "$source_dir/$file" ]]; then
        printf 'Missing template file: %s\n' "$source_dir/$file" >&2
        exit 1
    fi
done

if [[ -e "$destination/.pi" || -L "$destination/.pi" ]]; then
    if [[ ! -d "$destination/.pi" || -L "$destination/.pi" ]]; then
        printf 'Expected a real directory: %s/.pi\n' "$destination" >&2
        exit 1
    fi
fi

mkdir -p -- "$destination/.pi"
for file in "${files[@]}"; do
    cp -R -- "$source_dir/$file" "$destination/$file"
done
printf 'Copied project defaults to %s\n' "$destination"
