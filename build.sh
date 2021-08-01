#!/usr/bin/env bash
docker build -f docker/Dockerfile -t panoslin/finance .
docker stack deploy -c docker/docker-compose.yml finance