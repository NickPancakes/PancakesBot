# PancakesBot
IRC Bot written in Python 3 with [circuits](https://github.com/circuits/circuits).
Inspired by [kdb](https://github.com/prologic/kdb), [Cardinal](https://github.com/JohnMaguire/Cardinal), and [mIRC](http://www.mirc.com/) Scripting, PancakesBot is designed to be simple to create plugins for.

##Requirements
[Python 3.5](https://www.python.org/downloads/)
Latest git revision of [circuits](https://github.com/circuits/circuits).
Circuits Installation:
```
git clone https://github.com/circuits/circuits.git
cd circuits
sudo python3 setup.py install
```

##Running
Simply edit *config.json* to suit your needs and then run with `python3 main.py` in whatever folder you cloned into.
Plugins can be loaded and unloaded live with the *admin* plugin, but the commands will only respond to the designated admin user id. See *plugins/admin.py* for details.


##Writing Plugins
The *example* plugin provided displays most functionality, including how to capture events and use the basic functions built into *BasePlugin*. More details coming soon.
