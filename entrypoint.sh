#!/bin/bash
set -euo pipefail

exec waitress-serve gpyt_openai.injection.injector:app
