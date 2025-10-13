import psutil
import CommonUtil
Debugstat = CommonUtil.read_key_from_JSON("Debug")
try:
    import platform as plat
    from datetime import datetime
    print("="*40, "System Information", "="*40)
    print(f"System: {plat.system()}")
    print(f"Node Name: {plat.node()}")
    print(f"Release: {plat.release()}")
    print(f"Version: {plat.version()}")
    print(f"Machine: {plat.machine()}")
    system_name = plat.system() # Get the system name
    if system_name == "Darwin":
        print("You have mac os installed")
    elif system_name == "Linux":
        print("You have linux installed")
    elif system_name == "Windows":
        print("You have windows installed")
    print("="*50 +"="*50)
except ImportError:
    print("Error: we could not import the required modules")
if Debugstat:
    print("* Daddy Platkernel has successfully loaded!")
