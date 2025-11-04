#include <zephyr/drivers/rtc.h>
#include <zephyr/logging/log.h>
#include <zephyr/sys/timeutil.h>

LOG_MODULE_REGISTER(clock);

const struct device *rtc_dev = DEVICE_DT_GET(DT_NODELABEL(rtc));

int get_timestamp(int64_t *timestamp) {
	static struct rtc_time rtc_timestamp;

    int ret = rtc_get_time(rtc_dev, &rtc_timestamp);
	if (ret) {
		LOG_ERR("could not get timestamp. error %d", ret);
		return ret;
	}

	*timestamp = (timeutil_timegm64(rtc_time_to_tm(&rtc_timestamp)) * 1000) + (rtc_timestamp.tm_nsec / 1000000);
	return 0;
}

int init_clock(void) {
    int ret;

    if (!device_is_ready(rtc_dev)) {
		LOG_ERR("could not init rtc");
		return 0;
	}

	// set placeholder time if time has been lost
	struct rtc_time time;
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
		return -1;
	}
	LOG_INF("Current time: %d/%d-%04d %02d:%02d:%02d.03%d",
				time.tm_mday, time.tm_mon, time.tm_year + 1900,
				time.tm_hour, time.tm_min, time.tm_sec, time.tm_nsec / 1000000);

    return 0;
}