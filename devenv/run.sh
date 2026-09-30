#!/usr/bin/env bash

image="ghcr.io/parthkalgaonkar/protocol-challenge-devenv:latest"
proj_root=$(git rev-parse --show-toplevel)

run_flags=""
if [ "$#" -eq 0 ]; then
  # If no command, run bash in interactive
  run_flags="-it"
fi

docker run \
  ${run_flags} \
  -u $(id -u):$(id -g) \
  -v \
    "${proj_root}:/home" \
  ${image} \
  $@
