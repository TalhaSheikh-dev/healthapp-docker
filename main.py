#fool
from flask import Flask,request
from working import video_scrapper,id_scrapper
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
  status = request.form["status"]
  data = ""
  return jsonify({"all_claims_id":id_scrapper(from_date,end_date,status,user,password)})
  
      
if __name__ == '__main__':
    app.run()  

