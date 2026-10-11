#!/usr/bin/python3
# kg-wrap.py — preserve the runner's PID and process group; signals reach kogen directly.
# KG_STATS timing/RSS logging is dropped because this process becomes kogen.
import os
import sys

OFFLINE_ENV = {
    **{name: "http://127.0.0.1:9" for name in
       ("http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "all_proxy")},
    "NO_PROXY": "127.0.0.1,localhost",
    "no_proxy": "127.0.0.1,localhost",
    "UV_OFFLINE": "1", "CARGO_NET_OFFLINE": "true", "GOPROXY": "off", "HEX_OFFLINE": "1",
    "npm_config_offline": "true", "NPM_CONFIG_OFFLINE": "true",
}
BUILD_ENV = ("CARGO_HOME", "GOPATH", "GOMODCACHE", "GOCACHE", "MIX_HOME", "HEX_HOME",
             "BUN_INSTALL_CACHE_DIR", "BUN_RUNTIME_TRANSPILER_CACHE_PATH", "XDG_CACHE_HOME",
             "UV_CACHE_DIR", "MYPY_CACHE_DIR", "RUFF_CACHE_DIR", "RACE5_PY_CACHE_ROOT",
             "npm_config_cache", "RACE4_ARM_ROOT", "RACE3_KIT", "RUSTUP_HOME", "GOTOOLCHAIN")

if __name__ == "__main__":
    # The suite builds a filtered environment. Apply the scoring policy here,
    # without changing the frozen suite or its local fake-provider settings.
    os.environ.update(OFFLINE_ENV)
    os.environ.pop("GOFLAGS", None)  # Prebuilt output needs no module flags.
    for name in BUILD_ENV:
        os.environ.pop(name, None)
    real = os.environ["KG_REAL"]
    os.execv(real, [real] + sys.argv[1:])
