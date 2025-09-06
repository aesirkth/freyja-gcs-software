# freyja-gcs-software

## installation of zephyr env

```bash
cd app
```

### setup python env

with pip:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install .
```

or with uv:
```bash
uv venv
source .venv/bin/activate
uv sync
```

### download zephyr

```bash
west update
```


### install zephyr python packages

with pip:
```bash
pip install -U -r ext/zephyr/scripts/requirements-base.txt
```

or with uv:
```bash
uv pip install -U -r ext/zephyr/scripts/requirements-base.txt
```

### install zephyr sdk

```bash
west sdk install --toolchains arm-zephyr-eabi
```


## installation of dashboard env

```bash
cd dashboard
```

with pip:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install .
```

or with uv:
```bash
uv venv
source .venv/bin/activate
uv sync
```