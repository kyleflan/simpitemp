# Simpitemp

A simple web application to interface with a AM2302 (DHT22) temperature and humidity sensor.

## Items Needed

* [DHT22/AM2302 temperature and humidity sensor](https://amzn.to/2v1tZRX)
* [Raspberry Pi 3](https://amzn.to/2VfZylx)
* Jumper cables if your sensor did not include jumpers

## Wiring Your Sensor

There are a few varieties of the DHT22/AM2302 (and you could technically use 
the DHT11 if you swap out some libraries), but the one we're using from the
link above has the pull up resistor already incorporated so wiring is very
straightforward. 

There are three pins on the chip, VCC, ground and data. 

**V**CC -> Pin 2 (5V)
**G**round -> Pin 6 (GND)
**D**ata -> Pin 7 (GPIO4)

A la:

```
[ V * G * * * * * * * * * * ]
[ * * * D * * * * * * * * * ]
```

There are a lot of good guides online for how to wire up the chip if you'd like
more visuals! You can use a different GPIO pin as well, just make sure to
update `stats_collector.py` and change `board.D4` to `board.DX`.

## Let's get started

### Install Git and Python Utils (and vim if you're tinkering)

`sudo apt-get install git-core python3 build-essential python-dev python3-pip vim`

### Clone repo

`git clone https://github.com/kyleflan/simpitemp && cd ./simpitemp`

### Install Docker

`curl -fsSL https://get.docker.com -o get-docker.sh`

`sh get-docker.sh`

`sudo usermod -aG docker $USER`

### Install Libs and  NPM

`sudo apt-get install libgpiod2 npm`

### Install pm2

`npm install pm2 -g`

### Enable SPI and I2C

`sudo raspi-config`

Navigate to interfaces and enable SPI and I2C, reboot

### Start Redis

`mkdir ./redis_data`

`docker run --name redis-01 --restart always -p 6379:6379 -v /home/pi/app/redis_data:/data -d redis redis-server --appendonly yes`

### Start the app

`pm2 start ./pm2/process.json`

> Note: PM2 is a process manager, originally built for node.js apps, but 
> it's very user-friendly and works for generic apps as well

### Browse to the app

> By default, the flask app is set to be available outside of localhost (i.e from
> other devices on your network). To lock down the app to where it's only 
> accessible via the pi, edit `webapp.py` and remove `host=0.0.0.0` on the
> last line.

Go to this URL: http://<PI IP Address>:8080 you should see something like this:

![Simpitemp Screenshot](./screenshot.png?raw=True Screenshot)

### Startup Across Reboots

To have the app persist across reboots, do the following:

`pm2 startup`

Copy and past the generated command to create a startup script, then run:

`pm2 save`

...to save the current set of pm2 apps. 

