# Windows Task Scheduler Setup for DuckDNS Auto-Update

## Step 1: Edit the Batch File

1. Open `duckdns-update.bat` in Notepad
2. Replace:
   - `your-subdomain` → Your DuckDNS domain (e.g., `cognitiveload`)
   - `your-token-here` → Your DuckDNS token
3. Save the file to: `C:\DuckDNS\duckdns-update.bat`

## Step 2: Create Scheduled Task

1. Press `Win + R` → Type: `taskschd.msc` → Press Enter
2. Click **"Create Basic Task"**
3. Configure:

   **Name:** DuckDNS Auto-Update
   **Description:** Updates DuckDNS IP every 5 minutes

4. **Trigger:** Daily
   - Start: Today
   - Recur every: 1 days
   - Click Next

5. **Action:** Start a program
   - Program/script: `C:\DuckDNS\duckdns-update.bat`
   - Click Next → Finish

6. **Modify for 5-minute interval:**
   - Find your task in the list
   - Right-click → Properties
   - Go to **"Triggers"** tab → Edit
   - Check **"Repeat task every:"** → Select **5 minutes**
   - For a duration of: **Indefinitely**
   - Click OK

7. **Test it:**
   - Right-click the task → Run
   - Check `C:\DuckDNS\duckdns.log` to see if it worked

## Alternative: PowerShell Method

Create a PowerShell script instead:

1. Save this as `C:\DuckDNS\duckdns-update.ps1`:
```powershell
$domain = "your-subdomain"
$token = "your-token-here"
$url = "https://www.duckdns.org/update?domains=$domain&token=$token&ip="
Invoke-WebRequest -Uri $url -UseBasicParsing | Out-Null
Add-Content -Path "C:\DuckDNS\duckdns.log" -Value "[$(Get-Date)] Updated"
```

2. In Task Scheduler, use:
   - Program: `powershell.exe`
   - Arguments: `-ExecutionPolicy Bypass -File "C:\DuckDNS\duckdns-update.ps1"`

Done! Your IP will update automatically every 5 minutes.
