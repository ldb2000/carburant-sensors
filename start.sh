#!/bin/bash
rm home-assistant_v2.log
docker stop home-assistant
docker rm home-assistant
docker pull homeassistant/home-assistant
#docker run -d --network=host --name home-assistant -v /Users/laurentdeberti/Documents/perso/viessman-sensore:/config -p 8123:8123 homeassistant/home-assistant 
docker run -d --name home-assistant -v $PWD:/config -p 8123:8123 homeassistant/home-assistant 
