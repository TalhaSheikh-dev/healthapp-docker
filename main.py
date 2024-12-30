
from flask import Flask,request
from working import *
from flask import jsonify
import logging
app= Flask(__name__)
app.debug = False

@app.route('/health', methods=['POST'])
def health():
  return jsonify("successful")
      

@app.route('/tn-claims', methods=['POST'])
def therapynotes_claims():
  code = request.form["code"]
  user = request.form["user"]
  password = request.form["password"]
  start = request.form["start"]
  end = request.form["end"]      
  #try:
  if True:
      return therapynotes_claims_data(code,user,password,start,end)
  #except:
      #return jsonify({"message":"Not correct data"})
      

@app.route('/clients', methods=['POST'])
def clients_data():
  user = request.form["user"]
  password = request.form["password"]
  #try:
  if True:
      return jsonify(get_all_client(user,password))
  #except:
      #return jsonify({"message":"Not correct data"})
      



@app.route('/payer', methods=['POST'])
def payer():

  user = request.form["user"]
  password = request.form["password"]
  try:
    count = int(request.form["start"])
  except:
    return jsonify({"message":"count should be int"})
  try:
    data = payer_data(user,password,count)
    data = {"data":data}
    return jsonify(data)
  except:
    return jsonify({"message":"Not correct data"})
    
    
    
@app.route('/data', methods=['POST'])
def data():
  user = ""
  first_number = request.form["first_number"]
  second_number = request.form["second_number"]
  user = request.form["user"]
  password = request.form["password"]
  url = "https://secure.simplepractice.com/clients/"+str(first_number)+"/insurance_claims/"+str(second_number)
  try:
    return jsonify(video_get(url,user,password))
      
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
  try:
      return jsonify({"all_claims_id":id_get(from_date,end_date,status,user,password)})
  except Exception as e:
      return jsonify({"message":"bad request","all_claims_id":[]}),400

@app.route('/unbill', methods=['POST'])
def unbill():

  from_date = request.form["start"]
  end_date = request.form["end"]
  user = request.form["user"]
  password = request.form["password"]

  try:
      message = unbilled_create(from_date,end_date,user,password)
      return jsonify({"message":message})
  except Exception as e:
      logging.error(e,exc_info=True)
      return jsonify({"message":"bad request"}),400
  
      
if __name__ == '__main__':
    app.run()  

