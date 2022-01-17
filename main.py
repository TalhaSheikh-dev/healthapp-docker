from flask import Flask
from working import video_scrapper
from flask import send_file
app= Flask(__name__)
@app.route('/<int:number>/')
def index(number):

  url = "https://secure.simplepractice.com/clients/83cdf3a00620ca58/insurance_claims/"+str(number)
  data = video_scrapper(url)
  return data
  try:
    data = video_scrapper(url)
    return send_file(data, as_attachment=True,cache_timeout=0)
    return "successful"
  except:
    return "something is wrong"
    
  

