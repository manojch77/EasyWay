from flask import Flask, request
import firebase_admin
from firebase_admin import credentials, db
import datetime
cred = credentials.Certificate("serviceAccountKey1.json")  # Firebase Admin Key
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://easy-22b8-default-rtdb.firebaseio.com/'
})

app = Flask(__name__)

@app.route('/location', methods=['POST'])
def receive_location():
    data = request.form or request.get_json()
    if not data: return {"error": "no data"}, 400

    device_id = data.get('id') or data.get('uniqueId') or 'unknown'
    lat = data.get('latitude')
    lng = data.get('longitude')
    timestamp = data.get('fixTime') or datetime.datetime.now().isoformat()

    db.reference(f'/buses/{device_id}').set({
        'lat': lat,
        'lng': lng,
        'time': timestamp
    })
    return {"status": "updated"}
 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5055, debug=True)
