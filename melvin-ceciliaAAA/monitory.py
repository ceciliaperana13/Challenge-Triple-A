import psutil
import platform
import socket
import os
from datetime import datetime


# ---------- Fonctions utilitaires ----------
def usage_color(percent):
    
    if percent <= 50:
        return "green"
    elif percent <= 80:
        return "orange"
    else:
        return "red"

# ---------- Collecte des informations système ----------
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
machine_name = platform.node()
os_name = platform.system()
os_version = platform.version()
boot_time = datetime.fromtimestamp(psutil.boot_time())
uptime_seconds = (datetime.now() - boot_time).total_seconds()
uptime = f"{int(uptime_seconds // 3600)}h {int((uptime_seconds % 3600) // 60)}m"
user_count = len(psutil.users())
try:
    ip_address = socket.gethostbyname(socket.gethostname())
except:
    ip_address = "N/A"

# ---------- CPU ----------
cpu_cores = psutil.cpu_count(logical=True)
cpu_freq = round(psutil.cpu_freq().current / 1000, 2)
cpu_usage = psutil.cpu_percent(interval=1)
cpu_usage_color = usage_color(cpu_usage)

# CPU par cœur
per_core_usages = psutil.cpu_percent(interval=1, percpu=True)
per_core_gauges = ""
for idx, usage in enumerate(per_core_usages, start=1):
    color = usage_color(usage)
    per_core_gauges += f"""
    <div class="core-gauge">
        Core {idx}: <span class="{color}">{usage}%</span>
        <div class="progress-bar">
            <div class="progress" style="width: {usage}%; background-color: {color};"></div>
        </div>
    </div>
    """

# ---------- Mémoire ----------
ram = psutil.virtual_memory()
ram_total = round(ram.total / (1024**3), 2)
ram_used = round(ram.used / (1024**3), 2)
ram_percent = ram.percent
ram_usage_color = usage_color(ram_percent)

# ---------- Top 3 processus ----------
processes = []
for proc in psutil.process_iter(['name', 'cpu_percent', 'memory_percent']):
    processes.append(proc.info)
top_processes = sorted(processes, key=lambda x: (x['cpu_percent'] + x['memory_percent']), reverse=True)[:3]

top_processes_list = ""
for proc in top_processes:
    top_processes_list += f"<li>{proc['name']} - CPU: {proc['cpu_percent']}%, RAM: {proc['memory_percent']:.2f}%</li>\n"

# ---------- Analyse fichiers ----------
directory = os.path.expanduser("~/Documents")  
extensions = ['.txt', '.py', '.pdf', '.jpg']
file_stats = {}
total_files = 0

for root, dirs, files in os.walk(directory):
    for file in files:
        ext = os.path.splitext(file)[1].lower()
        if ext in extensions:
            file_stats[ext] = file_stats.get(ext, 0) + 1
            total_files += 1

file_stats_list = ""
for ext, count in file_stats.items():
    percent = round(count / total_files * 100, 2) if total_files > 0 else 0
    file_stats_list += f"<li>{ext}: {count} files ({percent}%)</li>\n"

# ---------- Préparer les remplacements ----------
replacements = {
    "{{ timestamp }}": timestamp,
    "{{ machine_name }}": machine_name,
    "{{ os_name }}": os_name,
    "{{ os_version }}": os_version,
    "{{ uptime }}": uptime,
    "{{ user_count }}": str(user_count),
    "{{ ip_address }}": ip_address,
    "{{ cpu_cores }}": str(cpu_cores),
    "{{ cpu_freq }}": str(cpu_freq),
    "{{ cpu_usage }}": str(cpu_usage),
    "{{ cpu_usage_color }}": cpu_usage_color,
    "{{ per_core_gauges }}": per_core_gauges,
    "{{ ram_total }}": str(ram_total),
    "{{ ram_used }}": str(ram_used),
    "{{ ram_percent }}": str(ram_percent),
    "{{ ram_usage_color }}": ram_usage_color,
    "{{ top_processes_list }}": top_processes_list,
    "{{ file_stats_list }}": file_stats_list
}

# ---------- Générer index.html ----------
with open("template.html", "r", encoding="utf-8") as f:
    html_content = f.read()

for key, value in replacements.items():
    html_content = html_content.replace(key, value)

with open("index.html", "w") as f:
    f.write(html_content)

print("Dashboard généré : index.html")
