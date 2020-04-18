/**
 ******************************************************************************
 * @file rf_scanner.h
 * @brief Scans frequencies from 2.400GHz to 2.525GHz (1MHz resolution)
 * with nRF24L01+ and plots the activity on each frequency through UART.
 * @author gemesa
 *
 * @attention
 *
 * Copyright (c) 2020 András Gémes. All rights reserved.
 *
 * This software component is licensed by András Gémes under GNU GPLv3 license.
 * You may obtain a copy of the license at: opensource.org/licenses/GPL-3.0
 *
 * SPDX-License-Identifier: gpl-3.0
 ******************************************************************************
 */

#ifndef GEN_DOC_RF_SCANNER_H_
#define GEN_DOC_RF_SCANNER_H_

extern void rf_scanner_init(void);
extern void rf_scanner_step(void);

#endif /* GEN_DOC_RF_SCANNER_H_ */
