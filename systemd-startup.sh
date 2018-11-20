# install the program to a hidden folder in the home folder
mkdir /home/$USER/.1dsync
cp -r * /home/$USER/.1dsync

# creates the init script to be used by the service
bash -c "cat > /home/$USER/.1dsync/1dsync.sh <<- EOM
#!/bin/sh
/usr/bin/nice -19 /usr/bin/python3 -B /home/$USER/.1dsync/1dsync.py 
EOM"
chmod +x /home/$USER/.1dsync/1dsync.sh

# creates the folder for the systemd user services if it doesn't exist already
mkdir /home/$USER/.config/systemd
mkdir /home/$USER/.config/systemd/user

# creates the service file
bash -c "cat > /home/$USER/.config/systemd/user/1dsync.service <<- EOM
[Unit]
Description=1D-Sync background user service
[Service]
ExecStart=/home/$USER/.1dsync/1dsync.sh
[Install]
WantedBy=default.target
EOM"

# to run without user login use this
# sudo loginctl enable-linger $USER

# enables the script
systemctl --user enable 1dsync

echo Ok!
