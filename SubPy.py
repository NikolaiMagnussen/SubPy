import urllib, zipfile, os, sys, glob, random

#Specifying formats, and download and subtitle string.
FORMAT = ['.mp4', '.avi', '.mkv']
DOWNLOAD = '/subtitle/download'
SUBTITLE = '/subtitles/'
MAXURL = 10

#Specifying variables to be used in the script.
skip = False
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
>>>>>>> e4a99c7a93bf70e26b537e4c25a921ebe8651425
def removeTags(siteList):
	i = 0
	while 1:
		try:
			#All info above this is removed.
			if siteList[i] != 'class="a1">':
				siteList.pop(i)	
			else:
				break
		except IndexError:
			print "No subtitle found..."
			sys.exit()

	while 1:
		i = len(siteList)-1
		#All info below this is removed.
		if siteList[i] != 'class="alternativeSearch">':
			siteList.pop(i)
		else:
			break

#Add valid subtitles to a list. Each element consists of a list of two elements[name, url].
def filterURL(siteList, phrase):
	urlList = []
	title = ""
	i = 0
	for l in siteList:
		if l[:6] == 'href="' and phrase in l:
			urlIdx = siteList.index(l)
			while urlIdx  <= len(siteList):
				if siteList[urlIdx-1] == '<span>':
					title = ""
					while siteList[urlIdx] != '</span>':
						title += siteList[urlIdx]
						urlIdx += 1
					break
				urlIdx += 1

			if title != "":
				urlList.append([title, l[6:-2]])
			else:
				urlList.append([l[6:-2]])
			
			if len(urlList) >= MAXURL:
				break

	return urlList

#Print help and exit.
def printHelp():
	print '\n', 'Help for SubPy:'
	print 'Run this script within the directory of the movie you wish to download subtitles for.'
	print 'Run with the argument "-lang=<your-language>" to get a subtitle of that language, or all to display all subtitles.'
	print 'Run with the argument "-dir=<full_directory_path>" to find video files in an alternative directory.'
	print 'Run with the argument "-skip" to automatically choose the top-most subtitle.'
	sys.exit()

#Generate path based on directory.
def genPath(directory):
	return directory + '/tmp' + str(random.randint(10000, 99999))

#Promts the user and return the chosen list item.
def chooseItem(iList, iType, nested):
	if len(iList) == 1:
		if nested:
			return iList[0][1]
		else:
			return iList[0]
	
	i = 1
	while i <= len(iList):
		if nested:
			print '[' + '{0:2d}'.format(i) + '] ' + iList[i-1][0]
		else:
			print '[' + str(i) + '] ' + iList[i-1]
		i += 1
	
	try:
		idx = int(raw_input("Choose " + iType + ": "))
	except ValueError:
		print "Invalid input!"
		sys.exit()
	
	if idx <= len(iList) and idx > 0:
		if nested:
			return iList[idx-1][1]
		else:
			return iList[idx-1]
	else:
		print "Invalid " + iType + " number!"
		sys.exit()

#Generate torrentName.
def genTorrentName(directory):
	tList = []
	for f in os.listdir(directory):
		for  extension in FORMAT:
			if extension in f:
				tList.append(f.replace(extension, ''))
	if len(tList) == 0:
		print "No video file in directory"
		sys.exit()
	else:
		return chooseItem(tList, "video", False)
	

#Generate torrentURL.
def genTorrentURL(torrentName):
	return 'http://www.subscene.com/subtitles/release?q=' + torrentName + '&r=true'

##### MAIN PART OF SCRIPT #####
for arg in sys.argv:
	#If help is given as argument, print help and exit.
	if arg == '-h' or arg == '--help':
		printHelp()
	else:
	#If any of the other acceptable arguments are given.
		if '-lang=' in arg:
			lang = arg.replace('-lang=', '')
		elif '-dir=' in arg:
			directory = arg.replace('-dir=', '')
			path = genPath(directory)
		elif '-skip' in arg:
			skip = True
			

torrentName = genTorrentName(directory)
torrentURL = genTorrentURL(torrentName)

print "Searching for: " + lang + ' - "' + torrentName + '"'

#Find and add all valid URL's to a list.
site = urllib.urlopen(torrentURL)
text = site.read()
tList = text.split()
removeTags(tList)
urlList = filterURL(tList, SUBTITLE)

#Find the correct language.
subURL = []
for url in urlList:
	if lang in url[1] or lang == 'all':
		subURL.append([url[0], 'http://www.subscene.com' + url[1]])

if len(subURL) == 0:
	print 'No subtitle available in that language'
	sys.exit()

#Get download-URL.
if skip:
	subSite = urllib.urlopen(subURL[0][1])
else:
	subSite = urllib.urlopen(chooseItem(subURL, 'subtitle', True))
line = (subSite.read()).split()
urlList = filterURL(line, DOWNLOAD)
url = 'http://www.subscene.com' + urlList[0][0] + '0'

#Handle redirects.
test = urllib.urlopen(url)
url = test.geturl()

#Get, unzip and delete.
subT = urllib.URLopener()

error = True
i = 0
while error:
	try:
		subT.retrieve(url, path)
		error = False
	except IOError as e:
		if i > 50:
			print("Problems retrieving file from subscene...exiting..")
			sys.exit()
		path = path.replace(path[-5:], str(random.randint(10000, 99999)))
		i += 1

ziptest = zipfile.ZipFile(path)
ziptest.extractall(directory)
os.remove(path)

print "Subtitle downloaded!"
