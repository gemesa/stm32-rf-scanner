# Wi-Fi scanner

This project contains the source code of an nRF24L01+ and Blue Pill (STM32F103C8T6) based Wi-Fi scanner.
A similar, Arduino libraries based design by **cpixip** can be found at [forum.arduino.cc](https://forum.arduino.cc/index.php?topic=54795.0). The code of this project has been implemented using

- Eclipse,
- STM32Fx project templates,
- STM32CubeMX,
- STM32 HAL.

A detailed description can be found in [docs/project_description.md](docs/project_description.md).

## Prerequisites

The prerequisites and the toolchain are detailed in [Mastering STM32](https://leanpub.com/mastering-stm32) written by **Carmine Noviello**.

### Mandatory tools:
- Eclipse
  - C/C++ Development Tools SDK
  - GNU ARM Eclipse Plug-ins
- GCC ARM
- make
- STM32CubeMX
- STM32CubeProgrammer

Note: Flash loader demonstrator can also be used for downloading but it is outdated.

The version numbers are stored in [docs/toolchain_versions.md](docs/toolchain_versions.md). Some issues which are not detailed in [Mastering STM32](https://leanpub.com/mastering-stm32) and might be encountered during the use of the toolchain are detailed in [docs/toolchain_issues.md](docs/toolchain_issues.md).

### Optional tools:
- OpenOCD + GDB ARM
- STSW-LINK007
- [tools/cubemx_importer.py](tools/cubemx_importer.py)
- Eclox doxygen plug-in
- Hercules (serial port terminal)

Note: STSW-LINK007 is used to upgrade the firmware of the ST-LINK for OpenOCD if necessary.

### Mandatory HWs:
- Blue Pill
- nRF24L01+
- ST-LINK/V2
- USB-UART adapter

Note: flash can be accessed without SWD using other interfaces. Refer to [www.st.com](https://www.st.com/en/development-tools/stm32cubeprog.html) for more information.

## Results

Measurement results can be found in the [meas](meas) folder.

## Deployment

Build the SW using Eclipse and GCC ARM. Download the binary with STM32CubeProgrammer or OpenOCD and GDB ARM.

## License

Under construction.

## SW architecture

The aim is to follow the AUTOSAR standards.
