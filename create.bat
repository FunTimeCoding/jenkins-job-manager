@echo off
if not exist tmp mkdir tmp
echo eth0> tmp/ethernet-device.txt
vagrant up
pause
