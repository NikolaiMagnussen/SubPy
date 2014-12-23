import urllib, zipfile, os, sys, glob

EXT = ['.mp4', '.avi', '.mkv']
lang = 'english'
directory = os.getcwd() + '/tmp'
path = os.getcwd()
files = glob.glob("*")
torrentURL = ""
torrentName = "<No file>"
for f in files:
	for e in EXT:
		if e in f:
			torrentName = f
			torrentURL = 'http://www.subscene.com/subtitles/release?q=' + f.replace(e, '') + '&r=true'
			break
	if len(torrentURL) != 0:
		break
DOWNLOAD = '/subtitle/download'
SUBTITLE = '/subtitles/'


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


##### MAIN PART OF SCRIPT #####
print "Searching for: " + torrentName

site = urllib.urlopen(torrentURL)
text = site.read()
tList = text.split()
removeTags(tList)

#Add all valid subtitle URL's to a list
urlList = filterURL(tList, SUBTITLE)

#Find the correct language
for url in urlList:
	if lang in url:
		subURL = 'http://www.subscene.com' + url[:-1]
		break

#Get download-URL
subSite = urllib.urlopen(subURL)
line = (subSite.read()).split()
uerrlList = filterURL(line, DOWNLOAD)
uerrl = 'http://www.subscene.com' + uerrlList[0]

#Handle redirects
test = urllib.urlopen(uerrl)
uerrl = test.geturl()

#Get, unzip and delete
subT = urllib.URLopener()
subT.retrieve(uerrl, directory)
ziptest = zipfile.ZipFile(directory)
ziptest.extractall(path)
os.remove(directory)

print "Subtitle downloaded!"
