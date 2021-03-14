from autowrt.router import Xiaomi
import os, sys


def main(imagedir: str = None, confpath: str = None, logdir: str = None):
    confpath = confpath or os.getcwd()
    imagedir = imagedir or os.getcwd()
    logdir = logdir or os.getcwd()
    confscript=os.path.join(confpath, 'config.py')
    if not os.path.isfile(confscript):
        print("Please copy config.py to {} and adjust to your needs!".format(confscript), file=sys.stderr)
    oldpath=sys.path
    sys.path.insert(0,confpath)
    import config
    sys.path=oldpath

    config.config.logdir=os.path.join(logdir, config.config.logdir)
    config.config.imagedir=os.path.join(imagedir, config.config.imagedir)

    xiaomi = Xiaomi(config.config)
    xiaomi.install_openwrt()


if __name__ == '__main__':
    from appdirs import *
    appname = "autowrt"
    appauthor = "krumelmonster"
    main(
        imagedir=user_data_dir(appname, appauthor),
        confpath=user_config_dir(appname, appauthor),
        logdir=user_log_dir(appname, appauthor)
    )
