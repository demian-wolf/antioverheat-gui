# AntiOverheat-GUI

#### What may you need it for?
Does your PC's/laptop's CPU overheat lately? Maybe, it even turns off without warning while doing some really
intensive tasks? If so, it might be time to clean up the device and reapply the thermal grease as soon as possible.

But if you can't do that at the moment, you can try this app as a temporary
solution!

#### How does it work?
In order to deal with overheating problems, you could try lowering maximum frequency of the CPU.

On Linux, it is possible to do that with **cpupower** (it is necessary to install it first;
see the next part of this README for that):
```
sudo cpupower frequency-set --max <frequency><unit>
```
Cpupower also provides a command to get frequency info:
```
cpupower frequency-info
```
Another command-line tool called **lm-sensors** provides information about CPU temperature values:
```
sensors
```
That said, opening the terminal and typing command(s) like these ones every time you need to get or
change CPU frequency/temperature isn't a really good idea. It might be really distracting and
time-consuming; there is also a risk you'll be doing something really important
and forget about monitoring CPU temperature, and your device would get too overheated.

This app can solve these problems.

It consists of two GUIs on top of the wrappers around the aforementioned terminal
commands.

* Power Manager
    * ![Power Manager screenshot](https://i.imgur.com/RADlu4F.png "Power Manager")
    * A tiny draggable window is displayed on the screen. The color of
    this window changes gradually from green (low CPU frequency) to red (high CPU frequency).
    * You can effortlessly manage the frequency of the CPU, moving the slider on the scale, increasing
    it when you care about speed, but decreasing it once you don't. The lower the CPU frequency,
    the lower is its temperature.
    * You can also enable "automode". It automatically does everything previously described.
    When CPU temperature is more-or-less low it increases the CPU frequency, once it is higher, it
    decreases it, and once it is very high, it sets it to the lowest possible value.
* Temperature Monitor
    * ![Temperature Monitor screenshot](https://i.imgur.com/GK3qMek.png "Temperature Monitor")
    * Another window at the top of the screen, that appears once CPU overheats. The color of this window also
    changes from yellow to red depending on the CPU frequency
    * Besides the warning, the actual temperature values for every CPU core are displayed.
    * Sound notification can be enabled via -s command-line argument (beeps)

#### How to install and use it?
**Note:** currently this app is available only for Linux. Other platforms are not supported yet.

**Note:** most of the commands below must be run with root privileges. It is a necessary measure,
since it would be impossible to change the CPU frequency without it.

1) Before installing this app itself, you have to install "cpupower" and "lm-sensors" on your
system (if they are not already installed). For Temperature Monitor beep sound notification,
there is an additional "SoX" dependency.
Commands for various Linux distros: [cpupower](https://command-not-found.com/cpupower),
[lm-sensors](https://command-not-found.com/sensors), and
[SoX](https://command-not-found.com/play)

1) Clone this repository
    ```
    git clone https://github.com/demian-wolf/AntiOverheat-GUI.git
    ```
2) Run setup.py:
    ```
    sudo python3 setup.py install
    ```
3) You can run the app like this:
    ```
    sudo python3 -m antioverheat -powerman -tempmon
    ``` 
   Or like this:
    ```
    sudo python3 -m antioverheat -powerman -a -tempmon -s -i 1000
    ```
   Arguments description:
    * -powerman stands for Power Manager
        * -a: if this argument is specified, "Automode" is enabled
    * -tempmon stands for Temperature Monitor
        * -s: if this argument is specified, Temperature Monitor will beep
        (**note:** SoX must be installed on your Linux system for this to work)
        * -i: is the interval (in ms) when the temperature values are updated
