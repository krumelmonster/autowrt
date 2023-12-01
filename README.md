# DON'T USE THIS SCRIPT: it fails to set a boot timeout, therefore if you brick your device, you can't even recover with UART pins soldered.

## Summary

AutoWRT is planned to be a python application to excecute handsfree out-of-the-box installation of OpenWRT. It requires no internet connection. It currently supports the Xiaomi 4A Gigabit and Xiaomi 4A 100m Routers via an [OpenWRTInvasion](https://github.com/acecilia/OpenWRTInvasion)-based exploit. Support for the Xiaomi 3Gv1 and Redmi RC2100 is planned to be implemented soon.

Please leave some feedback to the [discussion thread in the OpenWRT forums](https://forum.openwrt.org/t/autowrt-a-handsfree-installation-method-on-xiaomi-routers/91216).

This software is for educational purposes only. Excecute it on your own resposibility.

## Installation

`appdirs`, `requests` and `selenium` python packages as well as geckodriver are required. It is recommended not to install autowrt as a package but rather to install its dependencies, clone this repository, download your openwrt images, adjust `config.py` in the root directory accordingly and then run autowrt.py as described below.

If you choose to install autowrt as a package, you will have to copy `config.py` to the configuration directory, on linux this will be `~/.config/autowrt`. Image files will then be searched for in the program data dir; `~/.local/share/autowrt/images` on linux, logs will be kept in `~/.cache/autowrt/log` on linux.

## Usage

Download the OpenWRT images to the images directory and edit the `config.py` file. The `config.py` shipped contains links to where you find releases of OpenWRT 19.07. If you choose other images, don't forget to update the sha256 checksums in `config.py` as well. If 'SKIP' is provided in the checksum field, the checksum test will not be performed.

Once you're done with the configuration, connect a router in factory state via cable from its LAN port to your Computer, then run autowrt. You don't have to connect the router to the internet. autowrt will wait up to two minutes for a router that is still booting. Afterwards it will install your image according to configuration and reboot your device on success.

The OpenWRT image will not be modified, nor will OpenWRT be set up. Once AutoWRT has finished, you will have to set it up yourself (e.g. set passwords/install ssh-keys)

If enabled in `config.py`, AutoWRT will collect some information from the stock firmware as well as backups of all mtd sections to the log directory. You may want to delete those at some point.

<details>
  <summary>Example output</summary>
  
```
2021-03-14 20:47:21,005 - AutoWRT - INFO - Logging to /home/me/autowrt/log/2021-03-14T20:47:21.003883
2021-03-14 20:47:21,006 - AutoWRT - INFO - Data dir is /home/me/autowrt/images
2021-03-14 20:47:21,009 - AutoWRT - INFO - Xiaomi-Module started, loading Selenium driver
2021-03-14 20:47:25,392 - AutoWRT - INFO - Trying to access router web page at 192.168.31.1:
2021-03-14 20:47:26,730 - AutoWRT - INFO - Detected Xiaomi Router Chinese Edition (possibly xiaomi_mi_router_4a_100m or xiaomi_mi_router_4a_gigabit?)
2021-03-14 20:47:26,769 - AutoWRT - INFO - Starting router configuration
2021-03-14 20:47:38,103 - AutoWRT - INFO - Router successfully set up!
2021-03-14 20:47:55,404 - AutoWRT - INFO - Logged into Webinterface at http://192.168.31.1/cgi-bin/luci/;stok=00000000000000000000000000000000/web/home
2021-03-14 20:47:55,618 - AutoWRT - INFO - Upload OpenWRTInvasion
2021-03-14 20:47:57,023 - AutoWRT - INFO - Run OpenWRTInvasion
2021-03-14 20:47:59,766 - AutoWRT - INFO - OpenWRTInvasion succeeded!
2021-03-14 20:48:00,541 - AutoWRT - INFO - Router model detected as R4AC
2021-03-14 20:48:00,577 - AutoWRT - INFO - Save some command outputs in directory "/home/me/autowrt/log/2021-03-14T20:47:21.003883"
2021-03-14 20:48:00,577 - AutoWRT - INFO -  dmesg
2021-03-14 20:48:00,985 - AutoWRT - INFO -  uname -a
2021-03-14 20:48:01,067 - AutoWRT - INFO -  cat /proc/cpuinfo
2021-03-14 20:48:01,130 - AutoWRT - INFO -  for i in /sys/class/mtd/mtd*/*;do echo "$i"; cat "$i" 2> /dev/null;done
2021-03-14 20:48:06,423 - AutoWRT - INFO - Start backup of the mtd
2021-03-14 20:48:06,471 - AutoWRT - INFO - Back up mtd0 to mtd0_ALL.backup size 01000000
2021-03-14 20:48:34,685 - AutoWRT - INFO - Back up mtd1 to mtd1_Bootloader.backup size 00020000
2021-03-14 20:48:34,833 - AutoWRT - INFO - Back up mtd2 to mtd2_Config.backup size 00010000
2021-03-14 20:48:34,940 - AutoWRT - INFO - Back up mtd3 to mtd3_Factory.backup size 00010000
2021-03-14 20:48:35,003 - AutoWRT - INFO - Back up mtd4 to mtd4_crash.backup size 00010000
2021-03-14 20:48:35,080 - AutoWRT - INFO - Back up mtd5 to mtd5_cfg_bak.backup size 00010000
2021-03-14 20:48:35,187 - AutoWRT - INFO - Back up mtd6 to mtd6_overlay.backup size 00100000
2021-03-14 20:48:36,221 - AutoWRT - INFO - Back up mtd7 to mtd7_OS1.backup size 00c60000
2021-03-14 20:48:49,174 - AutoWRT - INFO - Back up mtd8 to mtd8_rootfs.backup size 00b00000
2021-03-14 20:48:59,555 - AutoWRT - INFO - Back up mtd9 to mtd9_disk.backup size 00240000
2021-03-14 20:49:02,172 - AutoWRT - INFO - Verify mtd0_ALL.backup
2021-03-14 20:49:13,030 - AutoWRT - WARNING - mtd0_ALL.backup failed the checksum verification against md5sum /dev/mtd0ro 'fd2d645fc41f209337cfd329d7c49498'/'6a4acebef96fe5d73a200c75d93dee71'
2021-03-14 20:49:13,030 - AutoWRT - INFO - Verify mtd1_Bootloader.backup
2021-03-14 20:49:13,118 - AutoWRT - INFO - Verify mtd2_Config.backup
2021-03-14 20:49:13,206 - AutoWRT - INFO - Verify mtd3_Factory.backup
2021-03-14 20:49:13,253 - AutoWRT - INFO - Verify mtd4_crash.backup
2021-03-14 20:49:13,310 - AutoWRT - INFO - Verify mtd5_cfg_bak.backup
2021-03-14 20:49:13,402 - AutoWRT - INFO - Verify mtd6_overlay.backup
2021-03-14 20:49:14,062 - AutoWRT - INFO - Verify mtd7_OS1.backup
2021-03-14 20:49:22,198 - AutoWRT - INFO - Verify mtd8_rootfs.backup
2021-03-14 20:49:29,520 - AutoWRT - INFO - Verify mtd9_disk.backup
2021-03-14 20:49:31,398 - AutoWRT - INFO - Backups are done, now upload OpenWRT-Image
2021-03-14 20:49:31,399 - AutoWRT - INFO - Uploading image 'openwrt-19.07.7-ramips-mt76x8-xiaomi_mir4a-100m-squashfs-sysupgrade.bin'...
2021-03-14 20:49:34,839 - AutoWRT - INFO - Verifying image 'openwrt-19.07.7-ramips-mt76x8-xiaomi_mir4a-100m-squashfs-sysupgrade.bin'...
2021-03-14 20:49:35,203 - AutoWRT - INFO - Image verification succeeded
2021-03-14 20:49:35,206 - AutoWRT - INFO - Installing OpenWRT NOW!..
2021-03-14 20:49:35,206 - AutoWRT - INFO - nohup mtd -e OS1 -q write openwrt-19.07.7-ramips-mt76x8-xiaomi_mir4a-100m-squashfs-sysupgrade.bin OS1
Unlocking OS1 ...
Erasing OS1 ...

Writing from openwrt-19.07.7-ramips-mt76x8-xiaomi_mir4a-100m-squashfs-sysupgrade.bin to OS1 ... 
2021-03-14 20:50:38,886 - AutoWRT - INFO - OpenWRT-Installation was successful, rebooting device...
```
</details>

## Other Tools

**Note: Recovery images may be in chinese language only**

This repository contains a script to debrick a xiaomi router in Linux. It assumes that NetworkManager and iproute2 are used. You will also have to install the dnsmasq package

To use it, download the firmware image for your device from [the manufacturer](http://www.miwifi.com/miwifi_download.html) and place it in the tools directory. For the 4a Gigabit edition, this could be `miwifi_r4a_firmware_72d65_2.28.62.bin` for example. use the `ip a` command to determine the name of your wired network interface, it should start with eth or enp. Then from the tools directory run the script e.g. `./unbrick.sh eth0 miwifi_r4a_firmware_72d65_2.28.62.bin`. Connect the LAN-Port of your device to your computer, hold the reset button, then power on the router. Hold the reset button until the LED of the router starts blinking orange after about 10 seconds. Then wait. After a few seconds, the script should output `dnsmasq-tftp: sent miwifi_r4a_firmware_72d65_2.28.62.bin to 192.168.1.81`. Keep waiting until the LED of the router turns blinking blue. Now you can unplug the router and it will be back to stock firmware.

## Acknowledgments

* Original vulnerabilities and exploit: [UltramanGaia](https://github.com/UltramanGaia/Xiaomi_Mi_WiFi_R3G_Vulnerability_POC)
* OpenWRTInvasion: [acecilia](https://github.com/acecilia/OpenWRTInvasion/)
* Instructions to install OpenWrt after exploit execution: [rogerpueyo](https://forum.openwrt.org/t/xiaomi-mi-router-4a-gigabit-edition-r4ag-r4a-gigabit-fully-supported-but-requires-overwriting-spi-flash-with-programmer/36685/21)
* Testing and detailed install instructions: [hey07](https://forum.openwrt.org/t/xiaomi-mi-router-4a-gigabit-edition-r4ag-r4a-gigabit-fully-supported-but-requires-overwriting-spi-flash-with-programmer/36685/349)
* Checking the URL of pending updates: [sicklesareterrible](https://forum.openwrt.org/t/xiaomi-mi-router-4a-gigabit-edition-r4ag-r4a-gigabit-fully-supported-and-flashable-with-openwrtinvasion/36685/1114?u=acecilia)

## Disclaimer

**THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.**
