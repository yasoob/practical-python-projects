"""
Using This Code Example
=========================
The code examples are provided by Yasoob Khalid to help you 
reference Practical Python Projects book. Code samples follow
PEP-0008, with exceptions made for the purposes of improving book
formatting. Example code is provided "as is".
Permissions
============
In general, you may use the code we've provided with this book in your
programs . You do not need to contact us for permission unless you're
reproducing a significant portion of the code and using it in educational
distributions. Examples:
* Writing an education program or book that uses several chunks of code from
    this course requires permission. 
* Selling or distributing a digital package from material taken from this
    book does require permission.
* Answering a question by citing this book and quoting example code does not
    require permission.
Attributions usually include the title, author, publisher and an ISBN. For
example, "Practical Python Projects, by Yasoob Khalid. Copyright 2020 Yasoob."
If you feel your use of code examples falls outside fair use of the permission
given here, please contact me at hi@yasoob.me.
"""

import json
import base64
from selenium import webdriver

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
            "width: Math.max(window.innerWidth, document.body.scrollWidth, " + \
                "document.documentElement.scrollWidth)|0," + \
            "height: Math.max(innerHeight, document.body.scrollHeight, " + \
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
driver = webdriver.Chrome()
remote_url = "https://zulko.github.io/moviepy/getting_started/effects.html"
driver.get(remote_url)
png = chrome_takeFullScreenshot(driver)
with open("website_image.png", 'wb') as f:
    f.write(png)
    
driver.close()
