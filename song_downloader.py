import spotipy
import os
import getpass
import pytube
from spotipy.oauth2 import SpotifyClientCredentials
from pyyoutube import Client
from dotenv import load_dotenv
from apiclient.discovery import build

load_dotenv()

#libraries
""" spotipy
    python-youtube
    google-api-python-client
    pytube
    git+https://github.com/pytube/pytube
"""

#Spotify Authentication
spotify_id = os.getenv('SPOTIFY_ID')
spotify_secret = os.getenv('SPOTIFY_SECRET')
spotify_credentials = SpotifyClientCredentials(client_id = spotify_id, client_secret = spotify_secret)
sp = spotipy.Spotify(client_credentials_manager = spotify_credentials)

#Youtube Authentican
youtube_api = os.getenv('YOUTUBE_API_KEY')
youtube = build('youtube', 'v3', developerKey = youtube_api)

#yeah
not_found = []

#Create folder 
user = getpass.getuser()
song_path = f"C:\\Users\\{user}\\Desktop\\Songs_MP3"
perm = 0o777

try:
    os.umask(0)
    os.mkdir(song_path)
    print("Folder created in desktop")
except:
    print("Folder already exists")
        

#Gets songs from the playlist
def get_playlist(playlist_url):
    global song
    playlist_id = playlist_url
    songs = sp.playlist_tracks(playlist_id)
    for x in songs['items']:
        song = x['track']['name']
        get_youtube_video(song)


#Get the video/ notify if not found
def get_youtube_video(song):
    global not_found
    try:
        request = youtube.search().list(q=song, part = 'snippet', type = 'video', maxResults = 1)
        res = request.execute()
        for song in res['items']:
            song_name = song['snippet']['title']
            song_id = song['id']['videoId']
            print(f"\nSong found - {song_name}") 
            get_youtube_link(song_id)  
    except:
        print(f"{song} not found")


#Get url of song to download
def get_youtube_link(video_id):
    global song
    try:
        song_url = f"https://www.youtube.com/watch?v={video_id}"
        print(f"Downloading song - {song}")
        download_song(song_url)
    except Exception as e:
        print(f"Error: {e}")
        print("Failed to download the song.")


#Download song and place in a folder
def download_song(url):
    global song
    try:
        yt = pytube.YouTube(url, use_oauth=True, allow_oauth_cache=True)
        yt_song = yt.streams.filter(only_audio=True, file_extension = 'mp4').first()
        yt_song.download(song_path)
        print(f"Downloaded at {song_path}\n")
    except Exception as e:
        print("Failed to download song\n")
        print(e)
        

playlist_url = input("Paste playlist url: ")
get_playlist(playlist_url)
if not_found != None:
    for x in not_found:
        print(f"Songs not downloaded: {x}")
else:
    print("All songs downloaded successfully")
      