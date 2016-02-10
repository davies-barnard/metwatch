metwatch - weewx extension that implements uses an RSS Feed from the UK Met Office to 
provide template variables to alert to weather alerts

Copyright 2016 Chris Davies

Installation instructions:

1) run the installer:

setup.py install --extension extensions/metwatch
#./bin/wee_extension --install=extensions/metwatch.tar.gz

2) restart weewx:

sudo /etc/init.d/weewx stop
sudo /etc/init.d/weewx start

Manual installation instructions:

1) copy files to the weewx user directory:

cp bin/user/metwatch.py /home/weewx/bin/user
cp -R skins/metwatch /home/weewx/skins/

2) in weewx.conf, add the following section 

[StdReport]
	[[metwatch]]
			url = http://www.metoffice.gov.uk/public/data/PWSCache/WarningsRSS/Region/sw
			skin = metwatch
			HTML_ROOT = public_html/metwatch

3) restart weewx

sudo /etc/init.d/weewx stop
sudo /etc/init.d/weewx start
