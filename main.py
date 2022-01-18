from flask import Flask
from working import video_scrapper
from flask import jsonify
app= Flask(__name__)
@app.route('/<int:number>/')
def index(number):

  url = "https://secure.simplepractice.com/clients/83cdf3a00620ca58/insurance_claims/"+str(number)
  data = video_scrapper(url)
  resp = jsonify(data)
  return resp
    
  

