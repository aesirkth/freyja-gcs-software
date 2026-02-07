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

static const struct gpio_dt_spec led_0 = GPIO_DT_SPEC_GET(DT_NODELABEL(tgl0_led), gpios);
static const struct gpio_dt_spec tgl_0 = GPIO_DT_SPEC_GET(DT_NODELABEL(tgl0), gpios);
static const struct gpio_dt_spec led_7 = GPIO_DT_SPEC_GET(DT_NODELABEL(tgl7_led), gpios);
static const struct gpio_dt_spec tgl_7 = GPIO_DT_SPEC_GET(DT_NODELABEL(tgl7), gpios);
static const struct gpio_dt_spec launch_btn = GPIO_DT_SPEC_GET(DT_NODELABEL(btn_launch), gpios);
static const struct gpio_dt_spec btn_arm = GPIO_DT_SPEC_GET(DT_NODELABEL(launch_armd), gpios);

/*
static const struct LedGpioMap led_gpio_map[] = {
    { &led_0, &tgl_0 },
};
*/

int main(void) {
	// LEDRegistry registry;
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

	if (!gpio_is_ready_dt(&led_0) || !gpio_is_ready_dt(&tgl_0) || !gpio_is_ready_dt(&led_7) ||  !gpio_is_ready_dt(&tgl_7) || !gpio_is_ready_dt(&launch_btn) || !gpio_is_ready_dt(&btn_arm)) {
		return 0;
	}

	// LED pin in
	ret = gpio_pin_configure_dt(&tgl_0, GPIO_INPUT);
	if (ret < 0) {
		LOG_ERR("Failed to configure LED pin 0 in");
		return 0;
	}
	ret = gpio_pin_configure_dt(&tgl_7, GPIO_INPUT);
	if (ret < 0) {
		LOG_ERR("Failed to configure LED pin 7 in");
		return 0;
	}

	// LED pin out
	ret = gpio_pin_configure_dt(&led_0, GPIO_OUTPUT);
	if (ret < 0) {
		LOG_ERR("Failed to configure LED pin 0 out");
		return 0;
	}
	ret = gpio_pin_configure_dt(&led_7, GPIO_OUTPUT);
	if (ret < 0) {
		LOG_ERR("Failed to configure LED pin 7 out");
		return 0;
	}

    ret = gpio_pin_configure_dt(&launch_btn, GPIO_INPUT);
    if (ret) {
        LOG_ERR("Failed to configure launch_btn %d", ret);
        return 0;
    }

    ret = gpio_pin_configure_dt(&btn_arm, GPIO_INPUT);
    if (ret) {
        LOG_ERR("Failed to configure btn_arm %d", ret);
        return 0;
    }
	
	LOG_INF("Started");

	while (1) {
		get_timestamp(&timestamp);

        int val_armd = gpio_pin_get_dt(&btn_arm);
		int val_launch = gpio_pin_get_dt(&launch_btn);
		int val_led_0 = gpio_pin_get_dt(&led_0);
		int val_tgl_0 = gpio_pin_get_dt(&tgl_0);
		int val_led_7 = gpio_pin_get_dt(&led_7);
		int val_tgl_7 = gpio_pin_get_dt(&tgl_7);

		const armd_pkt_t armd_pkt = {val_armd};
		const launch_pkt_t launch_pkt = {val_launch};
		const gcs_test_mode_pkt_t gcs_test_mode_pkt = {val_tgl_7};

		if (val_tgl_0 < 0 && val_tgl_0) {
			LOG_ERR("Failed to read LED toggle pin 0");
		} else {
			LOG_INF("led_0 = %d", val_led_0);
			LOG_INF("tgl_0 = %d", val_tgl_0);
		}
		if (val_tgl_7 < 0 && val_tgl_7) {
			LOG_ERR("Failed to read LED toggle pin 7");
		} else {
			LOG_INF("led_7 = %d", val_led_7);
			LOG_INF("tgl_7 = %d", val_tgl_7);
			int64_t timestamp;
    		int ret = get_timestamp(&timestamp);
			submit_usb_pkt(&gcs_test_mode_pkt, PKT_TYPE_GCS_TEST_MODE, timestamp);
		}

        if (val_launch < 0 || val_armd < 0) {
			LOG_ERR("Failed to read pins");
        } else {
			LOG_INF("launch_btn = %d, btn_arm = %d", val_launch, val_armd);
			submit_can_pkt(&armd_pkt, PKT_TYPE_ARMD);
			submit_can_pkt(&launch_pkt, PKT_TYPE_LAUNCH);
        }
		k_msleep(100);
	}
	return 0;
}
