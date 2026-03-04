# 🧠 Cognitive Load Estimation System - Complete Python Package

**A real-time cognitive load monitoring system using heart rate and breath rate sensors.**

---

## 📦 What's In This Package

### 🐍 Backend (Python Flask)
- `app.py` - Main Flask API server
- `cognitive_load_service.py` - Cognitive load calculation engine
- `requirements.txt` - Python dependencies

### 📡 ESP32 Heart Rate Sensor
- `ESP32_HeartRate_Client.ino` - Full-featured heart rate monitor
- `ESP32_Simple_Test.ino` - Simple test code (dummy data)

### 🌐 Remote Access (DuckDNS)
- `duckdns-update.bat` - Windows auto-update script
- `Windows-Task-Scheduler-Setup.md` - Automated IP updates

### 🚀 Quick Start Scripts
- `run-server.bat` - Windows: Double-click to start
- `run-server.sh` - Mac/Linux: Run server easily

### 📚 Documentation
- `COMPLETE-SETUP-GUIDE.md` - Step-by-step setup (this file)
- `README-Python.md` - Detailed Python backend docs
- `QUICKSTART-Python.md` - 5-minute quick start
- `ESPHome-Integration-Guide.md` - Breath sensor integration
- `Cognitive_Load_API.postman_collection.json` - API testing collection

### 🐳 Deployment
- `Dockerfile-Python` - Docker containerization

---

## ⚡ Super Quick Start (5 Minutes)

### Step 1: Install Python
**Windows:** Download from https://www.python.org/downloads/
**Mac:** `brew install python3`
**Linux:** `sudo apt install python3 python3-pip`

### Step 2: Install Dependencies
```bash
pip install Flask flask-cors requests aioesphomeapi
```

### Step 3: Configure Breath Sensor IP
Edit `cognitive_load_service.py` line 27:
```python
self.esp_ip = "10.16.129.122"  # ← Your breath sensor IP
```

### Step 4: Start Server
**Windows:** Double-click `run-server.bat`
**Mac/Linux:** `./run-server.sh`
**Or:** `python app.py`

### Step 5: Configure ESP32
Edit `ESP32_HeartRate_Client.ino`:
```cpp
const char* ssid = "YOUR_WIFI_NAME";
const char* password = "YOUR_WIFI_PASSWORD";
const char* serverUrl = "http://YOUR_PC_IP:8080/api/heartrate";
```
Upload to ESP32.

✅ **Done!** System is running at `http://localhost:8080`

---

## 🎯 Complete Setup Guide

### Part 1: Backend Setup (5 minutes)

#### 1.1 Install Python
- **Windows:** https://www.python.org/downloads/ (✅ Check "Add Python to PATH")
- **Mac:** Already installed or `brew install python3`
- **Linux:** `sudo apt update && sudo apt install python3 python3-pip`

Verify:
```bash
python --version
# or
python3 --version
```

#### 1.2 Install Dependencies
```bash
# Method 1: Install from requirements.txt
pip install -r requirements.txt

# Method 2: Install individually
pip install Flask==3.0.0
pip install flask-cors==4.0.0
pip install requests==2.31.0
pip install aioesphomeapi==24.6.2
```

#### 1.3 Configure Breath Sensor
Open `cognitive_load_service.py` in any text editor.

Find line 27 and update:
```python
# ESPHome breath sensor configuration
self.esp_ip = "10.16.129.122"  # ← Change to your breath sensor IP
self.breath_key = 3149911513   # ← Usually stays the same
```

**How to find your breath sensor IP:**
- Check your breath sensor code/display
- Or check your router's connected devices
- Common: `10.16.129.122` or `192.168.4.1`

#### 1.4 Start the Backend
**Option A - Windows (Easy):**
Double-click `run-server.bat`

**Option B - Mac/Linux:**
```bash
chmod +x run-server.sh
./run-server.sh
```

**Option C - Command Line:**
```bash
python app.py
```

**You should see:**
```
🔄 Starting ESPHome listener for breath sensor at 10.16.129.122
🚀 Starting Cognitive Load API...
📍 Server running on http://0.0.0.0:8080
✅ Connected to ESPHome breath sensor at 10.16.129.122
[14:23:45] Breath Rate: 16.0
```

✅ Backend is running!

---

### Part 2: ESP32 Heart Rate Sensor Setup (10 minutes)

#### 2.1 Install Arduino IDE
Download from: https://www.arduino.cc/en/software

#### 2.2 Install ESP32 Board Support
1. Open Arduino IDE
2. File → Preferences
3. In "Additional Board Manager URLs" add:
   ```
   https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
   ```
4. Tools → Board → Boards Manager
5. Search "ESP32" → Install "esp32 by Espressif Systems"

#### 2.3 Install Libraries
Tools → Manage Libraries → Install:
- `SparkFun Bio Sensor Hub Library`
- `WiFi` (built-in)
- `HTTPClient` (built-in)

#### 2.4 Configure ESP32 Code
Open `ESP32_HeartRate_Client.ino`

Update lines 12-17:
```cpp
// WiFi credentials
const char* ssid = "YourWiFiName";          // ← Your WiFi name
const char* password = "YourWiFiPassword";   // ← Your WiFi password

// Server URL
const char* serverUrl = "http://192.168.1.10:8080/api/heartrate";  // ← Your PC's IP
```

**Find your PC's IP:**
- **Windows:** Open CMD → type `ipconfig` → Look for "IPv4 Address"
- **Mac:** System Preferences → Network → Advanced → TCP/IP
- **Linux:** `hostname -I` or `ip addr`

Example: If your PC IP is `192.168.1.10`, use:
```cpp
const char* serverUrl = "http://192.168.1.10:8080/api/heartrate";
```

#### 2.5 Upload to ESP32
1. Connect ESP32 via USB
2. Tools → Board → Select your ESP32 board
3. Tools → Port → Select COM port (Windows) or /dev/ttyUSB0 (Linux)
4. Click Upload ⬆️

#### 2.6 Test ESP32
Open Serial Monitor (115200 baud)

You should see:
```
✓ WiFi Connected!
ESP32 IP Address: 192.168.1.XX
✓ Sent HR: 75 BPM | Response: 200
```

✅ ESP32 is sending heart rate data!

---

### Part 3: Testing the System (5 minutes)

#### 3.1 Test Backend Locally
Open browser: http://localhost:8080

You should see JSON with API endpoints.

#### 3.2 Test Heart Rate Endpoint
```bash
curl http://localhost:8080/api/heartrate
```

Response:
```json
{
  "currentHeartRate": 75.5,
  "baselineHeartRate": 0.0,
  "isCalibrated": false
}
```

#### 3.3 Test Breath Rate Endpoint
```bash
curl http://localhost:8080/api/breathrate
```

Response:
```json
{
  "currentBreathRate": 16.0,
  "baselineBreathRate": 0.0,
  "isCalibrated": false
}
```

If breath rate is 0.0, check:
- Breath sensor is running
- IP address is correct in `cognitive_load_service.py`
- Backend shows: `✅ Connected to ESPHome breath sensor`

#### 3.4 Start Calibration
```bash
curl -X POST http://localhost:8080/api/calibrate/start \
  -H "Content-Type: application/json" \
  -d "{\"seeedStudioIp\": \"10.16.129.122\"}"
```

**During calibration (90 seconds):**
- Make sure ESP32 is sending heart rate data
- Backend will collect 90 samples of both HR and BR
- Stay relaxed and breathe normally

**Backend will show:**
```
🔄 Calibration started for 90 seconds...
Calibration progress: 10s / 90s (HR: 10, BR: 10)
Calibration progress: 20s / 90s (HR: 20, BR: 20)
...
✅ Calibration complete!
Baseline Heart Rate: 72.50
Baseline Breath Rate: 16.20
```

#### 3.5 Check Cognitive Load
```bash
curl http://localhost:8080/api/cognitive-load/current
```

Response:
```json
{
  "currentCognitiveLoad": 1.0,
  "heartRateDelta": 0.0,
  "breathRateDelta": 0.0,
  "paasScale": "1-9",
  "isCalibrated": true
}
```

**Cognitive Load Scale (Paas 1-9):**
- 1-3: Low cognitive load (relaxed)
- 4-6: Moderate cognitive load (thinking/working)
- 7-9: High cognitive load (stressed/overloaded)

✅ System is fully operational!

---

### Part 4: Remote Access (Optional - For ESP32 Outside Home)

If you want your ESP32 to access the backend from **anywhere** (not just home WiFi), set up DuckDNS:

#### 4.1 Create DuckDNS Domain
1. Go to https://www.duckdns.org
2. Sign in (GitHub/Google/Twitter/Reddit)
3. Create subdomain (e.g., `cognitiveload`)
4. You get: `cognitiveload.duckdns.org`
5. Copy your token

#### 4.2 Configure Router Port Forwarding
1. Access router: `192.168.1.1` or `192.168.0.1`
2. Login (check router label)
3. Find "Port Forwarding" or "Virtual Server"
4. Add rule:
   ```
   External Port: 8080
   Internal IP: YOUR_PC_IP (e.g., 192.168.1.10)
   Internal Port: 8080
   Protocol: TCP
   ```
5. Save

#### 4.3 Allow Windows Firewall
```cmd
netsh advfirewall firewall add rule name="Cognitive Load API" dir=in action=allow protocol=TCP localport=8080
```

#### 4.4 Update DuckDNS IP
Edit `duckdns-update.bat`:
```batch
set DOMAIN=cognitiveload
set TOKEN=your-token-here
```

Run it:
```cmd
duckdns-update.bat
```

Set up auto-update: See `Windows-Task-Scheduler-Setup.md`

#### 4.5 Update ESP32
```cpp
const char* serverUrl = "http://cognitiveload.duckdns.org:8080/api/heartrate";
```

✅ Now ESP32 can access from anywhere!

---

## 📡 API Reference

### POST /api/heartrate
Receive heart rate from ESP32
```bash
curl -X POST http://localhost:8080/api/heartrate \
  -H "Content-Type: application/json" \
  -d '{"heartRate": 75.5}'
```

### GET /api/heartrate
Get current heart rate data
```bash
curl http://localhost:8080/api/heartrate
```

### GET /api/breathrate
Get current breath rate data
```bash
curl http://localhost:8080/api/breathrate
```

### GET /api/cognitive-load/current
Get current cognitive load with deltas
```bash
curl http://localhost:8080/api/cognitive-load/current
```

### GET /api/cognitive-load/predicted
Get predicted cognitive load
```bash
curl http://localhost:8080/api/cognitive-load/predicted
```

### POST /api/calibrate/start
Start 90-second calibration
```bash
curl -X POST http://localhost:8080/api/calibrate/start \
  -H "Content-Type: application/json" \
  -d '{"seeedStudioIp": "10.16.129.122"}'
```

### GET /api/calibrate/status
Check calibration status
```bash
curl http://localhost:8080/api/calibrate/status
```

---

## 🧮 Cognitive Load Formula

```
1. ΔHR = (HR_current - HR_baseline) / HR_baseline
2. ΔBR = (BR_current - BR_baseline) / BR_baseline
3. Load_raw = max(0, 0.6 × ΔHR + 0.4 × ΔBR)
4. Load_Paas = clamp(1 + (Load_raw / 0.40) × 8, 1, 9)
```

**Weights:**
- Heart Rate: 60%
- Breath Rate: 40%

**Scale:**
- 0% increase → Paas score 1
- 40% increase → Paas score 9

---

## 🔧 Troubleshooting

### Backend won't start
```
Error: No module named 'flask'
```
**Solution:** `pip install -r requirements.txt`

### Breath rate is always 0
```
⚠️ Warning: ESPHome breath sensor not connected!
```
**Check:**
1. Breath sensor is running
2. IP address correct in `cognitive_load_service.py`
3. Same network as backend
4. Port 6053 is open

### ESP32 can't connect
```
✗ POST Error: -1
```
**Check:**
1. Backend is running
2. PC IP address is correct in ESP32 code
3. ESP32 and PC on same WiFi
4. Firewall allows port 8080

### Calibration incomplete
**Make sure:**
- ESP32 is sending heart rate (check Serial Monitor)
- Breath sensor is connected (check backend logs)
- Wait full 90 seconds

### "Port 8080 already in use"
**Solution 1:** Find and stop the other program
```bash
# Windows
netstat -ano | findstr :8080

# Mac/Linux
lsof -i :8080
```

**Solution 2:** Change port in `app.py`:
```python
app.run(host='0.0.0.0', port=8081, debug=True)
```

---

## 📂 File Reference

| File | Purpose |
|------|---------|
| `app.py` | Main Flask server |
| `cognitive_load_service.py` | Cognitive load calculation |
| `requirements.txt` | Python dependencies |
| `ESP32_HeartRate_Client.ino` | ESP32 heart rate code |
| `ESP32_Simple_Test.ino` | ESP32 test code |
| `run-server.bat` | Windows startup script |
| `run-server.sh` | Mac/Linux startup script |
| `duckdns-update.bat` | DuckDNS update script |
| `README-Python.md` | Detailed backend docs |
| `QUICKSTART-Python.md` | Quick start guide |
| `ESPHome-Integration-Guide.md` | Breath sensor guide |
| `Windows-Task-Scheduler-Setup.md` | Auto-update setup |
| `Cognitive_Load_API.postman_collection.json` | API testing |
| `Dockerfile-Python` | Docker deployment |

---

## 🎯 Next Steps

1. ✅ **Test locally** - Verify everything works
2. 🔧 **Calibrate** - Run calibration for accurate baselines
3. 📊 **Monitor** - Watch cognitive load in real-time
4. 🌐 **Go remote** - Set up DuckDNS for remote access
5. 🚀 **Deploy** - Run 24/7 as a service

---

## 💡 Tips

**Run on Windows Startup:**
1. Create shortcut to `run-server.bat`
2. Press `Win+R` → type `shell:startup`
3. Put shortcut in Startup folder

**View Logs:**
```bash
python app.py > api.log 2>&1
```

**Production Server (Better Performance):**
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8080 app:app
```

**Docker Deployment:**
```bash
docker build -f Dockerfile-Python -t cognitive-load-api .
docker run -p 8080:8080 cognitive-load-api
```

---

## 📞 Support

**Check logs:**
- Backend shows connection status
- ESP32 Serial Monitor shows POST responses
- Both should show successful communication

**Common Success Messages:**
- Backend: `✅ Connected to ESPHome breath sensor`
- Backend: `[HH:MM:SS] Breath Rate: X.X`
- ESP32: `✓ Sent HR: XX BPM | Response: 200`

---

## 🎉 You're All Set!

Your cognitive load estimation system is ready to use!

**Quick Test:**
1. Start backend: `python app.py`
2. Upload ESP32 code
3. Calibrate: `POST /api/calibrate/start`
4. Monitor: `GET /api/cognitive-load/current`

**Happy monitoring!** 🧠📊
