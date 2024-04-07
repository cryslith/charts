#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")"

d="$(mktemp -d)"
mkdir "$d/elestrophe"
cp -r -t "$d/elestrophe" Duvet Gomen_ne_Iiko_ja_Irarenai
pushd "$d"
zip -r elestrophe.zip elestrophe
popd
mv "$d/elestrophe.zip" .
rm -rf "$d"
