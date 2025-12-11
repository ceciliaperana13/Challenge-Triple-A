import psutil
import platform
import socket
import os
import time
from datetime import datetime

GENERATOR_NAME = "Python System Monitor"
UPDATE_INTERVAL = 3  # secondes


def cpu_info():
    freq = psutil.cpu_freq()
    return {
        "cores": psutil.cpu_count(logical=True),
        "freq_mhz": freq.current if freq else 0,
        "usage": psutil.cpu_percent(interval=1)
    }


def memory_info():
    mem = psutil.virtual_memory()
    return {
        "used_mb": round(mem.used / (1024**2), 1),
        "total_mb": round(mem.total / (1024**2), 1),
        "percent": mem.percent
    }


def system_info():
    info = {}
    info["hostname"] = platform.node()
    info["os"] = f"{platform.system()} {platform.release()}"
    uptime_seconds = time.time() - psutil.boot_time()
    info["uptime"] = f"{uptime_seconds/3600:.2f} heures"
    info["user_count"] = len(psutil.users())
    hostname = socket.gethostname()
    info["ip"] = socket.gethostbyname(hostname)
    return info


def process_info():
    print("\n Informations sur les processus ")

    processes = []
    for p in psutil.process_iter(['pid', 'name', 'memory_percent']):
        try:
            # Appel initial pour commencer la mesure
            p.cpu_percent()
        except psutil.NoSuchProcess:
            continue

    # attends
    time.sleep(0.1)

    # passage
    processes = []
    for p in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            processes.append(p.info)
        except psutil.NoSuchProcess:
            continue

    print("\nTop 3 CPU (%) :")
    top_cpu = sorted(processes, key=lambda x: x['cpu_percent'], reverse=True)[:3]
    for proc in top_cpu:
        print(f"{proc['name']} (PID: {proc['pid']}) - CPU: {proc['cpu_percent']:.2f}%")

    print("\nTop 3 RAM (%) :")
    top_ram = sorted(processes, key=lambda x: x['memory_percent'], reverse=True)[:3]
    for proc in top_ram:
        print(f"{proc['name']} (PID: {proc['pid']}) - RAM: {proc['memory_percent']:.2f}%")


def file_analysis(folder):
    stats = {"total": 0, "images": 0, "videos": 0, "documents": 0, "others": 0}

    image_exts = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg'}
    doc_exts = {'.pdf', '.doc', '.docx', '.txt', '.rtf'}
    video_exts = {'.mp4', '.avi', '.mkv', '.mov', '.wmv'}

    for root, dirs, files in os.walk(folder):
        for file in files:
            stats["total"] += 1
            ext = os.path.splitext(file.lower())[1]
            if ext in image_exts:
                stats["images"] += 1
            elif ext in doc_exts:
                stats["documents"] += 1
            elif ext in video_exts:
                stats["videos"] += 1
            else:
                stats["others"] += 1

    return stats


def generate_dashboard():
    # Récupération des infos
    cpu = cpu_info()
    mem = memory_info()
    sys_info = system_info()
    procs = process_info()
    home = os.path.expanduser("~")
    files = file_analysis(home)

    # Charger template.html
    with open("template.html", "r", encoding="utf-8") as f:
        html = f.read()

    # Maintenant html existe, on peut remplacer :
    html = html.replace("{{ system_hostname }}", sys_info["hostname"])
    html = html.replace("{{ system_os }}", sys_info["os"])
    html = html.replace("{{ system_uptime }}", sys_info["uptime"])
    html = html.replace("{{ system_user_count }}", str(sys_info["user_count"]))
    
    # CPU
    html = html.replace("{{ cpu_core_count }}", str(cpu["cores"]))
    html = html.replace("{{ cpu_frequency_ghz }}", f"{cpu['freq_mhz']/1000:.2f}")
    html = html.replace("{{ cpu_usage_percent }}", f"{cpu['usage']:.1f}")

    # Memory
    html = html.replace("{{ memory_total_mb }}", str(mem["total_mb"]))
    html = html.replace("{{ memory_used_mb }}", str(mem["used_mb"]))
    html = html.replace("{{ memory_used_percent }}", str(mem["percent"]))

    # Network
    html = html.replace("{{ network_main_ip }}", sys_info["ip"])

    # Processes
    html = html.replace("{{ process_1_name }}", procs[0]["name"])
    html = html.replace("{{ process_1_cpu_percent }}", str(procs[0]["cpu"]))
    html = html.replace("{{ process_2_name }}", procs[1]["name"])
    html = html.replace("{{ process_2_cpu_percent }}", str(procs[1]["cpu"]))
    html = html.replace("{{ process_3_name }}", procs[2]["name"])
    html = html.replace("{{ process_3_cpu_percent }}", str(procs[2]["cpu"]))

    # Files
    html = html.replace("{{ files_total_count }}", str(files["total"]))
    html = html.replace("{{ files_images_count }}", str(files["images"]))
    html = html.replace("{{ files_videos_count }}", str(files["videos"]))
    html = html.replace("{{ files_documents_count }}", str(files["documents"]))
    html = html.replace("{{ files_others_count }}", str(files["others"]))

    # Footer
    html = html.replace("{{ generator_name }}", GENERATOR_NAME)
    html = html.replace("{{ generation_timestamp }}", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    # Sauvegarde dans index.html
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

    print("Dashboard generated → index.html")


if __name__ == "__main__":
    generate_dashboard()