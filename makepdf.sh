#!/bin/bash

# docker build -t pandoc-eisvogel-acm ./docker-msr

document=msr-challenge-2020

docker run \
  --rm \
  -v $GITHUB_WORKSPACE/$document:/project \
  -w /project \
  --entrypoint "./makepdf.sh" \
  pandoc-eisvogel \
  $document
