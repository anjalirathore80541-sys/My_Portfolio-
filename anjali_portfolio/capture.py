import subprocess
import os

chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
html_path = r"C:\Users\ravi\.gemini\antigravity\scratch\anjali_portfolio\index.html"
out_path = r"C:\Users\ravi\.gemini\antigravity\scratch\anjali_portfolio\portfolio_preview.png"

url = "file:///" + html_path.replace("\\", "/")

args = [
    chrome,
    "--headless=new",
    "--no-sandbox",
    "--disable-gpu",
    "--disable-software-rasterizer",
    "--hide-scrollbars",
    "--window-size=1200,1050",
    f"--screenshot={out_path}",
    url
]

print("Running headless Chrome with --no-sandbox...")
try:
    res = subprocess.run(args, capture_output=True, text=True, timeout=20)
    print("Return code:", res.returncode)
    print("File exists:", os.path.exists(out_path))
    if os.path.exists(out_path):
        print("File size:", os.path.getsize(out_path))
except Exception as e:
    print("Error:", e)
