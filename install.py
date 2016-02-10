# installer for Met Watch
# Copyright 2016 Chris Davies

from setup import ExtensionInstaller

def loader():
	return MetWatchInstaller()

class MetWatchInstaller(ExtensionInstaller):
	def __init__(self):
		super(MetWatchInstaller, self).__init__(
			version='0.1',
			name='metwatch',
			description='Uses an RSS Feed from the Met Office to provide template variables to alert to possible weather alerts',
			author='Chris Davies',
			author_email='weewx@davies-barnard.co.uk',
			config={
				'StdReport': {
						'metwatch': {
								'url' : 'http://www.metoffice.gov.uk/public/data/PWSCache/WarningsRSS/Region/sw',
								'skin': 'metwatch',
								'HTML_ROOT': 'metwatch'
						}
				}
			},
			files=[
				('bin/user', ['bin/user/metwatch.py']),
				('skins/metwatch', ['skins/metwatch/skin.conf', 'skins/metwatch/index.html.tmpl']),
			]
		)