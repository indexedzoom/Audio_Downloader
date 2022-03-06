import yt_dlp, os, wget
from mutagen.mp3 import MP3
from mutagen.id3 import ID3,APIC,error
from pytube import Playlist,YouTube

audio_path=""
cover_path=""
blocked_chars='\/:*?"<>|'
unblocked_chars="⧵∕;＊？“←→⸡"
count=0

def thumbnail(url,file_name):
    tn=wget.download(url,cover_path+"/"+file_name+".jpg")

    audio = MP3(audio_path+"/"+file_name+".mp3", ID3=ID3)
    # adding ID3 tag if it is not present
    try:
        audio.add_tags()
    except error:
        pass
    
    audio.tags.add(APIC(mime='image/jpeg',type=3,desc=u'Cover',data=open(tn,'rb').read()))
    print(file_name)
    # edit ID3 tags to open and read the picture from the path specified and assign it
    audio.save()  # save the current changes


def title(path):
    audio = ID3(path)
    if "- " in file:
        audio.add(TIT2(encoding=3, text=path.split("/")[-1].split(".mp3")[0].split("- ")[-1]))
    else:
        audio.add(TIT2(encoding=3, text=path.split("/")[-1].split(".mp3")[0]))
    audio.save()

def opts(name):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl':audio_path + name,
    }
    return ydl_opts
        
    
def download_audio():
    video_list=[]

    link = input("\nEnter Url here: ")
    
    if "playlist" in link:
        playlist_list=Playlist(link)
        playlist_range0=int(input("Enter start of range here: "))
        playlist_range1=int(input("Enter end of range here: "))
            
        
        for i in range(playlist_range0,playlist_range1):
            if i>=0:
                video_list.append(playlist_list.video_urls[i])
        link=link.split("&")[0]

        
    if "playlist" not in link:
        ydl_opts=opts('/%(title)s.%(ext)s')
        video_list.append(link)
        for a in YouTube(video_list[0]).title:
            if a in blocked_chars:
                video_title=YouTube(video_list[0]).title.replace(a,unblocked_chars[blocked_chars.index(a)])
                ydl_opts=opts("/"+video_title+".mp3")
                    
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download(video_list[0],)
            print("start")
            
        thumbnail(YouTube(video_list[0]).thumbnail_url,video_title)
        video_list.remove(link)
        
    else:
        end=False
        ydl_opts=opts('/%(title)s.%(ext)s')
        for a in YouTube(video_list[0]).title:
            if a in blocked_chars:
                video_title=YouTube(video_list[0]).title.replace(a,unblocked_chars[blocked_chars.index(a)])
                ydl_opts=opts("/"+video_title+".mp3")
                    
        for i in range(len(video_list)):
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                #download audio
                ydl.download((video_list[i],))
                
            thumbnail(YouTube(video_list[i]).thumbnail_url,YouTube(video_list[i]).title)

while True:
    download_audio()
