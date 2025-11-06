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
static const struct gpio_dt_spec launch_btn = GPIO_DT_SPEC_GET(DT_NODELABEL(btn_launch), gpios);
static const struct gpio_dt_spec btn_arm = GPIO_DT_SPEC_GET(DT_NODELABEL(launch_armd), gpios);

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

	if (!gpio_is_ready_dt(&led) || !gpio_is_ready_dt(&launch_btn) || !gpio_is_ready_dt(&btn_arm)) {
		return 0;
	}

	ret = gpio_pin_configure_dt(&led, GPIO_OUTPUT_ACTIVE);
	if (ret < 0) {
		LOG_ERR("Failed to configure pin");
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

	ret = gpio_pin_set_dt(&led, 1);
	if (ret < 0) {
		LOG_ERR("could not set pin");
		return 0;
	}

	LOG_INF("started");

	while (1) {
		get_timestamp(&timestamp);
		
        int val_armd = gpio_pin_get_dt(&btn_arm);
		int val_launch = gpio_pin_get_dt(&launch_btn);
		
		const armd_pkt_t armd_pkt = {val_armd};
		const launch_pkt_t launch_pkt = {val_launch};

        if (val_launch < 0 || val_armd < 0) {
			LOG_ERR("Failed to read pins");
        } else {
			LOG_INF("launch_btn = %d, btn_arm = %d", val_launch, val_armd);
			submit_can_pkt(&armd_pkt, PKT_TYPE_ARMD);
			submit_can_pkt(&launch_pkt, PKT_TYPE_LAUNCH);
        }
		k_msleep(1000);
	}
	return 0;
}
