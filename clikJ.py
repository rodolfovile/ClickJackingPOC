# -*- coding: utf-8 -*-
import requests
from ghost import Ghost, Session
import logging 
import os
import sys


if len(sys.argv) != 2:
	print "usage: %s URL" %(sys.argv[0])
	sys.exit(0)


URL = str(sys.argv[1])
request = requests.get(URL)



try:
	xframe = request.headers['x-frame-options']
	print "\n X-FRAME OPTIONS is present clickjacking not possible."
except:
	print "\n X-FRAME OPTIONS NOT PRESENTE !! :)"


print "\n"
print "[+][+]TRYING CLICKJACKING ATTACK[+][+]"
print "\n"


html = '''
<html>
<body>
<iframe src =" ''' + URL + ''' " height='600px' width='800px'></iframe>
</body>
</html> '''



html_filename = 'evilsite.html'

file_name = open(html_filename, 'w')
file_name.write(html)
file_name.close

log_filename = 'test.log'
file_handler = logging.FileHandler(log_filename)


g = Ghost(log_level=logging.INFO, log_handler=file_handler)
g = Session(g)

page, resources = g.open(html_filename)

log1 = open(log_filename, 'r')
if 'forbidden by X-Frame-Options.' in log1.read():
	print '\n Click jacking blocked by X-FRAME OPTIONS'
else:
	href = g.evaluate('document.location.href'[0])
	if html_filename not in href:
		print "\n Frame busting detected"
	else:
		print "\n Frame busting NOT detected.."
		print "\n PAGE IS VULNERABLE TO CLICKJACKING :)"
log1.close()

try:
	logging.getLogger('g').handlers[0].close()
	os.unlink(log_filename)
	os.unlink(html_filename)
except Exception as e:
    logging.exception("\n LOG ERROR :(")
