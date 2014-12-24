import urllib, zipfile, os, sys, glob, random

#Specifying formats, and download and subtitle string
FORMAT = ['.mp4', '.avi', '.mkv']
DOWNLOAD = '/subtitle/download'
SUBTITLE = '/subtitles/'

#Specifying variables to be used in the script
lang = 'english'
directory = os.getcwd() + '/tmp' + str(random.randint(10000, 99999))
path = os.getcwd()
files = glob.glob("*")
torrentURL = ""
torrentName = "<No file>"
for f in files:
	for extension in FORMAT:
		if  extension in f:
			torrentName = f
			torrentURL = 'http://www.subscene.com/subtitles/release?q=' + f.replace(extension, '') + '&r=true'
			break
	if len(torrentURL) != 0:
		break

#Function that check whether or not a word is in a list, and return 1 if in. 0 if not
def wordInList(word, wList):
	for w in wList:
		if w == word:
			return 1
	return 0

#Remove all unnecessary strings before and after the  table
def removeTags(siteList):
	i = 0
	while 1:
		try:
			if siteList[i] != 'class="a1">':
				siteList.pop(i)	
			else:
				break
		except IndexError:
			print "No subtitle found..."
			sys.exit()

	while 1:
		i = len(siteList)-1
		if siteList[i] != 'class="alternativeSearch">':
			siteList.pop(i)
		else:
			break

#Add valid subtitle URL's to a list
def filterURL(siteList, phrase):
	urlList = []
	for l in siteList:
		if l[:6] == 'href="' and phrase in l:
			urlList.append(l[6:-1])
	return urlList

#Print help and exit
def printHelp():
	print '\n', 'Help for SubPy'
	print 'Run this script within the directory of the movie you wish to download subtitles for.'
	print 'Run with the argument "-lang=<your-language>" to get a subtitle of that language.'
	sys.exit()

##### MAIN PART OF SCRIPT #####
for arg in sys.argv:
	#If help is given as argument, print help and exit
	if arg == '-h' or arg == '--help':
		printHelp()
	elif '-lang=' in arg:
		lang = arg.replace('-lang=', '')

if torrentName == '<No file>':
	print "No video file in directory"
	sys.exit()
else:
	print "Searching for: " + lang + ' - "' + torrentName + '"'

#Find and add all valid URL's to a list
site = urllib.urlopen(torrentURL)
text = site.read()
tList = text.split()
removeTags(tList)
urlList = filterURL(tList, SUBTITLE)

#Find the correct language
subURL = ''
for url in urlList:
	if lang in url:
		subURL = 'http://www.subscene.com' + url[:-1]
		break

if subURL == '':
	print 'No subtitle available in that language'
	sys.exit()

#Get download-URL
subSite = urllib.urlopen(subURL)
line = (subSite.read()).split()
urlList = filterURL(line, DOWNLOAD)
url = 'http://www.subscene.com' + urlList[0]

#Handle redirects
test = urllib.urlopen(url)
url = test.geturl()

#Get, unzip and delete
subT = urllib.URLopener()

error = True
while error:
	try:
		subT.retrieve(url, directory)
		error = False
	except IOError:
		directory.replace(directory[-5:], str(random.randint(10000, 99999)))

ziptest = zipfile.ZipFile(directory)
ziptest.extractall(path)
os.remove(directory)

print "Subtitle downloaded!"
