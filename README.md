# Checkers

This is a single end-point API that accepts valid JSON containg a square grid (rows=columns) of black/red/empty checkers and calculates locations and directions of consecutive matches of red or black checkers. The API returns JSON containing results with:
* The starting location of any matches
* The color (red/black) that matches
* The direction of the match

## Installation
### Install dependencies
sudo yum install git python36
python3 -m install virtualenv --user
### Create folder
mkdir ~/checkers && cd ~/checkers
### Clone this repository
git clone https://github.com/StephenButcherTXST/checkers .
### Setup virtual environment
virtualenv env
### Activate the virtual environment
source env/bin/activate
### Install Python requirements
pip install -r api/requirements.txt
### Modify the systemd service file
sed -i "s#&lt;user&gt;#$(whoami)#g" checkers_api.service 
### Install systemd file
sudo cp checkers_api.service /etc/systemd/system
### Enable and start service
sudo systemctl enable --now checkers_api.service
### Add firewall exception
#### Determine current firewall zone
firewall-cmd --get-active-zones
#### Open TCP port 5000 (change public if zone returned from firewall-cmd is different)
sudo firewall-cmd --zone=public --add-port=5000/tcp

## Configuration options
### Inside main.py, the following options can be modified for grid_config:
#### "size" : Size of the square grid
Default value: 8.

#### "consecutive_checkers" : Number of consecutive checkers to match
Default value: 4.

#### Expected string values to match black (B), red (R), empty square (-)
The values expected for representing Black, Red and Empty in the input JSON.
Default values: "black": "B", "red": "R", "empty": "-"

#### "case_sensitive" : Require case sensitive matching for black/red values
Default value: False. 

#### "allow_overlap" : Allow overlapping results
Default value: True

### The following changes can be made in /etc/systemd/system/checkers_api.service
#### Install location
If you install the service into a location outside of your home folder, you will need to modify the \[Service\] definition in checkers_api.service.
Ensure you update the paths for WorkingDirectory, Environment and ExecStart correctly, and that User and Group reflect a user and group that has access to the specified path(s).
#### Change IP and/or Port number
This service is run using the gunicorn application. The default bind IP address and port number that gunicorn uses is all interfaces and port 5000 (-b 0.0.0.0:5000). If you wish to change the IP or port number that the service listens on, you will need to update the -b parameter to &lt;ip address&gt;:&lt;port&gt; for ExecStart. Note: When changing this, be sure to update the firewall rule accordingly.
#### Change the number of workers
The default value is set to 4 workers (-w 4). In order to adjust the number of workers change the value after the -w parameter for ExecStart.
#### Additional settings / tuning
gunicorn supports many additional parameters which can be found by running gunicorn --help. Any additional parameters you wish to use will need to be appended to ExecStart.

## Testing
### Unit test with test_api.py
#### Activate the virtual environment
cd ~/checkers && source env/bin/activate
#### (Optional) modify the valid_grid in test_api.py
If you changed any grid settings ("size","black","red", "empty"), you will need to update "valid_grid"
#### Run the test
Run _python -m unittest test_api.py_

### Manual test with manual_test.py
A simplistic test file (manual_test.py) has been provided to test the service locally or remotely. Edit the file and modify "url" if you changed the port number, or wish to test a remote service. You will also need to modify "valid_grid" if you adjusted any grid settings ("size","black","red", "empty") in main.py.
