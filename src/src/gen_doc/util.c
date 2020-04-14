/**
 ******************************************************************************
 * @file util.c
 * @brief utility functions
 * @author gemesa
 ******************************************************************************
 */

#include "main.h"

/**
 * @brief TIMER2 handler instance.
 */
extern TIM_HandleTypeDef htim2;

/**
 * @brief Start TIMER2. Required for delay_us().
 */
void util_init(void)
{
    HAL_TIM_Base_Start(&htim2);
}

/**
 * @brief Bit shift: 1u << bit
 * @param bit
 * @return
 */
uint8_t bit(uint8_t bit)
{
    return 1u << bit;
}

/**
 * @brief Delays X microseconds.
 * @param delay
 */
void delay_us(uint16_t delay)
{
    __HAL_TIM_SET_COUNTER(&htim2, 0u);
    while (__HAL_TIM_GET_COUNTER(&htim2) < delay)
        ;
}

/**
 * @brief Blinks built in LED every 100ms. Has to be called in main() while loop. Nonblocking function.
 */
void blink_led(void)
{
    uint32_t c_time;
    static uint32_t p_time;

    c_time = HAL_GetTick();
    if ((c_time - p_time) >= 100U)
    {
        p_time = c_time;
        HAL_GPIO_TogglePin(GPIOC, GPIO_PIN_13);
    }
}
