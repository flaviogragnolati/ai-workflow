#!/usr/bin/env bash
set -euo pipefail

# Synchronize the approved zero-install Archify runtime subset from a pinned checkout.
# This maintainer command performs no network access; obtain and inspect the checkout first.

if [[ $# -ne 2 ]]; then
  echo "Usage: $0 <archify-checkout-path> <tag-or-commit>" >&2
  exit 2
fi

source_checkout=$(cd "$1" && pwd)
source_root="$source_checkout/archify"
source_ref=$2
repo_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)
runtime_dir="$repo_root/skills/tool/q-tool-archify/runtime"
mkdir -p "$(dirname "$runtime_dir")"
staging_dir=$(mktemp -d "$repo_root/skills/tool/q-tool-archify/.runtime-sync.XXXXXX")
trap 'rm -rf "$staging_dir"' EXIT

if [[ ! -f "$source_root/bin/archify.mjs" || ! -f "$source_root/skill-release.json" ]]; then
  echo "Archify runtime not found under $source_root" >&2
  exit 1
fi

source_commit=$(git -C "$source_checkout" rev-list -n 1 "$source_ref")
head_commit=$(git -C "$source_checkout" rev-parse HEAD)
if [[ "$source_commit" != "$head_commit" ]]; then
  echo "Checkout HEAD $head_commit does not match $source_ref ($source_commit)" >&2
  exit 1
fi

mkdir -p "$staging_dir/runtime"
target="$staging_dir/runtime"

# Copy only functional runtime material. Deliberately excluded: Archify SKILL.md,
# test/, generated HTML examples, package metadata, update checking, generators,
# repository automation, and every other repository-root file.
cp -R "$source_root/bin" "$target/bin"
cp -R "$source_root/renderers" "$target/renderers"
cp -R "$source_root/schemas" "$target/schemas"
mkdir -p "$target/assets" "$target/delta" "$target/migrations" "$target/recipes" "$target/references" "$target/scripts" "$target/examples"
cp "$source_root/assets/template.html" "$target/assets/template.html"
cp "$source_root/delta/architecture-delta.mjs" "$target/delta/architecture-delta.mjs"
cp "$source_root/migrations/workflow-v2.mjs" "$target/migrations/workflow-v2.mjs"
cp -R "$source_root/brand-marks" "$target/brand-marks"
cp "$source_root/recipes/scenarios.mjs" "$target/recipes/scenarios.mjs"
cp "$source_root/references/authoring-contract.md" "$target/references/authoring-contract.md"
cp "$source_root/references/delivery-contract.md" "$target/references/delivery-contract.md"
cp "$source_root/references/viewer-runtime.md" "$target/references/viewer-runtime.md"
cp "$source_root/references/brand-marks.md" "$target/references/brand-marks.md"
cp "$source_root/scripts/check-render-output.mjs" "$target/scripts/check-render-output.mjs"
cp "$source_root/scripts/render-examples.mjs" "$target/scripts/render-examples.mjs"
cp "$source_root"/examples/*.json "$target/examples/"
cp "$source_root/LICENSE" "$target/LICENSE"
cp "$source_root/THIRD_PARTY_NOTICES.md" "$target/THIRD_PARTY_NOTICES.md"
cp "$source_root/skill-release.json" "$target/skill-release.json"

runtime_version=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1], encoding="utf-8"))["version"])' "$target/skill-release.json")
printf 'version=%s\ncommit=%s\nsynced=%s\n' "$runtime_version" "$source_commit" "$(date +%F)" > "$target/ARCHIFY_VERSION"

if find "$target" -name SKILL.md -print -quit | grep -q .; then
  echo "Refusing a runtime containing a nested SKILL.md" >&2
  exit 1
fi
if [[ -e "$target/scripts/check-update.mjs" || -e "$target/package.json" ]]; then
  echo "Refusing forbidden Archify update or package metadata" >&2
  exit 1
fi

rm -rf "$runtime_dir"
mv "$target" "$runtime_dir"
echo "Synchronized Archify $runtime_version ($source_commit) into $runtime_dir"
