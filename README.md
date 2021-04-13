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

