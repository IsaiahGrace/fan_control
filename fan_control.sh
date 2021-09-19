#!/bin/bash

LOGDIR="/home/pi/fan_control/fan.log"

timestamp() {
    date +"%Y-%m-%d %T"
}

if [[ ! -e /sys/class/gpio/gpio14/value ]] || [[ `cat /sys/class/gpio/gpio14/direction` == "in" ]]
then
    echo `timestamp` " Action: Setting up gpio14" >> $LOGDIR
    # This can only be executed by root,
    echo "14" > /sys/class/gpio/export
    # Sleep for 2 seconds to allow the OS to configure gpio
    sleep 2
    echo "out" > /sys/class/gpio/gpio14/direction
    # Sleep for two more seconds to allow the OS to set the pin direction
    sleep 2
    echo "0" > /sys/class/gpio/gpio14/value
fi

# These are the cuttof points at which the fan will turn on or off, in C
MAX=56 # idle steady state without fan is ~55
MIN=44 # idle steady state with fan is ~36

# Measure the temp from the OS
TEMP=`vcgencmd measure_temp | cut -c6,7`

# Determine the state of the fan
STATUS=`cat /sys/class/gpio/gpio14/value`

# Create the log file if it does not exist
touch $LOGDIR

echo `timestamp` " Info: Temperature: $TEMP" >> $LOGDIR

if [[ $TEMP -gt $MAX ]] && [[ $STATUS -eq 0 ]];
then
    echo `timestamp` " Action: Starting fan." >> $LOGDIR
    echo "1" > /sys/class/gpio/gpio14/value

elif [[ $TEMP -lt $MIN ]] && [[ $STATUS -eq 1 ]];
then
    echo `timestamp` " Action: Stopping fan." >> $LOGDIR
    echo "0" > /sys/class/gpio/gpio14/value
fi
