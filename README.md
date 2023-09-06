# kb
A little bit of everything

Software for data visualization
Graphviz - https://graphviz.org/
Gephi - https://gephi.org/

# Selenium

## Headless and hover

If you have a script that cannot be used with headless because you need hover, you might need a graphical interface in your server. To do so without installing a window manager like gnome of kde, you can use Xvfb.

```shellscript
#!/bin/bash
pkill -f "Xvfb :99 -ac"
Xvfb :99 -ac &
export DISPLAY=:99
./yourscript.py
pkill -f "Xvfb :99 -ac"
```

# Clonezilla

Decompressing and mounting a clonezilla backup file

```
cat sdb1.ntfs-ptcl-img.gz.* | gunzip | partclone.restore --restore_raw_file -C -s - -o sdb1.ntfs.img
mount /dev/sdb1 /mnt/sdb1
```

# Windows

Manually configuring windows 11 ntp servers

```
net stop w32time
w32tm /config /syncfromflags:manual /manualpeerlist:"0.it.pool.ntp.org 1.it.pool.ntp.org 2.it.pool.ntp.org 3.it.pool.ntp.org"
net start w32time
w32tm /config /update
w32tm /resync /rediscover
```
