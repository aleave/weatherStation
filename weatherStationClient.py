#!/usr/bin/env python

import requests as re
import time


import datetime as dt
import numpy as np


from PIL import Image
from PIL import ImageDraw
import time
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics



# Configuration for the matrix
options = RGBMatrixOptions()
options.rows = 32
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'adafruit-hat'  # If you have an Adafruit HAT: 'adafruit-hat'

matrix = RGBMatrix(options = options)

#matrix colors
colout = (100,100,100)


#insert here the url with unique api key and your lat,lon obtained by DarkSky:
#https://darksky.net/dev
url = "https://api.darksky.net/forecast/your_key_and_lat_long_here?units=si&lang=it&exclude=hourly"



def weatherAct(matrix):
    font = graphics.Font()
    font.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/4x6.bdf") #folder with the fonts for the RGB matrix


    data = re.get("http://192.168.1.117/weather").json() #put here the IP of your NodeMCU
    data["time"] = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    #df = pd.DataFrame.from_records([data])
    posx=0
    posy0=6

    textColor = graphics.Color(colout[0], colout[1],colout[2])

    matrix.Clear()
    text1 = "T:"+ "{0:.1f}".format(data["BMP_Temperature"])+" C"
    text2 = "H:"+ "{0:.0f}".format(data["DHT_Humidity"]) + " %"
    text3= "{0:.0f}".format(data["BMP_Pressure"]/100)+" hPa"
    
    graphics.DrawText(matrix, font, posx, posy0, textColor, text1)
    graphics.DrawText(matrix, font, posx, posy0+6, textColor, text2)
    graphics.DrawText(matrix, font, posx, posy0+12, textColor, text3)




def displayIcon(icon, matrix, posx, posy, w,h, colout):
    image_file = "./weather-Icons/"+icon+".ppm" #the weather icons are saved in a subfolder named weather-Icons
    im = Image.open(image_file)
    im = im.convert('RGBA')
    
    data = np.array(im)   # "data" is a height x width x 4 numpy array
    red, green, blue, alpha = data.T # Temporarily unpack the bands for readability

    # Replace white with red... (leaves alpha values alone...)
    white_areas = (red == 255) & (blue == 255) & (green == 255)
    data[..., :-1][white_areas.T] = colout # Transpose back needed

    image = Image.fromarray(data)
    image.thumbnail((w, h), Image.ANTIALIAS)

    if icon in ["fog", "wind", "cloudy"]: #position adjustments for some icons
        posy +=2

    matrix.SetImage(image.convert('RGB'),posx,posy)
    

def runWeatherFcast(matrix, url):

        req = re.get(url)

        dat = req.json()
        icon_now=dat["currently"]["icon"]
        #icon_today=dat["daily"]["data"][0]["icon"]
        #temp = dat["currently"]["temperature"]
        icon_today=dat["daily"]["data"][0]["icon"]

        return icon_now,icon_today


        

icony = 18 #starting row for the weather icons
iconsiz = 14 #size in pixels of the weather icons

t0 = time.time()

#priming cycle
weatherAct(matrix)
icon_now, icon_today=runWeatherFcast(matrix, url)
displayIcon(icon_now, matrix, 1, icony,iconsiz,iconsiz,colout)
displayIcon(icon_today, matrix, 17, icony,iconsiz,iconsiz,colout)

time.sleep(30)

while 1:


    t1 = time.time()
    deltat = t1-t0
    
    weatherAct(matrix)
    


    #poll darksky only every 5 min, the free API has a limit of 1000 calls per day

    if (deltat > 300):
        icon_now, icon_today=runWeatherFcast(matrix, url)
        t0 = time.time() #restart the time counter
        print("updating weather forecast...")
        
    displayIcon(icon_now, matrix, 1, icony,iconsiz,iconsiz,colout)
    displayIcon(icon_today, matrix, 17, icony,iconsiz,iconsiz,colout)
    
    time.sleep(30)

 
