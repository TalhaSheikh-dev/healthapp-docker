from flask import Flask
from working import video_scrapper
from flask import send_file
app= Flask(__name__)
@app.route('/<int:number>/')
def index():
  client_id = "88672929"
  url = "https://secure.simplepractice.com/clients/83cdf3a00620ca58/insurance_claims/"+number
  data = video_scrapper(url)
  send_file(data, as_attachment=True)
  return "successful"
