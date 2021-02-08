# AntiOverheat-GUI

#### What do you may need it for?
Does your PC's/laptop's CPU overheat lately? Maybe, it even started to turn off without warning while doing some really
tough tasks? If so, it's time to clean up the device, reapply the thermal grease, and so...

But what if you can't (don't want to) do that at the moment? You can try this app as a temporary
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
and forget about monitoring CPU temperature, and your device would get so overheated
that it will turn off.

This app can solve such problems:
it consists of two GUIs on top of a wrappers around the aforementioned "cpupower" and "lm-sensors"
commands.

* Power Manager
    * ![Power Manager screenshot](https://i.imgur.com/RADlu4F.png "Power Manager")
    * A tiny window is displayed on the screen. This window is draggable on the screen. The color of
    this window changes gradually from green (low CPU frequency) to red (high CPU frequency).
    * You can effortlessly manage the frequency of the CPU, moving the slider on the scale, increasing
    it when you care about speed, but decreasing it once you don't. The lower the CPU frequency,
    the lower is its temperature.
    * You can also enable "automode". It does everything described previously automatically.
    When CPU temperature is more-or-less low it increases the CPU frequency, once it is higher, it
    decreases it, and once it is very high, it makes it as low as possible.
* Temperature Monitor
    * ![Temperature Monitor screenshot](https://i.imgur.com/GK3qMek.png "Temperature Monitor")
    * Another window at the top of the screen, that appears once CPU overheats. The color of this window also
    changes from yellow to red depending on the CPU frequency
    * Besides the warning, the actual temperature values for every CPU core are displayed.
    * Sound notification can be enabled via -s command-line argument (beeps)

#### How to install and use it?
**Note:** currently this app is available only for Linux. Other platforms are not yet supported.
1) Before installing this app itself, you might need to install cpupower and lm-sensors 
1) Clone this repository
    ```
    git clone https://github.com/demian-wolf/AntiOverheat-GUI.git
    ```
2) Run setup.py:
    ```
    python3 setup.py install
    ```
3) You can run the app like this:
    ```
    python3 -m antioverheat -powerman -tempmon
    ``` 
   Or like this:
    ```
    python3 -m antioverheat -powerman -p your_sudo_password -a -tempmon -s -i 1000
    ```
   Arguments description:
    * -powerman stands for Power Manager
        * -p is the password you enter with sudo. It is required to change the frequency of the CPU.
        If you don't specify it, the app will ask it in a special dialog window. Note the password is not required
        for the tempmon.
        * -a if this argument is specified, automode is enabled
    * -tempmon stands for Temperature Monitor
        * -s if this argument is specified, Temperature Monitor will beep (**note:** play must be installed on your Linux system)
        * -i is the interval (in ms) when the temperature values are updated
