/**
 ******************************************************************************
 * @file wifi_scanner.h
 * @brief Scans the 2.4..2.5GHz band with nrf24l01+
 * and plots the free and occupied frequencies through UART.
 * @author gemesa
 * @details  The SWC bypasses RTE and is directly connected to the HAL (SPI),
 * this results a complex driver architecture.
 ******************************************************************************
 */

#ifndef GEN_DOC_WIFI_SCANNER_H_
#define GEN_DOC_WIFI_SCANNER_H_

extern void wifi_scanner_init(void);
extern void wifi_scanner_step(void);

#endif /* GEN_DOC_WIFI_SCANNER_H_ */
