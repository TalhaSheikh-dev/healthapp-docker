#fool
from flask import Flask,request
from working import video_scrapper,id_scrapper,id_scrapper_page
from flask import jsonify
app= Flask(__name__)
app.debug = False
@app.route('/data', methods=['POST'])
def data():

  
  user = ""
  first_number = request.form["first_number"]
  second_number = request.form["second_number"]
  user = request.form["user"]
  password = request.form["password"]
  url = "https://secure.simplepractice.com/clients/"+str(first_number)+"/insurance_claims/"+str(second_number)
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
  return jsonify({"all_claims_id":id_scrapper(from_date,end_date,user,password)})
      
  
@app.route('/claimnumber', methods=['POST'])
def claimsnumber():
  
  full=data = value_all = resp = from_date= end_date= " "
  from_date = request.form["start"]
  end_date = request.form["end"]
  page = request.form["page"]

  user = request.form["user"]
  password = request.form["password"]
  
  try:
      full = id_scrapper_page(from_date,end_date,page,user,password)
      return jsonify({"total_page":full[1],"all_claims_id":full[0]})
      
  except:
      return jsonify({"message":"Not correct data"})
      
if __name__ == '__main__':
    app.run()  

