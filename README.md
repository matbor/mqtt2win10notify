# mqtt2win10notify

Quick example, proof of concept for displaying mqtt messages in  windows.

Based on example from; https://github.com/jithurjacob/Windows-10-Toast-Notifications
and inspired by https://github.com/jpmens/mqttwarn/pull/160

Requires a json message formatted like this 
```{"sub":"subject","txt":"text"}```

To be sent to the topic, however it will fall back to displaying just the message if no json message is found.

Can be run in the background if needed, just use ```pythonw.exe mqtt_notification.py```

Works on Windows 10 with Python 2.7. Requires;
- pywin32, http://sourceforge.net/projects/pywin32/ 
- pahoo-mqtt, http://www.eclipse.org/paho/

Example;
```mosquitto_pub -h mosquitto.org -t 'test/messages' -m '{"sub": "7NewsMelbourne", "txt": "RT @BrendanDonohoe7: Ambulance Vic hopes to move 100,000 patients to other care providers. Filter out non urgent cases."}'```

![balloon](https://raw.githubusercontent.com/matbor/mqtt2win10notify/master/assets/balloon.png)

![center](https://raw.githubusercontent.com/matbor/mqtt2win10notify/master/assets/action%20center.png)
