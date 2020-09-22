import requests 
import re
import urllib.parse
import sys

if len(sys.argv) < 4:
    print("Run the script like this\n\t$ python app.py video_url email password")
    sys.exit()

email = sys.argv[-2]
password = sys.argv[-1]

session = requests.session()
session.headers.update({
  'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:39.0) Gecko/20100101 Firefox/39.0'
})
response = session.get('https://m.facebook.com')
response = session.post('https://m.facebook.com/login.php', data={
  'email': email,
  'pass': password
}, allow_redirects=False)

if 'c_user' in response.cookies:
    # login was successful
    user_id = response.cookies['c_user']
    video_url = sys.argv[-3]
    print("Video url:  "+video_url)

    video_id = re.search('videos/(.+?)/', video_url).group(1)
    video_page = session.get(video_url)

    fb_dtsg_ag = re.search('"async_get_token":"(.+?)"', video_page.text).group(1)

    final_url = ("https://www.facebook.com/video/video_data_async/?"
                "video_id={0}&supports_html5_video=true&").format(video_id)
    
    data = {
        'fb_dtsg_ag':fb_dtsg_ag,
        '__user':user_id,
        '__a':'',
        '__dyn':'',
        '__req':'',
        '__be':'',
        '__pc':'',
        'dpr':'',
        '__rev':'',
        '__s':'',
        'jazoest':'',
        '__spin_r':'',
        '__spin_b':'',
        '__spin_t':'',
    }

    api_call = session.get(final_url, params=data)
    try:
        final_video_url = re.search('hd_src":"(.+?)",', api_call.text).group(1)
    except AttributeError:
        final_video_url = re.search('sd_src":"(.+?)"', api_call.text).group(1)

print(final_video_url.replace('\\',''))