# Overview
ssh links to the other two RPis were previously configured. The commands for accessing them are simply 

```bash
ssh rasp4
ssh rsap5
```

Sometimes, calling these functions will raise a name resolution error. 

# Fix
1. Confirm you are currently on the base RPi (rasp5-hobbs). The ssh aliases have not been configured on the other two devices.

2. Power cycle the device you can't connect to (unplug it, then plug it back in).
