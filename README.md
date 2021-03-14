## Summary

AutoWRT is a python application to excecute handsfree out-of-the-box installation of OpenWRT. It currently supports the Xiaomi 4A Gigabit and Xiaomi 4A 100m Routers via an [OpenWRTInvasion](https://github.com/acecilia/OpenWRTInvasion)-based exploit. Support for the Xiaomi 3Gv1 and Redmi RC2100 is planned to be implemented soon.

## Installation

`appdirs`, `requests` and `selenium` python packages as well as geckodriver are required. It is recommended not to install autowrt as a package but rather to install its dependencies, clone this repository, download your openwrt images, adjust `config.py` in the root directory accordingly and then run autowrt.py.

If you choose to install autowrt as a package, you will have to copy `config.py` to the configuration directory, on linux this will be `~/.config/autowrt` .

## Disclaimer

**THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.**
