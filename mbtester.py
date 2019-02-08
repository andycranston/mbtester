#
# @(!--#) @(#) mbtester.py, version 011, 08-february-2019
#
# drive the "Generic Modbus/Jbus Tester" windows program
# from Schneider Electric
#
# tester.exe available from:
#
#    https://www.schneider-electric.com/en/faqs/FA180037/
#
# version 4.7 (c) 1998-2008
#
# Links:
#
#    https://pyautogui.readthedocs.io/en/latest/
#    
#

#########################################################################

import sys
import os
import time
import datetime
import argparse
import pyautogui

#########################################################################

#
# constants
#

WINDOW_SIZE_X = 590
WINDOW_SIZE_Y = 417

MB_ICON_BITMAP_FILE_NAME = 'mbicon.bmp'
MB_ICON_PADDING_X        = 4
MB_ICON_PADDING_Y        = 5
TOP_LEFT_SCREEN_REGION   = (0, 0, 200, 200)

UNDER_WINDOW_ICON_X = 4
UNDER_WINDOW_ICON_Y = 24

PORT_DROP_DOWN_X = 78
PORT_DROP_DOWN_Y = 68

TCPIP_FIELD_X    = 20
TCPIP_FIELD_Y    = 151
TCPIP_FIELD_WIDE = 284

TIMEOUT_FIELD_X    = 102
TIMEOUT_FIELD_Y    = 215
TIMEOUT_FIELD_WIDE = 35

SAMPLE_RATE_FIELD_X    = 269
SAMPLE_RATE_FIELD_Y    = 215
SAMPLE_RATE_FIELD_WIDE = 35

SLAVE_ID_FIELD_X    = 18
SLAVE_ID_FIELD_Y    = 318
SLAVE_ID_FIELD_WIDE = 56

STARTING_REG_FIELD_X    = 128
STARTING_REG_FIELD_Y    = 318
STARTING_REG_FIELD_WIDE = 56

REG_COUNT_FIELD_X    = 237
REG_COUNT_FIELD_Y    = 318
REG_COUNT_FIELD_WIDE = 56


SAMPLE_MODE_DROP_DOWN_X = 295
SAMPLE_MODE_DROP_DOWN_Y = 180

DATA_TYPE_DROP_DOWN_X = 295
DATA_TYPE_DROP_DOWN_Y = 267

DROP_DOWN_MENU_MULTIPLER = 13

DISPLAY_MODE_DECIMAL_X = 342
DISPLAY_MODE_DECIMAL_Y = 69

DISPLAY_MODE_HEX_X = 430
DISPLAY_MODE_HEX_Y = 69

PROTOCOL_MODBUS_X = 508
PROTOCOL_MODBUS_Y = 186

PROTOCOL_JBUS_X = 508
PROTOCOL_JBUS_Y = 214

PROTOCOL_MODBUS_ASCII_X = 508
PROTOCOL_MODBUS_ASCII_Y = 244

BUTTON_STOP_X = 534
BUTTON_STOP_Y = 296

BUTTON_READ_X = 534
BUTTON_READ_Y = 328

BUTTON_WRITE_X = 534
BUTTON_WRITE_Y = 360

BUTTON_EXIT_X = 534
BUTTON_EXIT_Y = 394

RESULT_FIELD_0_X = 416
RESULT_FIELD_0_Y = 91
RESULT_FIELDS_Y = [ 91, 124, 156, 189, 221, 254, 286, 319, 351, 384 ]

RESULT_FIELD_WIDE = 56
RESULT_FIELD_TALL = 19

DEFAULT_CMD_FILE_NAME = 'mbcommands.txt'

#########################################################################

#
# globals
#



#########################################################################

def clickinwindow(x, y):
    global origin_x, origin_y
    
    pyautogui.moveTo(origin_x + x, origin_y + y)
    
    pyautogui.click()
    
    return

#########################################################################

def selectdropdown(dropdownx, dropdowny, index):
    global origin_x, origin_y

    pyautogui.moveTo(origin_x + dropdownx, origin_y + dropdowny)

    pyautogui.click()
    
    pyautogui.moveTo(origin_x + dropdownx, origin_y + dropdowny + (DROP_DOWN_MENU_MULTIPLER * index))

    pyautogui.click()
    
    pyautogui.moveTo(origin_x + dropdownx, origin_y + dropdowny)

    return    

#########################################################################

def fieldovertype(fieldx, fieldy, fieldwide, text):
    global origin_x, origin_y

    pyautogui.moveTo(origin_x + fieldx + fieldwide - 1, origin_y + fieldy)
    
    pyautogui.click(clicks=2)

    pyautogui.typewrite(text)
    
    return
    
#########################################################################

def getresults():
    global origin_x, origin_y
    global cmap
    
    results = []
    
    for fieldoffsety in RESULT_FIELDS_Y:
        fieldbitmap = pyautogui.screenshot(region=(origin_x + RESULT_FIELD_0_X, origin_y + fieldoffsety, RESULT_FIELD_WIDE, RESULT_FIELD_TALL))
    
        if False:
            for y in range(0, RESULT_FIELD_TALL):
                for x in range(0, RESULT_FIELD_WIDE):
                    rgb = fieldbitmap.getpixel( (x, y) )
                    
                    if rgb[0] == 0:
                        c = '#'
                    else:
                        c = '.'
                    
                    print(c, end='')
                
                print('')
        
        chars = ''
        
        bitmapsofar = ''
        
        x = 0
        
        while x < RESULT_FIELD_WIDE:
            row = ''
            for y in range(RESULT_FIELD_TALL - 7, 1, -1):
                rgb = fieldbitmap.getpixel( (x, y) )
                if rgb[0] == 0:
                    c = '1'
                else:
                    c = '0'
                row += c
            ### print(row)
            
            if (row == '00000000000') or (row == '11111111111'):
                bitmapsofar = ''
            else:
                bitmapsofar += row
                ### print('           ', bitmapsofar)
                
                if bitmapsofar in cmap:
                    ### print('Found character', cmap[bitmapsofar])
                    chars += cmap[bitmapsofar]
                    bitmapsofar = ''
            
            x += 1
        
        results.append(chars)

        ### print('Field-{} is: "{}"'.format(fieldoffsety, chars))
    
    ### print(results)

    return results
    
#########################################################################

def printresults(results):
    for result in results:
        print(' {:>6s}'.format(result), end='')
    print('')
    
    return

#########################################################################

def writeresults(resultfilename, results, datetimenow):
    try:
        resultfile = open(resultfilename, 'a')
    except IOError:
        return
        
    print('"{}"'.format(datetimenow), end='', file=resultfile)
    
    for result in results:
        print(',"{}"'.format(result), end='', file=resultfile)
    
    print('', file=resultfile)

    resultfile.flush()
    resultfile.close()
    
    return

#########################################################################

def resultsloop(resultsfilename, duration, interval):
    starttime = time.time()
    
    ### print('Start time... (float):', starttime)

    intstarttime = int(starttime)

    ### print('Start time..... (int):', intstarttime)
    
    difftime = 1 - (starttime - intstarttime)
    
    ### print('Diff:', difftime)
    
    time.sleep(difftime)
    
    starttime = time.time()
    
    while duration > 0.0:
        datetimenow = datetime.datetime.now()
        print(datetimenow)
        clickinwindow(BUTTON_READ_X, BUTTON_READ_Y)
        time.sleep(0.2)
        results = getresults()
        printresults(results)
        writeresults(resultsfilename, results, datetimenow)

        starttime += interval
        
        timenow = time.time()
        
        if timenow < starttime:
            ### print('A sleep is needed')
            time.sleep(starttime - timenow)
                    
        duration -= interval
        
    
    return

#########################################################################

def mbtester(cmdfile, cmdfilename):
    global origin_x, origin_y
    
    linenum = 0
    
    for line in cmdfile:
        linenum += 1
        
        line = line.strip()
        
        if len(line) == 0:
            continue
        
        if line[0:2] == ';;':
            continue
        
        print('line {} - {}'.format(linenum, line))
        
        fields = line.split()
        
        if (fields[0] == 'exit') or (fields[0] == 'quit'):
            return
        elif fields[0] == 'sleep':
            time.sleep(float(fields[1]))
        elif fields[0] == 'screenshot':
            pyautogui.screenshot(fields[1], region=(origin_x, origin_y, WINDOW_SIZE_X, WINDOW_SIZE_Y))
        elif fields[0] == 'port-tcpip':
            selectdropdown(PORT_DROP_DOWN_X, PORT_DROP_DOWN_Y, 1)
        elif fields[0] == 'port-com1':
            selectdropdown(PORT_DROP_DOWN_X, PORT_DROP_DOWN_Y, 2)
        elif fields[0] == 'port-com2':
            selectdropdown(PORT_DROP_DOWN_X, PORT_DROP_DOWN_Y, 3)
        elif fields[0] == 'port-com3':
            selectdropdown(PORT_DROP_DOWN_X, PORT_DROP_DOWN_Y, 4)
        elif fields[0] == 'sample-mode-manual':
            selectdropdown(SAMPLE_MODE_DROP_DOWN_X, SAMPLE_MODE_DROP_DOWN_Y, 1)
        elif fields[0] == 'sample-mode-scheduled':
            selectdropdown(SAMPLE_MODE_DROP_DOWN_X, SAMPLE_MODE_DROP_DOWN_Y, 2)
        elif fields[0] == 'sample-mode-scheduled-logging':
            selectdropdown(SAMPLE_MODE_DROP_DOWN_X, SAMPLE_MODE_DROP_DOWN_Y, 3)
        elif fields[0] == 'data-type-hold-reg':
            selectdropdown(DATA_TYPE_DROP_DOWN_X, DATA_TYPE_DROP_DOWN_Y, 1)
        elif fields[0] == 'data-type-input-reg':
            selectdropdown(DATA_TYPE_DROP_DOWN_X, DATA_TYPE_DROP_DOWN_Y, 2)
        elif fields[0] == 'data-type-single-hold-reg':
            selectdropdown(DATA_TYPE_DROP_DOWN_X, DATA_TYPE_DROP_DOWN_Y, 3)
        elif fields[0] == 'data-type-scattered-reg-read':
            selectdropdown(DATA_TYPE_DROP_DOWN_X, DATA_TYPE_DROP_DOWN_Y, 4)
        elif fields[0] == 'data-type-read-dev-id':
            selectdropdown(DATA_TYPE_DROP_DOWN_X, DATA_TYPE_DROP_DOWN_Y, 5)
        elif fields[0] == 'display-mode-decimal':
            clickinwindow(DISPLAY_MODE_DECIMAL_X, DISPLAY_MODE_DECIMAL_Y)
        elif fields[0] == 'display-mode-hex':
            clickinwindow(DISPLAY_MODE_HEX_X, DISPLAY_MODE_HEX_Y)
        elif fields[0] == 'protocol-modbus':
            clickinwindow(PROTOCOL_MODBUS_X, PROTOCOL_MODBUS_Y)
        elif fields[0] == 'protocol-jbus':
            clickinwindow(PROTOCOL_JBUS_X, PROTOCOL_JBUS_Y)
        elif fields[0] == 'protocol-modbus-ascii':
            clickinwindow(PROTOCOL_MODBUS_ASCII_X, PROTOCOL_MODBUS_ASCII_Y)
        elif fields[0] == 'button-stop':
            clickinwindow(BUTTON_STOP_X, BUTTON_STOP_Y)
        elif fields[0] == 'button-read':
            clickinwindow(BUTTON_READ_X, BUTTON_READ_Y)
        elif fields[0] == 'button-write':
            clickinwindow(BUTTON_WRITE_X, BUTTON_WRITE_Y)
        elif fields[0] == 'button-exit':
            clickinwindow(BUTTON_EXIT_X, BUTTON_EXIT_Y)
        elif fields[0] == 'tcpip-address':
            fieldovertype(TCPIP_FIELD_X, TCPIP_FIELD_Y, TCPIP_FIELD_WIDE, fields[1])
        elif fields[0] == 'timeout':
            fieldovertype(TIMEOUT_FIELD_X, TIMEOUT_FIELD_Y, TIMEOUT_FIELD_WIDE, fields[1])
        elif fields[0] == 'sample-rate':
            fieldovertype(SAMPLE_RATE_FIELD_X, SAMPLE_RATE_FIELD_Y, SAMPLE_RATE_FIELD_WIDE, fields[1])
        elif fields[0] == 'slave-id':
            fieldovertype(SLAVE_ID_FIELD_X, SLAVE_ID_FIELD_Y, SLAVE_ID_FIELD_WIDE, fields[1])
        elif fields[0] == 'starting-reg':
            fieldovertype(STARTING_REG_FIELD_X, STARTING_REG_FIELD_Y, STARTING_REG_FIELD_WIDE, fields[1])
        elif fields[0] == 'reg-count':
            fieldovertype(REG_COUNT_FIELD_X, REG_COUNT_FIELD_Y, REG_COUNT_FIELD_WIDE, fields[1])
        elif fields[0] == 'results':
            results = getresults()
            printresults(results)
            if len(fields) >= 2:
                writeresults(fields[1], results, datetime.datetime.now())
        elif fields[0] == 'results-loop':
            if len(fields) >= 4:
                resultsloop(fields[1], float(fields[2]), float(fields[3]))
        else:
            print('{}: unrecognised keyword "{}" at line {} in command file "{}"'.format(progname, fields[0], linenum, cmdfilename), file=sys.stderr)

    return

#########################################################################

def main():
    global progname
    global origin_x, origin_y
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--cmd',  help='command file name',                     default=DEFAULT_CMD_FILE_NAME)
    parser.add_argument('--ip',   help='IP address to preprogram for TCP/IP',   nargs=1)

    args = parser.parse_args()

    cmdfilename = args.cmd
    
    try:
        cmdfile = open(cmdfilename, 'r')
    except IOError:
        print('{}: cannot open command file name "{}" for reading'.format(progname, cmdfilename), file=sys.stderr)
        sys.exit(1)
    
    mbicon = pyautogui.locateOnScreen(MB_ICON_BITMAP_FILE_NAME, region=TOP_LEFT_SCREEN_REGION)
    
    if mbicon == None:
        print('{}: cannot find the icon in the Generic Modbus/Jbus tester window - is the program running?'.format(progname), file=sys.stderr)
        sys.exit(1)

    origin_x = mbicon[0]
    origin_y = mbicon[1]
    
    if origin_x < MB_ICON_PADDING_X:
        print('{}: the Generic Modbus/Jbus tester window is too close to the left hand edge of the screen'.format(progname), file=sys.stderr)
        sys.exit(1)

    if origin_y < MB_ICON_PADDING_Y:
        print('{}: the Generic Modbus/Jbus tester window is too close to the top edge of the screen'.format(progname), file=sys.stderr)
        sys.exit(1)

    origin_x -= MB_ICON_PADDING_X
    origin_y -= MB_ICON_PADDING_Y
    
    ### print(origin_x, origin_y)

    clickinwindow(UNDER_WINDOW_ICON_X, UNDER_WINDOW_ICON_Y)
    
    if args.ip:
        if len(args.ip) == 1:
            selectdropdown(PORT_DROP_DOWN_X, PORT_DROP_DOWN_Y, 1)
            fieldovertype(TCPIP_FIELD_X, TCPIP_FIELD_Y, TCPIP_FIELD_WIDE, args.ip[0])
        
    mbtester(cmdfile, cmdfilename)
    
    clickinwindow(UNDER_WINDOW_ICON_X, UNDER_WINDOW_ICON_Y)
        
    cmdfile.close()

    return 0

#########################################################################

progname = os.path.basename(sys.argv[0])

cmap = {}
cmap['0011111110001000000010010000000100100000001000111111100'] = '0'
cmap['000000001000000000010001111111110']                       = '1'
cmap['0110000010001010000010010010000100100010001001000011100'] = '2'
cmap['0010000010001000000010010001000100100010001000111011100'] = '3'
cmap['0001100000000010110000000100011000111111111000010000000'] = '4'
cmap['0010011111001000010010010000100100100001001000111100010'] = '5'
cmap['0011111110001000100010010001000100100010001000111000100'] = '6'
cmap['0000000001001110000010000011000100000001101000000000110'] = '7'
cmap['0011101110001000100010010001000100100010001000111011100'] = '8'
cmap['0010001110001000100010010001000100100010001000111111100'] = '9'
cmap['0011000000001001010000010010100000100101000001111100000'] = 'a'
cmap['0111111111001000010000010000100000100001000000111100000'] = 'b'
cmap['0011110000001000010000010000100000100001000000100100000'] = 'c'
cmap['0011110000001000010000010000100000100001000001111111110'] = 'd'
cmap['0011110000001001010000010010100000100101000000101100000'] = 'e'
cmap['0111111110000000010010']                                  = 'f'

origin_x = None
origin_y = None

sys.exit(main())

# end of file
