#include <zephyr/kernel.h>
#include <zephyr/drivers/gpio.h>
#include <zephyr/drivers/uart.h>
#include <zephyr/logging/log.h>

#include "can_com.h"
#include "clock.h"
#include "usb_com.h"
#include "protocol.h"

LOG_MODULE_REGISTER(main);

const struct device *cdc_acm = DEVICE_DT_GET(DT_NODELABEL(cdc_acm_uart0));

static const struct gpio_dt_spec led = GPIO_DT_SPEC_GET(DT_NODELABEL(tgl0_led), gpios);

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
		const state_pkt_t state_pkt = {9, 2, 6, 1, 0};
		const fafnir_pkt_t fafnir_pkt = {9.12f, 1, 0, 1, 1};
		const thrust_pkt_t thrust_pkt = {3.14f};
		const airbrake_pkt_t airbrake_pkt = {1, 0.32f};
		const pyro_pkt_t pyro_pkt = {1, 1, 1};
		const acc_pkt_1_t acc_pkt_1 = {50.0, 2.0};
		const acc_pkt_2_t acc_pkt_2 = {3.0};
		const vel_pkt_1_t vel_pkt_1 = {200.0, 3.0};
		const vel_pkt_2_t vel_pkt_2 = {3.0};
		const coords_pkt_t coords_pkt = {30.5, 120.5};
		const altitude_pkt_t altitude_pkt = {30.5};
		const sigurd_temp_pkt_1_t sigurd_temp_pkt_1 = {30.5, 20.5};
		const sigurd_temp_pkt_2_t sigurd_temp_pkt_2 = {30.5, 30.4};
		const bat_pkt_t bat_pkt = {8.5, 11.4};

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
