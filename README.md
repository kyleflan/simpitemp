# Install Docker

`curl -fsSL https://get.docker.com -o get-docker.sh`

`sh get-docker.sh`

`sudo usermod -aG docker $USER`

Logout and log back in

# Enable SPI and I2C

`sudo raspi-config`

Navigate to interfaces and enable SPI and I2C, reboot

# Install Libs and NPM

`sudo apt-get install libgpiod2 npm`

# Install Git and Python Utils (and vim)

`sudo apt-get install git-core python3 build-essential python-dev python3-pip vim`

# Start Redis

`mkdir /home/pi/app/redis_data`

`docker run --name redis-01 --restart always -p 6379:6379 -v /home/pi/app/redis_data:/data -d redis redis-server --appendonly yes`
