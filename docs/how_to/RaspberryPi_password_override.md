# Overview
When repairing the system, we realized that no one knew the sudo password for any of the three RPis (including the original creator of the system). Sudo access is required for adjusting permission (e.g., with camera device settings), installing new software, and a host of other tasks. 

As it turns out, you can circumvent and reset the administrative password on a RPi system if you have physical access to it. 

# Fix
Source: user "klricks" on forums.raspberrypi.com

Requirements:
    - a second device capable of reading/writing to a microSD card 
    - an external monitor, keyboard, and mouse for the RPi

0. Note the username for the administrative account ('yuanjian' on our systems)

1. Power off the RPi (unplug) and remove the microSD card.

2. Insert the microSD card into the other computer and navigate to the card's storage.

3. Open ```cmdline.txt``` in a text editor such as Notepad
    - The entire document should be contained on one line.
    - It may be worth storing a copy of this document in its original form somewhere on the secondary computer in case something goes wrong.

4. At the end of the first line, add a single space and the command ```init=/bin/sh``` (no internal spaces.
    - On our systems, the commands "quiet" and "splash" also had to be removed. 
    - Again, make sure this is not placed on a new line.

5. Save the file, eject the microSD (right-click on the device, select "Eject", then physically eject the card after confirmation), and re-insert it into the RPi. 

6. Restore power to the RPi and allow the system to begin booting up. 

7. After some kind of error appears ("can't access tty" or something similar), press [Enter] to get a ```#``` prompt. Enter the following commands:
```bash
mount -o remount rw /
passwd [USERNAME]
sync
exec /sbin/init
```

8. The system should bootup normally now. You can test the password reset was successful by running any command in the terminal as an administrator (ex. ```sudo ls```)

9. Repeat steps 1-6, only this time to undo the changes from step 4. If you saved a copy of the document at step 3, you can simply restore this copy to the microSD.
