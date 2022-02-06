from flask import Flask,request
from working import video_scrapper,id_scrapper,id_scrapper_page
from flask import jsonify
app= Flask(__name__)
app.debug = False
@app.route('/data', methods=['POST'])
def data():

  
  number = request.form["number"]
  user = request.form["user"]
  password = request.form["password"]
  user = ""
  url = "https://secure.simplepractice.com/clients/83cdf3a00620ca58/insurance_claims/"+str(number)
  try:
      return jsonify(video_scrapper(url,user,password))
      
  except:
      return jsonify({"message":"Not correct data"})
      
  

      
      
      
@app.route('/claim', methods=['POST'])
def claims():

  from_date = request.form["start"]
  end_date = request.form["end"]
  user = request.form["user"]
  password = request.form["password"]
  data = ""
  try:
      return jsonify({"all_claims_id":id_scrapper(from_date,end_date,user,password)})
      
  except:
      return jsonify({"message":"Not correct data"})
  
  
@app.route('/claimnumber', methods=['POST'])
def claimsnumber():

  from_date = request.form["start"]
  end_date = request.form["end"]
  page = request.form["page"]

  user = request.form["user"]
  password = request.form["password"]
  data,value = id_scrapper_page(from_date,end_date,page,user,password)
  data = {"all_claims_id":data,"total":value}
  resp = jsonify(data)
  return resp
  

