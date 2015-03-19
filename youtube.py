from __future__ import unicode_literals
import youtube_dl
from apiclient.discovery import build
from optparse import OptionParser

DEVELOPER_KEY = "AIzaSyAOEDulIVTM238j9O6sm7YqxfwiNhtWPEc"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


def youtube_search(options):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  search_response = youtube.search().list(
    q=options.q,
    part="id,snippet",
    maxResults=options.maxResults
  ).execute()

  return 'https://www.youtube.com/watch?v=' + search_response.get("items", [])[0]['id']['videoId']

def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


def search_song(artist, song_name):
  parser = OptionParser()
  parser.add_option("--q", dest="q", help="Search term",
  default=artist + ' - ' + song_name)

  parser.add_option("--max-results", dest="maxResults",
  help="Max results", default=10)
  (options, args) = parser.parse_args()
  return youtube_search(options)


def download_song(songUrl):
  ydl_opts = {
   'outtmpl': 'downloaded_songs/%(title)s.%(ext)s',
   'format': 'bestaudio/best',
   'postprocessors': [{
       'key': 'FFmpegExtractAudio',
       'preferredcodec': 'mp3',
       'preferredquality': '192',
    }],
   
   'progress_hooks': [my_hook],
   }

  with youtube_dl.YoutubeDL(ydl_opts) as ydl:
   ydl.download([songUrl])


def download_youtube(artist, title):
    try:
        download_song(search_song(artist, title))
        return True
    except HttpError, e:
        return False