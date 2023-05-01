/**
 ******************************************************************************
 * @file util.c
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

#include "main.h"

/**
 * @brief TIMER2 handler instance.
 */
extern TIM_HandleTypeDef htim2;

/**
 * @brief Start TIMER2. Required for delay_us().
 * @author gemesa
 */
void util_init(void)
{
    HAL_TIM_Base_Start(&htim2);
}

/**
 * @brief Bit shift: 1u << bit
 * @author gemesa
 * @param ui8_bit
 * @return
 */
uint8_t bit(uint8_t ui8_bit)
{
    return 1u << ui8_bit;
}

/**
 * @brief Delays X microseconds.
 * @author gemesa
 * @param ui16_delay
 */
void delay_us(uint16_t ui16_delay)
{
    __HAL_TIM_SET_COUNTER(&htim2, 0u);
    while (__HAL_TIM_GET_COUNTER(&htim2) < ui16_delay)
        ;
}

/**
 * @brief Blinks built in LED every 100ms. Has to be called in main() while loop. Nonblocking function.
 * @author gemesa
 */
void blink_led(void)
{
    uint32_t ui32_c_time;
    static uint32_t ui32_p_time;

    ui32_c_time = HAL_GetTick();
    if ((ui32_c_time - ui32_p_time) >= 100U)
    {
        ui32_p_time = ui32_c_time;
        HAL_GPIO_TogglePin(GPIOC, GPIO_PIN_13);
    }
}
