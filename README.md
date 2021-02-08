# AntiOverheat-GUI

#### What do you may need it for?
Does your PC's/laptop's CPU overheat lately? Maybe, it even started to turn off without warning while doing some really
tough tasks? If yes, it's time to clean up the device, reapply the thermal grease, replace the CPU
fan...

But what if you can't do that at the moment? You can use this app until you're ready!

#### How does it work?
This app consists of two subapps:

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
**Note:** currently this app is available only for Linux. Windows and Mac are not yet supported.
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
