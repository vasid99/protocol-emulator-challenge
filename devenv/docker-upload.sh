#!/usr/bin/env bash

set -x

cd $(git rev-parse --show-toplevel)/devenv
nix build .#container
docker load < result
docker tag "protocol-challenge-devenv:latest" "ghcr.io/parthkalgaonkar/protocol-challenge-devenv:latest"
docker push "ghcr.io/parthkalgaonkar/protocol-challenge-devenv:latest"
