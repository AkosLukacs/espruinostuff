#!/bin/false
# This file is part of Espruino, a JavaScript interpreter for Microcontrollers
#
# Copyright (C) 2013 Gordon Williams <gw@pur3.co.uk>
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# ----------------------------------------------------------------------------------------
# This file contains information for a specific board - the available pins, and where LEDs,
# Buttons, and other in-built peripherals are. It is used to build documentation as well
# as various source and header files for Espruino.
# ----------------------------------------------------------------------------------------

# # Board file for EBYTE's E73-TRM-01 based on the MDBT42Q.
# # There is no bootloader or anything, you need an SWD programmer to program it.
#
# # BUILD it:
# > make clean && BOARD=E73TRM01 RELEASE=1 BOOTLOADER=1 make
# > make clean && BOARD=E73TRM01 RELEASE=1 make
# 
# # unlock flash in case it's locked:
# > nrfjprog --recover
# # and flash it with an SWD programmer...

# Found this in a pastebin:
# Can't find EBYTE test board E73-TRM-01 V1.0 schematic, so figured out connections by myself:
#  
#  | NRF52832 | E73-2G4M04S1B |   Connected to  |
#  | -------- | ------------- | --------------- |
#  |   P0.05  |       21      | CH340G CTS      |
#  |   P0.06  |       22      | CH340G RX       |
#  |   P0.07  |       23      | CH340G RTS      |
#  |   P0.08  |       24      | CH340G TX       |
#  |   P0.13  |       29      | SW2 (act. low)  |
#  |   P0.14  |       30      | SW1 (act. low)  |
#  |   P0.17  |       33      | LED1 (act. low) |
#  |   P0.18  |       34      | LED2 (act. low) |
#  

import pinutils;

info = {
 'name' : "E73-TRM-01",
 'link' :  [ "http://ebyte.com/en/product-view-news.aspx?id=243" ],
 'espruino_page_link' : '',
 'default_console' : "EV_SERIAL1",
 'default_console_tx' : "D6",
 'default_console_rx' : "D8",
 'default_console_baudrate' : "9600",
 'variables' : 2500, # How many variables are allocated for Espruino to use. RAM will be overflowed if this number is too high and code won't compile.
 'bootloader' : 1,
 'binary_name' : 'espruino_%v_e73trm01.hex',
 'build' : {
   'optimizeflags' : '-Os',
   'libraries' : [
     'BLUETOOTH',
     'NET',
     'GRAPHICS',
     'CRYPTO','SHA256','SHA512',
     'AES',
     'NFC',
     'NEOPIXEL',
     'FILESYSTEM'
     #'TLS'
   ],
   'makefile' : [
     'DEFINES+=-DHAL_NFC_ENGINEERING_BC_FTPAN_WORKAROUND=1', # Looks like proper production nRF52s had this issue
     'DEFINES+=-DCONFIG_GPIO_AS_PINRESET', # Allow the reset pin to work
     'DEFINES+=-DBLUETOOTH_NAME_PREFIX=\'"E73-TRM-01"\'',
     'DFU_PRIVATE_KEY=targets/nrf5x_dfu/dfu_private_key.pem',
     'DFU_SETTINGS=--application-version 0xff --hw-version 52 --sd-req 0x8C'
   ]
 }
};

chip = {
  'part' : "NRF52832",
  'family' : "NRF52",
  'package' : "QFN48",
  'ram' : 64,
  'flash' : 512,
  'speed' : 64,
  'usart' : 1,
  'spi' : 1,
  'i2c' : 1,
  'adc' : 1,
  'dac' : 0,
  'saved_code' : {
    'address' : ((118 - 10) * 4096), # Bootloader takes pages 120-127, FS takes 118-119
    'page_size' : 4096,
    'pages' : 10,
    'flash_available' : 512 - ((31 + 8 + 2 + 10)*4) # Softdevice uses 31 pages of flash, bootloader 8, FS 2, code 10. Each page is 4 kb.
  },
};

devices = {
  'LED1' : { 'pin' : 'D17' },
  'LED2' : { 'pin' : 'D18', 'no_bootloader':True }, # don't use LED2 in the bootloader since we may be using a bare module
  'BTN1' : { 'pin' : 'D14', 'pinstate' : 'IN_PULLDOWN' },
  'BTN2' : { 'pin' : 'D13', 'pinstate' : 'IN_PULLDOWN' },
  'NFC': { 'pin_a':'D9', 'pin_b':'D10' },
  # Pin D22 is used for clock when driving neopixels - as not specifying a pin seems to break things
};

# left-right, or top-bottom order
board_module = {
  'left' : [ 'GND','','','','D25','D26','D27','D28','D29','D30','D31','DEC4','DCC','VDD'],
  'right2' : [ 'D24', '', 'D23'],
  'right' : [ 'GND','D22','SWDIO','SWDCLK','D21','D20','D19','D18','D17','D16','D15','D14','D13','D12','D11' ],
  'bottom' : [ 'GND','D0','D1','D2','D3','D4','D5','D6','D7','D8','D9','D10','GND' ],
  '_notes' : {
    'D21' : "Also NRST if configured",
    'D22' : "This is used as SCK when driving Neopixels with 'require('neopixel').write'. If not driving neopixels this behaves like any other pin.",
  }
};

board_module["_css"] = """
#board {
  width: 359px;
  height: 484px;
  top: 0px;
  left : 200px;
  background-image: url(img/MDBT42Q.jpg);
}
#boardcontainer {
  height: 650px;
}
#board #bottom {
    top: 440px;
    left: 56px;
}
#board #left {
    top: 115px;
    right: 316px;
}
#board #right2 {
    top: 115px;
    right: 110px;
}
#board #right {
    top: 115px;
    left: 316px;
}

#board .leftpin { height: 17px; }
#board .left2pin { height: 17px; }
#board .rightpin { height: 17px; }
#board .bottompin { width: 15px; padding:0px; }
""";

board_breakout = {
  'left' : [ 'D25','D26','D27','D28','D29','D30','D31','D3','D4','D5','D11' ],
  'right' : [ 'D22','D20','D19','D18','D17','D16','D15','D14','3.3','Vin','GND'],
  'bottom' : [ 'D6','D8','D7','Vin','GND' ],
  'top' : [ 'D9','D10' ],
  '_hide_not_on_connectors' : True,
  '_class' : "board_breakout",
  '_notes' : {
    'D8' : "Serial Console RX when Bluetooth disconnected",
    'D6' : "Serial Console TX when Bluetooth disconnected",
  }
};

board_breakout["_css"] = """
#board {
  width: 255px;
  height: 400px;
  top: 0px;
  left : 200px;
  background-image: url(img/MDBT42Q_BREAKOUT.png);
}
#boardcontainer {
  height: 600px;
}
#board #bottom {
    top: 410px;
    left: 40px;
}
#board #top {
    bottom: 75px;
    left: 167px;
}
#board #left {
    top: 17px;
    right: 256px;
}
#board #right {
    top: 17px;
    left: 256px;
}

#board .leftpin { height: 33px; }
#board .rightpin { height: 33px; }
#board .toppin { width: 15px; padding:0px; }
#board .bottompin { width: 31px; padding:0px; }
""";

boards = [board_module, board_breakout];


def get_pins():
  pins = pinutils.generate_pins(0,31) # 32 General Purpose I/O Pins.
  pinutils.findpin(pins, "PD0", True)["functions"]["XL1"]=0;
  pinutils.findpin(pins, "PD1", True)["functions"]["XL2"]=0;
  pinutils.findpin(pins, "PD9", True)["functions"]["NFC1"]=0;
  pinutils.findpin(pins, "PD10", True)["functions"]["NFC2"]=0;
  pinutils.findpin(pins, "PD2", True)["functions"]["ADC1_IN0"]=0;
  pinutils.findpin(pins, "PD3", True)["functions"]["ADC1_IN1"]=0;
  pinutils.findpin(pins, "PD4", True)["functions"]["ADC1_IN2"]=0;
  pinutils.findpin(pins, "PD5", True)["functions"]["ADC1_IN3"]=0;
  pinutils.findpin(pins, "PD28", True)["functions"]["ADC1_IN4"]=0;
  pinutils.findpin(pins, "PD6", True)["functions"]["USART1_TX"]=0;
  pinutils.findpin(pins, "PD8", True)["functions"]["USART1_RX"]=0;
  pinutils.findpin(pins, "PD29", True)["functions"]["ADC1_IN5"]=0;
  pinutils.findpin(pins, "PD30", True)["functions"]["ADC1_IN6"]=0;
  pinutils.findpin(pins, "PD31", True)["functions"]["ADC1_IN7"]=0;

  pinutils.findpin(pins, "PD13", True)["functions"]["NEGATED"]=0;
  pinutils.findpin(pins, "PD14", True)["functions"]["NEGATED"]=0;
  pinutils.findpin(pins, "PD17", True)["functions"]["NEGATED"]=0;
  pinutils.findpin(pins, "PD18", True)["functions"]["NEGATED"]=0;
  # everything is non-5v tolerant
  for pin in pins:
    pin["functions"]["3.3"]=0;

  #The boot/reset button will function as a reset button in normal operation. Pin reset on PD21 needs to be enabled on the nRF52832 device for this to work.
  return pins
