from selenium import webdriver
import time
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import StaleElementReferenceException
import warnings
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from urllib.request import HTTPError
import os
import pytube as pt
import shutil
from moviepy.video.io.VideoFileClip import VideoFileClip
from pytube.exceptions import RegexMatchError
import time
import re
from tqdm import tqdm
import glob
import sys

YT = 'https://www.youtube.com'

'''
Youtube page is basically use client Re-directing method.
They renew form with Ajax communication

- Use selenium with headless browser to get renewed HTML

- The selenium module has a weakness in finding the lower html element. 

- So i decided to get renewed html with selenium's webdriver and read page with BeautifulSoup and find inner html element.
'''


#ignore future warnings and selenium warnings
warnings.filterwarnings("ignore")

class getPlaylistURLs:
    def RedirectionLoader(self,driver):
        elem = driver.find_element_by_tag_name("html")
        count = 0
        while True:
            count += 1
            if count > 5:
                print("Redirection Finished!")
                return
            time.sleep(0.5)
            try:
                elem == driver.find_element_by_tag_name("html")
            except StaleElementReferenceException:
                return

    def ReturnURLsAsList(self,URL):
        options = webdriver.ChromeOptions()
        # Connect as headless brower. If not, youtube server recognize request as bot.
        options.add_argument('headless')
        driver = webdriver.Chrome(executable_path='chromedriver.exe',chrome_options=options)
        url = URL
        driver.get(url)
        os.system('cls')
        print("Redirecting Client.... it'll take a second")
        self.RedirectionLoader(driver)
        #In selenum they call 'class' as 'CLASS_NAME' beacause there's class method is java version selenium
        videorenderTags = driver.find_elements(By.CLASS_NAME, 'style-scope ytd-playlist-video-renderer')
        html = driver.page_source

        bs = BeautifulSoup(html, 'html.parser')
        # Non-Public Playlist -> Return Empty List
        # Not existing Playlist -> Return Empty List
        li = bs.findAll('ytd-thumbnail', {'class': 'style-scope ytd-playlist-video-renderer'})
        return li

    def DecideDirectoryName(self,directoryLi):
        startNumber = 1
        looper = True
        while looper:
            base = "Playlist_" + str(startNumber)
            if base in directoryLi:
                startNumber+=1
            else:
                looper = False
                return base

GL = getPlaylistURLs()

outer_loop = True
while outer_loop:
    inner_loop = True
    program_dir = os.getcwd()
    directorylist = os.listdir(os.getcwd())
    finalDirectoryName = GL.DecideDirectoryName(directorylist)
    print("Youtube playlist extractor made by Hoplin")
    print("This program is open source and protected by MIT License")
    print("Github : https://github.com/J-hoplin1/Youtube-Playlist-Extractor\n\n\n")
    try:
        print("Files will be saved in this directory : "+program_dir+"\\"+finalDirectoryName)
        playlistURL = input("Enter URL : ")
        YTPlaylist_Patter = re.compile('https\:\/\/www\.youtube\.com\/playlist\?list\=[A-Za-z0-9?=.&_#$]*')
        ckPattern = YTPlaylist_Patter.match(playlistURL)
        if ckPattern:
            while inner_loop:
                os.system('cls')
                print("Is this URL you want to extract? : ",playlistURL)
                print("Please check if the playlist is set to public!!\n\n")
                yon = input("Press 'n' key to re-enter. Or press 'y' key to move on to the next section. : ")
                if yon == 'n' or yon == "N":
                    print("Reload initial page...")
                    time.sleep(2.5)
                    os.system('cls')
                    inner_loop = False
                elif yon == 'y' or yon == "Y":
                    inner_loop = False
                    os.system('cls')
                    ulist = GL.ReturnURLsAsList(playlistURL)
                    if len(ulist) == 0:
                        print("Nothing to extract! These reasons can be the cause.")
                        print("1. Empty Playlist")
                        print("2. Not existing Playlist")
                        print("3. Play list is set as non-public\n\n")
                        print("Reload initial page...")
                        time.sleep(4)
                        os.system('cls')
                    else:
                        os.mkdir(program_dir + '\\' + finalDirectoryName + "\\")
                        downloadDirectory = program_dir + '\\' + finalDirectoryName # + "\\"
                        print("Now downloading files(Total "+str(len(ulist))+"links searched)...")
                        print("The download speed may vary depending on the number and size of images and the Internet environment...")
                        try:
                            for li in tqdm(range(len(ulist))):
                                YTu = pt.YouTube(YT + ulist[li].a['href'])
                                options = YTu.streams
                                defaultname = options[0].default_filename
                                options[0].download(downloadDirectory)
                                title = defaultname.split('.mp4')[0]
                                '''
                                Through this method, can't make mp4 -> mp3
                                
                                title = YTu.title
                                YTu.streams.filter(file_extension='mp4').first().download(
                                    downloadDirectory)
                                '''
                                clip = VideoFileClip(downloadDirectory + "\\" + defaultname)
                                clip.audio.write_audiofile(
                                    downloadDirectory + "\\" + title + ".mp3",
                                    logger=None
                                )
                            print("Finish to download. Now purge directories....")
                            os.mkdir(program_dir + '\\' + finalDirectoryName + "\\" + 'mp3')
                            mp3List = glob.glob(os.path.join(downloadDirectory, '*.mp3'))
                            for e in mp3List:
                                shutil.move(e, program_dir + '\\' + finalDirectoryName + "\\" + 'mp3' + '\\' +
                                            e.split('\\')[-1])
                            print("Process Finished! Go back to menu after 4 second")
                            time.sleep(4)
                            os.system('cls')
                        except IndexError as e:
                            print("Error : Wrong option number.")
                            time.sleep(2.5)
                            os.system('cls')
                        except FileNotFoundError as w:
                            print("Error : Unexpected critical error. Can't re-encode File.")
                            time.sleep(2.5)
                            os.system('cls')
                        except FileExistsError as e:
                            print("Error : Already existing directory name - ", defaultfilename.split('.mp4')[0])
                            time.sleep(2.5)
                            os.system('cls')
                        except HTTPError as e:
                            print("Error : Selected option has been blocked.")
                            time.sleep(2.5)
                            os.system('cls')
                            # Exception when ACodec = False
                        except AttributeError as e:
                            print("Download Completed")
                            time.sleep(2.5)
                            os.system('cls')
                            # Exception when download webm or ACodec
                        except KeyError as e:
                            print("Download Completed")
                            time.sleep(2.5)
                            os.system('cls')
                        except RegexMatchError as e:
                            print("Error : Unable to open URL. Check your URL again.")
                            time.sleep(2.5)
                            os.system('cls')
                        except EOFError as e:
                            print("Error : Unexpected Error....")
                            time.sleep(2.5)
                            os.system('cls')
                        except KeyboardInterrupt as e:
                            print("Error : Keyboard hit has been interrupted! Did you entered Ctrl + C?")
                            time.sleep(2.5)
                            os.system('cls')
        else:
            print("Wrong pattern type URL. Please check again.")
            time.sleep(2.5)
            os.system('cls')

    except KeyboardInterrupt:
        print("Keyboard interrupted! Reload initial page....")
        time.sleep(2.5)
        os.system('cls')
    except EOFError:
        print("Unexpected Error.... Reload initial page.....")
        time.sleep(2.5)
        os.system('cls')

