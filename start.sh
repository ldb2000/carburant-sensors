#!/bin/bash
rm home-assistant_v2.log
docker stop home-assistant
docker rm home-assistant
docker pull homeassistant/home-assistant
docker run -d --name home-assistant -v $PWD:/config -p 8123:8123 homeassistant/home-assistant 
