# author: gemesa
# Python version: 3.8.2

import sys
import os
import shutil

from distutils.dir_util import copy_tree


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

    for file in files_to_delete:
        path = os.path.join(eclipse_path, file)
        if os.path.isfile(path):
            os.remove(path)
            print(f'{path}\n'
                  f'deleted\n')
        else:
            print(f'{path}\n'
                  f'not found\n')
    print(f'--------------')


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
            print(f'Copy\n'
                  f'{cubemx_src_path}\n'
                  f'to\n'
                  f'{eclipse_src_path}\n')
    except Exception as e:
        # Middlewares folder is generated only when you use FATFS, FREERTOS or USB_DEVICE
        print(e)

    print(f'--------------')

    # gen_doc is the input folder of doxygen
    print(f'move generated files to the gen_doc folder\n')
    if not os.path.isdir(os.path.join(eclipse_path, "src\gen_doc")):
        os.mkdir(os.path.join(eclipse_path, "src\gen_doc"))

    # TODO: update this with new files if necessary
    os.replace(os.path.join(eclipse_path, "src\main.c"), os.path.join(eclipse_path, "src\gen_doc\main.c"))
    os.replace(os.path.join(eclipse_path, "src\stm32f1xx_it.c"), os.path.join(eclipse_path, "src\gen_doc\stm32f1xx_it.c"))

    print(f'--------------')

    # rename *.s to *.S
    cmsis_src_path_1 = os.path.join(eclipse_path, "system\src\cmsis\startup_stm32f103xb.s")
    cmsis_src_path_2 = os.path.join(eclipse_path, "system\src\cmsis\startup_stm32f103xb.S")
    os.rename(cmsis_src_path_1, cmsis_src_path_2)
    print(f'{cmsis_src_path_1}\n'
          f'has been renamed to\n'
          f'{cmsis_src_path_2}\n'
          f'--------------')


def mod_flash_address(eclipse_path: str) -> None:
    """
    Modify the starting flash address from 0x00000000 to 0x08000000.
    Args:
        eclipse_path:

    Returns:

    """
    path = os.path.join(eclipse_path, "ldscripts\\mem.ld")
    with open(path, "r") as file:
        buf = file.read()
        if "FLASH (rx) : ORIGIN = 0x00000000" in buf:
            print(f'Wrong flash address (0x00000000).')
            buf = buf.replace("FLASH (rx) : ORIGIN = 0x00000000",
                              "FLASH (rx) : ORIGIN = 0x08000000")
            print(f'Flash address has been replaced.\n'
                  f'--------------')
        elif "FLASH (rx) : ORIGIN = 0x08000000" in buf:
            print(f'Correct flash address (0x08000000).\n'
                  f'--------------')

    with open(path, "w") as file:
        file.write(buf)


def copy_doxyfile(eclipse_path: str,
                  doxyfile_path: str) -> None:
    """
    Copy the backup .doxyfile to the Eclipse project.
    Args:
        eclipse_path:
        doxyfile_path:

    Returns:

    """
    print(f'Copy {doxyfile_path}\n'
          f'to\n'
          f'{os.path.join(eclipse_path, "stm32.Doxyfile")}\n')
    try:
        shutil.copyfile(doxyfile_path, os.path.join(eclipse_path, "stm32.Doxyfile"))
    except Exception as e:
        print(e)

    print(f'--------------')


if __name__ == "__main__":

    try:
        eclipse_pj_path = sys.argv[1]
        cubemx_pj_path = sys.argv[2]
        stm32doxyfile_path = sys.argv[3]
    except IndexError:
        print("Please specify the input files:\n"
              "python cubemx_importer.py <eclipse_project_path> <cubemx_project_path> <stm32doxyfile_path>")
        sys.exit(1)

    print(f'cubemximporter is running...\n'
          f'--------------')

    delete_src(eclipse_pj_path)
    copy_src(eclipse_pj_path, cubemx_pj_path)
    copy_doxyfile(eclipse_pj_path, stm32doxyfile_path)
    mod_flash_address(eclipse_pj_path)

    # postprocess instructions
    print(f'The generated source files have been overwritten. Manually added changes have been lost.\n'
          f'Please format the code. (ctrl+shift+F).\n'
          f'Please define the STM32F103xB macro in your Eclipse project (debug and release also).'
          f' This is required for building. \n'
          f'Add src folder in Middlewares to the include folders if necessary (debug and release also).'
          f' This is required for building.\n'
          f'Add -Wno-unused-parameter compiler option if necessary.'
          f' 0 warnings should be displayed with this option enabled while building the unmodified base configuration.')

