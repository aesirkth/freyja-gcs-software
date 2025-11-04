#include <zephyr/drivers/can.h>
#include <zephyr/logging/log.h>
#include <zephyr/sys/util.h>
#include <errno.h>

#include "protocol.h"
#include "usb_com.h"

LOG_MODULE_REGISTER(can_com);

const struct device *const can_dev = DEVICE_DT_GET(DT_NODELABEL(fdcan1));


const struct can_filter filter = {
    .flags = 0,
    .id = 0x700,
    .mask = 0b11110000000 // match from 0x700 to 0x77F
};

void can_rx_cb(const struct device *const device, struct can_frame *frame, void *user_data) {
    LOG_DBG("rx: %#X", frame->id);

    int pkt_type = frame->id - 0x700;

    if (frame->dlc != pkt_size[pkt_type]) {
        LOG_ERR("received packet %#x has length %d but should be length %d", pkt_type, frame->dlc, pkt_size[pkt_type]);
    }

    submit_usb_pkt(frame->data, pkt_type);
}

void can_tx_cb(const struct device *device, int error, void *user_data) {
    if (error) {
        LOG_ERR("can send callback error [%d]", error);
    }
}

int submit_can_pkt(const void *packet, unsigned int type) {
    int ret = 0;

    const int length = pkt_size[type];
    struct can_frame frame = {
            .flags = 0,
            .id = type + 0x700,
            .dlc = length,
    };
    memcpy(frame.data, packet, length);
    ret = can_send(can_dev, &frame, K_MSEC(10), can_tx_cb, NULL);

    if (ret == -EAGAIN) {
        LOG_ERR("can send timeout");
    } else if (ret) {
        LOG_ERR("can send error [%d]", ret);
    }
    return ret;
}

int init_can(void) {
    int ret;
 
    if (!device_is_ready(can_dev)) {
        LOG_ERR("CAN device not ready");
        return -1;
    }
    
    ret = can_add_rx_filter(can_dev, can_rx_cb, NULL, &filter);
    if (ret) {
        LOG_ERR("adding can filter failed: %d", ret);
    } else {
        LOG_INF("adding can filter success");
    }

    ret = can_set_bitrate(can_dev, 500000); // 500 kb/s
    if (ret) {
        LOG_ERR("failed to set CAN nominal bitrate: [%d]", ret);
        return -1;
    } else {
        LOG_INF("CAN nominal bitrate successfully set to 500kb/s");
    }

    ret = can_set_bitrate_data(can_dev, 500000); // 500 kb/s
    if (ret) {
        LOG_ERR("failed to set CAN bitrate: [%d]", ret);
        return -1;
    } else {
        LOG_INF("CAN bitrate successfully set to 500kb/s");
    }

    ret = can_start(can_dev);
    if (ret) {
        LOG_ERR("failed to start CAN: %d", ret);
        return -1;
    } else{
        LOG_INF("CAN started");
    }

    return 0;
}