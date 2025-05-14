
# imports
from flask import Flask,request,jsonify
from working import *
import logging
import logging.handlers
import json
# initiating flask app 
app= Flask(__name__)
app.debug = False

# Configure logging
log_handler = logging.handlers.TimedRotatingFileHandler("app.log", when="midnight", interval=1, backupCount=1)
log_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
log_handler.suffix = "%Y-%m-%d"
log_handler.setLevel(logging.INFO)
logging.getLogger().addHandler(log_handler)
logging.getLogger().setLevel(logging.INFO)

# endpoint to test health of app
@app.route('/health', methods=['POST'])
def health_test():
    return jsonify({"message": "successful"})

# endpoint to get therapy notes claims
@app.route('/tn-claims', methods=['POST'])
def therapy_notes_claims():
    try:
        data = request.form
        return therapy_notes_claims_data(data["code"], data["user"], data["password"], data["start"], data["end"])
    except KeyError:
        return jsonify({"message": "Missing required fields"}), 400
    except Exception as e:
        logging.error(e, exc_info=True)
        return jsonify({"message": "Internal server error"}), 500

# endpoint to get all clients from simple health practice
@app.route('/clients', methods=['POST'])
def clients_data():
    try:
        user, password,secret_key = request.form["user"], request.form["password"],request.form["secretKey"]
        return jsonify(get_all_client(user, password,secret_key))
    except KeyError:
        return jsonify({"message": "Missing required fields"}), 400
    except Exception as e:
        logging.error(e, exc_info=True)
        return jsonify({"message": "Internal server error"}), 500

# endpoint to get all insurance payers data from simple health app
@app.route('/payer', methods=['POST'])
def payer():
    try:
        user, password,secret_key = request.form["user"], request.form["password"],request.form["secretKey"]
        count = int(request.form["start"])
        return jsonify({"data": payer_data(user, password, count,secret_key)})
    except KeyError:
        return jsonify({"message": "Missing required fields"}), 400
    except ValueError:
        return jsonify({"message": "Count should be an integer"}), 400
    except Exception as e:
        logging.error(e, exc_info=True)
        return jsonify({"message": "Internal server error"}), 500
    
# endpoint to get all the data of insured client
@app.route('/data', methods=['POST'])
def insured_data():
    try:
        user, password = request.form["user"], request.form["password"]
        first_number, second_number = request.form["first_number"], request.form["second_number"]
        secret_key = request.form["secretKey"]
        url = f"https://secure.simplepractice.com/clients/{first_number}/insurance_claims/{second_number}"
        return jsonify(get_insurance_client_data(url, user, password,secret_key))
    except KeyError:
        return jsonify({"message": "Missing required fields"}), 400
    except Exception as e:
        logging.error(e, exc_info=True)
        return jsonify({"message": str(e)}), 500

@app.route('/submitClaim', methods=['POST'])
def submit_claim():
    try:
        user, password = request.form["user"], request.form["password"]
        first_number, second_number = request.form["first_number"], request.form["second_number"]
        secret_key = request.form["secretKey"]
        modifiers = json.loads(request.form.get('modifiers', {"data":[]}))["data"]
        is_submit = request.form.get('is_submit', 'false').lower() == 'true'
        url = f"https://secure.simplepractice.com/clients/{first_number}/insurance_claims/{second_number}"
        return jsonify({"message":submit_claim_data(url, user, password,secret_key,modifiers,is_submit)})
    except KeyError:
        return jsonify({"message": "Missing required fields"}), 400
    except Exception as e:
        logging.error(e, exc_info=True)
        return jsonify({"message": str(e)}), 500
      
# endpoint to get all claims between start and end date from simple health app
@app.route('/claim', methods=['POST'])
def claims():
    try:
        from_date, end_date = request.form["start"], request.form["end"]
        user, password, status = request.form["user"], request.form["password"], request.form["status"]
        secret_key = request.form["secretKey"]
        return jsonify({"all_claims_id": get_all_claims(from_date, end_date, status, user, password,secret_key)})
    except KeyError:
        return jsonify({"message": "Missing required fields", "all_claims_id": []}), 400
    except Exception as e:
        logging.error(e, exc_info=True)
        return jsonify({"message": "Internal server error", "all_claims_id": []}), 500

# endpoint to convert unclaim to claim in simple health app
@app.route('/unbill', methods=['POST'])
def unbill():
    try:
        from_date, end_date = request.form["start"], request.form["end"]
        user, password = request.form["user"], request.form["password"]
        secret_key = request.form["secretKey"]

        return jsonify({"message": create_un_bill_user(from_date, end_date, user, password,secret_key)})
    except KeyError:
        return jsonify({"message": "Missing required fields"}), 400
    except Exception as e:
        logging.error(e, exc_info=True)
        return jsonify({"message": str(e)}), 500

      

if __name__ == '__main__':
    app.run()
    # app.run(host='0.0.0.0', port=8000)  # Default port is 5000 if not specified
