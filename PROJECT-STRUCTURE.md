# 📁 Project Structure

```
cognitive-load-estimation/
│
├── 🐍 Backend (Python Flask)
│   ├── app.py                          # Main Flask API server
│   ├── cognitive_load_service.py       # Cognitive load calculation engine  
│   └── requirements.txt                # Python dependencies
│
├── 📡 ESP32 Heart Rate Sensor
│   ├── ESP32_HeartRate_Client.ino      # Full-featured heart rate monitor
│   └── ESP32_Simple_Test.ino           # Simple test with dummy data
│
├── 🚀 Quick Start Scripts
│   ├── run-server.bat                  # Windows: Double-click to start
│   └── run-server.sh                   # Mac/Linux: Run server easily
│
├── 🌐 Remote Access (DuckDNS)
│   ├── duckdns-update.bat              # Windows DuckDNS updater
│   └── Windows-Task-Scheduler-Setup.md # Automated IP updates guide
│
├── 📚 Documentation
│   ├── COMPLETE-SETUP-GUIDE.md         # ⭐ START HERE - Complete guide
│   ├── README-Python.md                # Detailed Python backend docs
│   ├── QUICKSTART-Python.md            # 5-minute quick start
│   ├── ESPHome-Integration-Guide.md    # Breath sensor integration
│   └── PROJECT-STRUCTURE.md            # This file
│
├── 🧪 Testing
│   └── Cognitive_Load_API.postman_collection.json  # Postman API tests
│
├── 🐳 Deployment
│   └── Dockerfile-Python               # Docker containerization
│
└── ⚙️ Configuration
    └── .gitignore                      # Git ignore patterns
```

---

## 🎯 What Each File Does

### Backend Files

**`app.py`** - Main API Server
- Flask web server
- All API endpoints (POST/GET)
- CORS configuration
- Routes HTTP requests to service

**`cognitive_load_service.py`** - Core Logic
- ESPHome breath sensor listener
- Calibration process (90 seconds)
- Cognitive load calculation
- Heart rate & breath rate management
- Thread-safe data handling

**`requirements.txt`** - Dependencies
```
Flask==3.0.0
flask-cors==4.0.0
requests==2.31.0
aioesphomeapi==24.6.2
```

---

### ESP32 Files

**`ESP32_HeartRate_Client.ino`** - Production Code
- Connects to WiFi
- Reads SparkFun heart rate sensor
- Posts data to backend via HTTP
- Mode switching button
- Error handling
- Serial debugging

**`ESP32_Simple_Test.ino`** - Test Code
- Generates dummy heart rate (65-85 BPM)
- Tests WiFi connection
- Tests HTTP POST to backend
- No sensor required
- Good for testing backend

---

### Quick Start Scripts

**`run-server.bat`** - Windows
- Double-click to start server
- Shows friendly messages
- Automatically runs `python app.py`

**`run-server.sh`** - Mac/Linux
- `chmod +x run-server.sh` once
- `./run-server.sh` to start
- Displays local IP address

---

### Remote Access Files

**`duckdns-update.bat`** - DuckDNS Updater
- Updates DuckDNS with current IP
- Run manually or schedule
- Keeps domain pointing to your PC

**`Windows-Task-Scheduler-Setup.md`** - Automation
- Set up auto-updates every 5 minutes
- Windows Task Scheduler instructions
- Keep DuckDNS always updated

---

### Documentation Files

**`COMPLETE-SETUP-GUIDE.md`** - ⭐ MAIN GUIDE
- Complete setup from scratch
- Step-by-step instructions
- Backend + ESP32 + DuckDNS
- Troubleshooting section
- API reference

**`README-Python.md`** - Backend Details
- Python backend deep dive
- API endpoint details
- Configuration options
- Advanced features
- Performance tips

**`QUICKSTART-Python.md`** - Fast Start
- 5-minute setup
- Minimal instructions
- Get running ASAP
- Perfect for quick tests

**`ESPHome-Integration-Guide.md`** - Breath Sensor
- ESPHome API integration
- How breath sensor works
- Configuration guide
- Troubleshooting
- Real-time updates explained

**`PROJECT-STRUCTURE.md`** - This File
- Project organization
- File descriptions
- Quick reference

---

### Testing File

**`Cognitive_Load_API.postman_collection.json`**
- Import into Postman
- Pre-configured API requests
- Test all endpoints
- Examples included

---

### Deployment File

**`Dockerfile-Python`**
- Docker container definition
- Production deployment
- Easy scaling
- Portable deployment

---

### Configuration File

**`.gitignore`**
- Git ignore patterns
- Excludes logs, cache
- Python virtual environments
- IDE files

---

## 🚀 Quick Reference

### To Start Backend:
```bash
python app.py
# or double-click run-server.bat (Windows)
# or ./run-server.sh (Mac/Linux)
```

### To Upload ESP32:
1. Open `ESP32_HeartRate_Client.ino` in Arduino IDE
2. Update WiFi credentials and server URL
3. Upload to ESP32

### To Test API:
```bash
curl http://localhost:8080/api/heartrate
```

### To Calibrate:
```bash
curl -X POST http://localhost:8080/api/calibrate/start \
  -H "Content-Type: application/json" \
  -d '{"seeedStudioIp": "10.16.129.122"}'
```

---

## 📊 System Architecture

```
┌─────────────────┐
│  ESP32 MAX30102 │ ──┐
│  Heart Rate     │   │
└─────────────────┘   │
                      │ HTTP POST
                      │ /api/heartrate
                      ▼
              ┌──────────────┐
              │ Flask Backend│
              │  app.py      │
              └──────────────┘
                      ▲
                      │ ESPHome API
                      │ Real-time
                      │
┌─────────────────┐   │
│ ESPHome Device  │ ──┘
│ Breath Rate     │
└─────────────────┘
        │
        │ Cognitive Load
        │ Calculation
        ▼
┌─────────────────┐
│ Cognitive Load  │
│ Paas Scale 1-9  │
└─────────────────┘
```

---

## 🎯 Workflow

1. **Backend starts** → Connects to breath sensor via ESPHome
2. **ESP32 starts** → Connects to WiFi, posts heart rate
3. **Calibration** → 90 seconds to establish baselines
4. **Monitoring** → Real-time cognitive load calculation
5. **Remote Access** → DuckDNS for external access (optional)

---

## 💡 Key Features

- ✅ Real-time breath rate via ESPHome API
- ✅ Heart rate via HTTP POST from ESP32
- ✅ 90-second calibration for personalized baselines
- ✅ Paas 9-point cognitive load scale
- ✅ RESTful API for easy integration
- ✅ DuckDNS support for remote access
- ✅ Cross-platform (Windows/Mac/Linux)
- ✅ Docker deployment ready
- ✅ Comprehensive documentation

---

## 📖 Reading Order

1. **Start here:** `COMPLETE-SETUP-GUIDE.md`
2. **Quick test:** `QUICKSTART-Python.md`
3. **Breath sensor:** `ESPHome-Integration-Guide.md`
4. **Remote access:** `Windows-Task-Scheduler-Setup.md`
5. **Deep dive:** `README-Python.md`

---

**Everything you need is here!** 🎉
