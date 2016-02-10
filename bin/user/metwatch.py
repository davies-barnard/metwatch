#
#    Copyright (c) 2016 Chris Davies-Barnard <weewx@davies-barnard.co.uk>
#
#    See the file LICENSE.txt for your full rights.
#

""" This search list extension offers one extra tags:

		'metalert':	The next possible sighting of the MET (International Space Station).  
								This is a single occurance of the metwatch object
								
To use it, modify the option search_list in your skin.conf configuration file,
adding the name of this extension.


"""

from weewx.cheetahgenerator import SearchList

import sys
import syslog
from urllib2 import urlopen, HTTPError, URLError
from lxml import etree
import time
import datetime
import re


class METAlert(SearchList):
		"""Retrieves data from an MET Station RSS Feed and converts it into a variable that is available for templates."""
		
		namespaces = {'metadata': 'http://metadata.example.com'} # add more as needed

		def __init__(self, generator=None):
			SearchList.__init__(self, generator)

		def get_extension_list(self, timespan, db_lookup):
			"""Returns a search list extension with two additions. """
			
			#Pass the RSS feed from the weewx.conf to the processAlertUrl
			metstatus, metall = self.processAlertRSS(self.generator.config_dict['StdReport']['metwatch']['url'])
	
			# Now create a small dictionary with keys 'alltime' and 'seven_day':
			search_list_extension = { 'metall' : metall, 'metstatus':metstatus }
      
			# Finally, return our extension as a list:
			return [search_list_extension]
	
	
		def processAlertRSS(self,feedurl):
			
			#Retrieve the RSS feed
			try:
				feedsource = urlopen(feedurl)
			except HTTPError, e:
				print ('HTTPError = ' + str(e.code))
			except URLError, e:
				print ('URLError = ' + str(e.reason))
			except httplib.HTTPException, e:
				print ('HTTPException')
			except Exception:
				import traceback
				print ('generic exception: ' + traceback.format_exc())

			feeddata = feedsource.read()
			feedsource.close()
			
			#Convert into XML Doc
			xmldoc = etree.fromstring(feeddata)
			
			nsmap = {k:v for k,v in xmldoc.nsmap.iteritems() if k}
			
			metstatus = {}
			for alert in xmldoc.iter('channel'):
				metstatus['pubdate'] = alert.find('pubDate').text
				metstatus['title'] = alert.find('title').text
				metstatus['link'] = alert.find('link').text
				metstatus['description'] = alert.find('description').text
				metstatus['copyright'] = alert.find('copyright').text
								
			metall = []	
			for item in xmldoc.iter('item'):

				warningLevel = item.find('metadata:warningLevel', nsmap)
				warningKind = item.find('metadata:warningKind', nsmap)
				warningType = item.find('metadata:warningType', nsmap)
				description = item.find('description').text.split(":")
				description = description[1].split('valid from')

				alert = {
					'title' : item.find('title').text,
					'affects' : description[0],
					'validfrom' : description[1],
					'link' : item.find('link').text,
					'warninglevel' : warningLevel.text,
					'warningkind' : warningKind.text,
					'warningtype' : warningType.text
				}
				metall.append(alert)

			return metstatus, metall
				
			
		def get_ts(self,pubdate):
			"""Converts a Pub Date e.g. 19 Jan 2016 17:24:51 GMT into a timestamp"""

			pubdate = re.sub(' GMT$', '', pubdate)
			format = "%d %b %Y %H:%M:%S"
			return time.mktime(datetime.datetime.strptime(pubdate, format).timetuple())
				


		def clean(self,value):
			print ("Cleaning ",value)
			

"""This is for testing"""
#PYTHONPATH=bin python bin/user/metwatch.py weewx.conf
if __name__ == '__main__':
	
	import weewx
	import socket
	import configobj
	
	weewx.debug = 1
	syslog.openlog('wee_metwatch', syslog.LOG_PID|syslog.LOG_CONS)
	syslog.setlogmask(syslog.LOG_UPTO(syslog.LOG_DEBUG))

	if len(sys.argv) < 1 :
			print """Usage: metwatch.py path-to-configuration-file"""
			sys.exit(weewx.CMD_ERROR)
			
	try :
			config_dict = configobj.ConfigObj(sys.argv[1], file_error=True)
	except IOError:
			print "Unable to open configuration file ", sys.argv[1]
			raise
			
	socket.setdefaulttimeout(10)

	feedurl = config_dict['StdReport']['metwatch']['url']
	print (feedurl)
	
	metwatcher = METAlert()
	metstatus, metall = metwatcher.processAlertRSS(feedurl)
	
	print(metstatus)
	print(metall)
	