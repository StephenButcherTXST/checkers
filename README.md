# Checkers

This is a single end-point API that accepts valid JSON containg a square grid of black/red/empty checkers and calculates locations and directions of consecutive matches of red or black checkers. The API returns JSON containing results with:
* The starting location of any matches
* The color (red/black) that matches
* The direction of the match

## Installation
### Install dependencies
sudo yum install git python36
python3 -m install virtualenv --user
### Create folder
mkdir ~/checkers
cd ~/checkers
### Clone this repository
git clone https://github.com/StephenButcherTXST/checkers .
### Setup virtual environment
virtualenv env
### Activate the virtual environment
source env/bin/activate
### Install Python requirements
pip install -r checkers_api/requirements.txt
### Modify the systemd service file
sed -i "s#<user>#$(whoami)#g" checkers_api.service 
### Install systemd file
sudo cp checkers_api.service /etc/systemd/system
### Enable and start service


## Configuration
