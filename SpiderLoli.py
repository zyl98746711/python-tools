import requests
import json
import youtube_dl

videoUrl = 'https://live.qq.com/video/v/'
detailUrl = 'https://live.qq.com/api/video/detail'
cdnUrl = 'https://p7api.qiecdn.com/api/v1/video/stream/'
finalUrl = 'https://vod.qiecdn.com/'


def download(youtube_url):
    # 定义某些下载参数
    ydl_opts = {
        # outtmpl 格式化下载后的文件名，避免默认文件名太长无法保存
        'outtmpl': '%(id)s%(ext)s'
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])

if __name__ == '__main__':
    for i in range(1, 23):
      #  print(i)
        r = requests.get('https://live.qq.com/api/video/get_user_video?page=' + str(i) + '&type=time&user_id=3413208&pageSize=25')
        text = r.text
        array = json.loads(text)['result']
        for obj in array:
            url = videoUrl + str(obj['id'])
       #    print(obj['id'])
            data = {"video_id":obj['id']}
            res = requests.post(detailUrl, data)
            detail = json.loads(res.text)
            m3u8Url = cdnUrl + str(detail['data']['video_info']['stream_name'])
            response = requests.get(m3u8Url)
         # print(response)
            responseObj = json.loads(response.text)
            key = responseObj['result']['videos'][0]['key']
           # for m3u8 in responseObj['result']['videos']:
            print(finalUrl + key)
            download(finalUrl + key)

        #result = text.result
        #for id in result:
         #   print(id)

