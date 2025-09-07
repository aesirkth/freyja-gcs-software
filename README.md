# freyja-gcs-software

## installation of zephyr env

download and install stm32 cube prog 
https://www.st.com/en/development-tools/stm32cubeprog.html

then move to app directory:
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

### register zephyr as cmake package

```bash
west zephyr-export
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


## build app

to build:
```bash
make
```

to flash over usb enter bootloader by holding the upper button while pressing the
lower button briefly. and then:
```bash
make flash-app-usb
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


## can message specification

### gcs to fjalar

| CAN ID | bit | data             | type |
| ------ | --- | ---------------- | ---- |
| 0x700  | 0   | ready/arm fjalar | bool |
| 0x701  | 0   | launch           | bool |


### fjalar to gcs

| CAN ID | bit   | data                           | type  |
| ------ | ----- | ------------------------------ | ----- |
| 0x720  | 0~7   | flight state                   | uint8 |
|        | 8~15  | loki state                     | uint8 |
|        | 16~23 | loki substate                  | uint8 |
|        | 24    | drogue deployed                | bool  |
|        | 25    | main deployed/line cut         | bool  |
|        | 26    | freyr airbrake safety solenoid | bool  |
|        | 27    | gnss fix                       | bool  |
|        | 28    | pyro1 fired/connected          | bool  |
|        | 29    | pyro2 fired/connected          | bool  |
|        | 30    | pyro3 fired/connected          | bool  |
|        | 31    | fafnir motor solenoid 1        | bool  |
|        | 32    | fafnir motor solenoid 2        | bool  |
|        | 33    | fafnir motor solenoid 3        | bool  |
|        | 34    | fafnir motor solenoid 4        | bool  |
| 0x721  | 0~31  | fafnir main valve percantage   | f32   |
|        | 32~63 | airbrake percantage            | f32   |
| 0x722  | 0~31  | thrust (from loadcell)         | f32   |
| 0x723  | 0~31  | ax                             | f32   |
|        | 32~63 | ay                             | f32   |
| 0x724  | 0~31  | az                             | f32   |
| 0x725  | 0~31  | vx                             | f32   |
|        | 32~63 | vy                             | f32   |
| 0x726  | 0~31  | vz                             | f32   |
| 0x727  | 0~31  | roll                           | f32   |
|        | 32~63 | pitch                          | f32   |
| 0x728  | 0~31  | yaw                            | f32   |
| 0x729  | 0~31  | longitude                      | f32   |
|        | 32~63 | latitude                       | f32   |
| 0x72A  | 0~31  | altitude                       | f32   |
| 0x72B  | 0~31  | sigurd temperature 1           | f32   |
|        | 32~64 | sigurd temperature 1           | f32   |
| 0x72C  | 0~31  | fjalar bat voltage             | f32   |
|        | 32~63 | loki bat voltage               | f32   |



