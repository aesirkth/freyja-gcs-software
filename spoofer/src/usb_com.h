#pragma once

void submit_usb_pkt(const void *packet, unsigned int type, int64_t timestamp);

int init_usb(void);