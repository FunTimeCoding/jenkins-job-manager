@echo off
if not exist tmp mkdir tmp

if not exist tmp\bootstrap-salt.sh powershell -Command "Invoke-WebRequest https://bootstrap.saltstack.com -OutFile tmp/bootstrap-salt.sh"

if not exist tmp\salt mkdir tmp\salt
copy configuration\minion.yaml tmp\salt\minion.conf

if exist %USERPROFILE%\.gitconfig copy %USERPROFILE%\.gitconfig tmp\gitconfig.txt
if exist %USERPROFILE%\.gitignore_global copy %USERPROFILE%\.gitignore_global tmp\gitignore_global.txt

vagrant up
vagrant ssh --command /vagrant/script/vagrant/vagrant.sh
vagrant ssh --command /vagrant/script/vagrant/ansible.sh
pause
