class config:
    location = 'Germany'
    password = 'Not a safe password'
    imagedir = 'images'
    logdir = 'log'
    headless = True
    sysinfo = True
    mtdbackup = True

    models = {
        'R4AC': {
            # https://downloads.openwrt.org/releases/19.07.7/targets/ramips/mt76x8/
            'filename': "openwrt-19.07.7-ramips-mt76x8-xiaomi_mir4a-100m-squashfs-sysupgrade.bin",
            'checksum': '2f71104f35a4be7c9781e4091519e51267f17594f134d737eb97681a3ef3d126',
            },
        'R4A': {
            # https://github.com/araujorm/openwrt/releases/tag/v19.07-xiaomi-miwifi-3gv2-mt76updated-2021-02-02
            'filename': "openwrt-ramips-mt7621-xiaomi_mir3g-v2-squashfs-sysupgrade.bin",
            'checksum': '6b2cc16be173069adb50cc1dd6aa055482e35521ef789c83fae05759b4fa913c',
            },
        }
