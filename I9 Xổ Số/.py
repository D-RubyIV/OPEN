import easyocr
reader = easyocr.Reader(['en']) # this needs to run only once to load the model into memory
result = reader.readtext('image.jpg')
for (bblox, text, prob) in result:
    print(text)