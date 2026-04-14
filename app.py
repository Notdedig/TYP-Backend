"""
Cognitive Load Estimation Backend - Python Flask
Main API application
"""

from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from cognitive_load_service import CognitiveLoadService
import threading

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response

@app.route('/', defaults={'path': ''}, methods=['OPTIONS'])
@app.route('/<path:path>', methods=['OPTIONS'])
def handle_options(path):
    return '', 204

service = CognitiveLoadService()

DASHBOARD_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Cognitive Load Monitor</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#2e294e;color:#efbcd5;font-family:system-ui,sans-serif;padding:14px;min-height:100vh}
.hdr{text-align:center;padding:10px 0 16px}
.hdr h1{font-size:20px;font-weight:500;color:#efbcd5;letter-spacing:1px}
.hdr p{font-size:12px;color:#be97c6;margin-top:3px}
.mrow{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:9px;margin-bottom:12px}
.mc{background:#3a3560;border:0.5px solid #8661c1;border-radius:10px;padding:11px 13px}
.mc .lbl{font-size:10px;color:#be97c6;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:3px}
.mc .val{font-size:24px;font-weight:500;color:#efbcd5}
.mc .sub{font-size:10px;color:#be97c6;margin-top:2px}
.pbar{width:100%;height:5px;border-radius:3px;background:#1a1735;margin-top:7px;overflow:hidden}
.pfill{height:100%;border-radius:3px;background:#8661c1;transition:width 0.4s ease}
.crow{display:grid;grid-template-columns:1fr 1fr;gap:9px;margin-bottom:12px}
.cc{background:#3a3560;border:0.5px solid #8661c1;border-radius:10px;padding:11px 13px;margin-bottom:12px}
.lbl{font-size:10px;color:#be97c6;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:7px}
.srow{display:flex;align-items:center;gap:9px}
.srow input[type=range]{flex:1;accent-color:#8661c1}
.sv{font-size:13px;font-weight:500;color:#efbcd5;min-width:36px;text-align:right}
.brow{display:flex;gap:7px;margin-top:9px;flex-wrap:wrap;align-items:center}
.btn{background:#8661c1;color:#fff;border:none;border-radius:7px;padding:6px 13px;font-size:11px;cursor:pointer;transition:background 0.15s}
.btn:hover{background:#9e7ad4}
.btn:disabled{opacity:0.5;cursor:not-allowed}
.btn.ok{background:#3a8c6e}.btn.ok:hover{background:#4aad89}
.sdot{display:inline-block;width:7px;height:7px;border-radius:50%;margin-right:4px;flex-shrink:0;vertical-align:middle}
.g{background:#4aad89}.am{background:#e8a838}.r{background:#c0446a}
.chart-card{background:#3a3560;border:0.5px solid #8661c1;border-radius:10px;padding:13px;margin-bottom:12px}
.ct{font-size:12px;color:#be97c6;margin-bottom:9px;display:flex;align-items:center;gap:9px;flex-wrap:wrap}
.li{display:inline-flex;align-items:center;gap:3px;font-size:10px}
.ld{width:7px;height:7px;border-radius:2px}
.badge{font-size:10px;padding:2px 7px;border-radius:5px}
.b-sim{background:#3a2e60;color:#be97c6}
.b-live{background:#1e3a2e;color:#4aad89}
.b-err{background:#3a1e25;color:#e88a9a}
.api-row{display:flex;gap:6px;align-items:center;margin-bottom:8px}
.api-row input[type=text]{flex:1;background:#1a1735;border:0.5px solid #8661c1;color:#efbcd5;border-radius:6px;padding:5px 9px;font-size:11px;outline:none}
.api-row input::placeholder{color:#5a5280}
.calib-wrap{background:#1a1735;border-radius:5px;height:6px;margin-top:7px;overflow:hidden;display:none}
.calib-fill{height:100%;background:#8661c1;width:0%;transition:width 0.8s linear}
.mode-row{display:flex;align-items:center;gap:8px;margin-bottom:10px;background:#251f42;border:0.5px solid #8661c1;border-radius:8px;padding:6px 10px}
.mode-lbl{font-size:11px;color:#be97c6}
.tog{position:relative;width:36px;height:18px;cursor:pointer;flex-shrink:0}
.tog input{opacity:0;width:0;height:0}
.tsl{position:absolute;inset:0;background:#1a1735;border-radius:9px;transition:background 0.2s}
.tsl:before{content:'';position:absolute;width:12px;height:12px;left:3px;top:3px;background:#be97c6;border-radius:50%;transition:transform 0.2s}
input:checked+.tsl{background:#8661c1}
input:checked+.tsl:before{transform:translateX(18px);background:#fff}
.log{background:#1a1735;border-radius:7px;padding:8px 10px;font-size:10px;color:#be97c6;margin-top:8px;min-height:28px;line-height:1.6;font-family:monospace}
</style>
</head>
<body>

<div class="hdr">
  <h1>Cognitive Load Monitor</h1>
  <p>Paas 1–9 · Full API loop</p>
</div>

<div class="mrow">
  <div class="mc">
    <div class="lbl">Heart Rate</div>
    <div class="val" id="hrDisp">—</div>
    <div class="sub">bpm · base <span id="hrBase">—</span></div>
  </div>
  <div class="mc">
    <div class="lbl">Breath Rate</div>
    <div class="val" id="brDisp">—</div>
    <div class="sub">brpm · base <span id="brBase">—</span></div>
  </div>
  <div class="mc">
    <div class="lbl">Current Load</div>
    <div class="val" id="curLoad">—</div>
    <div class="sub">Paas · <span id="hrDelta">Δhr —</span></div>
    <div class="pbar"><div class="pfill" id="curBar" style="width:0%"></div></div>
  </div>
  <div class="mc">
    <div class="lbl">Predicted Load</div>
    <div class="val" id="predLoad">—</div>
    <div class="sub">trend estimate</div>
    <div class="pbar"><div class="pfill" id="predBar" style="width:0%;background:#efbcd5"></div></div>
  </div>
</div>

<div class="crow">
  <div class="cc" style="margin-bottom:0">
    <div class="lbl">API endpoint</div>
    <div class="api-row">
      <input type="text" id="apiUrl" placeholder="https://your-app.onrender.com" value="https://typ-backend-z2ut.onrender.com">
      <button class="btn ok" onclick="testApi()">Test</button>
    </div>
    <div style="display:flex;align-items:center;gap:6px;font-size:11px;color:#be97c6">
      <span id="apiStatus" style="display:flex;align-items:center"><span class="sdot am"></span>Not tested</span>
      <span class="badge b-sim" id="modeBadge" style="margin-left:auto">Disconnected</span>
    </div>
    <div class="log" id="apiLog">Waiting…</div>
  </div>

  <div class="cc" style="margin-bottom:0">
    <div class="lbl">Vitals source</div>
    <div class="mode-row">
      <span class="mode-lbl">Simulate</span>
      <label class="tog">
        <input type="checkbox" id="simToggle" checked>
        <span class="tsl"></span>
      </label>
      <span class="mode-lbl" id="simLbl" style="color:#efbcd5;font-weight:500">ON</span>
      <span class="badge b-sim" id="srcBadge" style="margin-left:auto">Sim</span>
    </div>
    <div id="simControls">
      <div class="srow">
        <span style="font-size:10px;color:#be97c6;width:16px">HR</span>
        <input type="range" id="hrSlider" min="40" max="180" step="1" value="72">
        <span class="sv" id="hrSV">72</span>
      </div>
      <div class="srow" style="margin-top:6px">
        <span style="font-size:10px;color:#be97c6;width:16px">BR</span>
        <input type="range" id="brSlider" min="6" max="40" step="1" value="16">
        <span class="sv" id="brSV">16</span>
      </div>
      <div class="brow">
        <button class="btn" onclick="sc('rest')">Rest</button>
        <button class="btn" onclick="sc('focus')">Focus</button>
        <button class="btn" onclick="sc('stress')">Stress</button>
        <button class="btn" onclick="sc('peak')">Peak</button>
      </div>
    </div>
    <div id="liveNote" style="display:none;font-size:11px;color:#be97c6;margin-top:8px">
      Reading live from ESP32 via API
    </div>
  </div>
</div>

<div class="cc">
  <div class="lbl">Calibration</div>
  <div class="brow" style="margin-top:0;align-items:center">
    <span id="calStatus" style="font-size:11px;color:#be97c6;display:flex;align-items:center"><span class="sdot am"></span>Not calibrated</span>
    <button class="btn ok" id="calBtn" onclick="startCal()" style="margin-left:auto">Start calibration (API)</button>
  </div>
  <div class="calib-wrap" id="calWrap"><div class="calib-fill" id="calFill"></div></div>
</div>

<div class="chart-card">
  <div class="ct">
    Cognitive load — live
    <span class="li"><span class="ld" style="background:#efbcd5"></span>Current</span>
    <span class="li"><span class="ld" style="background:#8661c1;border:1px dashed #be97c6"></span>Predicted</span>
    <span class="badge b-sim" id="clBadge" style="margin-left:auto">From API</span>
  </div>
  <div style="position:relative;width:100%;height:220px">
    <canvas id="loadChart"></canvas>
  </div>
</div>

<div class="chart-card">
  <div class="ct">
    Vitals — live
    <span class="li"><span class="ld" style="background:#efbcd5"></span>HR (bpm)</span>
    <span class="li"><span class="ld" style="background:#be97c6"></span>BR (brpm)</span>
    <span class="badge b-sim" id="vBadge" style="margin-left:auto">Simulated</span>
  </div>
  <div style="position:relative;width:100%;height:170px">
    <canvas id="vitalsChart"></canvas>
  </div>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js"></script>
<script>
const MAX_PTS = 60;
let curHR = 72, curBR = 16;
let recentLoads = [];
let simMode = true;
let apiBase = 'https://typ-backend-z2ut.onrender.com';
let apiOk = false;

const dCur=Array(MAX_PTS).fill(null), dPred=Array(MAX_PTS).fill(null);
const dHR=Array(MAX_PTS).fill(null), dBR=Array(MAX_PTS).fill(null);
const labels=Array(MAX_PTS).fill('');
const gc='#8661c130', tc='#be97c6';

const loadChart = new Chart(document.getElementById('loadChart').getContext('2d'),{
  type:'line',
  data:{labels:[...labels],datasets:[
    {label:'Current',data:[...dCur],borderColor:'#efbcd5',backgroundColor:'rgba(239,188,213,0.07)',tension:0.4,pointRadius:0,fill:true,borderWidth:2},
    {label:'Predicted',data:[...dPred],borderColor:'#8661c1',backgroundColor:'rgba(134,97,193,0.07)',tension:0.4,pointRadius:0,fill:true,borderWidth:2,borderDash:[5,4]}
  ]},
  options:{responsive:true,maintainAspectRatio:false,animation:false,
    plugins:{legend:{display:false}},
    scales:{x:{display:false},y:{min:1,max:9,ticks:{color:tc,font:{size:10},stepSize:1},grid:{color:gc},border:{color:'transparent'}}}
  }
});

const vitalsChart = new Chart(document.getElementById('vitalsChart').getContext('2d'),{
  type:'line',
  data:{labels:[...labels],datasets:[
    {label:'HR',data:[...dHR],borderColor:'#efbcd5',backgroundColor:'transparent',tension:0.4,pointRadius:0,borderWidth:1.5},
    {label:'BR',data:[...dBR],borderColor:'#be97c6',backgroundColor:'transparent',tension:0.4,pointRadius:0,borderWidth:1.5}
  ]},
  options:{responsive:true,maintainAspectRatio:false,animation:false,
    plugins:{legend:{display:false}},
    scales:{x:{display:false},y:{ticks:{color:tc,font:{size:10}},grid:{color:gc},border:{color:'transparent'}}}
  }
});

document.getElementById('hrSlider').addEventListener('input',e=>{curHR=+e.target.value;document.getElementById('hrSV').textContent=curHR;});
document.getElementById('brSlider').addEventListener('input',e=>{curBR=+e.target.value;document.getElementById('brSV').textContent=curBR;});

document.getElementById('simToggle').addEventListener('change',function(){
  simMode=this.checked;
  document.getElementById('simLbl').textContent=simMode?'ON':'OFF';
  document.getElementById('simLbl').style.color=simMode?'#efbcd5':'#5a5280';
  document.getElementById('simControls').style.display=simMode?'block':'none';
  document.getElementById('liveNote').style.display=simMode?'none':'block';
  const b=document.getElementById('srcBadge');
  b.className='badge '+(simMode?'b-sim':'b-live');
  b.textContent=simMode?'Sim':'Live ESP32';
  document.getElementById('vBadge').className='badge '+(simMode?'b-sim':'b-live');
  document.getElementById('vBadge').textContent=simMode?'Simulated':'From API';
});

function sc(s){
  const m={rest:{hr:62,br:12},focus:{hr:85,br:18},stress:{hr:105,br:24},peak:{hr:140,br:35}};
  curHR=m[s].hr; curBR=m[s].br;
  document.getElementById('hrSlider').value=curHR; document.getElementById('brSlider').value=curBR;
  document.getElementById('hrSV').textContent=curHR; document.getElementById('brSV').textContent=curBR;
}

function log(msg){
  const t=new Date().toLocaleTimeString('en-GB',{hour:'2-digit',minute:'2-digit',second:'2-digit'});
  document.getElementById('apiLog').textContent='['+t+'] '+msg;
}

async function testApi(){
  apiBase=document.getElementById('apiUrl').value.trim().replace(/\/$/,'');
  document.getElementById('apiStatus').innerHTML='<span class="sdot am"></span>Testing…';
  log('Testing /health…');
  try{
    const r=await fetch(apiBase+'/health',{signal:AbortSignal.timeout(5000)});
    if(r.ok){
      document.getElementById('apiStatus').innerHTML='<span class="sdot g"></span>Connected';
      apiOk=true;
      document.getElementById('modeBadge').className='badge b-live';
      document.getElementById('modeBadge').textContent='Connected';
      log('Connected — vitals now fetched from API');
    } else { throw new Error('HTTP '+r.status); }
  } catch(e){
    document.getElementById('apiStatus').innerHTML='<span class="sdot r"></span>Unreachable';
    apiOk=false;
    document.getElementById('modeBadge').className='badge b-err';
    document.getElementById('modeBadge').textContent='Unreachable';
    log('Error: '+e.message);
  }
}

async function startCal(){
  if(!apiOk){ log('Connect to API first'); return; }
  document.getElementById('calBtn').disabled=true;
  log('Posting /api/calibrate/start…');
  try{
    await fetch(apiBase+'/api/calibrate/start',{method:'POST',headers:{'Content-Type':'application/json'}});
    log('Calibration started on server — 90s. Keep sim posting.');
    document.getElementById('calStatus').innerHTML='<span class="sdot am"></span>Calibrating on server…';
    document.getElementById('calWrap').style.display='block';
    let elapsed=0;
    const t=setInterval(()=>{
      elapsed++;
      document.getElementById('calFill').style.width=Math.round(elapsed/90*100)+'%';
      document.getElementById('calStatus').innerHTML='<span class="sdot am"></span>Calibrating… '+elapsed+'s / 90s';
      if(elapsed>=90){
        clearInterval(t);
        document.getElementById('calBtn').disabled=false;
        document.getElementById('calWrap').style.display='none';
        document.getElementById('calStatus').innerHTML='<span class="sdot g"></span>Calibrated';
        log('Calibration complete');
      }
    },1000);
  } catch(e){ log('Cal error: '+e.message); document.getElementById('calBtn').disabled=false; }
}

function push(arr,v){arr.shift();arr.push(v);}
function clamp(v,a,b){return Math.max(a,Math.min(b,v));}

async function tick(){
  let hr = curHR, br = curBR;

  if(simMode){
    // In sim mode: add jitter, then POST to API so the server has real data
    hr = Math.round(curHR + (Math.random()*1.6-0.8));
    br = Math.round(curBR + (Math.random()*0.5-0.25));

    if(apiOk){
      try{
        await Promise.all([
          fetch(apiBase+'/api/heartrate',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({heartRate:hr}),signal:AbortSignal.timeout(2000)}),
          fetch(apiBase+'/api/breathrate',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({breathRate:br}),signal:AbortSignal.timeout(2000)})
        ]);
      } catch(e){ log('POST error: '+e.message); }
    }
  }

  // Always fetch vitals + load from API if connected
  if(apiOk){
    try{
      const [hrR, brR, clR, predR] = await Promise.all([
        fetch(apiBase+'/api/heartrate',{signal:AbortSignal.timeout(2000)}).then(r=>r.json()),
        fetch(apiBase+'/api/breathrate',{signal:AbortSignal.timeout(2000)}).then(r=>r.json()),
        fetch(apiBase+'/api/cognitive-load/current',{signal:AbortSignal.timeout(2000)}).then(r=>r.json()),
        fetch(apiBase+'/api/cognitive-load/predicted',{signal:AbortSignal.timeout(2000)}).then(r=>r.json()),
      ]);

      hr = hrR.currentHeartRate || hr;
      br = brR.currentBreathRate || br;
      const cl = clR.currentCognitiveLoad;
      const pl = predR.predictedCognitiveLoad;
      const isCal = clR.isCalibrated;
      const bhr = hrR.baselineHeartRate, bbr = brR.baselineBreathRate;

      document.getElementById('hrDisp').textContent=Math.round(hr);
      document.getElementById('brDisp').textContent=Math.round(br);
      document.getElementById('hrBase').textContent=bhr?bhr.toFixed(0):'—';
      document.getElementById('brBase').textContent=bbr?bbr.toFixed(0):'—';
      document.getElementById('hrDelta').textContent='Δhr '+clR.heartRateDelta.toFixed(2);
      document.getElementById('calStatus').innerHTML=isCal
        ?'<span class="sdot g"></span>Calibrated'
        :'<span class="sdot am"></span>Not calibrated';
      document.getElementById('clBadge').className='badge b-live';
      document.getElementById('clBadge').textContent='From API';

      push(dCur, cl); push(dPred, pl);
      push(dHR, Math.round(hr)); push(dBR, Math.round(br));

      if(isCal){
        document.getElementById('curLoad').textContent=cl.toFixed(1);
        document.getElementById('predLoad').textContent=pl.toFixed(1);
        document.getElementById('curBar').style.width=((cl-1)/8*100).toFixed(1)+'%';
        document.getElementById('predBar').style.width=((pl-1)/8*100).toFixed(1)+'%';
      }

      log((simMode?'SIM':'LIVE')+' · HR '+Math.round(hr)+' BR '+Math.round(br)+' → Load '+(isCal?cl.toFixed(1):'uncal'));

    } catch(e){
      log('Fetch error: '+e.message);
      document.getElementById('apiStatus').innerHTML='<span class="sdot r"></span>Fetch failed';
      push(dCur,null); push(dPred,null); push(dHR,null); push(dBR,null);
    }
  } else {
    // No API — show sim values locally only
    document.getElementById('hrDisp').textContent=Math.round(hr);
    document.getElementById('brDisp').textContent=Math.round(br);
    push(dHR,Math.round(hr)); push(dBR,Math.round(br));
    push(dCur,null); push(dPred,null);
    log('No API connection — connect to enable load tracking');
  }

  loadChart.data.datasets[0].data=[...dCur];
  loadChart.data.datasets[1].data=[...dPred];
  vitalsChart.data.datasets[0].data=[...dHR];
  vitalsChart.data.datasets[1].data=[...dBR];
  loadChart.update('none');
  vitalsChart.update('none');
}

setInterval(tick, 1000);
testApi();
</script>
</body>
</html>"""


@app.route('/')
def home():
    return jsonify({
        "message": "Cognitive Load Estimation API",
        "version": "1.0.0",
        "endpoints": {
            "POST /api/heartrate": "Receive heart rate data",
            "POST /api/breathrate": "Receive breath rate data",
            "GET /api/heartrate": "Get heart rate data",
            "GET /api/breathrate": "Get breath rate data",
            "GET /api/cognitive-load/current": "Get current cognitive load",
            "GET /api/cognitive-load/predicted": "Get predicted cognitive load",
            "GET /api/cognitive-load/current/uno": "Get only current cognitive load value (number)",
            "GET /api/cognitive-load/predicted/uno": "Get only predicted cognitive load value (number)",
            "POST /api/calibrate/start": "Start calibration",
            "GET /api/calibrate/status": "Get calibration status",
            "GET /dashboard": "Serve the cognitive load dashboard"
        }
    })


@app.route('/api/heartrate', methods=['POST'])
def receive_heartrate():
    remote = request.remote_addr
    print(f"Incoming POST /api/heartrate from {remote}")
    try:
        raw = request.get_data(as_text=True)
        print(f"Raw body: {raw}")
        data = request.get_json(silent=True)
    except Exception as e:
        print(f"Error reading request body: {e}")
        data = None

    if not data or 'heartRate' not in data:
        return jsonify({"status": "error", "message": "heartRate field is required"}), 400

    service.add_heart_rate_reading(data['heartRate'])
    return jsonify({"status": "success", "message": "Heart rate received"})


@app.route('/api/heartrate', methods=['GET'])
def get_heartrate():
    return jsonify({
        "currentHeartRate": service.get_current_heart_rate(),
        "baselineHeartRate": service.get_baseline_heart_rate(),
        "isCalibrated": service.is_calibrated()
    })


@app.route('/api/breathrate', methods=['POST'])
def receive_breathrate():
    remote = request.remote_addr
    print(f"Incoming POST /api/breathrate from {remote}")
    try:
        raw = request.get_data(as_text=True)
        print(f"Raw body: {raw}")
        data = request.get_json(silent=True)
    except Exception as e:
        print(f"Error reading request body: {e}")
        data = None

    if not data or 'breathRate' not in data:
        return jsonify({"status": "error", "message": "breathRate field is required"}), 400

    service.add_breath_rate_reading(data['breathRate'])
    return jsonify({"status": "success", "message": "Breath rate received"})


@app.route('/api/breathrate', methods=['GET'])
def get_breathrate():
    return jsonify({
        "currentBreathRate": service.get_current_breath_rate(),
        "baselineBreathRate": service.get_baseline_breath_rate(),
        "isCalibrated": service.is_calibrated()
    })


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok", "service": "Cognitive Load API"}), 200


@app.route('/api/cognitive-load/predicted', methods=['GET'])
def get_predicted_cognitive_load():
    return jsonify({
        "predictedCognitiveLoad": service.calculate_cognitive_load(),
        "paasScale": "1-9",
        "isCalibrated": service.is_calibrated()
    })


@app.route('/api/cognitive-load/current', methods=['GET'])
def get_current_cognitive_load():
    return jsonify({
        "currentCognitiveLoad": service.calculate_cognitive_load(),
        "heartRateDelta": service.get_heart_rate_delta(),
        "breathRateDelta": service.get_breath_rate_delta(),
        "paasScale": "1-9",
        "isCalibrated": service.is_calibrated()
    })


@app.route('/api/cognitive-load/current/uno', methods=['GET'])
def get_current_cognitive_load_value():
    return str(service.calculate_cognitive_load())


@app.route('/api/cognitive-load/predicted/uno', methods=['GET'])
def get_predicted_cognitive_load_value():
    return str(service.calculate_cognitive_load())


@app.route('/api/calibrate/start', methods=['POST'])
def start_calibration():
    thread = threading.Thread(target=service.start_calibration)
    thread.daemon = True
    thread.start()
    return jsonify({"status": "success", "message": "Calibration started", "duration": "90 seconds"})


@app.route('/api/calibrate/status', methods=['GET'])
def get_calibration_status():
    return jsonify({
        "isCalibrating": service.is_calibrating(),
        "isCalibrated": service.is_calibrated(),
        "remainingTime": service.get_remaining_calibration_time()
    })


@app.route('/dashboard')
def dashboard():
    return Response(DASHBOARD_HTML, mimetype='text/html')


if __name__ == '__main__':
    print("[*] Starting Cognitive Load API...")
    print("[*] Server running on http://0.0.0.0:8080")
    print("[*] Dashboard: http://localhost:8080/dashboard")
    app.run(host="0.0.0.0", port=8080, debug=False, use_reloader=False)