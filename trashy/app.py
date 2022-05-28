from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from PIL import Image
import os
import requests

from clarifai.rest import ClarifaiApp
import json

# name, grade, 3 bullet points, source
dictionary = {'Pepsi': {0: 'Large',
                        1: 'PepsiCo, parent company to Lays, has managed to decrease its total climate footprint from 2014 to 2017.'
                           'PepsiCo scores poorly because the brand remains secretive in its sustainability report'
                           'and refuses to disclose information. PepsiCo mentions target to reduce carbon emissions.',
                        2: 'https://rankabrand.org/soda/Pepsi'},
              'Coke': {0: 'Large',
                       1: 'Coca-Cola Company implements measures to reduce emissions, but has still increased in overall climate footprint.'
                          'The company mentions using renewable energy, but is not clear about how much.'
                          'Coca-Cola Company implements measures to purchase its other products, such as coffee, tea and fruits, from sustainable sources',
                       2: 'https://rankabrand.org/soda/Coca-Cola'},
              'Yerba': {0: 'Medium',
                        1: 'Guayaki harvests yerba in an organic and ecologically friendly manner.'
                            ' Guayaki actively contributes to environmental protection by working to restore 200,000 acres of rainforest. '
                            'The company creates 1,000 living wage jobs for local workers.',
                        2: 'https://magazine.wellwallet.com/gold-indios-guayakis-yerba-mate-ushering-sustainable-economy'},
              'Kettle Brand': {0: 'Medium',
                               1: 'After cooking chips with vegetable oil, Kettle Brand converts excess oil to biodiesel to fuel their vehicles.'
                                  'In 2019, Kettle Brand chips cut the amount of materials used in packaging by 43%,'
                                  'reducing greenhouse gas emissions from packaging by 51% and waste from packaging by 2 million pounds.',
                               2: 'https://www.kettlebrand.com/sustainability/'},
              'Fiji': {0: 'Small',
                       1: 'In 2007, Fiji Water has managed to keep their total annual carbon footprint low.'
                          'The company is taking measures to continue to lower their carbon emissions and packaging materials.'
                          'Fiji Water has goals to reduce the amount of fuel used in transporting their products.',
                       2: 'https://www.csrwire.com/press_releases/15107-FIJI-Water-Becomes-First-Bottled-Water-Company-to-Release-Carbon-Footprint-of-Its-Products'},
              'Smart Water': {0: 'Large',
                             1: 'Smartwater\'s parent company, Coca-Cola, implements measures to reduce emissions, but has still increased in overall climate footprint.'
                                'The company mentions using renewable energy, but is not clear about how much.'
                                'Coca-Cola Company implements measures to purchase its other products, such as coffee, tea and fruits, from sustainable sources'
                             ,2: 'https://rankabrand.org/soda/Coca-Cola'}
              }

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("home.html")

@app.route('/processImage', methods=['POST'])
def processImage():
    if request.method == 'POST':
        image = request.files.get("myFile")
        #print(image)
        im = Image.open(image, mode='r')#im is a pillow object

        im.save('userImages/userim.png')

        imageInfo = main('userImages/userim.png')

        print(imageInfo[0])

        return json.dumps(imageInfo)




newArray = [] # Array that is returned. Stored as [name,grade,description,source]
app2 = ClarifaiApp(api_key='a83ecce289b64338a8036f3603e8d551') # api call

def main(url):
    newArray = []
    model1 = app2.models.get('Brand')
    #url = input("URL of image: ")
    output = None
    print(output)
    output = model1.predict_by_filename(url)['outputs'][0]['data']['concepts']
    print(output)
    newJson = json.dumps(output[0]) # dumps json data into newJson
    completeJson = json.loads(newJson) # loads json data into completeJson
    for key in dictionary: # loops through dictionary
        isfound = False # boolean to determine if anything is found
        if key == completeJson['name']: # if dictionary key (name) equals the name in Json, executes code block
            if completeJson['value'] < .8: # Checks if API is over 50% sure of its prediction
                # print('None found, value was only:', completeJson['value'] * 100, "% accurate.")
                return None # returns null if api was too unsure
            newArray.append(key) # first element of array is the name (or key of dictionary
            for size in range(0, 3): # loops from 0-2
                newArray.append(dictionary[key][size]) # appends the 0-2 key values of the original key
            isfound = True
            break
    if isfound: #checks if database name was found and matched
        #print(newArray)
        return newArray
    else:
        print('None found')
        return None

if __name__ == '__main__':
    app.secret_key= 'secret123'
    app.run(debug=True)
