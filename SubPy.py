import urllib, zipfile, os, sys, glob, random

#Specifying formats, and download and subtitle string
FORMAT = ['.mp4', '.avi', '.mkv']
DOWNLOAD = '/subtitle/download'
SUBTITLE = '/subtitles/'

#Specifying variables to be used in the script
lang = 'english'
directory = os.getcwd()
path = directory + '/tmp' + str(random.randint(10000, 99999))
torrentURL = ""
torrentName = "<No file>"

#Return 1 if the word is in the list, 0 if not.
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

#Add valid subtitle URL's to a list, and return it
def filterURL(siteList, phrase):
	urlList = []
	for l in siteList:
		if l[:6] == 'href="' and phrase in l:
			urlList.append(l[6:-1])
	return urlList

#Print help and exit
def printHelp():
	print '\n', 'Help for SubPy:'
	print 'Run this script within the directory of the movie you wish to download subtitles for.'
	print 'Run with the argument "-lang=<your-language>" to get a subtitle of that language.'
	print 'Run with the argument "-dir=<full_directory_path>" to find video files in an alternative directory.'
	sys.exit()

#Generate path based on directory
def genPath(directory):
	return directory + '/tmp' + str(random.randint(10000, 99999))

#Generate torrentName
def genTorrentName(directory):
	tList = []
	i = 1
	for f in os.listdir(directory):
		for  extension in FORMAT:
			if extension in f:
				tList.append(f.replace(extension, ''))
	if len(tList) == 0:
		print "No video file in directory"
		sys.exit()
	elif len(tList) == 1:
	 	return tList[0]

	while i <= len(tList):
		print '[' + str(i) + '] ' + tList[i-1]
		i += 1
	
	try:
		idx = int(raw_input("Choose video: "))
	except ValueError:
		print "Invalid input!"
		sys.exit()

	if idx <= len(tList) and idx > 0:
		return tList[idx-1]
	else:
		print "Invalid video number!"
		sys.exit()
	

#Generate torrentURL
def genTorrentURL(torrentName):
	return 'http://www.subscene.com/subtitles/release?q=' + torrentName + '&r=true'

##### MAIN PART OF SCRIPT #####
for arg in sys.argv:
	#If help is given as argument, print help and exit
	if arg == '-h' or arg == '--help':
		printHelp()
	else:
	#If any of the other acceptable arguments are given
		if '-lang=' in arg:
			lang = arg.replace('-lang=', '')
		if '-dir=' in arg:
			directory = arg.replace('-dir=', '')
			path = genPath(directory)

torrentName = genTorrentName(directory)
torrentURL = genTorrentURL(torrentName)

#if torrentName == '<No file>':
#print "No video file in directory"
#sys.exit()
#else:
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
		subT.retrieve(url, path)
		error = False
	except IOError:
		directory.replace(path[-5:], str(random.randint(10000, 99999)))

ziptest = zipfile.ZipFile(path)
ziptest.extractall(directory)
os.remove(path)

print "Subtitle downloaded!"
