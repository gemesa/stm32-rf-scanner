# author: gemesa
# Python version: 3.8.2

# Copyright (c) 2024 András Gémes. All rights reserved.

# This software component is licensed by András Gémes under GNU GPLv3 license.
# You may obtain a copy of the license at: opensource.org/licenses/GPL-3.0

# SPDX-License-Identifier: gpl-3.0

import sys
import os
import shutil

from distutils.dir_util import copy_tree
from termcolor import colored
# colorama init is necessary for termcolor on Windows
from colorama import init


def delete_src(eclipse_path: str) -> None:
    """
    Delete obsolete C source files from the Eclipse project.
    Args:
        eclipse_path:

    Returns:

    """
    files_to_delete = ["src\\main.c",
                       "src\\Timer.c",
                       "system\\src\\cmsis\\system_stm32f1xx.c",
                       "system\\src\\cmsis\\vectors_stm32f1xx.c",
                       "include\\Timer.h",
                       "system\\src\\newlib\\_sbrk.c"]

    # colorama init is necessary for termcolor on Windows
    init()

    for file in files_to_delete:
        path = os.path.join(eclipse_path, file)
        if os.path.isfile(path):
            os.remove(path)
            print(f'{colored("delete", "red")} {path}')
        else:
            print(f'{colored("not found", "yellow")} {path}')

    print(f'\n--------------\n')


def copy_src(eclipse_path: str,
             cubemx_path: str) -> None:
    """
    Copy STM32CubeMX C source files to the Eclipse project.
    Args:
        eclipse_path:
        cubemx_path:

    Returns:

    """

    src_files = [["include", "Inc"], # application
                 ["src", "Src"],
                 ["system\include\stm32f1xx", "Drivers\STM32F1xx_HAL_Driver\Inc"], # HAL
                 ["system\src\stm32f1xx", "Drivers\STM32F1xx_HAL_Driver\Src"],
                 ["system\include\cmsis", "Drivers\CMSIS\Include"], # CMSIS
                 ["system\include\cmsis", "Drivers\CMSIS\Device\ST\STM32F1xx\Include"],
                 ["system\src\cmsis", "startup"],
                 ["src\Middlewares", "Middlewares"],] # FATFS etc.

    try:
        for path in src_files:
            eclipse_src_path = os.path.join(eclipse_path, path[0])
            cubemx_src_path = os.path.join(cubemx_path, path[1])
            copy_tree(cubemx_src_path, eclipse_src_path)
            print(f'{colored("copy", "green")} {cubemx_src_path}\n'
                  f'{colored("to  ", "green")} {eclipse_src_path}\n')
    except Exception as e:
        # Middlewares folder is generated only when you use FATFS, FREERTOS or USB_DEVICE
        print('No middleware has been configured.')
        print(f'{e}\n')

    print(f'--------------\n')

    # gen_doc is the input folder of doxygen
    gen_doc_path = os.path.join(eclipse_path, "src\gen_doc")
    if not os.path.isdir(gen_doc_path):
        os.mkdir(gen_doc_path)

    # update this with new files if necessary
    # TODO: implement for loop
    main_c_src = os.path.join(eclipse_path, "src\main.c")
    main_c_dest = os.path.join(eclipse_path, "src\gen_doc\main.c")
    print(f'{colored("move", "green")} {main_c_src}\n'
          f'{colored("to  ", "green")} {main_c_dest}\n')
    os.replace(main_c_src, main_c_dest)

    stm32f1xx_it_c_src = os.path.join(eclipse_path, "src\stm32f1xx_it.c")
    stm32f1xx_it_c_dest = os.path.join(eclipse_path, "src\gen_doc\stm32f1xx_it.c")
    print(f'{colored("move", "green")} {stm32f1xx_it_c_src}\n'
          f'{colored("to  ", "green")} {stm32f1xx_it_c_dest}\n')
    os.replace(stm32f1xx_it_c_src, stm32f1xx_it_c_dest)

    print(f'--------------\n')

    # rename *.s to *.S
    cmsis_src = os.path.join(eclipse_path, "system\src\cmsis\startup_stm32f103xb.s")
    cmsis_dest = os.path.join(eclipse_path, "system\src\cmsis\startup_stm32f103xb.S")
    print(f'{colored("rename", "green")} {cmsis_src}\n'
          f'{colored("to    ", "green")} {cmsis_dest}\n')
    os.rename(cmsis_src, cmsis_dest)

    print(f'--------------\n')


def mod_flash_address(eclipse_path: str) -> None:
    """
    Modify the starting flash address from 0x00000000 to 0x08000000.
    Args:
        eclipse_path:

    Returns:

    """
    path = os.path.join(eclipse_path, "ldscripts\\mem.ld")
    wrong_address = 'FLASH (rx) : ORIGIN = 0x00000000'
    correct_address = 'FLASH (rx) : ORIGIN = 0x08000000'
    with open(path, "r") as file:
        buf = file.read()
        if wrong_address in buf:
            print(f'{colored("replace", "green")} {wrong_address}\n'
                  f'{colored("with   ", "green")} {correct_address}\n')
            buf = buf.replace(wrong_address, correct_address)
        elif correct_address in buf:
            print(f'Flash address is correct (0x08000000). mem.ld has not been modified.\n')

    with open(path, "w") as file:
        file.write(buf)

    print('--------------\n')


def copy_doxyfile(eclipse_path: str,
                  doxyfile_path: str) -> None:
    """
    Copy the backup .doxyfile to the Eclipse project.
    Args:
        eclipse_path:
        doxyfile_path:

    Returns:

    """
    try:
        doxyfile_path_dest = os.path.join(eclipse_path, "stm32.Doxyfile")
        print(f'{colored("copy", "green")} {doxyfile_path}\n'
              f'{colored("to  ", "green")} {doxyfile_path_dest}\n')
        shutil.copyfile(doxyfile_path, doxyfile_path_dest)
    except Exception as e:
        print(f'{e}\n')

    print(f'--------------\n')


if __name__ == "__main__":

    if len(sys.argv) == 3:
        delete_src(sys.argv[1])
        copy_src(sys.argv[1], sys.argv[2])
        mod_flash_address(sys.argv[1])
    elif len(sys.argv) == 4:
        delete_src(sys.argv[1])
        copy_src(sys.argv[1], sys.argv[2])
        mod_flash_address(sys.argv[1])
        copy_doxyfile(sys.argv[1], sys.argv[3])
    else:
        print("Please specify the input files where <stm32doxyfile_path> is optional:\n"
              "python cubemx_importer.py <eclipse_project_path> <cubemx_project_path> [<stm32doxyfile_path>]")
        sys.exit(1)

    # postprocess instructions
    print(f'The generated source files have been overwritten. Manually added changes have been lost.\n'
          f'Format the code. (ctrl+shift+F).\n'
          f'Define the STM32F103xB macro in your Eclipse project (debug and release also).'
          f' This is required for building. \n'
          f'Add src folder in Middlewares to the include folders if necessary (debug and release also).'
          f' This is required for building.\n'
          f'Add -Wno-unused-parameter compiler option if necessary.'
          f' 0 warnings should be displayed with this option enabled while building the unmodified base configuration.')

