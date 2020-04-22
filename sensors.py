#!/usr/bin/python
import smbus
import time
import matplotlib.pyplot as plt
import numpy as np
from ctypes import c_short
from ctypes import c_byte
from ctypes import c_ubyte

class BH1750:
    def __init__(self, mode='ONE_TIME_HIGH_RES_MODE_1'):

        # Constants taken from the datasheet
        self.DEVICE     = 0x23 # Default device I2C address
        self.POWER_DOWN = 0x00 # No active state
        self.POWER_ON   = 0x01 # Power on
        self.RESET      = 0x07 # Reset data register value


        MODES           = {
        # Start measurement at 4 lx resolution. Time typically 16ms.
        'CONTINUOUS_LOW_RES_MODE': 0x13,         
        # Start measurement at 1 lx resolution. Time typically 120ms
        'CONTINUOUS_HIGH_RES_MODE_1':  0x10,     
        # Start measurement at 0.5 lx resolution. Time typically 120ms
        'CONTINUOUS_HIGH_RES_MODE_2': 0x11,         
        # Start measurement at 1 lx resolution. Time typically 120ms
        # Device is automatically set to Power Down after measurement.
        'ONE_TIME_HIGH_RES_MODE_1': 0x20,
        # Start measurement at 0.5 lx resolution. Time typically 120ms
        # Device is automatically set to Power Down after measurement.
        'ONE_TIME_HIGH_RES_MODE_2': 0x21,         
        # Start measurement at 1 lx resolution. Time typically 120ms
        # Device is automatically set to Power Down after measurement.
        'ONE_TIME_LOW_RES_MODE': 0x23
        }
       
        #bus = smbus.SMBus(0) # Rev 1 Pi uses 0
        self.bus = smbus.SMBus(1)  # Rev 2 Pi uses 1

        if not mode in MODES.keys():
            raise Exception('Please provide a measuring mode or leave empty (default is ONE_TIME_HIGH_RES_MODE_1. Possible are: {}'.format(MODES.keys()))

        self.mode_bit = MODES[mode]

    def lux(self):
      print(self.DEVICE)
      data = self.bus.read_i2c_block_data(self.DEVICE, self.mode_bit)
      # Simple function to convert 2 bytes of data
      # into a decimal number
      return ((data[1] + (256 * data[0])) / 1.2)

class BME280:
    def __init__(self):
        self.DEVICE = 0x76 # Default device I2C address
        self.REG_ID = 0xD0
        self.bus = smbus.SMBus(1) # Rev 2 Pi, Pi 2 & Pi 3 uses bus 1
                     # Rev 1 Pi uses bus 0
        # Register Addresses
        self.REG_DATA = 0xF7
        self.REG_CONTROL = 0xF4
        self.REG_CONFIG  = 0xF5
    
        # Oversample setting - page 27
        self.OVERSAMPLE_TEMP = 2
        self.OVERSAMPLE_PRES = 2
        self.MODE = 1

    def read_id(self):
        """
        Chip ID Register Address
        """
        (chip_id, chip_version) = bus.read_i2c_block_data(self.DEVICE, self.REG_ID, 2)
        return (chip_id, chip_version)
    
    def temp_and_pressure(self):

        def getShort(data, index):
            """
            return two bytes from data as a signed 16-bit value
            """
            return c_short((data[index+1] << 8) + data[index]).value
        
        def getUShort(data, index):
            """
            return two bytes from data as an unsigned 16-bit value
            """
            return (data[index+1] << 8) + data[index]
        
        def getChar(data,index):
            """
            return one byte from data as a signed char
            """
            result = data[index]
            if result > 127:
              result -= 256
            return result
        
        def getUChar(data,index):
            """
            return one byte from data as an unsigned char
            """
            result =  data[index] & 0xFF
            return result

        control = self.OVERSAMPLE_TEMP<<5 | self.OVERSAMPLE_PRES<<2 | self.MODE
        self.bus.write_byte_data(self.DEVICE, self.REG_CONTROL, control)
      
        # Read blocks of calibration data from EEPROM
        # See Page 22 data sheet
        cal1 = self.bus.read_i2c_block_data(self.DEVICE, 0x88, 24)
        cal2 = self.bus.read_i2c_block_data(self.DEVICE, 0xA1, 1)
        cal3 = self.bus.read_i2c_block_data(self.DEVICE, 0xE1, 7)
      
        # Convert byte data to word values
        dig_T1 = getUShort(cal1, 0)
        dig_T2 = getShort(cal1, 2)
        dig_T3 = getShort(cal1, 4)
      
        dig_P1 = getUShort(cal1, 6)
        dig_P2 = getShort(cal1, 8)
        dig_P3 = getShort(cal1, 10)
        dig_P4 = getShort(cal1, 12)
        dig_P5 = getShort(cal1, 14)
        dig_P6 = getShort(cal1, 16)
        dig_P7 = getShort(cal1, 18)
        dig_P8 = getShort(cal1, 20)
        dig_P9 = getShort(cal1, 22)
      
        # Wait in ms (Datasheet Appendix B: Measurement time and current calculation)
        wait_time = 1.25 + (2.3 * self.OVERSAMPLE_TEMP) + ((2.3 * self.OVERSAMPLE_PRES) + 0.575)
        time.sleep(wait_time/1000)  # Wait the required time  
      
        # Read temperature/pressure
        data = self.bus.read_i2c_block_data(self.DEVICE, self.REG_DATA, 8)
        pres_raw = (data[0] << 12) | (data[1] << 4) | (data[2] >> 4)
        temp_raw = (data[3] << 12) | (data[4] << 4) | (data[5] >> 4)
      
        #Refine temperature
        var1 = ((((temp_raw>>3)-(dig_T1<<1)))*(dig_T2)) >> 11
        var2 = (((((temp_raw>>4) - (dig_T1)) * ((temp_raw>>4) - (dig_T1))) >> 12) * (dig_T3)) >> 14
        t_fine = var1+var2
        temperature = float(((t_fine * 5) + 128) >> 8);
      
        # Refine pressure and adjust for temperature
        var1 = t_fine / 2.0 - 64000.0
        var2 = var1 * var1 * dig_P6 / 32768.0
        var2 = var2 + var1 * dig_P5 * 2.0
        var2 = var2 / 4.0 + dig_P4 * 65536.0
        var1 = (dig_P3 * var1 * var1 / 524288.0 + dig_P2 * var1) / 524288.0
        var1 = (1.0 + var1 / 32768.0) * dig_P1
        if var1 == 0:
          pressure=0
        else:
          pressure = 1048576.0 - pres_raw
          pressure = ((pressure - var2 / 4096.0) * 6250.0) / var1
          var1 = dig_P9 * pressure * pressure / 2147483648.0
          var2 = pressure * dig_P8 / 32768.0
          pressure = pressure + (var1 + var2 + dig_P7) / 16.0
      
        return temperature/100.0,pressure/100.0
      
