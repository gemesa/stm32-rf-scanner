/**
 ******************************************************************************
 * @file rf_scanner.c
 * @brief Scans frequencies from 2.400GHz to 2.525GHz (1MHz resolution)
 * with nRF24L01+ and plots the activity on each frequency through UART.
 * @author gemesa
 ******************************************************************************
 */

#include "main.h"
#include "util.h" /* TRUE, FALSE, delay_us, bit */
#include <stdio.h> /* sprintf */
#include <string.h> /* memset */

/* number of the RF channels
 * datasheet chapter:
 *      - 6.3 */
const uint8_t NUM_OF_CH = 126u;

/* number of scans per call */
const uint16_t NUM_OF_SCAN = 180u;

/**
 * SPI1 handler instance.
 */
extern SPI_HandleTypeDef hspi1;
/**
 * UART2 handler instance.
 */
extern UART_HandleTypeDef huart2;

static uint8_t get_reg(uint8_t ui8_reg);
static void set_reg(uint8_t ui8_reg, uint8_t ui8_val);
static void get_freq_data(uint8_t aui8_rpd[]);
static uint8_t max_array(uint8_t aui8_array[], uint8_t ui8_size);
static uint8_t calc_norm(uint8_t aui8_rpd[], uint8_t aui8_rpd_norm[], uint8_t ui8_size);
static void plot_freq_data(uint8_t aui8_rpd[]);
void rf_scanner_step(void);
void rf_scanner_init(void);
static void plot_layout(void);
static void nrf24l01p_init(void);

/**
 * @brief Reads out a register through SPI.
 * @author gemesa
 * @param ui8_reg register address
 * @return register value
 * @details
 * datasheet chapter:
 *      - 8
 *      - 9.1
 */
static uint8_t get_reg(uint8_t ui8_reg)
{
    uint8_t ui8_data_rx;
    const uint8_t ui8_data_tx = ui8_reg; /* R_REGISTER = 0b000AAAAA */

    HAL_GPIO_WritePin(GPIOB, SS_Pin, GPIO_PIN_RESET);
    HAL_SPI_Transmit(&hspi1, (uint8_t*) &ui8_data_tx, sizeof ui8_data_tx, 10u);
    HAL_SPI_Receive(&hspi1, &ui8_data_rx, sizeof ui8_data_rx, 10u);
    HAL_GPIO_WritePin(GPIOB, SS_Pin, GPIO_PIN_SET);

    return ui8_data_rx;
}

/**
 * @brief Writes a register through SPI.
 * @author gemesa
 * @param ui8_reg register address
 * @param ui8_val register value
 * @details
 * datasheet chapter:
 *      - 8
 *      - 9.1
 */
static void set_reg(uint8_t ui8_reg, uint8_t ui8_val)
{
    const uint8_t ui8_data_tx_reg = ui8_reg | bit(5u); /* W_REGISTER = 0b001AAAAA */
    const uint8_t ui8_data_tx_val = ui8_val;

    HAL_GPIO_WritePin(GPIOB, SS_Pin, GPIO_PIN_RESET);
    HAL_SPI_Transmit(&hspi1, (uint8_t*) &ui8_data_tx_reg, sizeof ui8_data_tx_reg, 10u);
    HAL_SPI_Transmit(&hspi1, (uint8_t*) &ui8_data_tx_val, sizeof ui8_data_tx_val, 10u);
    HAL_GPIO_WritePin(GPIOB, SS_Pin, GPIO_PIN_SET);
}

/**
 * @brief Checks which frequencies (channels) are occupied.
 * @author gemesa
 * @param aui8_rpd pointer to RPD array
 * @details
 * datasheet chapter:
 *      - 6.1.4
 *      - 6.4
 *      - 9.1
 */
static void get_freq_data(uint8_t aui8_rpd[])
{
    uint16_t i;
    uint8_t j;
    const uint16_t TSTBY2A = 130u; /* [us], standby mode --> RX mode */
    const uint16_t TDELAY_AGC = 40u; /* automatic gain control */
    /* TSTBY2A + TDELAY_AGC = delay for RPD status to set */
    const uint8_t REG_RF_CH = 0x05u; /* RF channel */
    const uint8_t REG_RPD = 0x09u; /* received power detector */

    for (i = 0u; i < NUM_OF_SCAN; i++)
    {
        for (j = 0u; j < NUM_OF_CH; j++)
        {
            set_reg(REG_RF_CH, j);
            HAL_GPIO_WritePin(GPIOB, CE_Pin, GPIO_PIN_SET);
            /* wait for RPD flag to be set, it is set and correct if
             *      - signal level at pin is > -64dBm
             *      - signal is present for at least 40us
             *      - TSTBY2A + TDELAY_AGC = 130us + 40us wait time elapsed
             * this wait time is the bottleneck:
             * NUM_OF_SCAN * NUM_OF_CH * (TSTBY2A + TDELAY_AGC) = 180 * 126 * (130us + 40us) = 3855600us = 3.86s
             * speed can be increased by:
             *      - decreasing NUM_OF_SCAN
             *      - decreasing NUM_OF_CH
             *      - using multiple nrf24l01+ HWs
             * speed can not be increased by reducing TSTBY2A + TDELAY_AGC delay time
             * because RPD flag might be incorrect */
            delay_us(TSTBY2A + TDELAY_AGC);
            HAL_GPIO_WritePin(GPIOB, CE_Pin, GPIO_PIN_RESET); /* RPD flag is set here */
            /* check RPD flag */
            if (get_reg(REG_RPD) == bit(0u))
            {
                aui8_rpd[j]++;
            }
        }
    }
}

/**
 * @brief Finds max element in an array.
 * @author gemesa
 * @param aui8_array pointer to target array
 * @param ui8_size size of target array
 */
static uint8_t max_array(uint8_t aui8_array[], uint8_t ui8_size)
{
    uint8_t i;
    uint8_t ui8_max = 0u;

#pragma GCC unroll 9 // 126/9 = 14
    for (i = 0u; i < ui8_size; i++)
    {
        if (aui8_array[i] > ui8_max)
        {
            ui8_max = aui8_array[i];
        }
    }

    return ui8_max;
}

/**
 * @brief Calculates normalized values. Returns the maximum value in the default array.
 * @author gemesa
 * @param aui8_rpd pointer to RPD array
 * @param aui8_rpd_norm pointer to normalized RPD array
 * @param ui8_size size of RPD array (= size of normalized RPD array)
 */
static uint8_t calc_norm(uint8_t aui8_rpd[], uint8_t aui8_rpd_norm[], uint8_t ui8_size)
{
    /* find max reference RPD for normalizing */
    uint8_t ui8_rpd_ref = max_array(aui8_rpd, ui8_size);
    if (ui8_rpd_ref == 0u)
    {
        /* do nothing, all RPD values are 0s */
        return ui8_rpd_ref;
    }

    const uint8_t GREY_SIZE = 10u;
    const uint8_t aui8_greyscale[] = " .:-=+*#%@";
    uint8_t i;
    uint8_t ui8_grey_val;

#pragma GCC unroll 9 // 126/9 = 14
    for (i = 0u; i < ui8_size; i++)
    {
        /* calculations are necessary only if RPD value is not 0 */
        if (aui8_rpd[i] != 0u)
        {
            /* add 0.5 for proper rounding */
            ui8_grey_val = (uint8_t) (((float) aui8_rpd[i] * (float) (GREY_SIZE - 1u)) / (float) ui8_rpd_ref + 0.5f);
            /* keep weak signals */
            if (ui8_grey_val == 0u)
            {
                ui8_grey_val = 1u;
            }
            aui8_rpd_norm[i] = aui8_greyscale[ui8_grey_val];
        }
        else
        {
            /* RPD value is 0 */
            aui8_rpd_norm[i] = aui8_greyscale[0u];
        }
    }

    return ui8_rpd_ref;
}

/**
 * @brief Plots which frequencies (channels) are occupied.
 * @author gemesa
 * @param aui8_rpd pointer to RPD array
 */
static void plot_freq_data(uint8_t aui8_rpd[])
{
    /* plot layout after every 18th line */
    static uint8_t ui8_line_cntr = 18u;
    if (ui8_line_cntr == 18u)
    {
        plot_layout();
        ui8_line_cntr = 0u;
    }
    ui8_line_cntr++;

    /* calculate normalized data and reference RPD */
    uint8_t aui8_rpd_norm[NUM_OF_CH + 1u]; /* +1 char: null terminator */
    memset(aui8_rpd_norm, 0u, sizeof aui8_rpd_norm);
    uint8_t ui8_rpd_ref = calc_norm(aui8_rpd, aui8_rpd_norm, NUM_OF_CH);

    /* print normalized data and reference RPD */
    uint8_t aui8_uart_tx[1u + NUM_OF_CH + 14u + 1u]; // = 142u (141 chars + null terminator)
    memset(aui8_uart_tx, 0u, sizeof aui8_uart_tx);
    snprintf((char*) aui8_uart_tx, sizeof aui8_uart_tx, "%s%s%s%3d%s%3d%s", "|", aui8_rpd_norm, "| ", ui8_rpd_ref, " | ", NUM_OF_SCAN, " |\n");
    HAL_UART_Transmit(&huart2, (uint8_t*) aui8_uart_tx, sizeof aui8_uart_tx, 100u);
}

/**
 * @brief Step function of the SWC.
 * @author gemesa
 */
void rf_scanner_step(void)
{
    /* array to store the counted RPD flags for each channel
     * an RPD flag indicates whether the frequency is free or occupied */
    uint8_t aui8_rpd[NUM_OF_CH];
    memset(aui8_rpd, 0u, sizeof aui8_rpd);
    get_freq_data(aui8_rpd);
    plot_freq_data(aui8_rpd);
}

/**
 * @brief Init function of the SWC.
 * @author gemesa
 */
void rf_scanner_init(void)
{
    nrf24l01p_init();
}

/**
 * @brief Plots the frequency layout.
 * @author gemesa
 */
static void plot_layout(void)
{
    const uint8_t aui8_layout[] = "|------------------------------------------------------------------------------------------------------------------------------|-----|-----|\n"
            "|Frequency layout [GHz]                                                                                                        |Ref. |Max. |\n"
            "|2.4       2.41      2.42      2.43      2.44      2.45      2.46      2.47      2.48      2.49      2.5       2.51      2.52  |RPD  |RPD  |\n"
            "||         |         |         |         |         |         |         |         |         |         |         |         |     |[pcs]|[pcs]|\n"
            "|------------------------------------------------------------------------------------------------------------------------------|-----|-----|\n";

    HAL_UART_Transmit(&huart2, (uint8_t*) aui8_layout, sizeof aui8_layout, 100u);
}

/**
 * @brief Initializes the nrf24l01+ HW. Configures RX mode and POWER UP state.
 * @author gemesa
 * @details
 * datasheet chapter:
 *      - 6.1.1
 *      - 6.1.4
 *      - 6.1.7
 *      - 9.1
 */
static void nrf24l01p_init(void)
{
    /* switching off and on the PSU sets the default register values */

    const uint8_t REG_CONFIG = 0x00u;
    const uint8_t REG_EN_AA = 0x01u; /* auto acknowledgment */
    const uint16_t TPD2STBY = 1500u; /* [us] */
    uint8_t ui8_reg_val;

    /* read a register through SPI
     * reason: the first SPI operation is inefficient
     * cause: unknown
     * possible cause: there is an SS transition during initialization */
    get_reg(0x00u);

    /* disable AA because this functionality is unnecessary
     * disable on all data pipes for simplicity */
    set_reg(REG_EN_AA, 0x0u);

    /* enable RX mode */
    ui8_reg_val = get_reg(REG_CONFIG);
    set_reg(REG_CONFIG, ui8_reg_val | bit(0u)); /* PRIM_RX = BIT0 */

    /* power up
     * 1.5ms delay is necessary after powering up */
    ui8_reg_val = get_reg(REG_CONFIG);
    set_reg(REG_CONFIG, ui8_reg_val | bit(1u)); /* PWR_UP = BIT1 */
    delay_us(TPD2STBY);
}
