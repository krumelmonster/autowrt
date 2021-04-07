import logging
import os
import re
import socket
import sys
import time

from logging import Logger

from autowrt.openwrtinvasion import OpenWRTInvasion


class Router:
    logpath: str
    logger: Logger
    logfile: logging.FileHandler
    logstream: logging.Handler

    def __init__(self, config):
        from datetime import datetime

        self._seleniumdriver = None

        self.logpath = os.path.join(config.logdir, datetime.now().isoformat())
        os.makedirs(self.logpath)
        self.logger = logging.getLogger('AutoWRT')

        self.logger.setLevel(logging.DEBUG)
        # create file handler which logs even debug messages
        self.logfile = logging.FileHandler(os.path.join(self.logpath, 'autowrt.log'))
        self.logfile.setLevel(logging.DEBUG)
        # create console handler with a higher log level
        self.logstream = logging.StreamHandler()
        self.logstream.setLevel(logging.INFO)
        # create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logfile.setFormatter(formatter)
        self.logstream.setFormatter(formatter)
        # add the handlers to the logger
        self.logger.addHandler(self.logfile)
        self.logger.addHandler(self.logstream)

        self.config=config
        if not self.config or 'logdir' not in self.config.__dict__:
            self.logger.error("Log Path not configured!")
            exit(123)

        self.logger.info("Logging to {logpath}".format(logpath=self.logpath))
        self.logger.info("Data dir is {imagedir}".format(imagedir=self.config.imagedir))

    @property
    def seleniumdriver(self):
        from selenium import webdriver
        if not self._seleniumdriver:
            options = webdriver.firefox.options.Options()
            options.headless = self.config.headless
            firefox_profile = webdriver.FirefoxProfile()
            firefox_profile.set_preference('intl.accept_languages', 'en')
            self._seleniumdriver = webdriver.Firefox(firefox_profile=firefox_profile, options=options, log_path=os.path.join(self.logpath, 'webdriver.log'))
        return self._seleniumdriver


class Xiaomi(Router):
    def __init__(self, config):
        import random
        super().__init__(config)
        self.ncport = random.randrange(2000, 65500)
        self.router_ip_address = '192.168.31.1'
        self.locale = None
        self.location = self.config.location
        self.password = self.config.password
        self.supported_models={
            'R4AC': {
                'filename_re':'.*ramips-mt76x8-xiaomi_mir4a-100m-.*\\.bin',
                'flashcmd': 'mtd -e OS1 -q write {filename} OS1',
            },
            'R4A': {
                'filename_re':'.*ramips-mt7621-xiaomi_mi(r3g-v2|router-4a-gigabit)-.*\\.bin',
                'flashcmd': 'mtd -e OS1 -q write {filename} OS1',
            },
        }

        assert self.location, self.password

    def _t(self, en, cn):
        if self.locale == 'en':
            return en
        elif self.locale == 'cn':
            return cn
        else:
            raise

    def loadRouter(self, driver):
        try:
            driver.get("http://" + self.router_ip_address)
        except Exception:
            self.logger.debug("Failed attempt at loading router start page")
        return driver.title == "Mi Router" or driver.title == '小米路由器'

    def _load_webinterface(self):
        from selenium.webdriver.support.wait import WebDriverWait

        driver = self.seleniumdriver
        driver.set_page_load_timeout(5)

        self.logger.info("Trying to access router web page at {}:".format(self.router_ip_address))

        # FIXME: Why was this here?!
        # driver.refresh()

        # TODO: Disable retry in config for fast model detection?
        WebDriverWait(driver, 120, 2).until(lambda driver: self.loadRouter(driver))

        if driver.title == '小米路由器':
            self.locale = 'cn'
            self.logger.info("Detected Xiaomi Router Chinese Edition "
                             "(possibly xiaomi_mi_router_4a_100m or xiaomi_mi_router_4a_gigabit?)")
        else:
            self.locale = 'en'
            self.logger.info("Detected Xiaomi Router Global Edition "
                             "(possibly xiaomi_mi_router_4a_100m or xiaomi_mi_router_4a_gigabit?)")

    def _setup_router(self):
        from selenium.webdriver.common.keys import Keys
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.wait import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        import time

        self.logger.info("Starting router configuration")

        driver = self.seleniumdriver
        locale = self.locale
        t = self._t

        wait = WebDriverWait(driver, 30)

        # TODO: improve code quality
        click = driver.find_element_by_link_text(t('Click to select>', '《用户许可使用协议》'))

        if locale == 'en':
            click.click()

            elem = driver.find_element_by_name("input")
            elem.clear()
            elem.send_keys(self.location)

            click = driver.find_element_by_xpath("//span[.='" + self.location + "']")
            assert click
            click.click()

            click = driver.find_element_by_xpath("//button[.='Next']")
            assert click
            click.click()

        check = driver.find_element_by_name("protocal")
        assert check
        if not check.is_selected():
            check.click()

        click = driver.find_element_by_class_name("join")
        assert click
        click.click()

        click = wait.until(lambda driver: driver.find_element_by_link_text(
            t("Continue setup without connecting a network cable", '不插网线，继续配置')))
        click.click()

        text = t('Static IP', '静态IP')
        try:
            click = driver.find_element_by_xpath("//span[.='" + text + "']")
        except:
            click = driver.find_element_by_xpath("//li[.='" + text + "']")
        click.click()
        driver.find_element_by_class_name("button").click()

        wait.until(lambda driver: driver.find_element_by_name("ip"))
        elem = driver.find_element_by_name("ip")
        elem.clear()
        elem.send_keys("192.168.32.2")
        elem = driver.find_element_by_name("mask")
        elem.clear()
        elem.send_keys("255.255.255.0")
        elem = driver.find_element_by_name("gateway")
        elem.clear()
        elem.send_keys("192.168.32.1")
        elem = driver.find_element_by_name("dns1")
        elem.clear()
        elem.send_keys("192.168.32.1")
        driver.find_element_by_class_name("button").click()

        # wait.until(lambda driver: driver.find_element_by_name("password"))
        # elem = driver.find_element_by_name("password")
        elem = wait.until(EC.element_to_be_clickable((By.NAME, "password")))
        elem.clear()
        elem.send_keys(self.password)
        elem.send_keys(Keys.RETURN)

        WebDriverWait(driver, 120, 2).until(lambda driver: driver.find_element_by_xpath(
            "//p[.='" + t('Setup complete, Wi-Fi restarting', '配置完成，WiFi重启中') + "']"))
        self.logger.info("Router successfully set up!")
        time.sleep(10)
        #driver.get("http://" + self.router_ip_address)
        WebDriverWait(driver, 120, 2).until(lambda driver: self.loadRouter(driver))

    def _login(self):
        from selenium.webdriver.support.wait import WebDriverWait
        from selenium.webdriver.common.keys import Keys
        from selenium.webdriver.support import expected_conditions
        from selenium.webdriver.common.by import By
        import re

        driver = self.seleniumdriver
        wait = WebDriverWait(driver, 30)

        elem = wait.until(expected_conditions.element_to_be_clickable((By.NAME, "router_password")))
        assert elem
        elem.clear()
        elem.send_keys(self.password)
        elem.send_keys(Keys.RETURN)
        wait.until(lambda driver: driver.current_url != "http://" + self.router_ip_address + "/cgi-bin/luci/web")
        self.logger.info("Logged into Webinterface at {}".format(driver.current_url))

        url = driver.current_url
        # url='http://192.168.31.1/cgi-bin/luci/;stok=f7688cc83517d6d7c907e3ceed8d5dc6/web/home#router'
        reg = '^http://' + self.router_ip_address + '/cgi-bin/luci/;stok=([a-f0-9]+).*$'
        stok = re.sub(reg, r"\1", url)
        assert stok
        return stok

    def install_openwrt(self):
        from autowrt.nccli import NcCli, Multiwriter
        from autowrt.util import md5sum, sha256sum
        t = self._t

        self.logger.info("Xiaomi-Module started, loading Selenium driver")

        driver = self.seleniumdriver
        driver.set_page_load_timeout(5)

        self._load_webinterface()

        click = None
        try:
            click = driver.find_element_by_link_text(t('Click to select>', '《用户许可使用协议》'))
        except Exception:
            self.logger.warning("Router already set up? Skipping setup")
        if (click):
            self._setup_router()

        stok = self._login()

        wrti = OpenWRTInvasion(self.router_ip_address, self.ncport, self.logger)
        shellsock = wrti.run(stok)

        # FIXME: seleniumdriver should now be set to None
        driver.close()
        if not shellsock:
            self.logger.info("Consider to reboot your device or file a bug report")
            exit(-1)
        cli = NcCli(shellsock)

        delim = 'erqUHgKWCzI0vO7g'
        cli.run('PS1=' + delim + ';echo;echo AutoWRT is ready!')
        self.logger.debug(cli.result(delim))
        #self.logger.info("Shell is ready, fetching some info to {}".format(os.path.join(os.getcwd(), self.logpath)))


        #####
        cli.run("nvram show")
        nvram = cli.result(delim)

        with open(os.path.join(self.logpath, 'nvram'), 'x') as fd:
            fd.write(nvram)
        reg = '^model=([a-zA-Z0-9_-]+)$'
        modelname = re.findall(reg, nvram, flags=re.MULTILINE)[0]

        self.logger.info("Router model detected as {modelname}".format(modelname=modelname))
        if modelname not in self.supported_models:
            self.logger.error('Router "{modelname}" not currently supported.'.format(modelname=modelname))
            exit(123)

        if modelname not in self.config.models:
            self.logger.error('No image is configured for Router "{modelname}".'.format(modelname=modelname))
            exit(123)

        model = self.config.models[modelname]
        if 'filename' not in model or 'checksum' not in model:
            self.logger.error('No image is configured for Router "{modelname}".'.format(modelname=modelname))
            exit(123)

        if not re.fullmatch(self.supported_models[modelname]['filename_re'], model['filename']):
            self.logger.warning('Unexpected filename for {modelname}. Expected {filename_re} but got {filename}'
                                .format(
                                    modelname=modelname,
                                    filename_re=self.supported_models[modelname]['filename_re'],
                                    filename=model['filename']))

            if 'ignorename' not in model or not model['ignorename']:
                self.logger.error('Got an unexpected filename and the ignorename option is not set. Exiting')
                exit(123)

        imagefile = os.path.join(self.config.imagedir, model['filename'])
        if not os.path.isfile(imagefile):
            self.logger.error('The image file could not be found at {} as configured in config.py'.format(imagefile))
            exit(123)
        if model['checksum'] != 'IGNORE' or model['checksum'] != 'SKIP':
            hash_file = sha256sum(imagefile)
            if hash_file != model['checksum']:
                self.logger.error(
                    "The image file you supplied doesn't match the checksum listed in your config.")
                exit(123)
        else:
            self.logger.warning("The image checksum is set to IGNORE. It is recommended to supply a sha256 checksum "
                                "as given on the OpenWRT download page.")

        if self.config.sysinfo:
            self.logger.info("Save some command outputs in directory \"{}\"".format(self.logpath))
            commands = [
                ('dmesg', 'dmesg'),
                ('uname -a', 'uname_-a'),
                ('cat /proc/cpuinfo', 'cpuinfo'),
                ('for i in /sys/class/mtd/mtd*/*;do echo "$i"; cat "$i" 2> /dev/null;done', 'class-mtd'),
                #('nvram show', 'nvram')
            ]

            for command, filename in commands:
                self.logger.info(" {}".format(command))
                with open(os.path.join(self.logpath, filename), 'xb') as fd:
                    cli.run(command + ' 2> errorpipe')
                    cli.write_result(fd, delim)

                cli.run('echo $?')
                retval = cli.result(delim)

                ph=Multiwriter(textwriters=[sys.stderr])
                cli.run('cat errorpipe')
                cli.write_result(ph, delim)

                if retval != '0\n':
                    self.logger.error("Command {} returned nonzero exit code".format(command))

        if self.config.mtdbackup:
            self.logger.info("Start backup of the mtd")

            cli.run("cat /proc/mtd")
            mtddesc = cli.result(delim)

            with open(os.path.join(self.logpath, 'mtd'), 'x') as fd:
                fd.write(mtddesc)

            reg = '\n(mtd[0-9]+): ([0-9a-f]+) ([01]+) "([a-zA-Z0-9_]+)"'
            result = re.findall(reg, mtddesc)
            for dev, size, erasesize, name in result:
                command = "dd if=/dev/{dev}ro 2>/dev/null".format(dev=dev)
                filename = "{dev}_{name}.backup".format(dev=dev, name=name)
                self.logger.info("Back up {dev} to {filename} size {size}".format(dev=dev, filename=filename, size=size))
                with open(os.path.join(self.logpath, filename), 'xb') as fd:
                    cli.run(command)
                    cli.write_result(fd, delim)

            for dev, size, erasesize, name in result:
                command = "md5sum /dev/{dev}ro 2> /dev/null".format(dev=dev)
                filename = "{dev}_{name}.backup".format(dev=dev, name=name)
                self.logger.info("Verify {filename}".format(filename=filename))
                cli.run(command)
                localsum=md5sum(os.path.join(self.logpath, filename))
                remotesum=cli.result(delim)[:32]
                if localsum != remotesum:
                    self.logger.warning("{filename} failed the checksum verification against md5sum /dev/{dev}ro "
                                      "'{localsum}'/'{remotesum}'"
                                      .format(filename=filename, dev=dev, localsum=localsum, remotesum=remotesum))

            self.logger.info("Backups are done, now upload OpenWRT-Image")

        #FIXME: RCE
        self.logger.info("Uploading image '{}'...".format(model['filename']))
        port=self.ncport+1
        cli.run("nc -lp {port} > '{filename}'".format(port=port, filename=model['filename']))
        time.sleep(3)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as filesock:
            filesock.connect((self.router_ip_address, port))
            with open(imagefile, 'rb') as f:
                filesock.send(f.read())
            filesock.shutdown(socket.SHUT_WR)

        cli.result(delim)
        self.logger.info("Verifying image '{}'...".format(model['filename']))
        cli.run("md5sum '{}' 2> /dev/null".format(model['filename']))
        localsum=md5sum(imagefile)
        remotesum=cli.result(delim)[:32]
        if localsum != remotesum:
             self.logger.warning("Failed to upload {} (checksum)".format(model['filename']))
             exit(123)

        self.logger.info("Image verification succeeded")
        with open(os.path.join(self.logpath, 'mtd-write-log'),'xb') as fd:
            ph=Multiwriter(textwriters=[sys.stderr], binarywriters=[fd])
            flashcmd='nohup '+self.supported_models[modelname]['flashcmd'].format(filename=model['filename'])
            self.logger.info("Installing OpenWRT NOW!..")
            self.logger.info(flashcmd)
            cli.run(flashcmd)
            cli.write_result(ph, delim)

        cli.run('echo $?')
        retval = cli.result(delim)
        if retval != '0\n':
            self.logger.error("OpenWRT installation seems to have failed, this is bad!")
            self.logger.info("Please recover manually using a shell: nc {} 4445".format(self.router_ip_address))
            cli.run('mkfifo em; cat em|/bin/sh -si 2>&1|nc -lp 4445 >em')
            cli.result(delim)
            self.logger.info("The shell was quit. bye")
            exit(123)

        self.logger.info("OpenWRT-Installation was successful, rebooting device...")
        cli.run('reboot')
        cli.result(delim)