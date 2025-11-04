#include <zephyr/kernel.h>
#include <zephyr/drivers/gpio.h>
#include <zephyr/drivers/rtc.h>
#include <zephyr/drivers/uart.h>
#include <zephyr/logging/log.h>

#include "can_com.h"
#include "usb_com.h"
#include "protocol.h"

LOG_MODULE_REGISTER(main);

const struct device *cdc_acm = DEVICE_DT_GET(DT_NODELABEL(cdc_acm_uart0));

const struct device *rtc_dev = DEVICE_DT_GET(DT_NODELABEL(rtc));

static const struct gpio_dt_spec led = GPIO_DT_SPEC_GET(DT_NODELABEL(tgl0_led), gpios);

int main(void) {
	int ret;
	struct rtc_time time;

	if (init_usb() < 0) {
		LOG_ERR("could not init usb");
		return 0;
	}

	if (init_can() < 0) {
		LOG_ERR("could not init can");
		return 0;
	}

	if (!device_is_ready(rtc_dev)) {
		LOG_ERR("could not init rtc");
		return 0;
	}

	// set placeholder time if time has been lost
	if (rtc_get_time(rtc_dev, &time) != 0) {
		struct rtc_time new_time = { 
			.tm_year=2025 - 1900,
			.tm_mon=1,
			.tm_mday=1,
			.tm_hour=0, 
			.tm_min=0, 
			.tm_sec=0 
		};
		ret = rtc_set_time(rtc_dev, &new_time);
		if (ret) {
			LOG_ERR("rtc time set error %d", ret);
			return 0;
		}
	}
	ret = rtc_get_time(rtc_dev, &time);
	if (ret) {
		LOG_ERR("rtc time get err %d", ret);
		return 0;
	}
	LOG_INF("Current time: %d/%d-%04d %02d:%02d:%02d\n",
				time.tm_mday, time.tm_mon, time.tm_year + 1900,
				time.tm_hour, time.tm_min, time.tm_sec);

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
		const thrust_pkt_t pkt = {3.14f};
		submit_usb_pkt(&pkt, PKT_TYPE_THRUST);
		submit_can_pkt(&pkt, PKT_TYPE_THRUST);
		k_msleep(1000);
	}
	return 0;
}
