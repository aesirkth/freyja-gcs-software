#include <zephyr/drivers/uart.h>
#include <zephyr/logging/log.h>
#include <zephyr/sys/util.h>
#include "protocol.h"

LOG_MODULE_REGISTER(cdc_com);

#define TX_BUF_LEN 12 // 2 header bytes, 8 timstamp bytes, 1 byte packet type, 1 length, CAN packet max length of 8 
#define PKT_HEADER (uint8_t[]){0xAA, 0xAA}

static const struct device *const usb_uart = DEVICE_DT_GET(DT_NODELABEL(cdc_acm_uart0));

void submit_usb_pkt(const void *packet, unsigned int type, int64_t timestamp) {
    const int length = pkt_size[type];
    uint8_t tx_buf[TX_BUF_LEN];
    tx_buf[0] = PKT_HEADER[0];
    tx_buf[1] = PKT_HEADER[1];
    memcpy(tx_buf + 2, &timestamp, 8);
    tx_buf[10] = type;
    tx_buf[11] = length;
    memcpy(tx_buf + 12, packet, length);
    for (const char *p = (const char *)tx_buf; p < (const char *)tx_buf + 12 + length; ++p) {
        uart_poll_out(usb_uart, *p);
    }
}

int init_usb(void) {
    if (!device_is_ready(usb_uart)) {
        return -1;
    }

    return 0;
}