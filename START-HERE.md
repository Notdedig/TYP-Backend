# 🧠 Cognitive Load Estimation System

**Real-time cognitive load monitoring using heart rate and breath rate sensors**

---

## 🚀 START HERE

### ⚡ Super Quick Start (5 Minutes)

1. **Install Python** from https://www.python.org/downloads/
2. **Install dependencies:** `pip install -r requirements.txt`
3. **Update breath sensor IP in** `cognitive_load_service.py` (line 27)
4. **Start server:** Double-click `run-server.bat` (Windows) or `python app.py`
5. **Upload ESP32 code** from `ESP32_HeartRate_Client.ino`

✅ **Done! Visit** http://localhost:8080

---

## 📚 Documentation

| File | Purpose | When to Read |
|------|---------|-------------|
| **COMPLETE-SETUP-GUIDE.md** | 📖 Full setup guide | ⭐ START HERE |
| **QUICKSTART-Python.md** | ⚡ 5-minute quick start | Need speed |
| **PROJECT-STRUCTURE.md** | 📁 File organization | Understand layout |
| **README-Python.md** | 🐍 Backend details | Deep dive |
| **ESPHome-Integration-Guide.md** | 🫁 Breath sensor guide | Breath sensor setup |
| **Windows-Task-Scheduler-Setup.md** | 🌐 Auto-update DuckDNS | Remote access |

---

## 📦 What's Included

### Core Files (Need These!)
- ✅ `app.py` - Flask API server
- ✅ `cognitive_load_service.py` - Cognitive load engine
- ✅ `requirements.txt` - Python dependencies
- ✅ `ESP32_HeartRate_Client.ino` - Heart rate sensor code

### Helper Scripts
- 🚀 `run-server.bat` / `run-server.sh` - Easy server start
- 🌐 `duckdns-update.bat` - DuckDNS IP updater

### Testing & Deployment
- 🧪 `Cognitive_Load_API.postman_collection.json` - API tests
- 🐳 `Dockerfile-Python` - Docker deployment
- 📝 `.gitignore` - Git configuration

---

## 🎯 System Overview

```
ESP32 Heart Rate Sensor → HTTP POST → Backend
                                        ↓
ESPHome Breath Sensor → ESPHome API → Backend
                                        ↓
                              Cognitive Load (1-9)
```

**Formula:**
- Heart Rate: 60% weight
- Breath Rate: 40% weight
- Output: Paas 9-point scale (1=relaxed, 9=stressed)

---

## 🔧 Quick Commands

### Start Backend
```bash
python app.py
```

### Test API
```bash
curl http://localhost:8080/api/heartrate
```

### Start Calibration
```bash
curl -X POST http://localhost:8080/api/calibrate/start
```

### Get Cognitive Load
```bash
curl http://localhost:8080/api/cognitive-load/current
```

---

## 📡 API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/heartrate` | POST | ESP32 sends heart rate |
| `/api/heartrate` | GET | Get heart rate data |
| `/api/breathrate` | GET | Get breath rate data |
| `/api/cognitive-load/current` | GET | Get cognitive load |
| `/api/calibrate/start` | POST | Start 90s calibration |
| `/api/calibrate/status` | GET | Check calibration |

---

## ⚙️ Configuration

### Breath Sensor IP
Edit `cognitive_load_service.py` line 27:
```python
self.esp_ip = "10.16.129.122"  # Your breath sensor IP
```

### ESP32 Server URL
Edit `ESP32_HeartRate_Client.ino` line 14:
```cpp
const char* serverUrl = "http://192.168.1.10:8080/api/heartrate";
```

---

## 🆘 Troubleshooting

### Backend won't start
```
pip install -r requirements.txt
```

### Breath rate is 0
- Check IP in `cognitive_load_service.py`
- Look for: `✅ Connected to ESPHome breath sensor`

### ESP32 can't connect
- Check PC IP address
- Make sure backend is running
- Check firewall allows port 8080

---

## 📖 Recommended Reading Order

1. **This file** (you're here!) - Get overview
2. **COMPLETE-SETUP-GUIDE.md** - Full setup instructions
3. **QUICKSTART-Python.md** - If you want speed
4. **ESPHome-Integration-Guide.md** - Understand breath sensor
5. **PROJECT-STRUCTURE.md** - Understand file organization
6. **README-Python.md** - Deep technical details

---

## 🎓 Features

- ✅ Real-time breath rate via ESPHome API
- ✅ Heart rate via HTTP from ESP32
- ✅ 90-second personalized calibration
- ✅ Paas 9-point cognitive load scale
- ✅ RESTful API
- ✅ DuckDNS support for remote access
- ✅ Cross-platform (Windows/Mac/Linux)
- ✅ Docker ready
- ✅ Comprehensive documentation

---

## 🎯 Typical Workflow

1. **Setup** (5-10 minutes)
   - Install Python
   - Install dependencies
   - Configure IPs

2. **First Run** (2 minutes)
   - Start backend
   - Upload ESP32 code
   - Verify connections

3. **Calibration** (90 seconds)
   - Run calibration
   - Establish baselines
   - Relax and breathe normally

4. **Monitor** (Ongoing)
   - View real-time cognitive load
   - Track mental workload
   - Adjust tasks accordingly

5. **Remote Access** (Optional, 15 minutes)
   - Set up DuckDNS
   - Configure port forwarding
   - Access from anywhere

---

## 💡 Key Points

- **Python only** - No Java/Spring Boot needed
- **Simple setup** - Just 3 core files
- **Real-time** - Instant breath rate updates
- **Accurate** - Personalized calibration
- **Flexible** - Local or remote access
- **Well-documented** - Guides for everything

---

## 📞 Need Help?

**Check these in order:**
1. COMPLETE-SETUP-GUIDE.md (Troubleshooting section)
2. Backend console logs
3. ESP32 Serial Monitor output
4. ESPHome-Integration-Guide.md

**Common issues:**
- Breath rate = 0 → Check IP and ESPHome connection
- ESP32 error → Check WiFi credentials and server URL
- Port 8080 in use → Change port in `app.py`

---

## 🎉 Ready to Start!

**Everything you need is here. Choose your path:**

- 🏃 **Fast:** QUICKSTART-Python.md (5 minutes)
- 📖 **Thorough:** COMPLETE-SETUP-GUIDE.md (Full guide)
- 🔍 **Explorer:** PROJECT-STRUCTURE.md (Understand first)

**Happy monitoring!** 🧠📊

---

## 📊 File Count

- **3** Core files (Backend)
- **2** ESP32 files
- **2** Quick start scripts
- **6** Documentation files
- **2** Remote access files
- **3** Testing/deployment files

**Total: 18 files - Everything you need!**
