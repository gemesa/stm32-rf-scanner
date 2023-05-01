/**
 ******************************************************************************
 * @file util.h
 * @brief Utility functions.
 * @author gemesa
 *
 * @attention
 *
 * Copyright (c) 2023 András Gémes. All rights reserved.
 *
 * This software component is licensed by András Gémes under GNU GPLv3 license.
 * You may obtain a copy of the license at: opensource.org/licenses/GPL-3.0
 *
 * SPDX-License-Identifier: gpl-3.0
 ******************************************************************************
 */

#ifndef GEN_DOC_UTIL_H_
#define GEN_DOC_UTIL_H_

#include <stdint.h> /* uint8_t, uint16_t */

/**
 * Bool define.
 */
#define TRUE     (uint8_t)1u
/**
 * Bool define.
 */
#define FALSE    (uint8_t)0u

extern void util_init(void);
extern uint8_t bit(uint8_t bit);
extern void delay_us(uint16_t delay);
extern void blink_led(void);

#endif /* GEN_DOC_UTIL_H_ */
