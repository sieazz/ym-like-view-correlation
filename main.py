import requests
import json


with open('token', 'r') as f:
    token = f.readline()


channel_id = "UCNHkaIrmVGA7JgylP7EP28Q"
data = dict()

url_channel = f"https://www.googleapis.com/youtube/v3/search?&order=viewCount&part=snippet&channelId={channel_id}&type=video&maxResults=50&key={token}"
res_channel = requests.get(url_channel).json()

while True:
    for item in res_channel["items"]:
        video_id = item["id"]["videoId"]
        title = item["snippet"]["title"]
        print(title)
        url_video_statistics = f"https://www.googleapis.com/youtube/v3/videos?part=statistics&id={video_id}&key={token}"
        statistics = requests.get(url_video_statistics).json()
        view_count = int(statistics["items"][0]["statistics"]["viewCount"])
        like_count = int(statistics["items"][0]["statistics"]["likeCount"])
        if title in data and data[title]['view'] > view_count:
            continue
        data[title] = {"view": view_count, "like": like_count, "ratio": like_count / view_count}
    
    if "nextPageToken" in res_channel:
        url_channel = f"https://www.googleapis.com/youtube/v3/search?&order=viewCount&part=snippet&channelId={channel_id}&type=video&pageToken={res_channel['nextPageToken']}&maxResults=50&key={token}"
        res_channel = requests.get(url_channel).json()
    else:
        break


for key, val in sorted(data.items(), key=lambda x: x[1]["ratio"], reverse=True):
    print(key, val)


with open("./pas.json", 'w') as outfile:
    json.dump(data, outfile, ensure_ascii=False)