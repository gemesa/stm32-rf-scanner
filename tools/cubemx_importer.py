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


def copy_doxyfile(eclipse_path: str) -> None:
    """
    Copy the backup .doxyfile to the Eclipse project.
    Args:
        eclipse_path:

    Returns:

    """
    doxyfile_path = "F:\STM32\stm32.Doxyfile"
    print(f'Copy {doxyfile_path}\n'
          f'to\n'
          f'{os.path.join(eclipse_path, "stm32.Doxyfile")}\n'
          f'--------------\n')
    shutil.copyfile(doxyfile_path, os.path.join(eclipse_path, "stm32.Doxyfile"))


if __name__ == "__main__":
    print(f'cubemximporter is running...\n'
          f'--------------')

    delete_src(sys.argv[1])
    copy_src(sys.argv[1], sys.argv[2])
    copy_doxyfile(sys.argv[1])
    mod_flash_address(sys.argv[1])

    print(f'format the code! (ctrl+shift+F)')
    # print(f'merge the code of stm32_notes.txt and main.c!') # TODO: script this
    print(f'define the STM32F103xB macro in your Eclipse project! (debug and release also)')
    print(f'Add src folder in Middlewares to the include folders! (debug and release also)')

