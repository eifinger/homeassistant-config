<h1 align="center">
  <a name="logo" href=""><img src="https://github.com/eifinger/homeassistant-config/blob/master/www/images/logo-round-192x192.png?raw=true" alt="Home Assistant Logo" width="192"></a>
  <br>
  My Home Assistant Configuration
</h1>
<h4 align="center">Be sure to :star: my repo so you can keep up to date on the daily progress!.</h4>
<div align="center">
  <h4>
    <a href="https://github.com/eifinger/homeassistant-config/workflows/Home%20Assistant%20Installed/badge.svg"><img src="https://github.com/eifinger/homeassistant-config/workflows/Home%20Assistant%20Installed/badge.svg"/></a>
    <a href="https://github.com/eifinger/homeassistant-config/stargazers"><img src="https://img.shields.io/github/stars/eifinger/homeassistant-config.svg?style=plasticr"/></a>
    <a href="https://github.com/eifinger/homeassistant-config/commits/master"><img src="https://img.shields.io/github/last-commit/eifinger/homeassistant-config.svg?style=plasticr"/></a>
  </h4>
</div>
<p><font size="3">
This Repo is designed for Smart Home inspiration.  The configuration, devices and layout should help inspire you to jump head first into the IOT world.  This is the live working configuration of <strong>my Smart Home</strong>. Use the menu links to jump between sections.  All of the code is free to use and contribute to. This readme is based on the great documentation of <a href="https://github.com/CCOSTAN/Home-AssistantConfig/blob/master/README.md">CCOSTAN</a>

This repository is a companion to my [appdeamon-scripts](https://github.com/eifinger/appdaemon-scripts) where all my automations are.</p>

![Screenshot of Home Assistant Header](https://i.imgur.com/vjDH1LJ.png)
<hr>

#### <a name="software"></a>Notable Software making up my Smart Home System:

* [Docker](https://Docker.com) - Docker runs on a Ubuntu Server compose file at the bottom
* [Home Assistant Container](https://hub.docker.com/r/homeassistant/home-assistant/) - It all starts here
* DDNS via [Strato](https://www.strato.de/)
* SSL via [letsencrypt](https://letsencrypt.org/) - Support a more secure and privacy-respecting Web
* Indoor positioning with [find3](https://www.internalpositioning.com/) - Machine Learning tells your phone location without any other hardware
* MQTT Broker [mosquitto-docker](https://hub.docker.com/_/eclipse-mosquitto/)
* [Face Recognition Container](https://hub.docker.com/r/eifinger/face_recognition) - Forked from [JanLoebel](https://github.com/JanLoebel/face_recognition)
* [MySQL Docker](https://hub.docker.com/_/mysql/)
* [Appdaemon](https://github.com/eifinger/appdaemon) - See my Appdaemon scripts [here](https://github.com/eifinger/appdaemon-scripts)
* HAASKA [Haaska-repo](https://github.com/mike-grant/haaska) - Alexa Smarthome V3 API for all your HA devices
* Tasmota [Tasmota-repo](https://github.com/arendst/Sonoff-Tasmota) - Custom Firmware for ESP8266 devices offering MQTT and much more.
* Raspberry Pi running [PiHole](https://pi-hole.net/) - DNS Server and AdBlocker
* [hassalarm](https://github.com/Johboh/hassalarm) - link my android alarms to HA

![diagram](http://www.plantuml.com/plantuml/proxy?cache=no&src=https://raw.github.com/eifinger/homeassistant-config/master/www/plantuml/homeassistant-architecture.puml&fmt=svg)

<a name="devices"></a>
<div align="center">
  <h4>
    <a href="https://github.com/eifinger/homeassistant-config#networking">
      Networking / Server
    </a>
    <span> | </span>
    <a href="https://github.com/eifinger/homeassistant-config#alexa">
      Alexa
    </a>
    <span> | </span>
    <a href="https://github.com/eifinger/homeassistant-config#voice">
      Voice
    </a>
    <span> | </span>
    <a href="https://github.com/eifinger/homeassistant-config#hubs">
      Hubs
    </a>
    <span> | </span>
    <a href="https://github.com/eifinger/homeassistant-config#lights">
      Lights
    </a>
    <span> | </span>
    <a href="https://github.com/eifinger/homeassistant-config#switches">
      Switches
    </a>
    <span> | </span>
    <a href="https://github.com/eifinger/homeassistant-config#cameras">
      Cameras
    </a>
    <span> | </span>
    <a href="https://github.com/eifinger/homeassistant-config#streaming">
      TV Streaming
    </a>
    <span> | </span>
    <a href="https://github.com/eifinger/homeassistant-config#sensors">
      Sensors
    </a>
    <span> | </span>
    <a href="https://github.com/eifinger/homeassistant-config#climate">
      Climate
    </a>
    <span> | </span>
    <a href="https://github.com/eifinger/homeassistant-config#compose">
      docker-compose.yaml
    </a>
    <span> | </span>
    <a href="https://github.com/eifinger/homeassistant-config#screenshots">
      Screenshots
    </a>
  </h4>
</div>

<table align="center" border="0">
<tr><td colspan="4">

#### Networking / Server <a name="networking" href="https://github.com/eifinger/homeassistant-config#networking"><img align="right" border="0" src="https://raw.githubusercontent.com/eifinger/homeassistant-config/master/www/images/up_arrow.png" width="22"> </a>
</td></tr>
<tr><td align="center" colspan="1">

[AVM FRITZ!Box 7490](https://amzn.to/2NWAoSi)
</td><td align="center" colspan="1">

[Ubiquiti Networks UAP-AC-PRO](https://amzn.to/2RkaKww)
</td><td align="center" colspan="1">

[Ubiquiti USG](https://amzn.to/2HjGfS5)
</td><td align="center" colspan="1">

[HP Microserver Gen10](https://amzn.to/2DmHPRf)
</td></tr>
<tr><td align="center" colspan="1"><a href="https://www.amazon.de/AVM-Router-DECT-Basis-geeignet-Deutschland/dp/B00EO777DI/ref=as_li_ss_il?s=computers&ie=UTF8&qid=1536327184&sr=1-1-spons&keywords=fritzbox+7490&psc=1&linkCode=li1&tag=kevineifinger-21&linkId=07a0c1999ece256ed8ae69ae6ccef04d&language=de_DE" target="_blank"><img border="0" src="https://images-eu.ssl-images-amazon.com/images/I/41Y51Zr3ngL.jpg" width="100" height="100"></a><img src="https://ir-de.amazon-adsystem.com/e/ir?t=kevineifinger-21&language=de_DE&l=li1&o=3&a=B00EO777DI" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />
</td><td align="center" colspan="1"><a href="https://www.amazon.de/Ubiquiti-UAP-AC-PRO-Networks-wei%C3%9F/dp/B016XYQ3WK/ref=as_li_ss_il?ie=UTF8&qid=1547046545&sr=8-2&keywords=unifi+ap&linkCode=li1&tag=kevineifinger-21&linkId=4ac94e88d228472e5b7ab3cec4cb99ee&language=de_DE" target="_blank"><img border="0" src="https://ws-eu.amazon-adsystem.com/widgets/q?_encoding=UTF8&ASIN=B016XYQ3WK&Format=_SL110_&ID=AsinImage&MarketPlace=DE&ServiceVersion=20070822&WS=1&tag=kevineifinger-21&language=de_DE" ></a><img src="https://ir-de.amazon-adsystem.com/e/ir?t=kevineifinger-21&language=de_DE&l=li1&o=3&a=B016XYQ3WK" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />
</td><td align="center" colspan="1"><a href="https://www.amazon.de/Ubiquiti-USG-Netzwerk-Gigabit-Ethernet-Ports-UniFi-Controller/dp/B00LV8YZLK/ref=as_li_ss_il?__mk_de_DE=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=3GCDKBYM1FMPY&keywords=usg+ubiquiti&qid=1552575266&s=gateway&sprefix=usg,aps,177&sr=8-1&linkCode=li1&tag=kevineifinger-21&linkId=9091365635548ef03d65dfb06163c713&language=de_DE" target="_blank"><img border="0" src="https://ws-eu.amazon-adsystem.com/widgets/q?_encoding=UTF8&ASIN=B00LV8YZLK&Format=_SL110_&ID=AsinImage&MarketPlace=DE&ServiceVersion=20070822&WS=1&tag=kevineifinger-21&language=de_DE" ></a><img src="https://ir-de.amazon-adsystem.com/e/ir?t=kevineifinger-21&language=de_DE&l=li1&o=3&a=B00LV8YZLK" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />
</td><td align="center" colspan="1"><a href="https://www.amazon.de/ProLiant-MicroServer-Hot-Plug-f%C3%A4hig-200-W-Netzteil-Einstiegsserver/dp/B072X2YJ2N/ref=as_li_ss_il?_encoding=UTF8&pd_rd_i=B072X2YJ2N&pd_rd_r=9aa43e3f-e0fe-11e8-9a86-056d0d37c5cd&pd_rd_w=xb4Yt&pd_rd_wg=oVBqF&pf_rd_i=desktop-dp-sims&pf_rd_m=A3JWKAKR8XB7XF&pf_rd_p=51bcaa00-4765-4e8f-a690-5db3c9ed1b31&pf_rd_r=0F177YEG4J1VA3R23QV6&pf_rd_s=desktop-dp-sims&pf_rd_t=40701&psc=1&refRID=0F177YEG4J1VA3R23QV6&linkCode=li1&tag=kevineifinger-21&linkId=97434f67b4777536cc0c07309f06324c&language=de_DE" target="_blank"><img border="0" src="https://ws-eu.amazon-adsystem.com/widgets/q?_encoding=UTF8&ASIN=B072X2YJ2N&Format=_SL110_&ID=AsinImage&MarketPlace=DE&ServiceVersion=20070822&WS=1&tag=kevineifinger-21&language=de_DE" ></a><img src="https://ir-de.amazon-adsystem.com/e/ir?t=kevineifinger-21&language=de_DE&l=li1&o=3&a=B072X2YJ2N" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />
</td></tr>
<tr><td colspan="4">

Using a Fritzbox as this is one of the official supported modems for Telekom. The rest is running on Ubiquiti. Rock solid and fun to use.

As a server running Homeassistant and everything else I use a HP Microserver Gen 10.

*Click on the sections to expand them* 
<details>
  <summary>Notify if an unkown device is found on the network</summary><p align="center">
  <a href=https://github.com/eifinger/appdaemon-scripts#newwifidevicenotify>
  Appdaemon App - newWifiDeviceNotify</a><br>
<p></details>
<details>
  <summary>Allow a device internet access via Telegram Bot (Fritzbox only)</summary><p align="center">
  <a href=https://github.com/eifinger/appdaemon-scripts#newwifidevicenotify>
  Appdaemon App - newWifiDeviceNotify</a><br>
<p></details>
</td></tr>

<tr><td colspan="4">

#### Alexa Echo Devices<a name="alexa" href="https://github.com/eifinger/homeassistant-config#devices"><img align="right" border="0" src="https://raw.githubusercontent.com/eifinger/homeassistant-config/master/www/images/up_arrow.png" width="22" ></a>
</td></tr>
<tr><td align="center" colspan="4">

[Amazon Echo DOT](https://amzn.to/2wTfsFj)
</td></tr>

<tr><td align="center"colspan="4"><a href="https://www.amazon.de/dp/B01DFKBG54/ref=as_li_ss_il?ref=spkl_6_2_30ea6d6a-e1ad-4aff-ad16-1fd8883a90ad&qid=1536328708&pf_rd_p=30ea6d6a-e1ad-4aff-ad16-1fd8883a90ad&pf_rd_m=A1PA6795UKMFR9&pf_rd_t=301&pf_rd_s=desktop-auto-sparkle&pf_rd_r=X0VVHP8J5XRHQCMK7TX9&pf_rd_i=echo+dot+2&linkCode=li1&tag=kevineifinger-21&linkId=73d4776542a81675ba804d0e8197dd4f&language=de_DE" target="_blank"><img border="0" src="https://ws-eu.amazon-adsystem.com/widgets/q?_encoding=UTF8&ASIN=B01DFKBG54&Format=_SL110_&ID=AsinImage&MarketPlace=DE&ServiceVersion=20070822&WS=1&tag=kevineifinger-21&language=de_DE" ></a><img src="https://ir-de.amazon-adsystem.com/e/ir?t=kevineifinger-21&language=de_DE&l=li1&o=3&a=B01DFKBG54" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />
</td></tr>

<tr><td colspan="4">

The Alexa devices in my house are for automation overrides.  They are primarily an input device into Home Assistant.  Using [haaska](https://github.com/mike-grant/haaska), I am able to turn on /off most HA devices even if they don't have native Alexa support. I use them for Multiroom Audio and some custom skills.

*Click on the sections to expand them* 
<details>
<summary>Alexa tell Homeassistant to turn off Ventilator in 10 Minutes</summary><p align="center">
<a href=https://github.com/eifinger/appdaemon-scripts/tree/master/alexa#turnentityoffinx>
Appdaemon App - turnEntityOffInX</a><br>
<p></details>
<details>
<summary>Alexa ask Home Assistant whether all windows are closed</summary><p align="center">
<a href=https://github.com/eifinger/appdaemon-scripts/blob/master/alexa/README.md#windowsopen>
Appdaemon App - windowsOpen</a><br>
<p></details>
<details>
<summary>Alexa ask Home Assistant when the next bus departs</summary><p align="center">
<a href=https://github.com/eifinger/appdaemon-scripts/blob/master/alexa/README.md#nextbusintent>
Appdaemon App - nextBusIntent</a><br>
<p></details>
<details>
<summary>Turn on Receiver Bluetooth when Alexa is playing something so it plays on the big speakers.</summary><p align="center">
<a href=https://github.com/eifinger/appdaemon-scripts#alexaspeakerconnector>
Appdaemon App - alexaSpeakerConnector</a><br>
<p></details>
</details>
</td></tr>

<tr><td colspan="4">

#### Voice Notifications - [Appdaemon App - Notifier](https://github.com/eifinger/appdaemon-scripts#notify)<a name="voice" href="https://github.com/eifinger/homeassistant-config#devices"><img align="right" border="0" src="https://raw.githubusercontent.com/eifinger/homeassistant-config/master/www/images/up_arrow.png" width="22" ></a>
</td></tr>
<tr><td align="center" colspan="2">

[Denon AVRX1300W](https://amzn.to/2NYT6sR)
</td><td align="center" colspan="2">

[TP-Link Smart Plug](https://amzn.to/2wPNJ7F)
</td></tr>

<tr><td align="center" colspan="2"><a href="https://www.amazon.de/Denon-AVRX1300WBKE2-7-2-Kanal-AV-Receiver-Bluetooth/dp/B01GQ85GW6/ref=as_li_ss_il?s=computers&ie=UTF8&qid=1536329265&sr=8-2&keywords=denon+avr+x1300&linkCode=li1&tag=kevineifinger-21&linkId=c0677ebccc90d28fec772d2f5bdec65f&language=de_DE" target="_blank"><img border="0" src="https://ws-eu.amazon-adsystem.com/widgets/q?_encoding=UTF8&ASIN=B01GQ85GW6&Format=_SL110_&ID=AsinImage&MarketPlace=DE&ServiceVersion=20070822&WS=1&tag=kevineifinger-21&language=de_DE" ></a><img src="https://ir-de.amazon-adsystem.com/e/ir?t=kevineifinger-21&language=de_DE&l=li1&o=3&a=B01GQ85GW6" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />
</td><td align="center" colspan="2"><a href="https://www.amazon.de/TP-Link-Steckdose-Stromverbrauchsaufzeichnung-funktionieren-erforderlich/dp/B017X72IES/ref=as_li_ss_il?s=computers&ie=UTF8&qid=1536329452&sr=1-1&keywords=hs110&linkCode=li1&tag=kevineifinger-21&linkId=25d7083477f36e734235264c18a3bccc&language=de_DE" target="_blank"><img border="0" src="https://ws-eu.amazon-adsystem.com/widgets/q?_encoding=UTF8&ASIN=B017X72IES&Format=_SL110_&ID=AsinImage&MarketPlace=DE&ServiceVersion=20070822&WS=1&tag=kevineifinger-21&language=de_DE" ></a><img src="https://ir-de.amazon-adsystem.com/e/ir?t=kevineifinger-21&language=de_DE&l=li1&o=3&a=B017X72IES" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />
</td></tr>

<tr><td colspan="4">

I am using the great [Alexa TTS Component](https://github.com/keatontaylor/custom_components) by [keatontaylor](https://github.com/keatontaylor) to let Alexa notify me of everything when I am home.

*Click on the sections to expand them*
<details>
<summary>Voice announcements whenever someone comes home.</summary><p align="center">
<a href=https://github.com/eifinger/appdaemon-scripts#homearrivalnotifier>
Appdaemon App -  homeArrivalNotifier</a><br>
</details>
<details>
<summary>Notify if a user is leaving a zone after being there for a certain amount of time.</summary><p align="center">
<a href=https://github.com/eifinger/appdaemon-scripts#leavingzonenotifier>
Appdaemon App -  leavingZoneNotifier</a><br>
</details>
<br>
Once you can teach your house to talk, you just keep expanding on it's vocabulary. It's addicting. :)
</td></tr>

<tr><td colspan="4">

#### Various Hubs<a name="hubs" href="https://github.com/eifinger/homeassistant-config#devices"><img align="right" border="0" src="https://raw.githubusercontent.com/eifinger/homeassistant-config/master/www/images/up_arrow.png" width="22" ></a>
</td></tr>
<tr><td align="center">

[Xiaomi Mi Smart Home Hub](https://amzn.to/2yLtslM)
</td><td align="center">

[RM Mini3 by Broadlink](https://amzn.to/2DhWltn)
</td><td align="center" colspan="2">

[RM Pro by Broadlink](https://amzn.to/2yKO5OO)

<tr><td align="center"><a href="https://www.amazon.de/Control-mehrzweckger%C3%A4te-16-Millionen-intelligente-Verbindung/dp/B079L1F96D/ref=as_li_ss_il?ie=UTF8&qid=1541146761&sr=8-8&keywords=xiaomi+smart+home&linkCode=li2&tag=kevineifinger-21&linkId=e33fb59bf6778f7ab8eba9b913053fbc&language=de_DE" target="_blank"><img border="0" src="https://ws-eu.amazon-adsystem.com/widgets/q?_encoding=UTF8&ASIN=B079L1F96D&Format=_SL160_&ID=AsinImage&MarketPlace=DE&ServiceVersion=20070822&WS=1&tag=kevineifinger-21&language=de_DE" ></a><img src="https://ir-de.amazon-adsystem.com/e/ir?t=kevineifinger-21&language=de_DE&l=li2&o=3&a=B079L1F96D" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />
</td><td align="center"><a href="https://www.amazon.de/Broadlink-Universal-Fernbedienung-iPhone-Android-schwarz/dp/B0786KVWYF/ref=as_li_ss_il?ie=UTF8&qid=1541147339&sr=8-1&keywords=rm+mini3&linkCode=li2&tag=kevineifinger-21&linkId=967b52cfbd9d2e89adfe6a54f24e7428&language=de_DE" target="_blank"><img border="0" src="https://ws-eu.amazon-adsystem.com/widgets/q?_encoding=UTF8&ASIN=B0786KVWYF&Format=_SL160_&ID=AsinImage&MarketPlace=DE&ServiceVersion=20070822&WS=1&tag=kevineifinger-21&language=de_DE" ></a><img src="https://ir-de.amazon-adsystem.com/e/ir?t=kevineifinger-21&language=de_DE&l=li2&o=3&a=B0786KVWYF" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />
</td><td align="center" colspan="2"><a href="https://www.amazon.de/Broadlink-Automation-Universal-Compatible-Smartphones/dp/B06XQRMJ46/ref=as_li_ss_il?ie=UTF8&qid=1541147389&sr=8-1&keywords=rm+pro+3&linkCode=li2&tag=kevineifinger-21&linkId=a4a2167a61548bb0a23fbae93a5d880f&language=de_DE" target="_blank"><img border="0" src="https://ws-eu.amazon-adsystem.com/widgets/q?_encoding=UTF8&ASIN=B06XQRMJ46&Format=_SL160_&ID=AsinImage&MarketPlace=DE&ServiceVersion=20070822&WS=1&tag=kevineifinger-21&language=de_DE" ></a><img src="https://ir-de.amazon-adsystem.com/e/ir?t=kevineifinger-21&language=de_DE&l=li2&o=3&a=B06XQRMJ46" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />
</td></tr>
<tr><td colspan="4">

The Hubs help the home communicate across all the various protocols running in the house. Most of my sensors are Xiaomi Sensors running over 1 gateway. I use the RM hubs to control non smart TVs and Receivers as well as my canopy via 433MHZ.

<tr><td colspan="4">

#### Lights<a name="lights" href="https://github.com/eifinger/homeassistant-config#devices"><img align="right" border="0" src="https://raw.githubusercontent.com/eifinger/homeassistant-config/master/www/images/up_arrow.png" width="22" ></a>
</td></tr>
<tr><td align="center" colspan="2">

[Xiaomi Yeelight](https://amzn.to/2DizYUY)
</td><td align="center" colspan="2">

[Magichome RGB LED Controller](https://amzn.to/2DfhwfX)
</td></tr>

<tr><td align="center" colspan="2"><a href="https://www.amazon.de/Yeelight-dimmerbar-Xiaomi-kompatibel-Assitant/dp/B01LRTWQJ0/ref=as_li_ss_il?ie=UTF8&qid=1541148576&sr=8-3&keywords=xiaomi+yeelight&linkCode=li1&tag=kevineifinger-21&linkId=07e42493a33391febb018580fe308e91&language=de_DE" target="_blank"><img border="0" src="https://ws-eu.amazon-adsystem.com/widgets/q?_encoding=UTF8&ASIN=B01LRTWQJ0&Format=_SL110_&ID=AsinImage&MarketPlace=DE&ServiceVersion=20070822&WS=1&tag=kevineifinger-21&language=de_DE" ></a><img src="https://ir-de.amazon-adsystem.com/e/ir?t=kevineifinger-21&language=de_DE&l=li1&o=3&a=B01LRTWQJ0" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />
</td><td align="center" colspan="2"><a href="https://www.amazon.de/Controller-Streifen-Strips-Android-kompatibel/dp/B073SD5RQL/ref=as_li_ss_il?ie=UTF8&qid=1541148184&sr=8-2&keywords=magichome+led&linkCode=li1&tag=kevineifinger-21&linkId=b1b4e59ff7886c74ae43115e5fa4b029&language=de_DE" target="_blank"><img border="0" src="https://ws-eu.amazon-adsystem.com/widgets/q?_encoding=UTF8&ASIN=B073SD5RQL&Format=_SL110_&ID=AsinImage&MarketPlace=DE&ServiceVersion=20070822&WS=1&tag=kevineifinger-21&language=de_DE" ></a><img src="https://ir-de.amazon-adsystem.com/e/ir?t=kevineifinger-21&language=de_DE&l=li1&o=3&a=B073SD5RQL" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />
</td></tr>
<tr><td colspan="4">

Almost all of my lights are Xiaomi Yeelight Color bulbs. Before I started using them I used SonOffs with [Tasmota](https://github.com/arendst/Sonoff-Tasmota) and I stil do. You will find them in the [switches](https://github.com/eifinger/homeassistant-config#switches) section. I have one lightstrip under my bar table controlled by a MagicHome LED Controller also running [Tasmota](https://github.com/arendst/Sonoff-Tasmota).

*Click on the sections to expand them* 
<details>
<summary>Turn Bar Red when Homeassistant goes offline</summary><p align="center">
As I sometimes restart HA when working on it from remote I turn the Bar lights to red with [this script](https://github.com/eifinger/homeassistant-config/blob/master/updateHomeassistant.sh). This way everyone can see HA is currently unavailable. If it comes back up again this<br>
</details>
</td></tr>

<tr><td colspan="4">

#### Switches <a name="switches" href="https://github.com/eifinger/homeassistant-config#devices"><img align="right" border="0" src="https://raw.githubusercontent.com/eifinger/homeassistant-config/master/www/images/up_arrow.png" width="22" ></a>
</td></tr>
<tr><td align="center">

[Sonoff S20](https://amzn.to/2SEMtys)
</td><td align="center">

[Sonoff Basic](https://amzn.to/2P1RjaV)
</td><td align="center">

[Teckin Smart Plug](https://amzn.to/2UOUfH0)
</td><td align="center">

[TP-Link Smart Plug](https://amzn.to/2wPNJ7F)</td></tr>

<tr><td align="center"><a href="https://www.amazon.de/Steckdose-Sonoff-Intelligente-Timing-Funktion-Kompatibel/dp/B07CGBHFS9/ref=as_li_ss_il?ie=UTF8&qid=1541149751&sr=8-6&keywords=sonoff&linkCode=li1&tag=kevineifinger-21&linkId=e49e6b40be4fe88bcc33f31322f8cac0&language=de_DE" target="_blank"><img border="0" src="https://ws-eu.amazon-adsystem.com/widgets/q?_encoding=UTF8&ASIN=B07CGBHFS9&Format=_SL110_&ID=AsinImage&MarketPlace=DE&ServiceVersion=20070822&WS=1&tag=kevineifinger-21&language=de_DE" ></a><img src="https://ir-de.amazon-adsystem.com/e/ir?t=kevineifinger-21&language=de_DE&l=li1&o=3&a=B07CGBHFS9" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />
</td><td align="center"><a href="https://www.amazon.de/Universal-Schalter-Fernbedienung-Funkschalter-Android/dp/B078B8N4P3/ref=as_li_ss_il?ie=UTF8&qid=1541149751&sr=8-7&keywords=sonoff&linkCode=li1&tag=kevineifinger-21&linkId=f69891456bd8d90e506ed7d5fadc436e&language=de_DE" target="_blank"><img border="0" src="https://ws-eu.amazon-adsystem.com/widgets/q?_encoding=UTF8&ASIN=B078B8N4P3&Format=_SL110_&ID=AsinImage&MarketPlace=DE&ServiceVersion=20070822&WS=1&tag=kevineifinger-21&language=de_DE" ></a><img src="https://ir-de.amazon-adsystem.com/e/ir?t=kevineifinger-21&language=de_DE&l=li1&o=3&a=B078B8N4P3" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />
</td><td align="center"><a href="https://www.amazon.de/TECKIN-Intelligente-fernbedienbar-Stromverbrauch-funktioniert/dp/B07CDCYLQ6/ref=as_li_ss_il?ie=UTF8&linkCode=li1&tag=kevineifinger-21&linkId=69e5f6d262ca3b01ca172bfb4d36717d&language=de_DE" target="_blank"><img border="0" src="https://ws-eu.amazon-adsystem.com/widgets/q?_encoding=UTF8&ASIN=B07CDCYLQ6&Format=_SL110_&ID=AsinImage&MarketPlace=DE&ServiceVersion=20070822&WS=1&tag=kevineifinger-21&language=de_DE" ></a><img src="https://ir-de.amazon-adsystem.com/e/ir?t=kevineifinger-21&language=de_DE&l=li1&o=3&a=B07CDCYLQ6" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />
</td><td align="center"><a href="https://www.amazon.de/TP-Link-Steckdose-Stromverbrauchsaufzeichnung-funktionieren-erforderlich/dp/B017X72IES/ref=as_li_ss_il?s=computers&ie=UTF8&qid=1536329452&sr=1-1&keywords=hs110&linkCode=li1&tag=kevineifinger-21&linkId=25d7083477f36e734235264c18a3bccc&language=de_DE" target="_blank"><img border="0" src="https://ws-eu.amazon-adsystem.com/widgets/q?_encoding=UTF8&ASIN=B017X72IES&Format=_SL110_&ID=AsinImage&MarketPlace=DE&ServiceVersion=20070822&WS=1&tag=kevineifinger-21&language=de_DE" ></a><img src="https://ir-de.amazon-adsystem.com/e/ir?t=kevineifinger-21&language=de_DE&l=li1&o=3&a=B017X72IES" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" /></td></tr>
<tr><td colspan="4">

Before I used smart bulbs I bought SonOff switches because they are much cheaper than a $20 bulb and put them in front of "normal" bulbs. I use 2 S20 to control lightstrips.

*Click on the sections to expand them* 
<details>
<summary>Notify me when the dishwasher starts/stops</summary><p align="center">
<a href=https://github.com/eifinger/appdaemon-scripts#powerusagenotification>
Appdaemon App -  powerUsageNotification</a><br>
</details>
</td></tr>

<tr><td colspan="4">

#### Cameras <a name="cameras" href="https://github.com/eifinger/homeassistant-config#devices"><img align="right" border="0" src="https://raw.githubusercontent.com/eifinger/homeassistant-config/master/www/images/up_arrow.png" width="22" ></a>
</td></tr>
<tr><td align="center" colspan="4">

[Android IP Webcam](https://play.google.com/store/apps/details?id=com.pas.webcam&hl=en)
</tr>

<tr><td align="center" colspan="4"><a href="https://play.google.com/store/apps/details?id=com.pas.webcam&hl=en" target="_blank"><img border="0" width="120" height="120"src="https://images-na.ssl-images-amazon.com/images/I/61AZLo3EW7L._SY355_.png" ></a><img src="https://images-na.ssl-images-amazon.com/images/I/61AZLo3EW7L._SY355_.png" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />
</td></tr>
<tr><td colspan="4">

I currently only use old Anroid Smartphones as IP Cameras.

*Click on the sections to expand them* 
<details>
<summary>Selflearning Facerecognition for the Frontdoor</summary><p align="center">
<a href=https://github.com/eifinger/appdaemon-scripts#facerecognitionbot>
AppDaemon App - faceRecognitionBot</a><br>
</details>
</td></tr>

<tr><td colspan="4">

#### TV Streaming <a name="streaming" href="https://github.com/eifinger/homeassistant-config#devices"><img align="right" border="0" src="https://raw.githubusercontent.com/eifinger/homeassistant-config/master/www/images/up_arrow.png" width="22" ></a>
</td></tr>
</td><td align="center" colspan="4">

[Amazon Fire TV Stick](https://amzn.to/2yLEfwd)

</td></tr>

<tr><td align="center" colspan="4"><a href="https://www.amazon.de/dp/B079QHMFWC/ref=as_li_ss_il?ie=UTF8&linkCode=li1&tag=kevineifinger-21&linkId=3b697358637b841d88b45935835e710d&language=de_DE" target="_blank"><img border="0" src="https://ws-eu.amazon-adsystem.com/widgets/q?_encoding=UTF8&ASIN=B079QHMFWC&Format=_SL110_&ID=AsinImage&MarketPlace=DE&ServiceVersion=20070822&WS=1&tag=kevineifinger-21&language=de_DE" ></a><img src="https://ir-de.amazon-adsystem.com/e/ir?t=kevineifinger-21&language=de_DE&l=li1&o=3&a=B079QHMFWC" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />
</td></tr>
<tr><td colspan="4">

Just the usual things for Netflix

</td></tr>

<tr><td colspan="4">

#### Sensors <a name="sensors" href="https://github.com/eifinger/homeassistant-config#devices"><img align="right" border="0" src="https://raw.githubusercontent.com/eifinger/homeassistant-config/master/www/images/up_arrow.png" width="22" ></a>
</td></tr>
<tr><td align="center">

[Xiaomi Motion Sensor](https://amzn.to/2P3riYF)
</td><td align="center">

[Xiaomi Door/Window Sensor](https://amzn.to/2AI1AAg)
</td><td align="center">

[Xiaomi Temperature Sensor](https://amzn.to/2P6gw3K)
</td><td align="center">

[Sonoff Sensor AM2301](https://amzn.to/2DhbUS9)
</td></tr>

<tr><td align="center"><a href="https://www.amazon.de/HAPQIN-Original-Menschlichen-Bewegungssensor-Sicherheitsger%C3%A4t/dp/B07G3BHK71/ref=as_li_ss_il?ie=UTF8&qid=1541154123&sr=8-18&keywords=xiaomi+aqara&linkCode=li1&tag=kevineifinger-21&linkId=007076ae44e05e7e2b78794ba1d639d9&language=de_DE" target="_blank"><img border="0" src="https://ws-eu.amazon-adsystem.com/widgets/q?_encoding=UTF8&ASIN=B07G3BHK71&Format=_SL110_&ID=AsinImage&MarketPlace=DE&ServiceVersion=20070822&WS=1&tag=kevineifinger-21&language=de_DE" ></a><img src="https://ir-de.amazon-adsystem.com/e/ir?t=kevineifinger-21&language=de_DE&l=li1&o=3&a=B07G3BHK71" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />
</td><td align="center"><a href="https://www.amazon.de/Xiaomi-Smart-T%C3%BCr-Fenstersensor-Steuerung/dp/B06XHWRBKY/ref=as_li_ss_il?_encoding=UTF8&pd_rd_i=B06XHWRBKY&pd_rd_r=1e64c5cf-de84-11e8-a302-fbbd6e716d43&pd_rd_w=UFU9R&pd_rd_wg=g2tKY&pf_rd_i=desktop-dp-sims&pf_rd_m=A3JWKAKR8XB7XF&pf_rd_p=51bcaa00-4765-4e8f-a690-5db3c9ed1b31&pf_rd_r=6X9008FWH81JD7VHV1AK&pf_rd_s=desktop-dp-sims&pf_rd_t=40701&psc=1&refRID=6X9008FWH81JD7VHV1AK&linkCode=li1&tag=kevineifinger-21&linkId=50cb4d60b18d56ec0a75789190599ed6&language=de_DE" target="_blank"><img border="0" src="https://ws-eu.amazon-adsystem.com/widgets/q?_encoding=UTF8&ASIN=B06XHWRBKY&Format=_SL110_&ID=AsinImage&MarketPlace=DE&ServiceVersion=20070822&WS=1&tag=kevineifinger-21&language=de_DE" ></a><img src="https://ir-de.amazon-adsystem.com/e/ir?t=kevineifinger-21&language=de_DE&l=li1&o=3&a=B06XHWRBKY" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />
</td><td align="center"><a href="https://www.amazon.de/Intelligente-Temperatur-Luftfeuchtigkeit-Drahtlose-Echtzeit/dp/B07GRGPL6Y/ref=as_li_ss_il?ie=UTF8&qid=1541154113&sr=8-3&keywords=xiaomi+aqara&linkCode=li1&tag=kevineifinger-21&linkId=a906155d75b9d856137fe1ec7f96b128&language=de_DE" target="_blank"><img border="0" src="https://ws-eu.amazon-adsystem.com/widgets/q?_encoding=UTF8&ASIN=B07GRGPL6Y&Format=_SL110_&ID=AsinImage&MarketPlace=DE&ServiceVersion=20070822&WS=1&tag=kevineifinger-21&language=de_DE" ></a><img src="https://ir-de.amazon-adsystem.com/e/ir?t=kevineifinger-21&language=de_DE&l=li1&o=3&a=B07GRGPL6Y" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />
</td><td align="center"><a href="https://www.amazon.de/Sonoff-Waterproof-Temperature-Monitoring-Triggering/dp/B06ZZGX886/ref=as_li_ss_il?ie=UTF8&qid=1541154274&sr=8-4&keywords=sonoff+th&th=1&linkCode=li1&tag=kevineifinger-21&linkId=94e08413b92e90a652287695a508d4ef&language=de_DE" target="_blank"><img border="0" src="https://ws-eu.amazon-adsystem.com/widgets/q?_encoding=UTF8&ASIN=B06ZZGX886&Format=_SL110_&ID=AsinImage&MarketPlace=DE&ServiceVersion=20070822&WS=1&tag=kevineifinger-21&language=de_DE" ></a><img src="https://ir-de.amazon-adsystem.com/e/ir?t=kevineifinger-21&language=de_DE&l=li1&o=3&a=B06ZZGX886" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />
</td></tr>
<tr><td colspan="4">

All of my windows have Xiaomi Contact Sensors and my Terrace Doors have two so I can distinguish between open and tilted. I have several Motion Sensors which I use for presence detection and light control. To get a good overview of the temperature distribution I use Xiaomi temperature sensors where I don't already have Sonoff TH16s.

*Click on the sections to expand them* 
<details>
<summary>Turn on light when sun is down and motion detected</summary><p align="center">
<a href=https://github.com/eifinger/appdaemon-scripts#motiontrigger>
AppDaemon App - motionTrigger</a><br>
<a href=https://github.com/eifinger/appdaemon-scripts#bedroommotiontrigger>
AppDaemon App - bedroommotionTrigger</a><br></p>
</details>
<details>
<summary>Alexa ask Home Assistant whether all windows are closed</summary><p align="center">
<a href=https://github.com/eifinger/appdaemon-scripts/blob/master/alexa/README.md#windowsopen>
Appdaemon App - windowsOpen</a><br>
</p></details>
<details>
<summary>Know the exact moment when someone leaves or comes home</summary><p align="center">
<a href=https://github.com/eifinger/appdaemon-scripts#isuserhomedeterminer>
Appdaemon App - isUserHomeDeterminer</a><br>
</p></details>
</td></tr>

<tr><td colspan="4">

#### Climate <a name="climate" href="https://github.com/eifinger/homeassistant-config#devices"><img align="right" border="0" src="https://raw.githubusercontent.com/eifinger/homeassistant-config/master/www/images/up_arrow.png" width="22" ></a>
</td></tr>
<tr><td align="center" colspan="4">

[Decdeal WIFI Thermostat](https://amzn.to/2P21PyV)
</td></tr>

<tr><td align="center" colspan="4"><a href="https://www.amazon.de/gp/product/B075R74XQQ/ref=as_li_ss_il?ie=UTF8&psc=1&linkCode=li1&tag=kevineifinger-21&linkId=ef5c802f42a1a92d94709e2475c3a227&language=de_DE" target="_blank"><img border="0" src="https://ws-eu.amazon-adsystem.com/widgets/q?_encoding=UTF8&ASIN=B075R74XQQ&Format=_SL110_&ID=AsinImage&MarketPlace=DE&ServiceVersion=20070822&WS=1&tag=kevineifinger-21&language=de_DE" ></a><img src="https://ir-de.amazon-adsystem.com/e/ir?t=kevineifinger-21&language=de_DE&l=li1&o=3&a=B075R74XQQ" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />
</td></tr>
<tr><td colspan="4">

I am using a [custom_component](https://community.home-assistant.io/t/beta-for-hysen-thermostats-powered-by-broadlink/56267/) for Broadlink Thermostats which works perfectly.

*Click on the sections to expand them* 
<details>
<summary>Turn on floor heating for 1 hour before wake up</summary><p align="center">
<a href=https://github.com/eifinger/appdaemon-scripts#setthermostat>
AppDaemon App - setThermostat</a></p>
</details>
</td></tr>

<tr><td colspan="4">

#### docker-compose-yaml <a name="compose" href="https://github.com/eifinger/homeassistant-config#devices"><img align="right" border="0" src="https://raw.githubusercontent.com/eifinger/homeassistant-config/master/www/images/up_arrow.png" width="22" ></a>
</td></tr>

<tr><td colspan="4">

```yaml
# Version > 3 does not work as it doesn't support 'depends_on'
version: '2.1'
services:
  homeassistant:
    container_name: homeassistant
    image: homeassistant/home-assistant:0.113.3
    volumes:
      - /home/admin/homeassistant:/config
      - /etc/localtime:/etc/localtime:ro
    restart: always
    network_mode: host
    depends_on:
      influxdb:
        condition: service_healthy
      mysql-homeassistant:
        condition: service_healthy
      mosquitto:
        condition: service_started
  appdaemon:
    container_name: appdaemon
    restart: unless-stopped
    image: acockburn/appdaemon:3.0.5
    volumes:
      - /etc/localtime:/etc/localtime:ro
      - /home/admin/appdaemon:/conf
      - /home/admin/homeassistant/www:/config/www
    environment:
      - HA_URL="https://hidden.de"
      - TOKEN="secure"
      - DASH_URL="http://hidden:5050"
    ports:
      - "5050:5050"
      - "8124:8124"
    links:
      - facerec_service
    depends_on:
      - splunk
  facerec_service:
    container_name: facerec_service
    restart: unless-stopped
    image: eifinger/face_recognition:latest
    volumes:
     - /home/admin/facerec_service:/root/faces
    ports:
     - "9922:8080"
  influxdb:
    container_name: influxdb
    restart: unless-stopped
    image: influxdb:latest
    healthcheck:
      test: ["CMD", "curl", "-sI", "http://127.0.0.1:8086/ping"]
      interval: 30s
      timeout: 1s
      retries: 24
    volumes:
      - /etc/localtime:/etc/localtime:ro
      - /home/admin/influxdb:/var/lib/influxdb
    ports:
      - "8083:8083"
      - "8086:8086"
      - "8090:8090"
  timescaledb:
    container_name: timescaledb
    restart: unless-stopped
    image: timescale/timescaledb-postgis:1.7.0-pg12
    volumes:
      - /etc/localtime:/etc/localtime:ro
      - /home/admin/timescaledb/data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_PASSWORD=admin
  grafana:
    container_name: grafana
    restart: unless-stopped
    image: grafana/grafana:7.0.3
    volumes:
      - grafana-storage:/var/lib/grafana
    environment:
      - GF_SECURITY_ADMIN_PASSWORD="admin"
      - GF_ANALYTICS_REPORTING_ENABLED=false
      - GF_USERS_ALLOW_SIGN_UP=false
      - GF_AUTH_ANONYMOUS_ENABLED=false
      - GF_RENDERING_SERVER_URL=http://grafana-renderer:8081/render
      - GF_RENDERING_CALLBACK_URL=http://grafana:3000
    ports:
      - "3000:3000"
    depends_on:
      - influxdb
  grafana-renderer:
    image: grafana/grafana-image-renderer:latest
    container_name: grafana-renderer
    ports:
      - "8081:8081"
  mysql-homeassistant:
    container_name: mysql-homeassistant
    restart: unless-stopped
    image: mysql:latest
    healthcheck:
        test: "/usr/bin/mysql --user=root --password=secure --execute \"SHOW DATABASES;\""
        interval: 2s
        timeout: 20s
        retries: 10
    environment:
      - MYSQL_ROOT_PASSWORD=secure
      - MYSQL_DATABASE=hass_db
      - MYSQL_USER=hassuser
      - MYSQL_PASSWORD=secure
    volumes:
      - /home/admin/mysql-homeassistant/mysql:/var/lib/mysql
    ports:
      - "3307:3306"
  mosquitto:
    container_name: mosquitto
    restart: unless-stopped
    image: eclipse-mosquitto
    volumes:
      - /home/admin/mosquitto/data:/mosquitto/data
      - /home/admin/mosquitto/log:/mosquitto/log
      - /home/admin/mosquitto/config:/mosquitto/config
    ports:
      - "1883:1883"
      - "9001:9001"
      - "8883:8883"
  hass-data-detective:
    container_name: hass-data-detective
    hostname: hass-data-detective
    restart: unless-stopped
    image: kylerw/hass-data-detective:latest
    network_mode: host
    volumes:
      - /home/admin/homeassistant:/hass-config:ro
      - /etc/localtime:/etc/localtime:ro
      - /home/admin/hass-data-detective/:/home/jovyan
    environment:
      - JUPYTER_ENABLE_LAB="yes"
    depends_on:
      - homeassistant
  glances:
    container_name: glances
    image: eifinger/glances-docker:3.1.4
    restart: unless-stopped
    pid: "host"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - /home/admin/glances/conf/glances.pwd:/root/.config/glances/glances.pwd
      - /media:/media:ro
    environment:
      - "GLANCES_OPT=-w --password"
    ports:
      - "61208:61208"
      - "61209:61209"
  esphome:
    container_name: esphome
    image: esphome/esphome:1.14.3
    volumes:
      - /home/admin/esphome:/config
      - /etc/localtime:/etc/localtime:ro
    restart: always
    network_mode: host
  seq:
    container_name: seq
    image: datalust/seq:2020.1.4212
    volumes:
      - /home/damin/seq/data:/data
    ports:
      - "5342:80"
      - "5341:5341"
    environment:
      - "ACCEPT_EULA=Y"
volumes:
  grafana-storage:
```

</td></tr>

<tr><td colspan="4">

#### Screenshots <a name="screenshots" href="https://github.com/eifinger/homeassistant-config#devices"><img align="right" border="0" src="https://raw.githubusercontent.com/eifinger/homeassistant-config/master/www/images/up_arrow.png" width="22" ></a>
</td></tr>

<tr><td colspan="4">

![default_view](https://raw.githubusercontent.com/eifinger/homeassistant-config/master/www/images/default_view.png)
![alarm_view](https://raw.githubusercontent.com/eifinger/homeassistant-config/master/www/images/alarm_view.png)
![travel_view](https://raw.githubusercontent.com/eifinger/homeassistant-config/master/www/images/travel_view.png)
![fuel_view](https://raw.githubusercontent.com/eifinger/homeassistant-config/master/www/images/fuel_view.png)
![sensor_view](https://raw.githubusercontent.com/eifinger/homeassistant-config/master/www/images/sensor_view.png)
![automation_view](https://raw.githubusercontent.com/eifinger/homeassistant-config/master/www/images/automation_view.png)
![settings_view_1](https://raw.githubusercontent.com/eifinger/homeassistant-config/master/www/images/settings_view_1.png)
![floorplan_view](https://raw.githubusercontent.com/eifinger/homeassistant-config/master/www/images/floorplan_view.png)

</td></tr>
</table>

**All files are now being edited with [VSCode](https://code.visualstudio.com/).**

**All of my configuration files are tested against the most stable version of home-assistant using Github Actions.**

**Still have questions on my Config?**
**Message me on twitter :** [@eifinger](https://twitter.com/eifinger)

<br>
</p>
