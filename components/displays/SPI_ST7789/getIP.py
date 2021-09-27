
HOMEPATH = "/home/pi/RPi-Jukebox-RFID"
with open(f"{HOMEPATH}/settings/PhonieboxInstall.conf", 'r') as conf:
    for line in conf:
        if "WIFIip=" in line:
            IP = line.replace("\n", "").replace("WIFIip=", "").strip('"')
    print(IP)
