from pytube import YouTube
from PIL import Image,ImageFilter,ImageEnhance
from moviepy.editor import *
import requests, os


def downloadYouTube(preid):
    idv      = preid
    urlPr    = 'http://i.ytimg.com/vi/'+idv+'/hqdefault.jpg'
    urlVideo = 'https://www.youtube.com/watch?v='+idv

    try:
        yt  = YouTube(urlVideo)
    except:
        input('\nНеверный ID Видео. Для выхода нажмите Enter.')
        exit ()

    print('Скачивание превью.')
    raw = requests.get(urlPr,stream=True).raw

    print('Уникализация превью.')
    image    = Image.open(raw)
    image    = image.filter(ImageFilter.GaussianBlur(0.8))
    image    = image.filter(ImageFilter.UnsharpMask(1.3))
    enhancer = ImageEnhance.Contrast(image)
    if not os.path.exists('./' + idv):
        os.makedirs('./' + idv)
    enhancer.enhance(1.5).save('./' + idv + '/preview.png')

    def downloadYouTube(videourl, path):
        yt          = YouTube(videourl)
        author      = yt.author
        title       = yt.title
        description = yt.description
        tags        = str(yt.keywords).strip('[]')
        tags        = tags.replace("'","")

        file = open('./' + idv + '/title.txt','w', encoding='utf-8')
        file.write(title)
        file.close()

        file = open('./' + idv + '/description.txt','w', encoding='utf-8')
        file.write(description)
        file.close()
        
        file = open('./' + idv + '/tags.txt','w', encoding='utf-8')
        file.write(str(tags))
        file.close()

        print('Скачивание видео.')
        yt          = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        yt.download(path, 'prevideo.mp4')
        
        if not os.path.exists('./' + idv):
            os.makedirs('./' + idv)
        
        print('Уникализация видео (занимает некоторое время).')
        video       = VideoFileClip('./' + idv + '/prevideo.mp4')
        video       = video.fx(vfx.lum_contrast, contrast=0.05)
        video       = video.cutout(0,2)
        text        = TextClip(author, font='Purisa Bold', color='white', fontsize=30)
        text        = text.set_duration(video.duration)
        text        = text.set_pos('top')
        audio       = video.audio
        audio       = audio.fx(afx.volumex, 1.15)
        audio       = audio.fx(afx.audio_fadein, 1.15)
        audio       = audio.fx(afx.audio_fadeout, 1.15)
        video       = video.set_audio(audio)   
        final       = CompositeVideoClip([video, text])
        final.write_videofile('./' + idv + '/video.mp4', threads = 8, codec = 'libx264')
        video.close()
        final.close()
        os.remove('./' + idv + '/prevideo.mp4')
    downloadYouTube(urlVideo,'./' + idv)
idv = str(input('\nID Video: '))
downloadYouTube(idv)