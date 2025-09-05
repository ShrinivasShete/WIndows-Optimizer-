import os
import subprocess
import tkinter as tk
from tkinter import messagebox
import winreg
import ctypes
import sys
import shutil

# -------------------------
# Admin Check
# -------------------------
def run_as_admin():
    if not ctypes.windll.shell32.IsUserAnAdmin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        sys.exit()

run_as_admin()

# -------------------------
# Backup Registry
# -------------------------
def backup_registry():
    backup_path_hklm = os.path.expanduser("~\\Desktop\\registry_backup_HKLM.reg")
    backup_path_hkcu = os.path.expanduser("~\\Desktop\\registry_backup_HKCU.reg")
    try:
        os.system(f"reg export HKLM {backup_path_hklm} /y")
        os.system(f"reg export HKCU {backup_path_hkcu} /y")
    except:
        messagebox.showwarning("Backup Failed", "Could not backup registry.")
    return backup_path_hklm, backup_path_hkcu

# -------------------------
# BIOS & Windows Tweaks
# -------------------------
def is_ultimate_performance_active():
    try:
        output = subprocess.check_output("powercfg /getactivescheme", shell=True, text=True)
        return "Ultimate Performance" in output
    except:
        return False

def set_ultimate_performance_power_plan():
    os.system("powercfg -duplicatescheme e9a42b02-d5df-448d-aa00-03f14749eb61 >nul 2>&1")
    os.system("powercfg -setactive e9a42b02-d5df-448d-aa00-03f14749eb61")

def is_visual_effects_disabled():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             r"Software\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects",
                             0, winreg.KEY_READ)
        val, _ = winreg.QueryValueEx(key, "VisualFXSetting")
        winreg.CloseKey(key)
        return val == 2
    except:
        return False

def disable_visual_effects():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             r"Software\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects",
                             0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "VisualFXSetting", 0, winreg.REG_DWORD, 2)
        winreg.CloseKey(key)
    except:
        pass

def is_priority_set():
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                             r"SYSTEM\CurrentControlSet\Control\PriorityControl",
                             0, winreg.KEY_READ)
        val, _ = winreg.QueryValueEx(key, "Win32PrioritySeparation")
        winreg.CloseKey(key)
        return val == 38
    except:
        return False

def set_win32priorityseparation():
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                             r"SYSTEM\CurrentControlSet\Control\PriorityControl",
                             0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "Win32PrioritySeparation", 0, winreg.REG_DWORD, 38)
        winreg.CloseKey(key)
    except PermissionError:
        messagebox.showwarning("Permission Error", "Win32PrioritySeparation tweak requires admin.")

def is_gpu_scheduling_enabled():
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                             r"SYSTEM\CurrentControlSet\Control\GraphicsDrivers",
                             0, winreg.KEY_READ | winreg.KEY_WOW64_64KEY)
        val, _ = winreg.QueryValueEx(key, "HwSchMode")
        winreg.CloseKey(key)
        return val == 2
    except FileNotFoundError:
        return False

def set_gpu_scheduling(enable=True):
    try:
        key = winreg.CreateKeyEx(winreg.HKEY_LOCAL_MACHINE,
                                 r"SYSTEM\CurrentControlSet\Control\GraphicsDrivers", 0,
                                 winreg.KEY_SET_VALUE | winreg.KEY_WOW64_64KEY)
        winreg.SetValueEx(key, "HwSchMode", 0, winreg.REG_DWORD, 2 if enable else 0)
        winreg.CloseKey(key)
    except PermissionError:
        messagebox.showwarning("Permission Error", "GPU Scheduling tweak requires admin.")

# -------------------------
# Network Tweaks
# -------------------------
def is_network_throttling_index_set():
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                             r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters",
                             0, winreg.KEY_READ | winreg.KEY_WOW64_64KEY)
        val, _ = winreg.QueryValueEx(key, "NetworkThrottlingIndex")
        winreg.CloseKey(key)
        return val == 0xFFFFFFFF
    except:
        return False

def set_network_throttling_index():
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                             r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters",
                             0, winreg.KEY_SET_VALUE | winreg.KEY_WOW64_64KEY)
        winreg.SetValueEx(key, "NetworkThrottlingIndex", 0, winreg.REG_DWORD, 0xFFFFFFFF)
        winreg.CloseKey(key)
    except PermissionError:
        messagebox.showwarning("Permission Error", "Network Throttling tweak requires admin.")

def is_tcp_ack_frequency_set():
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                             r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters",
                             0, winreg.KEY_READ | winreg.KEY_WOW64_64KEY)
        val, _ = winreg.QueryValueEx(key, "TcpAckFrequency")
        winreg.CloseKey(key)
        return val == 1
    except:
        return False

def set_tcp_ack_frequency():
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                             r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters",
                             0, winreg.KEY_SET_VALUE | winreg.KEY_WOW64_64KEY)
        winreg.SetValueEx(key, "TcpAckFrequency", 0, winreg.REG_DWORD, 1)
        winreg.CloseKey(key)
    except PermissionError:
        messagebox.showwarning("Permission Error", "TCP ACK Frequency tweak requires admin.")

def is_tcp_no_delay_set():
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                             r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters",
                             0, winreg.KEY_READ | winreg.KEY_WOW64_64KEY)
        val, _ = winreg.QueryValueEx(key, "TCPNoDelay")
        winreg.CloseKey(key)
        return val == 1
    except:
        return False

def set_tcp_no_delay():
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                             r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters",
                             0, winreg.KEY_SET_VALUE | winreg.KEY_WOW64_64KEY)
        winreg.SetValueEx(key, "TCPNoDelay", 0, winreg.REG_DWORD, 1)
        winreg.CloseKey(key)
    except PermissionError:
        messagebox.showwarning("Permission Error", "TCP No Delay tweak requires admin.")

def is_tcp_deltick_set():
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                             r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters",
                             0, winreg.KEY_READ | winreg.KEY_WOW64_64KEY)
        val, _ = winreg.QueryValueEx(key, "TCPDelAckTicks")
        winreg.CloseKey(key)
        return val == 0
    except:
        return False

def set_tcp_deltick():
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                             r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters",
                             0, winreg.KEY_SET_VALUE | winreg.KEY_WOW64_64KEY)
        winreg.SetValueEx(key, "TCPDelAckTicks", 0, winreg.REG_DWORD, 0)
        winreg.CloseKey(key)
    except PermissionError:
        messagebox.showwarning("Permission Error", "TCP DelTick tweak requires admin.")

# -------------------------
# New Tweaks Functions
# -------------------------
# Power Throttling
def is_power_throttling_disabled():
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                             r"SYSTEM\CurrentControlSet\Control\Power\PowerThrottling",
                             0, winreg.KEY_READ)
        val, _ = winreg.QueryValueEx(key, "PowerThrottlingOff")
        winreg.CloseKey(key)
        return val == 1
    except:
        return False

def disable_power_throttling():
    try:
        key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE,
                               r"SYSTEM\CurrentControlSet\Control\Power\PowerThrottling")
        winreg.SetValueEx(key, "PowerThrottlingOff", 0, winreg.REG_DWORD, 1)
        winreg.CloseKey(key)
    except PermissionError:
        messagebox.showwarning("Permission Error", "Power Throttling tweak requires admin.")

# MMCSS Tweaks
def is_mmcss_applied():
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                             r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile",
                             0, winreg.KEY_READ)
        val1, _ = winreg.QueryValueEx(key, "NetworkThrottlingIndex")
        val2, _ = winreg.QueryValueEx(key, "SystemResponsiveness")
        winreg.CloseKey(key)
        return val1 == 10 and val2 == 0
    except:
        return False

def apply_mmcss():
    try:
        key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE,
                               r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile")
        winreg.SetValueEx(key, "NetworkThrottlingIndex", 0, winreg.REG_DWORD, 10)
        winreg.SetValueEx(key, "SystemResponsiveness", 0, winreg.REG_DWORD, 0)
        winreg.CloseKey(key)
    except PermissionError:
        messagebox.showwarning("Permission Error", "MMCSS tweak requires admin.")

# Fullscreen Optimizations
def is_fs_optimization_disabled():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             r"System\GameConfigStore",
                             0, winreg.KEY_READ)
        val, _ = winreg.QueryValueEx(key, "GameDVR_Enabled")
        winreg.CloseKey(key)
        return val == 0
    except:
        return False

def disable_fs_optimization():
    try:
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER,
                               r"System\GameConfigStore")
        winreg.SetValueEx(key, "GameDVR_Enabled", 0, winreg.REG_DWORD, 0)
        winreg.SetValueEx(key, "GameDVR_FSEBehaviorMode", 0, winreg.REG_DWORD, 2)
        winreg.SetValueEx(key, "GameDVR_HonorUserFSEBehaviorMode", 0, winreg.REG_DWORD, 0)
        winreg.SetValueEx(key, "GameDVR_DXGIHonorFSEWindowsCompatible", 0, winreg.REG_DWORD, 1)
        winreg.SetValueEx(key, "GameDVR_EFSEFeatureFlags", 0, winreg.REG_DWORD, 0)
        winreg.CloseKey(key)
    except PermissionError:
        messagebox.showwarning("Permission Error", "Fullscreen Optimization tweak requires admin.")

# Processes Kill / Menu Show
def is_process_tweaks_set():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             r"Control Panel\Desktop",
                             0, winreg.KEY_READ)
        val1, _ = winreg.QueryValueEx(key, "AutoEndTasks")
        val2, _ = winreg.QueryValueEx(key, "HungAppTimeout")
        val3, _ = winreg.QueryValueEx(key, "WaitToKillAppTimeout")
        val4, _ = winreg.QueryValueEx(key, "LowLevelHooksTimeout")
        val5, _ = winreg.QueryValueEx(key, "MenuShowDelay")
        winreg.CloseKey(key)
        return val1=="1" and val2=="1000" and val3=="2000" and val4=="1000" and val5=="0"
    except:
        return False

def apply_process_tweaks():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             r"Control Panel\Desktop",
                             0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "AutoEndTasks", 0, winreg.REG_SZ, "1")
        winreg.SetValueEx(key, "HungAppTimeout", 0, winreg.REG_SZ, "1000")
        winreg.SetValueEx(key, "WaitToKillAppTimeout", 0, winreg.REG_SZ, "2000")
        winreg.SetValueEx(key, "LowLevelHooksTimeout", 0, winreg.REG_SZ, "1000")
        winreg.SetValueEx(key, "MenuShowDelay", 0, winreg.REG_SZ, "0")
        winreg.CloseKey(key)
        # WaitToKillServiceTimeout
        key2 = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                              r"SYSTEM\CurrentControlSet\Control",
                              0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key2, "WaitToKillServiceTimeout", 0, winreg.REG_SZ, "2000")
        winreg.CloseKey(key2)
    except PermissionError:
        messagebox.showwarning("Permission Error", "Process tweaks require admin.")

# Auto Maintenance
def is_auto_maintenance_disabled():
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                             r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Schedule\Maintenance",
                             0, winreg.KEY_READ)
        val, _ = winreg.QueryValueEx(key, "MaintenanceDisabled")
        winreg.CloseKey(key)
        return val==1
    except:
        return False

def disable_auto_maintenance():
    try:
        key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE,
                               r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Schedule\Maintenance")
        winreg.SetValueEx(key, "MaintenanceDisabled", 0, winreg.REG_DWORD, 1)
        winreg.CloseKey(key)
    except PermissionError:
        messagebox.showwarning("Permission Error", "Auto Maintenance tweak requires admin.")

# Hibernation
def is_hibernation_disabled():
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                             r"SYSTEM\CurrentControlSet\Control\Power",
                             0, winreg.KEY_READ)
        val, _ = winreg.QueryValueEx(key, "HibernateEnabled")
        winreg.CloseKey(key)
        return val==0
    except:
        return False

def disable_hibernation():
    try:
        key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE,
                               r"SYSTEM\CurrentControlSet\Control\Power")
        winreg.SetValueEx(key, "HibernateEnabled", 0, winreg.REG_DWORD, 0)
        winreg.CloseKey(key)
    except PermissionError:
        messagebox.showwarning("Permission Error", "Hibernation tweak requires admin.")

# -------------------------
# Cleanup Tweaks
# -------------------------
def optimize_ssd_cleanup():
    subprocess.run("defrag C: /O", shell=True)
    messagebox.showinfo("SSD Optimization", "SSD optimization complete.")

def disk_cleanup():
    subprocess.run("cleanmgr", shell=True)
    messagebox.showinfo("Disk Cleanup", "Disk Cleanup completed.")

def temp_cleanup():
    temp_dir = os.environ.get("TEMP", "")
    if temp_dir and os.path.exists(temp_dir):
        try:
            for filename in os.listdir(temp_dir):
                file_path = os.path.join(temp_dir, filename)
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            messagebox.showinfo("Temp Cleanup", "Temp files cleaned.")
        except Exception as e:
            messagebox.showwarning("Temp Cleanup", f"Could not delete some temp files.\n{e}")
    else:
        messagebox.showinfo("Temp Cleanup", "Temp folder not found.")

def flush_dns():
    try:
        subprocess.run("ipconfig /flushdns", shell=True)
        messagebox.showinfo("Flush DNS", "DNS Cache Flushed Successfully.")
    except Exception as e:
        messagebox.showwarning("Flush DNS", f"Failed to flush DNS.\n{e}")

# -------------------------
# GUI
# -------------------------
root = tk.Tk()
root.title("AceTweaks – PC Optimizer")
root.geometry("1350x500")  
root.configure(bg="#1C1C1C")

tk.Label(root, text="AceTweaks", font=("Arial", 22, "bold"), fg="#00CED1", bg="#1C1C1C").pack(pady=10)
tk.Label(root, text="Select tweaks to apply:", font=("Arial", 14), fg="white", bg="#1C1C1C").pack(pady=5)

frame_bios = tk.LabelFrame(root, text="BIOS & Windows Tweaks", font=("Arial", 12, "bold"), fg="white",
                           bg="#2F2F2F", padx=15, pady=15)
frame_bios.place(x=20, y=70, width=450, height=400)

frame_network = tk.LabelFrame(root, text="Network Tweaks", font=("Arial", 12, "bold"), fg="white",
                              bg="#2F2F2F", padx=15, pady=15)
frame_network.place(x=490, y=70, width=450, height=400)

frame_cleanup = tk.LabelFrame(root, text="Cleanup", font=("Arial", 12, "bold"), fg="white",
                              bg="#2F2F2F", padx=15, pady=15)
frame_cleanup.place(x=960, y=70, width=350, height=400)

# -------------------------
# Checkbox Variables
# -------------------------
var_power_plan = tk.BooleanVar(value=is_ultimate_performance_active())
var_visuals = tk.BooleanVar(value=is_visual_effects_disabled())
var_priority = tk.BooleanVar(value=is_priority_set())
var_gpu = tk.BooleanVar(value=is_gpu_scheduling_enabled())
var_power_throttle = tk.BooleanVar(value=is_power_throttling_disabled())
var_mmcss = tk.BooleanVar(value=is_mmcss_applied())
var_fsopt = tk.BooleanVar(value=is_fs_optimization_disabled())
var_process = tk.BooleanVar(value=is_process_tweaks_set())
var_auto_maint = tk.BooleanVar(value=is_auto_maintenance_disabled())
var_hibernate = tk.BooleanVar(value=is_hibernation_disabled())

var_network_throttling = tk.BooleanVar(value=is_network_throttling_index_set())
var_tcp_ack = tk.BooleanVar(value=is_tcp_ack_frequency_set())
var_tcp_no_delay = tk.BooleanVar(value=is_tcp_no_delay_set())
var_tcp_deltick = tk.BooleanVar(value=is_tcp_deltick_set())

# -------------------------
# Helper for Checkboxes
# -------------------------
def add_checkbox(parent, text, var, desc):
    tk.Checkbutton(parent, text=text, variable=var, bg="#2F2F2F", fg="white", selectcolor="#1C1C1C").pack(anchor='w', padx=10)
    tk.Label(parent, text=desc, font=("Arial", 8), fg="#CCCCCC", bg="#2F2F2F").pack(anchor='w', padx=25, pady=(0,5))

# BIOS & Windows
add_checkbox(frame_bios, "Ultimate Performance Power Plan", var_power_plan, "→ Maximizes Windows power plan for FPS")
add_checkbox(frame_bios, "Disable Visual Effects", var_visuals, "→ Turns off animations and transparency")
add_checkbox(frame_bios, "Win32PrioritySeparation", var_priority, "→ Gives more CPU priority to foreground apps (Value: 38)")
add_checkbox(frame_bios, "GPU Scheduling", var_gpu, "→ Enable Hardware-accelerated GPU scheduling")
add_checkbox(frame_bios, "Disable Power Throttling", var_power_throttle, "→ Disables CPU power throttling")
add_checkbox(frame_bios, "MMCSS Tweaks", var_mmcss, "→ Optimizes multimedia task priorities")
add_checkbox(frame_bios, "Disable Fullscreen Optimizations", var_fsopt, "→ Global fullscreen optimization off")
add_checkbox(frame_bios, "Process Kill & Menu Tweaks", var_process, "→ Faster app close & menu response")
add_checkbox(frame_bios, "Disable Auto Maintenance", var_auto_maint, "→ Turns off Windows auto maintenance")
add_checkbox(frame_bios, "Disable Hibernation", var_hibernate, "→ Turn off hibernate feature")

# Network Tweaks
add_checkbox(frame_network, "Network Throttling Index", var_network_throttling, "→ Optimized value: 0xFFFFFFFF")
add_checkbox(frame_network, "TCP ACK Frequency", var_tcp_ack, "→ Optimized value: 1")
add_checkbox(frame_network, "TCP No Delay", var_tcp_no_delay, "→ Optimized value: 1")
add_checkbox(frame_network, "TCP DelTick", var_tcp_deltick, "→ Optimized value: 0")

# Cleanup Buttons
def add_cleanup_button(text, command):
    btn = tk.Button(frame_cleanup, text=text, command=command, width=25, height=2, bg="#00CED1", fg="black")
    btn.pack(pady=10)
    btn.bind("<Enter>", lambda e: e.widget.config(bg="#00BFFF"))
    btn.bind("<Leave>", lambda e: e.widget.config(bg="#00CED1"))

add_cleanup_button("Optimize SSD / Defrag", optimize_ssd_cleanup)
add_cleanup_button("Disk Cleanup", disk_cleanup)
add_cleanup_button("Temp Files Cleanup", temp_cleanup)
add_cleanup_button("Flush DNS", flush_dns)

# -------------------------
# Apply Selected Tweaks
# -------------------------
def apply_selected_tweaks():
    backup_registry()
    applied = []

    # BIOS & Windows
    if var_power_plan.get(): set_ultimate_performance_power_plan(); applied.append("Ultimate Performance Power Plan")
    if var_visuals.get(): disable_visual_effects(); applied.append("Disabled Visual Effects")
    if var_priority.get(): set_win32priorityseparation(); applied.append("Win32PrioritySeparation")
    if var_gpu.get(): set_gpu_scheduling(True); applied.append("GPU Scheduling Enabled")
    else: set_gpu_scheduling(False); applied.append("GPU Scheduling Disabled")
    if var_power_throttle.get(): disable_power_throttling(); applied.append("Power Throttling Disabled")
    if var_mmcss.get(): apply_mmcss(); applied.append("MMCSS Tweaks Applied")
    if var_fsopt.get(): disable_fs_optimization(); applied.append("Fullscreen Optimization Disabled")
    if var_process.get(): apply_process_tweaks(); applied.append("Process Kill & Menu Tweaks Applied")
    if var_auto_maint.get(): disable_auto_maintenance(); applied.append("Auto Maintenance Disabled")
    if var_hibernate.get(): disable_hibernation(); applied.append("Hibernation Disabled")

    # Network
    if var_network_throttling.get(): set_network_throttling_index(); applied.append("Network Throttling Index")
    if var_tcp_ack.get(): set_tcp_ack_frequency(); applied.append("TCP ACK Frequency")
    if var_tcp_no_delay.get(): set_tcp_no_delay(); applied.append("TCP No Delay")
    if var_tcp_deltick.get(): set_tcp_deltick(); applied.append("TCP DelTick")

    if applied:
        messagebox.showinfo("Tweaks Applied", "Applied Tweaks:\n- " + "\n- ".join(applied))
    else:
        messagebox.showinfo("No Tweaks Selected", "Please select at least one tweak to apply.")

# -------------------------
# Restore Defaults
# -------------------------
def restore_defaults():
    backup_hklm = os.path.expanduser("~\\Desktop\\registry_backup_HKLM.reg")
    backup_hkcu = os.path.expanduser("~\\Desktop\\registry_backup_HKCU.reg")
    restored = False
    for backup in [backup_hklm, backup_hkcu]:
        if os.path.exists(backup):
            os.system(f'reg import "{backup}"')
            restored = True
    if restored:
        messagebox.showinfo("Restore", "Registry restored from backup.")
    else:
        messagebox.showwarning("Restore", "Backup not found on Desktop.")

# -------------------------
# Apply & Restore Buttons
# -------------------------
btn_apply = tk.Button(root, text="Apply Selected Tweaks", command=apply_selected_tweaks,
                      width=50, height=2, bg="#00CED1", fg="black")
btn_apply.place(x=300, y=480)
btn_apply.bind("<Enter>", lambda e: e.widget.config(bg="#00BFFF"))
btn_apply.bind("<Leave>", lambda e: e.widget.config(bg="#00CED1"))

btn_restore = tk.Button(root, text="Restore Defaults", command=restore_defaults,
                        width=50, height=2, bg="#FF6347", fg="black")
btn_restore.place(x=760, y=480)
btn_restore.bind("<Enter>", lambda e: e.widget.config(bg="#FF4500"))
btn_restore.bind("<Leave>", lambda e: e.widget.config(bg="#FF6347"))

root.mainloop()
