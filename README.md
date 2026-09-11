# mbtester

Automation tool for the Generic Modbus/Jbus Tester program from Schneider Electric.

[Watch a two and a half minute demonstration video on YouTube](https://www.youtube.com/watch?v=_Y-cJOoy14s)

By using a command file the Tester.exe program can be controlled.  For example
the following line in the command file:

```
sample-rate 1000
```

will set the sample rate field to 1000 milliseconds.

## Limitations

The program currently only supports driving a Modbus TCP/IP connection.

While the program is running you cannot use the desktop for any other activities.
This is because the underlying Python PyAutoGUI module "takes control" of the mouse,
keyboard and screen.

## Requirements

A Windows desktop environment.  The program was developed on Windows 10 but previous
versions may work.

Python 3 installed.  Developed on Python 3.7 but earlier versions of Python 3
may work.

Python module PyAutoGUI installed.  Developed with version 0.9.39 of PyAutoGUI.

The Tester.exe file downloaded from:

[Video: What is Modbus Tester and how do I use it?](https://www.schneider-electric.com/en/faqs/FA180037/)

The file is 208,896 bytes in size and the MD5 checksum should be:

```
69650ba883553246c26eee449f4fb263
```

You will also need access to a device running Modbus over TCP/IP.

## Setup

Create a new empty directory - this documentation will use the `C:\andyc\projects\mbtester`
directory as an example.

From the repository copy the following files:

```
mbcommands.txt
mbicon.bmp
mbtester.py
```

to the `C:\andyc\projects\mbtester` directory.

Copy the:

```
Tester.exe
```

that was downloaded from the Schneider Electric website
to the `C:\andyc\projects\mbtester` directory.

Open a command prompt window and change to the `C:\andyc\projects\mbtester` directory.

Type:

```
tester
```

to start the Generic Modbus/Jbus Tester program.  Move the program window to the top left
hand corner of the screen.  It does not need to be exactly in the corner.

Go back to the command prompt window and type:

```
python mbtester.py
```

The program now reads the command lines in the file `mbcommands.txt` and
takes the appropriate action.

Chances are you will need to edit the `mbcommands.txt` file and change the IP address on
the `tcpip-address`.  Also the `slave-id`, `starting-reg` and `reg-count` will
probably need to be changed depending on the layout of the Modbus map on the
device you are connecting to.

## mbcommands.txt file

By default the `mbtester.py` program reads commands, a line at a time, from the
`mbcommands.txt` file.  Each line can be a command with optional arguments, blank or a comment line.
Comment lines begin `;;` and are ignored.  Blank lines are also ignored.

The next sections document the allowable commands in this file.

### port-tcpip

Selects TCP/IP as the port.

### tcpip-address

One argument required.  The argument is copied
to the "TCP/IP Address or URL:" field.

Example:

```
tcpip-address 192.168.1.4
```

### sample-mode-manual

Selects "Manual" from the "Sample Mode:" drop down menu.

### sample-mode-scheduled

Selects "Scheduled" from the "Sample Mode:" drop down menu.

### sample-mode-scheduled-logging

Selects "Scheduled with Logging (Automated)" from the "Sample Mode:" drop down menu.

### timeout

One argument required.  The argument is copied to the "Timeout in ms:" field.

Example:

```
timeout 2000
```

### sample-rate

One argument required.  The argument is copied to the "Sample Rate in ms:" field.

Example:

```
sample-rate 1000
```

### data-type-hold-reg

Selects "Holding Register (R03/W16)" from the "Data Type:" drop down menu.

### data-type-input-reg

Selects "Input Register (R04)" from the "Data Type:" drop down menu.

### data-type-single-hold-reg

Selects "Single Holding Register (R03/W06)" from the "Data Type:" drop down menu.

### data-type-scattered-reg-read

Selects "Scattered Register Read (R100[04])" from the "Data Type:" drop down menu.

### data-type-read-dev-id

Selects "Read Device Identification (R43[14])" from the "Data Type:" drop down menu.

### slave-id

One argument required.  The argument is copied to the "Slave ID:" field.

Example:

```
slave-id 1
```

### starting-reg

One argument required.  The argument is copied to the "Starting Register:" field.

Example:

```
starting-reg 2049
```

### reg-count

One argument required.  The argument is copied to the "# of Registers:" field.

Example:

```
reg-count 8
```

### display-mode-decimal

Selects the "Decimial" (sic) radio button from "Display Mode".

### display-mode-hex

Selects the "Hex" radio button from "Display Mode".

### protocol-modbus

Selects the "Modbus" radio buttom from "Protocol".

### protocol-jbus

Selects the "Jbus" radio buttom from "Protocol".

### protocol-modbus-ascii

Selects the "Modbus ASCII" radio buttom from "Protocol".

### button-stop

Clicks the "Stop" button.

### button-read

Clicks the "read" button.

### button-write

Clicks the "Write" button.

### button-exit

Clicks the "Exit" button.

### results

One argument required.  Append the current result values (10 in total)
to the file name argument.  Use CSV (comma seperated values) format.
The results are printed to the screen as well.
If the file name does not exist it is created.

Example:

```
results resultfile.csv
```

### resultsloop

Three arguments required.  First argument is a file name.  Second argument
is a duration value in seconds as a floating point number.  Third
argument is an interval value in seconds as a floating point number.

The program clicks the "Read" button, extracts the results appending them to the
file name argument in CSV format.  The results are printed to the screen as well.
The program waits for the next interval period and then repeats these steps.
Once the duration time has been exceeded the command completes.

Example:

```
resultsloop resultfile.csv 10.0 1.0
```

### screenshot

One argument required.  Take a screen shot of the program window
and save into the file name argument.

Example:

```
screenshot currentwindow.png
```

### sleep

One argument required.  Sleeps for the specified number of seconds.  Seconds
must be a floating point number such as `1.0` (i.e. make sure there is
a decimal point).

Example:

```
sleep 5.0
```

### exit

Exit the program without processing any more lines from the command file.

### quit

Does the same as the `exit` command.

## Warnings

NOT for production use!!!

The program does minimal error checking of the `mbcommands.txt` file.  Bad and missing
values in this file will break the program easily.  The code has been kept minimal
as the primary use is to demonstrate the concept of adding extra functionality to
a Windows program using software automation.  Lots of error checking code
would get in the way :-]

----------------------------------------
End of file
