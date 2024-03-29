# Project description

This document contains the detailed project description.

## Prerequisites

The prerequisites and the toolchain are detailed in [Mastering STM32](https://leanpub.com/mastering-stm32) written by **Carmine Noviello**.

### Mandatory tools:
- [Eclipse](https://www.eclipse.org/)
  - [C/C++ Development Tools SDK](https://marketplace.eclipse.org/content/eclipse-embedded-cc)
  - [GNU ARM Eclipse Plug-ins](https://marketplace.eclipse.org/content/eclipse-embedded-cc)
- [GCC ARM](https://developer.arm.com/Tools%20and%20Software/GNU%20Toolchain)
- [make](https://www.gnu.org/software/make/)
- [STM32CubeMX](https://www.st.com/en/development-tools/stm32cubemx.html)
- [STM32CubeProgrammer](https://www.st.com/en/development-tools/stm32cubeprog.html)

Note: [Flash loader demonstrator](https://www.st.com/en/development-tools/flasher-stm32.html) can also be used for downloading but it is outdated.

The version numbers are stored in [docs/toolchain_versions.md](https://github.com/gemesa/2-4ghz-rf-scanner/blob/master/docs/toolchain_versions.md). Some issues which are not detailed in [Mastering STM32](https://leanpub.com/mastering-stm32) and might be encountered during the use of the toolchain are detailed in [docs/toolchain_issues.md](https://github.com/gemesa/2-4ghz-rf-scanner/blob/master/docs/toolchain_issues.md).

### Optional tools:
- [OpenOCD](https://openocd.org/) + [GDB ARM](https://developer.arm.com/Tools%20and%20Software/GNU%20Toolchain)
- [STSW-LINK007](https://www.st.com/en/development-tools/stsw-link007.html)
- [tools/cubemx_importer.py](https://github.com/gemesa/2-4ghz-rf-scanner/blob/master/tools/cubemx_importer.py)
- [Eclox doxygen plug-in](https://marketplace.eclipse.org/content/eclox)
- [Hercules](https://www.hw-group.com/software/hercules-setup-utility) (serial port terminal)

Note: STSW-LINK007 is used to upgrade the firmware of the ST-LINK for OpenOCD if necessary.

### Mandatory HWs:
- [Blue Pill](https://stm32-base.org/boards/STM32F103C8T6-Blue-Pill.html)
- [nRF24L01+](https://www.sparkfun.com/datasheets/Components/SMD/nRF24L01Pluss_Preliminary_Product_Specification_v1_0.pdf)
- [USB-UART adapter](https://ftdichip.com/products/ft232rl/)

### Optional HWs:
- [ST-LINK/V2](https://www.st.com/en/development-tools/st-link-v2.html)

Note: flash can be accessed without SWD using other interfaces. Refer to [www.st.com](https://www.st.com/en/development-tools/stm32cubeprog.html) for more information.

## STM32CubeMX

The basic configuration is generated with STM32CubeMX. The following peripherals are configured:
- UART - USB-UART adapter <-- Blue Pill
- SPI  - Blue Pill <--> nRF24L01+
- TIM  - required for delay function
- GPIO - required for CE, SS and LED pins
- SYS  - SWD is required for ST-LINK/V2 flashing and debugging

A basic 72MHz SYSCLK is configured currently.

The UART parameters:
- baud rate: 		115200bits/s
- word length: 		8 bits (including parity)
- parity: 			none
- stop bits: 		1

The `blue_pill_config.ioc` project file contains the necessary configuration. The CubemX project is stored in [config/cubemx](https://github.com/gemesa/2-4ghz-rf-scanner/tree/master/config/cubemx).

## Eclipse

An STM32F1xx C project has been created using the ARM Cortex-M C/C++ Project template (with the proper memory sizes and CMSIS). The files generated by CubeMX are copied to the proper folders of the Eclipse project by running [tools/cubemx_importer.py](https://github.com/gemesa/2-4ghz-rf-scanner/blob/master/tools/cubemx_importer.py):

```
python cubemx_importer.py <eclipse_project_path> <cubemx_project_path> [<stm32doxyfile_path>]
```

The STM32F103xB macro is defined for building. Optimization level is set to -O3. The manually implemented code is polling based and is added directly to the main function.

Includes:
```c
#include "util.h"
#include "rf_scanner.h"
```

Init functions:
```c
util_init();
rf_scanner_init();
```

Step functions:
```c
rf_scanner_step();
blink_led();
```

## Building

The project can be built in the Eclipse GUI or from command line:

```
cd <path>\stm32-rf-scanner\src\Debug
make all
```

## Pin description

CE and SPI connections:

| pin   | Blue Pill | nRF24L01+ |
|:-----:|:---------:|:---------:|
| CE    | PB1       | 3         |
| SS    | PB0       | 4         |
| SCK   | PA5       | 5         |
| MOSI  | PA7       | 6         |
| MISO  | PA6       | 7         |

UART and SWD pins:

| pin   | Blue Pill |
|:-----:|:---------:|
| TX    | PA2       |
| SWDIO | PA13      |
| SWCLK | PA14      |

The ST-LINK/V2 has to be connected to the SWD interface. Both HWs require 3.3V and common ground. The UART logic level is 3.3V also, so the USB-UART adapter has to be configured this way. Most of them has a jumper for this purpose.

## Downloading

The binary file can be downloaded using STM32CubeProgrammer or OpenOCD and GDB ARM.

STM32CubeProgrammer:
- Both the `.elf` and `.hex` files can be selected for downloading.

OpenOCD and GDB ARM:
- OpenOCD has to be configured as an external tool in Eclipse and a debug configuration has to be also created.
- Only the `.elf` file can be used for downloading because the symbols are required for debugging.

## Measurement

The measured data is sent out via UART and can be observed with an USB-UART adapter.

Measurement results are stored in the [meas](https://github.com/gemesa/2-4ghz-rf-scanner/tree/master/meas) folder.