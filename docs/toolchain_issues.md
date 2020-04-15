# Toolchain issues

This document collects solutions for some issues which are not detailed in [Mastering STM32](https://leanpub.com/mastering-stm32) and might be encountered during the use of the Eclipse toolchain.

## Issue 1

GCC ARM is not recognized while creating an STM32 C project (`Finish` button is gray) even when it is properly added to PATH.
The `C/C++->Build->Global Tools Paths` can be set in the `Window->Preferences` also, for example:
- build tools folder: `\msys64\usr\bin`
- toolchain folder: `\gcc-arm\bin`

### Solution 1:

Start creating an STM32 C project with an other template (STM32F2xx instead of STM32F10x for example) but do not click `Finish`. Go back and select the desired template and create a project.

### Solution 2:

Create an STM32 C project by selecting an other toolchain. Delete this project and create a new one with the GCC ARM toolchain.

### Solution 3:

Try creating the project with an other name.

## Issue 2

Building the project raises the following error:

```
make: /bin/sh: No such file or directory
```

### Solution 1:

Use `make` from Cygwin instead of msys64. Update build tools folder: `\msys64\usr\bin` --> `\cygwin64\bin`

