#!/bin/bash
# Install Python dependencies for AI Auto-Remediation
sudo apt-get update
sudo apt-get install -y python3-pip jq
pip3 install google-genai requests
