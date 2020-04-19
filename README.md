# 2.4GHz RF scanner

This project contains the source code of an nRF24L01+ and Blue Pill (STM32F103C8T6) based RF scanner. The Blue Pill scans frequencies from 2.400GHz to 2.525GHz (1MHz resolution) with nRF24L01+ and plots the activity on each frequency through UART.

This is what the UART output looks like (explained below):

    |------------------------------------------------------------------------------------------------------|-----|-----|
    |Frequency layout [GHz]                                                                                |Ref. |Max. |
    |2.4       2.41      2.42      2.43      2.44      2.45      2.46      2.47      2.48      2.49..2.52  |RPD  |RPD  |
    ||         |         |         |         |         |         |         |         |         |     |     |[pcs]|[pcs]|
    |------------------------------------------------------------------------------------------------------|-----|-----|
    |   :-.               ::  ::..%%@%@#%@@@%%%%#@@@                              .-: ::                   |  10 | 180 |
    |.  ....                 .. . @@#%@@#%@@@%%%%#@@                              ::     .                 |  10 | 180 |
    |   ....                ...  .%@#%%%%%%%####%##%                            ..  ..:.                   |  16 | 180 |
    |                     ..  ...:##***###%@%%@@@%#@                            .:::                       |  11 | 180 |
    | ....                ...:... %%%%@%%%%%#***%#%%                                                       |  16 | 180 |
    |:.    .              : .:. ..-###%%@###%##%##=:                              ...:.  :                 |  11 | 180 |
    |..  ..                .:....: %%%%%%%%%%%@@%%#                             ::...                      |  12 | 180 |
    |.... ...               ..   ..@%%@@%%%@%%%%%%%                                 ..  ..                 |  18 | 180 |
    |                     .  .::.  @%#%%%#########*                             .                          |  11 | 180 |
    |..  ..                      ::%%%%@%%%%@%%@@@%                                  .:..:                 |  12 | 180 |
    |..::::                ..    . @#**#%***##*#%##                             ..   .-:.                  |  10 | 180 |
    | ... ..                 ...   @%%%%@%%@%%##%%*                              .. ...  .                 |  13 | 180 |
    |   .. .                 ..   :*%*%%%%%@%%%%@@%                             ....... ..                 |  14 | 180 |
    |..                    ....   .-:::--::------::              .+@@@*           .......                  |  57 | 180 |
    |...                    .. ....::.:............             -#@@@#.         .       ..                 |  72 | 180 |
    |  ..  .              ..  ..   ................             :*@@@#     ...  ..                         |  73 | 180 |
    |                      ..  ....:...............             -+@@@#           ..                        |  73 | 180 |
    |  ......             ...    ..................            .##@@%#          .....   ..                 |  74 | 180 |
    |   ....                .......:...............             #@@%%=            ..    ..                 |  75 | 180 |
    |. ...                 . ....  ::::::::::::::::             *#@@%*                                     |  38 | 180 |
    |:....                ..     ..@#**##**%**+****                               ... ...                  |  14 | 180 |
    |...   .                  ...  %**%%%%@%%##%#*#                              ..    ..                  |  16 | 180 |
    |      .               ..  ....##*#%###*%%#%@##                                 .....:                 |  14 | 180 |

    Unknown sig.       Unknown sig. Wi-Fi (WLAN 6)          Microwave oven     Unknown sig.

The axes:

            f[GHz]
        ------------->
        |
     t  |
    [s] |
        |
        V

The time difference between each line is ~4s. The greyscale characters represent the signal strengths relative to each other. The signal classification have been added manually.

A similar, Arduino libraries based design by **cpixip** can be found at [forum.arduino.cc](https://forum.arduino.cc/index.php?topic=54795.0). The code of this project has been implemented using

- Eclipse,
- STM32Fx project templates,
- STM32CubeMX,
- STM32 HAL.

A detailed description can be found in [docs/project_description.md](docs/project_description.md).

## Deployment

Quick deployment process:
- Build the SW from command line with `make` and `arm-none-eabi-gcc`:

```
cd <path>\2-4ghz-rf-scanner\src\Debug
make all
```

- Connect the configured pins (SWD, SPI and UART). Refer to [docs/project_description.md#pin-description](docs/project_description.md#pin-description).
- Download the binary to the Blue Pill with STM32CubeProgrammer.
- Run the SW and plot the UART output using an USB-UART adapter and a serial port terminal.

Note: The SW can be built from Eclipse also. `.project` is stored in [src](src).

## Results

Measurement results are stored in the [meas](meas) folder.

## License

This project contains files from multiple sources with different licenses. The relevant license is added to every source file.

The configuration files generated by Eclipse using the ARM Cortex-M C/C++ Project template are licensed (depending on the file) by:
- Arm Limited under Apache license 2.0 (Copyright (c) 2009-2018 Arm Limited. All rights reserved.)
- Liviu Ionescu under MIT license (Copyright (c) 2014 Liviu Ionescu)

The configuration files generated by STM32CubeMX are licensed by:
- ST under BSD 3-Clause license (Copyright (c) 2020 STMicroelectronics. All rights reserved.)

The files implementing the logic of the scanner functionality are licensed by:
- András Gémes under GNU GPLv3 license (Copyright (c) 2020 András Gémes. All rights reserved.)
