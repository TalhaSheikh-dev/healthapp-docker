#fff
from flask import Flask,request
from working import video_scrapper,id_scrapper,unbilled_create,get_all_client,payer_data
from flask import jsonify
app= Flask(__name__)
app.debug = False

@app.route('/clients', methods=['POST'])
def clients_data():
  user = request.form["user"]
  password = request.form["password"]
  #try:
  return jsonify(get_all_client(user,password))
      
  #except:
  #    return jsonify({"message":"Not correct data"})
      



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
  #return jsonify(video_scrapper(url,user,password))
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
  
@app.route('/unbill', methods=['POST'])
def unbill():

  from_date = request.form["start"]
  end_date = request.form["end"]
  user = request.form["user"]
  password = request.form["password"]

  try:
      unbilled_create(from_date,end_date,user,password)
      #good
      return jsonify({"message":"successfull"})
  except:
      return jsonify({"message":"Unable to create unbilled"})
  
      
if __name__ == '__main__':
    app.run()  

