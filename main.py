from flask import Flask
from working import video_scrapper
app= Flask(__name__)
@app.route('/')
def index():
  client_id = "88672929"
  url = "https://secure.simplepractice.com/clients/83cdf3a00620ca58/insurance_claims/"+client_id
  video_scrapper(url)
  return "<h1>Welcome to CodingX</h1>"
