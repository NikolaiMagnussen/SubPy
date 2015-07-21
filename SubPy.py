#!/usr/bin/python3
import os
import sys
import random
from zipfile import ZipFile

import requests
from lxml.html import parse
from lxml import etree

LANGUAGE = "English"
FORMATS = (".mp4", ".avi", ".mkv")

def main():
    sd = SubDownloader()

    releases = sd.get_releases()
    idx = sd.user_choose(releases)
    sd.get_subs(releases[idx])

    sd.download_sub(sd.user_choose(sd.get_titles()))

def exit(error):
    """Prints the error string given, before exiting."""
    print(error)
    input("Exiting...Press Enter to continue")
    sys.exit()

class SubDownloader:
    def user_choose(self, contentList):
        """Print the user a menu and return the index of the user's choice."""
        if len(contentList) == 0:
            exit("There are no possible choices..")

        for (idx, f) in enumerate(contentList):
            print("[{idx}] {f}".format(idx = idx, f = f))

        while True:
            try:
                idx = int(input("Choose an element from the list, or -1 to exit: "))
            except:
                continue

            if 0 <= idx < len(contentList):
                break
            elif idx == -1:
                exit("")

        return idx

    def get_releases(self):
        """Get the all releases in the current directory, returning them in a list."""
        return [x[:-4] for x in os.listdir(os.getcwd()) if x.endswith(FORMATS)]

    def get_subs(self, release):
        """Generate the search url, set the."""
        url =  "http://www.subscene.com/subtitles/release?q={release}&r=true".format(release = release)
        doc = parse(url).getroot()
        subtitles = doc.cssselect('html body div#content.clearfix div.subtitles.byFilm.byReleaseName div.box div.content table tbody tr td.a1 a')
        subtitles = [x for x in subtitles if x[0].text_content().strip() == LANGUAGE]
        self.subtitles = [x for x in subtitles if x.getparent().getparent().cssselect('td.a40')]

    def get_titles(self):
        """Generate a list of titles from the subtitles to be printed for the menu."""
        return [x[1].text_content().strip() for x in self.subtitles]

    def download_sub(self, idx):
        """Download the chosen subtitle, and removing the zip-file afterwards."""
        url = "http://www.subscene.com{link}".format(link = self.subtitles[idx].get('href'))
        dl = parse(url).getroot().xpath('//*[@id="downloadButton"]')
        dl_url = "http://www.subscene.com{link}".format(link = dl[0].get('href'))

        fn = "{cd}/tmp{random}".format(cd = os.getcwd(), random = random.randrange(10000))
        with open(fn, 'wb') as f:
            for chunk in requests.get(dl_url):
                f.write(chunk)

        with ZipFile(fn, 'r') as zf:
            zf.extractall()

        os.remove(fn)

if __name__ == "__main__":
    main()
