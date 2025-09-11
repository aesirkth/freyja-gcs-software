#include <zephyr/kernel.h>
#include <zephyr/drivers/gpio.h>
#include <zephyr/drivers/uart.h>
#include <zephyr/logging/log.h>

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

	if (!gpio_is_ready_dt(&led)) {
		return 0;
	}

	ret = gpio_pin_configure_dt(&led, GPIO_OUTPUT_ACTIVE);
	if (ret < 0) {
		return 0;
	}
	ret = gpio_pin_set_dt(&led, 1);
	if (ret < 0) {
		return 0;
	}

	LOG_INF("started");

	while (1) {
		const thrust_pkt_t pkt = {3.14f};
		submit_usb_pkt(&pkt, PKT_TYPE_THRUST);
		k_msleep(10);
	}
	return 0;
}
