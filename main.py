#!/bin/env python
# -*- coding: cp1252 -*-
# ==========================================================================

# ==========================================================================
# IMPORTS
# ==========================================================================
from hw_interface import *

# ==========================================================================
# GLOBALS
# ==========================================================================
handle = hw_interface(config.DEVICE_I2C_ADDR, config.HW_INTERFACE)


# ==========================================================================
# main
# ==========================================================================

def i2c_demo_test():
    handle.hw_open(config.HW_INTERFACE, config.PORT, config.SPI_PORT, config.BITRATE, config.SPIBITRATE,
                   config.DEVICE_I2C_ADDR)
    print("-----------")
    from array import array, ArrayType

    dev_addr = 0x31
    handle.hw_set_i2c_addr(dev_addr)

    register = 0x38
    i2c_wt = array('B', [register & 0xff])
    # i2c_wt = array('B', [0, 1, 2, 3, 4, 5, 6, 7])
    handle.hw_i2c_write(i2c_wt)
    hw_sleep_ms(10)
    # handle.hw_i2c_write_no_stop(array('B', [register & 0xff]))
    # hw_sleep_ms(10)

    length = 8
    (count, data_in) = handle.hw_i2c_read(length)
    print(count, data_in)

    handle.hw_close()


def spi_demo_test():
    from array import array, ArrayType
    try:
        handle.hw_open(config.HW_INTERFACE, config.PORT, config.SPI_PORT, config.BITRATE, config.SPIBITRATE,
                       config.DEVICE_I2C_ADDR)
    except Exception as e:
        print(e.args)
        sys.exit()

    # erase 1M flash
    # 1M / 4K = 255
    for i in range(255):
        handle.hw_spi_flash_erase(i * 0x1000, 1)

    addr = 0x0
    filedata = array('B', [])
    handle.hw_spi_write(addr, filedata)

    # Truncate the array to the exact data size
    length = 10
    if length < SPI_PAGE_SIZE:
        del filedata[length:]

    # read the data from the bus
    (count, readcomp) = handle.hw_spi_read(addr, len(filedata))
    print(count, readcomp)

    handle.hw_close()


def gpio_demo_test(port):
    import time
    try:
        handle.hw_open(config.HW_INTERFACE, config.PORT, config.SPI_PORT, config.BITRATE, config.SPIBITRATE,
                       config.DEVICE_I2C_ADDR)
    except Exception as e:
        print(e.args)
        sys.exit()

    for i in range(10):
        pins_h = "11111111"
        handle.hw_gpio_write(port, 255, int(pins_h, 2))
        ret_read = handle.hw_gpio_read(port, 1)
        print("read:", bin(ret_read))
        time.sleep(0.5)
        pins_l = "00000000"
        handle.hw_gpio_write(port, 255, int(pins_l, 2))
        ret_read = handle.hw_gpio_read(port, 1)
        print("read:", bin(ret_read))
        time.sleep(0.5)

    handle.hw_close()


def get_gpio(self, line):
    """Retrieve the level of a GPIO input pin

       :param line: specify which GPIO to read out.
       :return: True for high-level, False for low-level
    """
    value = self._gpio.read_port()
    print(value)
    return bool(value & (1 << line))


def set_gpio(self, line, on):
    """Set the level of a GPIO ouput pin.

       :param line: specify which GPIO to madify.
       :param on: a boolean value, True for high-level, False for low-level
    """
    if on:
        state = self._state | (1 << line)
    else:
        state = self._state & ~(1 << line)
    self._commit_state(state)


#########################################
# FT2232HL hw define
#########################################
# AD0 -16-- SPI-CLK
# AD1 -17-- SPI-MOSI
# AD2 -18-- SPI-MISO
# AD3 -19-- SPI-SS
# AD4 -21-- GPIO-A0
# AD5 -22-- GPIO-A1
# AD6 -23-- GPIO-A2
# AD7 -24-- GPIO-A3
#########################################
# BD0 -26-- I2C-SCL
# BD1 -27-- I2C-SDA--|   BD1 must short with BD2
# BD2 -28-- I2C-SDA--|
# BD3 -29-- NC
# BD4 -30-- GPIO-B0
# BD5 -32-- GPIO-B1
# BD6 -33-- GPIO-B2
# BD7 -34-- GPIO-B3
#########################################
##open ocd## JTAG #######################
# BD0 -26-- TCK|SWD-CLK
# BD1 -27-- TDI
# BD2 -28-- TDO|SWO
# BD3 -29-- TMS|SWD-IO
# BD4 -30-- \TRST
# BD5 -32-- DBGRQ
# BD6 -33-- \RST
# BD7 -34-- RTCK
#########################################
# FT232R  features 1 single port, which is 8-bit wide: DBUS,
# FT232H  features 1 single port, which is 16-bit wide: ADBUS/ACBUS,
# FT2232D features 2 ports, which are 12-bit wide each: ADBUS/ACBUS and BDBUS/BCBUS,
# FT2232H features 2 ports, which are 16-bit wide each: ADBUS/ACBUS and BDBUS/BCBUS,
# FT4232H features 4 ports, which are 8-bit wide each: ADBUS, BDBUS, CDBUS and DDBUS,
# FT230X  features 1 single port, which is 4-bit wide,
# FT231X  feature  1 single port, which is 8-bit wide


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1][:2] == '0x':
            address = int(sys.argv[1], 16)
            config.DEVICE_I2C_ADDR = address
        else:
            address = int(sys.argv[1])
            config.DEVICE_I2C_ADDR = address
    try:
        gpio_demo_test("PORT-A")
        gpio_demo_test("PORT-B")
        # gpio_demo_test("PORT-C")

        i2c_demo_test()
        spi_demo_test()
    except Exception as e:
        print(e)
        sys.exit()
    sys.exit()
