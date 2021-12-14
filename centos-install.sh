#!/bin/bash

trap "exit" INT

echo "This script will perform the following actions:"
echo "  Install dependencies (git, python36) [sudo]"
echo "  Download code from git into ~/checkers"
echo "  Create a python virtual environment, and populate it with packages from requirements.txt"
echo "  Register and start the service with systemd [sudo]"
echo "  Automatically add firewall exception, if FirewallD is in use. [sudo]"

echo ""
read -p "Continue (Y/N):" -n 1 -r CONTINUE
if [[ ! $CONTINUE =~ ^[Yy]$ ]]; then 
    echo ""
    exit 1
fi

echo ""
echo "===== Testing sudo access ====="
sudo -v
if [ $? != 0 ]; then
    echo "Error using sudo. Confirm you have sudo access and then retry installation."
    exit 1
fi

echo "===== Installing dependencies ====="
sudo yum install -y git python36
python3 -m pip install virtualenv --user

echo "===== Creating folder ====="
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

echo "===== Modifying the systemd service file for current user ====="
sed -i "s#<user>#$(whoami)#g" checkers_api.service

echo "===== Installing systemd service file ====="
sudo cp checkers_api.service /etc/systemd/system

echo "===== Enabling systemd service ====="
sudo systemctl enable checkers_api.service

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

echo ""
read -p "Would you like to start the service (Y/N):" -n 1 -r CONTINUE
if [[ ! $CONTINUE =~ ^[Yy]$ ]]; then 
    echo ""
    exit 1
else
    echo ""
    echo "===== Starting service ====="
    sudo systemctl start checkers_api.service
fi
