# coding: utf-8

import os
import re
import requests

TiebaPrefix = "https://tieba.baidu.com/"
Headers = {
    "Connection" : "keep-alive",
    "user-Agent" : "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
}

def downloadFile(url,folderName=""):
    fileName = url.split('/')[-1]
    r = requests.get(url,headers=Headers)
    if(folderName):
        if not os.path.exists(folderName):
            os.makedirs(folderName)
        filePath = folderName + "/" + fileName
    else:
        filePath = fileName
    f = open(filePath, 'wb')
    for chunk in r.iter_content(chunk_size=512 * 1024):
        if chunk:
            f.write(chunk)
    f.close()
    return

'''
Get the urls of 'tiezi' in the given pageRange from a specific tieba.
'''
def getPages(tiebaName,pageRange):
    pagePattern = '<a rel="noreferrer" href="/p/(.*?)".*?>.*?</a>'
    pageIndexes = []
    num = 1
    print("Start Requesting PageIndexes from " + tiebaName + "...")
    for pn in pageRange:
        html = requests.get(TiebaPrefix + "/f?kw=" + tiebaName + "&pn=" + str(pn*50),headers=Headers).text
        pageIndexes += (re.findall(pagePattern,html))
        print("Requesting...   " + str(num) + "/" + str(len(pageRange)) + " Completed")
        num += 1
    print("PageIndexes Requests Completed\n")
    pageIndexes = list(set(pageIndexes))
    return pageIndexes

'''
Get all the urls of contextual pictures from a specific tiezi.
'''
def getPictures(pageIndex):
    picturePattern = '<img class="BDE_Image".*?src="(.*?)".*?>'
    html = requests.get(TiebaPrefix + "/p/" + str(pageIndex),headers=Headers).text
    pictureUrls = re.findall(picturePattern,html)
    return pictureUrls

'''
Download pictures on a pictureUrl list.
'''
def downloadPictures(pictures,folderName):
    for picture in pictures:
        downloadFile(picture,folderName)


def main(tiebaNames,pageRange):
    for tiebaName in tiebaNames:
        pageIndexes = getPages(tiebaName,pageRange)
        i = 1
        for pageIndex in pageIndexes:
            pictureUrls = getPictures(pageIndex)
            print("Downloading Pictures from " + pageIndex)
            filePath = tiebaName + "/" + str(pageIndex)
            if not os.path.exists(filePath):
                downloadPictures(pictureUrls, filePath)
            print("Download Complete " + str(i) + "/" + str(len(pageIndexes)))
            print("\n")
            i+=1


# getPages("python",range(3))
# downloadPictures(getPictures("5913731259"),"5913731259")
# tiebaNames = ["00后","05后早恋"]

tiebaNames = ["00后"]

main(tiebaNames,pageRange=range(20))