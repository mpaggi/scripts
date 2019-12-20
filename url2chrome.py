# Small and simple script to read a list of URLs and
# create a HTML that would be easy to import in Chrome
# A new line will push the creation of a new file {filename}-{num}
import urllib2
import time
import sys
import os.path
from BeautifulSoup import BeautifulSoup
reload(sys)
sys.setdefaultencoding('utf-8')

DEBUG=0

try:
  fileurls = sys.argv[1]
  filehtml =  sys.argv[2]
except:
  print "Syntax: "+sys.argv[0]+" input.txt output.html"
  print "  where input.txt is the text file containing the URLs"
  print "  and output.html is the file where to save the HTML generated"
  sys.exit(1)

fout = open(filehtml, 'w')

with open(fileurls) as fp:
  line = fp.readline()
  cnt = 1
  fc=1
  fout.write('<HTML>\n<HEAD><TITLE>Bookmarks from file [1]</TITLE></HEAD>\n<BODY>\n')
  while line:
    if line.startswith('http'):
      if (DEBUG):
        print("Line {}: {}".format(cnt, line.strip()))

      # getting the URL and title
      if (DEBUG):
        print("Going to soup for {}".format(line.strip()))
      try:
        hdr = {'User-Agent': 'Mozilla/5.0'}
        req = urllib2.Request(line.strip(),headers=hdr)
        resp = urllib2.urlopen(req)
        page = resp.read()
        soup = BeautifulSoup(page)
        title = soup.title.string
        if (DEBUG):
          print title
        # building the HTML
        linehtml='<a href="' + line.strip() + '">' + title + '</a><br>\n'
        fout.write(linehtml)
      except Exception as e:
        print e
    else:
      if line in ['\n', '\r\n']:
        if (DEBUG):
          print "New line found, going to create a new file."
        fout.write('</BODY>\n</HTML>\n')
        fout.close()
        fc = str(fc+1)
        fn = os.path.splitext(filehtml)[0]
        ext = os.path.splitext(filehtml)[1]
        newfilehtml = fn+fc+ext
        fout = open(newfilehtml, 'w')
        fout.write('<HTML>\n<HEAD><TITLE>Bookmarks from file ['+fc+']</TITLE></HEAD>\n<BODY>\n')
      if (DEBUG):
        print("Line {}: not an url, skipping".format(cnt))
    cnt += 1
    line = fp.readline()
  fout.write('</BODY>\n</HTML>\n')
  fout.close()
