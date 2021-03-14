## Summary

AutoWRT is planned to be a python application to excecute handsfree out-of-the-box installation of OpenWRT. It currently supports the Xiaomi 4A Gigabit and Xiaomi 4A 100m Routers via an [OpenWRTInvasion](https://github.com/acecilia/OpenWRTInvasion)-based exploit. Support for the Xiaomi 3Gv1 and Redmi RC2100 is planned to be implemented soon.

This software is for educational purposes only. Excecute it on your own resposibility.

## Installation

`appdirs`, `requests` and `selenium` python packages as well as geckodriver are required. It is recommended not to install autowrt as a package but rather to install its dependencies, clone this repository, download your openwrt images, adjust `config.py` in the root directory accordingly and then run autowrt.py as described below.

If you choose to install autowrt as a package, you will have to copy `config.py` to the configuration directory, on linux this will be `~/.config/autowrt`. Image files will then be searched for in the program data dir; `~/.local/share/autowrt/images` on linux, logs will be kept in `~/.cache/autowrt/log` on linux.

## Usage

Download the OpenWRT images to the images directory and edit the `config.py` file. The `config.py` shipped contains links to where you find releases of OpenWRT 19.07. If you choose other images, don't forget to update the sha256 checksums in `config.py` as well. If 'SKIP' is provided in the checksum field, the checksum test will not be performed.

Once you're done with the configuration, connect a router in factory state via cable from its LAN port to your Computer, then run autowrt. autowrt will wait up to two minutes for a router that is still booting. Afterwards it will install your image according to configuration and reboot your device on success.

The OpenWRT image will not be modified, nor will OpenWRT be set up. Once AutoWRT has finished, you will have to set it up yourself (e.g. set passwords/install ssh-keys)

If enabled in `config.py`, AutoWRT will collect some information from the stock firmware as well as backups of all mtd sections to the log directory. You may want to delete those at some point.

## Other Tools

**Note: Recovery images may be in chinese language only**

This repository contains a script to debrick a xiaomi router in Linux. It assumes that NetworkManager and iproute2 are used. You will also have to install the dnsmasq package

To use it, download the firmware image for your device from [the manufacturer](http://www.miwifi.com/miwifi_download.html) and place it in the tools directory. For the 4a Gigabit edition, this could be `miwifi_r4a_firmware_72d65_2.28.62.bin` for example. use the `ip a` command to determine the name of your wired network interface, it should start with eth or enp. Then from the tools directory run the script e.g. `./unbrick.sh eth0 miwifi_r4a_firmware_72d65_2.28.62.bin`. Connect the LAN-Port of your device to your computer, hold the reset button, then power on the router. Hold the reset button until the LED of the router starts blinking orange after about 10 seconds. Then wait. After a few seconds, the script should output `dnsmasq-tftp: sent miwifi_r4a_firmware_72d65_2.28.62.bin to 192.168.1.81`. Keep waiting until the LED of the router turns blinking blue. Now you can unplug the router and it will be back to stock firmware.

## Disclaimer

**THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.**
