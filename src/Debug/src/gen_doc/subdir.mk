################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../src/gen_doc/main.c \
../src/gen_doc/rf_scanner.c \
../src/gen_doc/stm32f1xx_it.c \
../src/gen_doc/util.c 

OBJS += \
./src/gen_doc/main.o \
./src/gen_doc/rf_scanner.o \
./src/gen_doc/stm32f1xx_it.o \
./src/gen_doc/util.o 

C_DEPS += \
./src/gen_doc/main.d \
./src/gen_doc/rf_scanner.d \
./src/gen_doc/stm32f1xx_it.d \
./src/gen_doc/util.d 


# Each subdirectory must supply rules for building sources it contributes
src/gen_doc/%.o: ../src/gen_doc/%.c
	@echo 'Building file: $<'
	@echo 'Invoking: Cross ARM GNU C Compiler'
	arm-none-eabi-gcc -mcpu=cortex-m3 -mthumb -O3 -fmessage-length=0 -fsigned-char -ffunction-sections -fdata-sections -ffreestanding -fno-move-loop-invariants -Wall -Wextra  -g3 -DDEBUG -DSTM32F103xB -DTRACE -I"../include" -I"../system/include" -I"../system/include/cmsis" -I"../system/include/stm32f1xx" -std=gnu11 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@)" -c -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


