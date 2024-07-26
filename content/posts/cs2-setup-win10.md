---
title: "cs2 setup windows 10"
date: 2024-07-26T15:14:18+02:00
draft: false
toc: false
description: 
author: loeken
summary: installation notes for windows 10 and counter strike
images:
tags:
  - counter strike 2
---

# my hardware specs

- b650 aorus elite ax v2
- amd ryzen 7800x3d
- 32GB G.Skill Flare X5 DDR5-6000 DIMM CL30 Dual Kit
- nzxt h6 flow
- 3090 ti ( 24GB )

# creating bootable media

download the windows 10 media creation tool and use it to create an iso. then grab rufus, which we ll use to write the iso to an usb stick. we are using rufus in order to create non cloud connected local accounts.

https://rufus.ie/en/


# bios settings

## xmp
overclock memory to reach the 6000mh/s, you can verify the speed of your memory in taskmanager -> performance tab -> memory, my memory can do 6000mhz so it should show 6000MT/s under speed

## safe mode
safe mode should be enabled, required for faceit anti cheat

# windows 10 install

just normal install

# edit power plan
change energy settings to not turn of pc ( while steam downloads game, feel free to touch grass, while game downloads without pc going into hibernation ). set it to performance this usually includes no turning off

# steampowered.com installer for cs
get steam installer and start installation for game

# nvidia game ready driver
im installing it without the geforce experience bloatware

# nvidia control panel
3d settings -> adjust image settings with preview: change to performance

# disable mouse acceleration in windows 

for better mouse movement consistency:
Go to Windows Search and type "Control Panel."
Open the Control Panel app.
Click on Hardware and Sound.
Click on the Mouse under the Devices and Printers.
In the Mouse Properties window, navigate to the Pointer Options tab.
In the Motion section, uncheck the box left to Enhance pointer precision, which controls the mouse acceleration in Windows. Unchecking it will disable the mouse acceleration.
Click Apply and hit Ok.

# sticky keys such as strg/ctrl

Using the Settings App:

Press Win + I to open the Settings app.
Go to Ease of Access.
Click on Keyboard.
Under the "Use Sticky Keys" section, toggle the switch off.
Also uncheck the checkbox allow the shortcut key to toggle on sticky keys

# logitec g-hub
to manage my mouse dpi

# faceit client and anti-cheat

# ensure windows updates are installed
and wont be installed during first rounds ;)