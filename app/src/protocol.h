#pragma once

#include <stdint.h>
#include <stdbool.h>

typedef enum {
    STATE_IDLE,
    STATE_AWAITING_INIT,
    STATE_INITIATED,
    STATE_AWAITING_LAUNCH,
    STATE_BOOST,
    STATE_COAST,
    STATE_DROGUE_DESCENT,
    STATE_MAIN_DESCENT,
    STATE_LANDED,
} fjalar_flight_state_t;

typedef enum {
    STATE_LOKI_STARTUP = 1,
    STATE_LOKI_READY,
    STATE_LOKI_ARMED,
    STATE_LOKI_ERROR_TEMP,
    STATE_LOKI_ERROR_PERM,
    STATE_LOKI_WARN_EXT,
} loki_state_t;

typedef enum {
    SUB_STATE_IDLE,
    SUB_STATE_ENGAGE,
    SUB_STATE_DISENGAGE,
} loki_substate_t;

typedef struct armd_pkt {
    bool armd;
} armd_pkt_t;

typedef struct launch_pkt {
    bool launch;
} launch_pkt_t;

typedef struct state_pkt {
    uint8_t fjalar_flight_state;
    uint8_t loki_state;
    uint8_t loki_substate;
    bool drogue_deployed;
    bool gnss_fixed;
} state_pkt_t;

typedef struct fafnir_pkt {
    float main_valve_percantage;
    bool solenoid_1;
    bool solenoid_2;
    bool solenoid_3;
    bool solenoid_4;
} fafnir_pkt_t;

typedef struct thrust_pkt {
    float thrust;
} thrust_pkt_t;

typedef struct airbrake_pkt {
    bool airbrake_safety;
    float airbrake_percantage;
} airbrake_pkt_t;

typedef struct pyro_pkt {
    bool pyro1_connected;
    bool pyro2_connected;
    bool pyro3_connected;
} pyro_pkt_t;

typedef struct acc_pkt_1 {
    float ax;
    float ay;
} acc_pkt_1_t;

typedef struct acc_pkt_2 {
    float az;
} acc_pkt_2_t;

typedef struct vel_pkt_1 {
    float vx;
    float vy;
} vel_pkt_1_t;

typedef struct vel_pkt_2 {
    float vz;
} vel_pkt_2_t;

typedef struct coords_pkt {
    float longitude;
    float latitude;
} coords_pkt_t;

typedef struct altitude_pkt {
    float altitude;
} altitude_pkt_t;

typedef struct sigurd_temp_pkt_1 {
    float temp_1;
    float temp_2;
} sigurd_temp_pkt_1_t;

typedef struct sigurd_temp_pkt_2 {
    float temp_3;
    float temp_4;
} sigurd_temp_pkt_2_t;

typedef struct bat_pkt {
    float fjalar_bat_volts;
    float loki_bat_volts;
} bat_pkt_t;

typedef enum {
    // gcs -> fjalar
    PKT_TYPE_ARMD = 0x00,
    PKT_TYPE_LAUNCH,
    // fjalar -> gcs
    PKT_TYPE_STATE = 0x20,
    PKT_TYPE_FAFNIR,
    PKT_TYPE_THRUST,
    PKT_TYPE_AIRBRAKE,
    PKT_TYPE_PYRO,
    PKT_TYPE_ACC_1,
    PKT_TYPE_ACC_2,
    PKT_TYPE_VEL_1,
    PKT_TYPE_VEL_2,
    PKT_TYPE_COORDS,
    PKT_TYPE_ALTITUDE,
    PKT_TYPE_SIGURD_TEMP_1,
    PKT_TYPE_SIGURD_TEMP_2,
    PKT_TYPE_BAT,
    PKT_COUNT,
} pkt_type_t;

static const size_t pkt_size[PKT_COUNT] = {
    [PKT_TYPE_ARMD] = sizeof(armd_pkt_t),
    [PKT_TYPE_LAUNCH] = sizeof(launch_pkt_t),
    [PKT_TYPE_STATE] = sizeof(state_pkt_t),
    [PKT_TYPE_FAFNIR] = sizeof(fafnir_pkt_t),
    [PKT_TYPE_THRUST] = sizeof(thrust_pkt_t),
    [PKT_TYPE_AIRBRAKE] = sizeof(airbrake_pkt_t),
    [PKT_TYPE_PYRO] = sizeof(pyro_pkt_t),
    [PKT_TYPE_ACC_1] = sizeof(acc_pkt_1_t),
    [PKT_TYPE_ACC_2] = sizeof(acc_pkt_2_t),
    [PKT_TYPE_VEL_1] = sizeof(vel_pkt_1_t),
    [PKT_TYPE_VEL_2] = sizeof(vel_pkt_2_t),
    [PKT_TYPE_COORDS] = sizeof(coords_pkt_t),
    [PKT_TYPE_ALTITUDE] = sizeof(altitude_pkt_t),
    [PKT_TYPE_SIGURD_TEMP_1] = sizeof(sigurd_temp_pkt_1_t),
    [PKT_TYPE_SIGURD_TEMP_2] = sizeof(sigurd_temp_pkt_2_t),
    [PKT_TYPE_BAT] = sizeof(bat_pkt_t),
};
