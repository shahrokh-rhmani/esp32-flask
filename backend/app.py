from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

# ذخیره آخرین موقعیت دریافت شده
last_location = {
    'latitude': 35.6892,
    'longitude': 51.3890,
    'timestamp': datetime.now().isoformat(),
    'city': 'Tehran',
    'message': 'تهران - پایتخت ایران'
}

@app.route('/api/location', methods=['GET', 'POST'])
def handle_location():
    global last_location
    
    if request.method == 'POST':
        # Receiving data from ESP32
        data = request.get_json()
        
        # ذخیره داده دریافتی
        last_location = {
            'latitude': data.get('latitude', 35.6892),
            'longitude': data.get('longitude', 51.3890),
            'timestamp': data.get('timestamp', datetime.now().isoformat()),
            'city': 'Tehran',
            'message': 'موقعیت به روز شده از دستگاه GPS'
        }
        
        return jsonify({'status': 'success', 'message': 'Location updated'})
    
    # Return the last position for a GET request.
    return jsonify(last_location)

if __name__ == '__main__':
    app.run(debug=True)