This program was set up on a Ubuntu machine and assumes you already have python3 installed.  
You will need to install selenium: pip3 install selenium  
Download the Firefox driver(v0.26.0) tarball from here: https://github.com/mozilla/geckodriver/releases  
Extract the tarball into /usr/bin  
    cd /usr/bin  
    sudo tar -xf ~/Downloads/geckodriver-v0.26.0-linux64.tar.gz  
Run with python3: <project_dir>/python3 main.py