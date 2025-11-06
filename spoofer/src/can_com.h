#pragma once

int init_can(void);

void submit_can_pkt(const void *packet, unsigned int type);
