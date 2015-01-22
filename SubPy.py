import urllib, zipfile, os, sys, glob, random

#Specifying formats, and download and subtitle string.
FORMAT = ['.mp4', '.avi', '.mkv']
DOWNLOAD = '/subtitle/download'
SUBTITLE = '/subtitles/'
MAXURL = 20

#Specifying variables to be used in the script.
skip = False
lang = 'english'
hi = "off"
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
def filterURL(siteList, phrase, hiFilter):
	urlList = []
	title = ""
	i = 0
	for l in siteList:
		if l[:6] == 'href="' and phrase in l:
			urlIdx = siteList.index(l)
			hi = False
			#Get title
			while urlIdx  <= len(siteList) and phrase == SUBTITLE:
				if siteList[urlIdx-1] == '<span>':
					title = ""
					while siteList[urlIdx] != '</span>':
						title += siteList[urlIdx]
						urlIdx += 1
					break
				urlIdx += 1

			#Get HI status
			if phrase == SUBTITLE:
				while siteList[urlIdx] != 'class="a41">' and siteList[urlIdx] != 'class="a40">':
					urlIdx += 1
				if siteList[urlIdx] == 'class="a41">':
					hi = True


			#Append subtitle to the list based on hiFilter
			if title != "":
				print "HI:Filter is - " + hiFilter
				if hiFilter == 'off':
					print "filter off"
					urlList.append([title, l[6:-2], hi])
				elif hiFilter == 'on' and hi:
					print "filter on"
					urlList.append([title, l[6:-2], hi])
				elif hiFilter == 'no' and not hi:
					print "no filter"
					urlList.append([title, l[6:-2], hi])
			#Appending download link
			else:
				urlList.append([l[6:-2]])
			
	return urlList

#Print help and exit.
def printHelp():
	print '\n', 'Help for SubPy:'
	print 'Run this script within the directory of the movie you wish to download subtitles for.'
	print 'Run with the argument "-lang=<your-language>" to get a subtitle of that language, or all to display all subtitles.'
	print 'Run with the argument "-dir=<full_directory_path>" to find video files in an alternative directory.'
	print 'Run with the argument "-skip" to automatically choose the top-most subtitle.'
	print 'Run with the argument "-hi=<on/no/off>" to only display HI, display no HI, or display both.'
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
			if iList[i-1][2]:
				print '[' + '{0:2d}'.format(i) + '] ' + iList[i-1][0] + ' - HI'
			else:
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

def processArgs(args):
	for arg in args:
		#If help is given as argument, print help and exit.
		if arg == '-h' or arg == '--help':
			printHelp()
		else:
		#If any of the other acceptable arguments are given.
			if '-lang=' in arg:
				global lang
				lang = arg.replace('-lang=', '')
			elif '-dir=' in arg:
				global path
				directory = arg.replace('-dir=', '')
				path = genPath(directory)
			elif '-skip' in arg:
				global skip
				skip = True
			elif 'hi=' in arg:
				global hi
				hi = arg.replace('-hi=', '')
				print hi
	

def main():
	processArgs(sys.argv)

	torrentName = genTorrentName(directory)
	torrentURL = genTorrentURL(torrentName)
	
	print "Searching for: " + lang + ' - "' + torrentName + '"'
	
	#Find and add all valid URL's to a list.
	site = urllib.urlopen(torrentURL)
	text = site.read()
	tList = text.split()
	removeTags(tList)
	print "Filtering HI: " + hi
	urlList = filterURL(tList, SUBTITLE, hi)
	
	#Find the correct language.
	subURL = []
	for url in urlList:
		if (lang in url[1] or lang == 'all') and len(subURL) < MAXURL:
			subURL.append([url[0], 'http://www.subscene.com' + url[1], url[2]])
	
	if len(subURL) == 0:
		print 'No subtitle available in that language'
		sys.exit()
	
	#Get download-URL.
	if skip:
		subSite = urllib.urlopen(subURL[0][1])
	else:
		subSite = urllib.urlopen(chooseItem(subURL, 'subtitle', True))
	line = (subSite.read()).split()
	urlList = filterURL(line, DOWNLOAD, hi)
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
	ziptest.close()
	os.remove(path)
	
	print "Subtitle downloaded!"

if __name__ == "__main__":
	main()
