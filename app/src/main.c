#include <zephyr/kernel.h>
#include <zephyr/drivers/gpio.h>
#include <zephyr/drivers/uart.h>
#include <zephyr/logging/log.h>

#include "can_com.h"
#include "usb_com.h"
#include "protocol.h"

LOG_MODULE_REGISTER(main);

const struct device * cdc_acm = DEVICE_DT_GET(DT_NODELABEL(cdc_acm_uart0));

static const struct gpio_dt_spec led = GPIO_DT_SPEC_GET(DT_NODELABEL(tgl0_led), gpios);

int main(void) {
	int ret;

	if (init_usb() < 0) {
		LOG_ERR("could not init usb");
		return 0;
	}

	if (init_can() < 0) {
		LOG_ERR("could not init can");
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
		const state_pkt_t state_pkt = {1, 0, 0, 1, 1};
		const fafnir_pkt_t fafnir_pkt = {67, 0, 0, 1, 1};
		const thrust_pkt_t thrust_pkt = {2.14f};
		const airbrake_pkt_t airbrake_pkt = {1, 8.14f};
		const pyro_pkt_t pyro_pkt = {1, 0, 1};
		const acc_pkt_1_t acc_1_pkt = {5.14f, 6.14f};
		const acc_pkt_2_t acc_2_pkt = {2.14f};
		const vel_pkt_1_t vel_1_pkt = {24.14f, 12.2f};
		const vel_pkt_2_t vel_2_pkt = {1.14f};
		const coords_pkt_t coords_pkt = {1.14f, 2.64f};
		const altitude_pkt_t altitude_pkt = {120.2f};
		const sigurd_temp_pkt_1_t sigurd_temp_pkt_1 = {12.2f, 20.2f};
		const sigurd_temp_pkt_2_t sigurd_temp_pkt_2 = {20.2f, 32.2f};
		const bat_pkt_t bat_pkt = {6.2f, 6.4f};

		submit_usb_pkt(&state_pkt, PKT_TYPE_STATE);
		submit_usb_pkt(&fafnir_pkt, PKT_TYPE_FAFNIR);
		submit_usb_pkt(&thrust_pkt, PKT_TYPE_THRUST);
		submit_usb_pkt(&airbrake_pkt, PKT_TYPE_AIRBRAKE);
		submit_usb_pkt(&pyro_pkt, PKT_TYPE_PYRO);
		submit_usb_pkt(&acc_1_pkt, PKT_TYPE_ACC_1);
		submit_usb_pkt(&acc_2_pkt, PKT_TYPE_ACC_2);
		submit_usb_pkt(&vel_1_pkt, PKT_TYPE_VEL_1);
		submit_usb_pkt(&vel_2_pkt, PKT_TYPE_VEL_2);
		submit_usb_pkt(&coords_pkt, PKT_TYPE_COORDS);
		submit_usb_pkt(&altitude_pkt, PKT_TYPE_ALTITUDE);
		submit_usb_pkt(&sigurd_temp_pkt_1, PKT_TYPE_SIGURD_TEMP_1);
		submit_usb_pkt(&sigurd_temp_pkt_2, PKT_TYPE_SIGURD_TEMP_2);
		
		k_msleep(10);
	}
	return 0;
}
