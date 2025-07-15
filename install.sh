#!/usr/bin/env bash
set -e
apt-get update
apt-get install -y python3 python3-pip
pip3 install --no-cache-dir fastapi==0.110.0 "uvicorn[standard]"==0.29.0 pydantic==1.10.14
