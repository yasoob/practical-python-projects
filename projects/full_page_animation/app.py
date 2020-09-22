import json
import base64
import os
from selenium import webdriver
from moviepy.editor import ImageClip, ColorClip, CompositeVideoClip
import click

def chrome_takeFullScreenshot(driver) :

    def send(cmd, params):
        resource = "/session/%s/chromium/send_command_and_get_result" % \
			driver.session_id
        url = driver.command_executor._url + resource
        body = json.dumps({'cmd':cmd, 'params': params})
        response = driver.command_executor._request('POST', url, body)
        return response.get('value')

    def evaluate(script):
        response = send('Runtime.evaluate', {
			'returnByValue': True, 
			'expression': script
		})
        return response['result']['value']

    metrics = evaluate( \
        "({" + \
            "width: Math.max(window.innerWidth, document.body.scrollWidth," + \
                "document.documentElement.scrollWidth)|0," + \
            "height: Math.max(innerHeight, document.body.scrollHeight," + \
                "document.documentElement.scrollHeight)|0," + \
            "deviceScaleFactor: window.devicePixelRatio || 1," + \
            "mobile: typeof window.orientation !== 'undefined'" + \
        "})")
    send('Emulation.setDeviceMetricsOverride', metrics)
    screenshot = send('Page.captureScreenshot', {
		'format': 'png', 
		'fromSurface': True
	})
    send('Emulation.clearDeviceMetricsOverride', {})

    return base64.b64decode(screenshot['data'])

@click.command()
@click.option('--url', prompt='The URL',
              help='The URL of webpage you want to animate')
@click.option('--output', prompt='Output file name',
              help='Output file name where the animation will be saved')
def main(url, output):
    driver = webdriver.Chrome()
    remote_url = url
    driver.get(remote_url)
    
    png = chrome_takeFullScreenshot(driver)
    with open("website_image.png", 'wb') as f:
        f.write(png)

    driver.close()

    clip = ImageClip('website_image.png')
    
    video_width = int(clip.size[0] + 800)
    video_height = int(video_width/1.5)

    bg_clip = ColorClip(size=(video_width, video_height), color=[228, 220, 220])

    scroll_speed = 180
    total_duration = (clip.h - 800)/scroll_speed

    fl = lambda gf,t : gf(t)[int(scroll_speed*t):int(scroll_speed*t)+800,:]
    clip = clip.fl(fl, apply_to=['mask'])

    video = CompositeVideoClip([bg_clip, clip.set_pos("center")])
    video.duration = total_duration
    if not output.endswith('.mp4'):
        output += '.mp4'
    video.write_videofile(output, fps=26)
    os.remove('website_image.png')

if __name__ == '__main__':
    main()