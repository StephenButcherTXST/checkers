#!/bin/bash

echo "This script will perform the following actions:"
echo "  Enable EPEL repository [sudo]"
echo "  Install dependencies (git, python36) [sudo]"
echo "  Download code from git into ~/checkers [git]"
echo "  Create a python virtual environment, and populate it with packages from requirements.txt"
echo "  Register and start the service with systemd [sudo]"
echo "  Automatically add firewall exception, if FirewallD is in use. [sudo]"

echo 
read -p "Continue (Y/N):" -n 1 -r CONTINUE
if [[ ! $CONTINUE =~ ^[Yy]$ ]]; then 
    echo ""
    exit 1
fi

echo "===== Installing dependencies ====="
sudo yum install -y epel-release
sudo yum install -y git python36
python3 -m pip install virtualenv --user

echo "===== ===== Creating folder ====="
mkdir ~/checkers && cd ~/checkers

echo "===== Cloning the repository ====="
git clone https://github.com/StephenButcherTXST/checkers .

echo "===== Creating virtual environment ====="
virtualenv env

echo "===== Entering the virtual environment ====="
source env/bin/activate

echo "===== Installing Python requirements into the virtual environment ====="
pip install -r api/requirements.txt

echo "===== Leaving the virtual environment ====="
deactivate

echo "===== Modify the systemd service file ====="
sed -i "s#<user>#$(whoami)#g" checkers_api.service

echo "===== Install systemd file ====="
sudo cp checkers_api.service /etc/systemd/system

echo "===== Enable and start service ====="
sudo systemctl enable --now checkers_api.service

echo "===== Getting current firewall zone ====="
FWD=$(sudo firewall-cmd --state)
if [[ "$FWD" -eq "running" ]]; then
    ZONE=$(firewall-cmd --get-active-zones | egrep -B 1 '(ens|eth)' | head -n 1)
    echo "===== Adding firewall exception to zone: $ZONE ====="
    sudo firewall-cmd --zone=$ZONE --add-port=5000/tcp
else
    echo "FirewallD not running or not found."
    echo "Firewall rule will need to be added manually at allow inbound 5000/tcp"
fi
