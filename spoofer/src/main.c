#include <zephyr/kernel.h>
#include <zephyr/drivers/gpio.h>
#include <zephyr/drivers/uart.h>
#include <zephyr/logging/log.h>
#include <zephyr/random/random.h>

#include "can_com.h"
#include "clock.h"
#include "usb_com.h"
#include "protocol.h"
#include <stdint.h>

LOG_MODULE_REGISTER(main);

const struct device *cdc_acm = DEVICE_DT_GET(DT_NODELABEL(cdc_acm_uart0));

static const struct gpio_dt_spec led = GPIO_DT_SPEC_GET(DT_NODELABEL(tgl0_led), gpios);

int int_randomizer(int min, int max) {
    if (max < min) { int t = min; min = max; max = t; }
    uint32_t span = (uint32_t)(max - min) + 1u;
    uint32_t r = sys_rand32_get();
    return min + (int)(r % span);
}

float float_randomizer(float min, float max) {
    uint32_t r = sys_rand32_get();
    float u = (float)r / (float)UINT32_MAX;
    return min + u * (max - min);
}

int main(void) {
	int ret;
	int64_t timestamp;

	if (init_usb() < 0) {
		LOG_ERR("could not init usb");
		return 0;
	}

	if (init_can() < 0) {
		LOG_ERR("could not init can");
		return 0;
	}

	if (init_clock() < 0) {
		LOG_ERR("could not init clock");
		return 0;
	}

	if (!gpio_is_ready_dt(&led)) {
		return 0;
	}

	ret = gpio_pin_configure_dt(&led, GPIO_OUTPUT_ACTIVE);
	if (ret < 0) {
		LOG_ERR("could not configure pin");
		return 0;
	}
	ret = gpio_pin_set_dt(&led, 1);
	if (ret < 0) {
		LOG_ERR("could not set pin");
		return 0;
	}

	LOG_INF("started");

	while (1) {
		const state_pkt_t state_pkt = {
			int_randomizer(0, 20),
			int_randomizer(0, 20),
			int_randomizer(0, 20),
			1,
			0
		};
		const fafnir_pkt_t fafnir_pkt = {
			float_randomizer(0.0f, 20.0f),
			1,
			0,
			1,
			1
		};
		const thrust_pkt_t thrust_pkt = {
			float_randomizer(0.0f, 20.0f)
		};
		const airbrake_pkt_t airbrake_pkt = {
			1,
			float_randomizer(0.0f, 20.0f)
		};
		const pyro_pkt_t pyro_pkt = {
			1,
			0,
			1
		};
		const acc_pkt_1_t acc_pkt_1 = {
			float_randomizer(0.0f, 20.0f), 
			float_randomizer(0.0f, 20.0f)
		};
		const acc_pkt_2_t acc_pkt_2 = {
			float_randomizer(0.0f, 20.0f)
		};
		const vel_pkt_1_t vel_pkt_1 = {
			float_randomizer(0.0f, 20.0f),
			float_randomizer(0.0f, 20.0f)
		};
		const vel_pkt_2_t vel_pkt_2 = {
			float_randomizer(0.0f, 20.0f)
		};
		const coords_pkt_t coords_pkt = {
			float_randomizer(0.0f, 20.0f),
			float_randomizer(0.0f, 20.0f)
		};
		const altitude_pkt_t altitude_pkt = {
			float_randomizer(0.0f, 20.0f)
		};
		const sigurd_temp_pkt_1_t sigurd_temp_pkt_1 = {
			float_randomizer(0.0f, 20.0f),
			float_randomizer(0.0f, 20.0f)
		};
		const sigurd_temp_pkt_2_t sigurd_temp_pkt_2 = {
			float_randomizer(0.0f, 20.0f),
			float_randomizer(0.0f, 20.0f)
		};
		const bat_pkt_t bat_pkt = {
			float_randomizer(0.0f, 30.0f),
			float_randomizer(0.0f, 30.0f)
		};

		submit_can_pkt(&state_pkt, PKT_TYPE_STATE);
		submit_can_pkt(&fafnir_pkt, PKT_TYPE_FAFNIR);
		submit_can_pkt(&thrust_pkt, PKT_TYPE_THRUST);
		submit_can_pkt(&airbrake_pkt, PKT_TYPE_AIRBRAKE);
		submit_can_pkt(&pyro_pkt, PKT_TYPE_PYRO);
		submit_can_pkt(&acc_pkt_1, PKT_TYPE_ACC_1);
		submit_can_pkt(&acc_pkt_2, PKT_TYPE_ACC_2);
		submit_can_pkt(&vel_pkt_1, PKT_TYPE_VEL_1);
		submit_can_pkt(&vel_pkt_2, PKT_TYPE_VEL_2);
		submit_can_pkt(&coords_pkt, PKT_TYPE_COORDS);
		submit_can_pkt(&altitude_pkt, PKT_TYPE_ALTITUDE);
		submit_can_pkt(&sigurd_temp_pkt_1, PKT_TYPE_SIGURD_TEMP_1);
		submit_can_pkt(&sigurd_temp_pkt_2, PKT_TYPE_SIGURD_TEMP_2);
		submit_can_pkt(&bat_pkt, PKT_TYPE_BAT);

		k_msleep(1000);
	}
	return 0;
}
