"""
Cognitive Load Estimation Backend - Python Flask
Main API application
"""

from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from cognitive_load_service import CognitiveLoadService
import threading

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize service
service = CognitiveLoadService()


@app.route('/')
def home():
    """Welcome endpoint"""
    return jsonify({
        "message": "Cognitive Load Estimation API",
        "version": "1.0.0",
        "endpoints": {
            "POST /api/heartrate": "Receive heart rate data",
            "GET /api/heartrate": "Get heart rate data",
            "GET /api/breathrate": "Get breath rate data",
            "GET /api/cognitive-load/current": "Get current cognitive load",
            "GET /api/cognitive-load/predicted": "Get predicted cognitive load",
            "POST /api/calibrate/start": "Start calibration",
            "GET /api/calibrate/status": "Get calibration status"
        }
    })


@app.route('/api/heartrate', methods=['POST'])
def receive_heartrate():
    """Receive heart rate data from ESP32"""
    remote = request.remote_addr
    print(f"Incoming POST /api/heartrate from {remote}")
    try:
        raw = request.get_data(as_text=True)
        print(f"Raw body: {raw}")
        # Parse JSON silently to avoid raising on bad content-type
        data = request.get_json(silent=True)
    except Exception as e:
        print(f"Error reading request body: {e}")
        data = None

    if not data or 'heartRate' not in data:
        print("Invalid payload or missing 'heartRate' field")
        return jsonify({
            "status": "error",
            "message": "heartRate field is required"
        }), 400

    heart_rate = data['heartRate']
    service.add_heart_rate_reading(heart_rate)

    return jsonify({
        "status": "success",
        "message": "Heart rate received"
    })


@app.route('/api/heartrate', methods=['GET'])
def get_heartrate():
    """Get current and baseline heart rate data"""
    return jsonify({
        "currentHeartRate": service.get_current_heart_rate(),
        "baselineHeartRate": service.get_baseline_heart_rate(),
        "isCalibrated": service.is_calibrated()
    })


@app.route('/api/breathrate', methods=['GET'])
def get_breathrate():
    """Get current and baseline breath rate data"""
    return jsonify({
        "currentBreathRate": service.get_current_breath_rate(),
        "baselineBreathRate": service.get_baseline_breath_rate(),
        "isCalibrated": service.is_calibrated()
    })


@app.route('/health', methods=['GET'])
def health_check():
    """Simple health endpoint for network reachability checks"""
    return jsonify({
        "status": "ok",
        "service": "Cognitive Load API"
    }), 200


@app.route('/api/cognitive-load/predicted', methods=['GET'])
def get_predicted_cognitive_load():
    """Get predicted estimated cognitive load"""
    return jsonify({
        "predictedCognitiveLoad": service.calculate_cognitive_load(),
        "paasScale": "1-9",
        "isCalibrated": service.is_calibrated()
    })


@app.route('/api/cognitive-load/current', methods=['GET'])
def get_current_cognitive_load():
    """Get current estimated cognitive load with detailed metrics"""
    return jsonify({
        "currentCognitiveLoad": service.calculate_cognitive_load(),
        "heartRateDelta": service.get_heart_rate_delta(),
        "breathRateDelta": service.get_breath_rate_delta(),
        "paasScale": "1-9",
        "isCalibrated": service.is_calibrated()
    })


@app.route('/api/calibrate/start', methods=['POST'])
def start_calibration():
    """Start 90-second calibration process"""
    data = request.get_json()
    
    if not data or 'seeedStudioIp' not in data:
        return jsonify({
            "status": "error",
            "message": "seeedStudioIp is required"
        }), 400
    
    seeed_studio_ip = data['seeedStudioIp']
    
    # Start calibration in background thread
    thread = threading.Thread(target=service.start_calibration, args=(seeed_studio_ip,))
    thread.daemon = True
    thread.start()
    
    return jsonify({
        "status": "success",
        "message": "Calibration started",
        "duration": "90 seconds"
    })


@app.route('/api/calibrate/status', methods=['GET'])
def get_calibration_status():
    """Get calibration status"""
    return jsonify({
        "isCalibrating": service.is_calibrating(),
        "isCalibrated": service.is_calibrated(),
        "remainingTime": service.get_remaining_calibration_time()
    })


if __name__ == '__main__':
    # Run on all interfaces, port 8080
    print("[*] Starting Cognitive Load API...")
    print("[*] Server running on http://0.0.0.0:8080")
    print("[*] Access locally: http://localhost:8080")
    print("[*] API Documentation: http://localhost:8080")
    app.run(host="0.0.0.0", port=8080, debug=False, use_reloader=False)
