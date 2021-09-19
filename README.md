## fan_control
A very simple bash script controlling a GPIO fan on my Raspberry Pi.

### fan_cotrol.sh
This script is executed by crontab every minute and actually controlls the functionality of the fan

### graph_temp.py
This script prints out a pretty graph of the fans history, showing upper and lower cutoffs, as well as time jumps (shutdowns)
In addition to these two scripts, the follows helps these features run:

### crontab entry
`* * * * * /home/pi/fan_control/fan_control.sh`

### .zshrc.local (.bashrc equivalent)
```
fan-log () {
	(cd ~/fan_control; graph_temp.py)
}
```
