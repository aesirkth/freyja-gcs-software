#include <zephyr/kernel.h>
#include <zephyr/drivers/gpio.h>
#include <zephyr/drivers/uart.h>
#include <zephyr/logging/log.h>

LOG_MODULE_REGISTER(main);

const struct device * cdc_acm = DEVICE_DT_GET(DT_NODELABEL(cdc_acm_uart0));

static const struct gpio_dt_spec led = GPIO_DT_SPEC_GET(DT_NODELABEL(tgl0_led), gpios);

int main(void)
{
	int ret;
	bool led_state = true;

	if (!gpio_is_ready_dt(&led)) {
		return 0;
	}

	ret = gpio_pin_configure_dt(&led, GPIO_OUTPUT_ACTIVE);
	if (ret < 0) {
		return 0;
	}

	while (1) {
		LOG_INF("toggling");
		ret = gpio_pin_toggle_dt(&led);
		if (ret < 0) {
			return 0;
		}

		/* Send some bytes */
		const char *msg = "Hello over CDC ACM!\r\n";
		for (const char *p = msg; *p; ++p) {
			uart_poll_out(cdc_acm, *p);   // simple, blocking
		}

		led_state = !led_state;
		k_msleep(1000);
	}
	return 0;
}
