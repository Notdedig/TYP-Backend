# Cognitive Load Estimation Backend - Python Flask

A lightweight Python Flask REST API for estimating cognitive load using heart rate and breathing rate sensors.

## 🚀 Quick Start (Windows/Mac/Linux)

### Step 1: Install Python

**Download Python 3.8 or higher:**
- Windows: https://www.python.org/downloads/
- Mac: `brew install python3` or download from python.org
- Linux: Usually pre-installed, or `sudo apt install python3 python3-pip`

**Verify installation:**
```bash
python --version
# or
python3 --version
```

### Step 2: Install Dependencies

```bash
# Install required packages
pip install -r requirements.txt

# Or install manually:
pip install Flask flask-cors requests
```

### Step 3: Run the API

```bash
python app.py
```

**Server starts at:** `http://localhost:8080`

You should see:
```
🚀 Starting Cognitive Load API...
📍 Server running on http://0.0.0.0:8080
📍 Access locally: http://localhost:8080
📊 API Documentation: http://localhost:8080
```

---

## 📁 Project Structure

```
cognitive-load-python/
├── app.py                      # Main Flask application
├── cognitive_load_service.py   # Business logic & calculations
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

That's it! Just 2 Python files instead of 10+ Java files!

---

## 🧪 Testing the API

### 1. Test Welcome Page

Open browser: http://localhost:8080

Or:
```bash
curl http://localhost:8080
```

### 2. Send Heart Rate (Simulate ESP32)

```bash
curl -X POST http://localhost:8080/api/heartrate \
  -H "Content-Type: application/json" \
  -d "{\"heartRate\": 75.5}"
```

### 3. Get Heart Rate Data

```bash
curl http://localhost:8080/api/heartrate
```

### 4. Start Calibration

```bash
curl -X POST http://localhost:8080/api/calibrate/start \
  -H "Content-Type: application/json" \
  -d "{\"seeedStudioIp\": \"192.168.1.100\"}"
```

### 5. Check Calibration Status

```bash
curl http://localhost:8080/api/calibrate/status
```

### 6. Get Cognitive Load

```bash
curl http://localhost:8080/api/cognitive-load/current
```

### 7. Get Predicted Load (uses last 10 estimates)

```bash
curl http://localhost:8080/api/cognitive-load/predicted
```

---

## 📡 API Endpoints

All endpoints are identical to the Java version:

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/heartrate` | POST | Receive HR from ESP32 |
| `/api/heartrate` | GET | Get HR data |
| `/api/breathrate` | GET | Get BR data |
| `/api/cognitive-load/current` | GET | Get current load |
| `/api/cognitive-load/predicted` | GET | Get predicted load (returns current + extrapolated value) |
| `/api/calibrate/start` | POST | Start calibration |
| `/api/calibrate/status` | GET | Check calibration |

---

## 🔧 Configuration

### Change Port

Edit `app.py`, line at the bottom:
```python
app.run(host='0.0.0.0', port=8080, debug=True)
```

Change `port=8080` to any port you want.

### Disable Debug Mode (Production)

```python
app.run(host='0.0.0.0', port=8080, debug=False)
```

---

## 🐳 Docker Deployment (Optional)

### Create Dockerfile:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py cognitive_load_service.py ./

EXPOSE 8080

CMD ["python", "app.py"]
```

### Build and Run:

```bash
docker build -t cognitive-load-api .
docker run -p 8080:8080 cognitive-load-api
```

---

## 🌐 DuckDNS Integration

**Same as Java version!**

1. Create DuckDNS domain: https://www.duckdns.org
2. Set up port forwarding on router (port 8080)
3. Allow through firewall
4. Update ESP32 to use: `http://your-domain.duckdns.org:8080/api/heartrate`

See the DuckDNS guide files for detailed instructions.

---

## 🆚 Python vs Java Comparison

| Feature | Python (Flask) | Java (Spring Boot) |
|---------|----------------|-------------------|
| **Lines of Code** | ~200 lines | ~500+ lines |
| **Setup Time** | 2 minutes | 10+ minutes |
| **Dependencies** | 3 packages | 10+ packages |
| **Memory Usage** | ~50MB | ~200MB |
| **Startup Time** | <1 second | 5-10 seconds |
| **Easy to Learn** | ✅ Very easy | ⚠️ Moderate |
| **Performance** | ⚠️ Good | ✅ Excellent |

**For this project:** Python is simpler and more than fast enough!

---

## 🔥 Running 24/7 (Windows)

### Option 1: Keep Terminal Open

Just leave the command prompt window running.

### Option 2: Run as Background Service

**Using NSSM (recommended):**

1. Download NSSM: https://nssm.cc/download
2. Extract and run:
```cmd
nssm install CognitiveLoadAPI
```
3. Configure:
   - Path: `C:\Python\python.exe`
   - Startup directory: `C:\path\to\your\project`
   - Arguments: `app.py`
4. Click "Install service"
5. Start service:
```cmd
nssm start CognitiveLoadAPI
```

---

## 🐧 Running 24/7 (Linux/Mac)

### Using systemd (Linux):

Create `/etc/systemd/system/cognitive-load.service`:

```ini
[Unit]
Description=Cognitive Load API
After=network.target

[Service]
Type=simple
User=youruser
WorkingDirectory=/path/to/project
ExecStart=/usr/bin/python3 /path/to/project/app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable cognitive-load
sudo systemctl start cognitive-load
```

---

## 📊 Monitoring

### Check if running:

```bash
curl http://localhost:8080
```

### View logs:

The Flask app prints to console. To save logs:

```bash
python app.py > api.log 2>&1
```

---

## 🆘 Troubleshooting

### Port 8080 already in use

**Find what's using it:**
```bash
# Windows
netstat -ano | findstr :8080

# Linux/Mac
lsof -i :8080
```

**Change port in app.py or kill the process.**

### Module not found error

```bash
pip install Flask flask-cors requests
```

### Can't access from ESP32

1. Check firewall (see DuckDNS guide)
2. Verify port forwarding
3. Test with: `curl http://YOUR_PC_IP:8080`

---

## 🎯 ESP32 Integration

**Same code as Java version!** Just point to your Python server:

```cpp
const char* serverUrl = "http://192.168.1.10:8080/api/heartrate";
// Or with DuckDNS:
const char* serverUrl = "http://your-domain.duckdns.org:8080/api/heartrate";
```

---

## ⚡ Performance Tips

1. **Use gunicorn for production:**
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8080 app:app
```

2. **Use nginx as reverse proxy** (advanced)

3. **Enable caching** for breath rate requests

---

## 📝 License

MIT License - Do whatever you want with this code!

---

## 🎉 That's It!

Python version is:
- ✅ Simpler to set up
- ✅ Easier to understand
- ✅ Faster to develop
- ✅ Same functionality as Java
- ✅ Works with same ESP32 code
- ✅ Works with DuckDNS

**Both versions work identically from the ESP32's perspective!**
