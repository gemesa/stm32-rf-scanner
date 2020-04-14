/**
 ******************************************************************************
 * @file util.h
 * @brief utility functions
 * @author gemesa
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
