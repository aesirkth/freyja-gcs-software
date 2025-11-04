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
make flash-app
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

| CAN ID | byte | data                           | type  |
| ------ | ---- | ------------------------------ | ----- |
| 0x720  | 0    | flight state                   | uint8 |
|        | 1    | loki state                     | uint8 |
|        | 2    | loki substate                  | uint8 |
|        | 3    | drogue deployed                | bool  |
|        | 4    | main deployed/line cut         | bool  |
|        | 5    | gnss fix                       | bool  |
| 0x721  | 0~3  | fafnir main valve percantage   | f32   |
|        | 4    | fafnir motor solenoid 1        | bool  |
|        | 5    | fafnir motor solenoid 2        | bool  |
|        | 6    | fafnir motor solenoid 3        | bool  |
|        | 7    | fafnir motor solenoid 4        | bool  |
| 0x722  | 0~3  | thrust (from loadcell)         | f32   |
| 0x723  | 0    | freyr airbrake safety solenoid | bool  |
|        | 1~4  | airbrake percantage            | f32   |
| 0x724  | 0    | pyro1 fired/connected          | bool  |
|        | 1    | pyro2 fired/connected          | bool  |
|        | 2    | pyro3 fired/connected          | bool  |
| 0x725  | 0~3  | ax                             | f32   |
|        | 4~7  | ay                             | f32   |
| 0x726  | 0~3  | az                             | f32   |
| 0x727  | 0~3  | vx                             | f32   |
|        | 4~7  | vy                             | f32   |
| 0x72A  | 0~3  | vz                             | f32   |
| 0x72B  | 0~3  | roll                           | f32   |
|        | 4~7  | pitch                          | f32   |
| 0x72C  | 0~3  | yaw                            | f32   |
| 0x72D  | 0~3  | longitude                      | f32   |
|        | 4~7  | latitude                       | f32   |
| 0x72E  | 0~3  | altitude                       | f32   |
| 0x72F  | 0~3  | sigurd temperature 1           | f32   |
|        | 4~7  | sigurd temperature 2           | f32   |
| 0x730  | 0~3  | sigurd temperature 3           | f32   |
|        | 4~7  | sigurd temperature 4           | f32   |
| 0x731  | 0~3  | fjalar bat voltage             | f32   |
|        | 4~7  | loki bat voltage               | f32   |


## usb message specification

the can packets are packaged with a header that's for byte long and then sent
over usb cdc acm.

| byte  | data | description                       |
| ----- | ---- | --------------------------------- |
| 0     | 0xAA | header byte 1                     |
| 1     | 0xAA | header byte 2                     |
| 2~9   | x    | milliseconds since 1970-01-01 UTC |
| 10    | x    | packet type i.e. CAN ID - 0x700   |
| 11    | x    | length of CAN packet              |
| 12~19 | x    | CAN packet                        |

note that the CAN packet's size is between 1 and 8 bytes. 