import subprocess
import platform
import cpuinfo

def get_nvidia_gpu_vram(name):
    try:
        total_memory_output = subprocess.check_output(
            "nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits", shell=True
        ).decode().strip()
        free_memory_output = subprocess.check_output(
            "nvidia-smi --query-gpu=memory.free --format=csv,noheader,nounits", shell=True
        ).decode().strip()

        # Assuming there's only one NVIDIA GPU for simplicity
        total_memory = int(total_memory_output.split('\n')[0])  # Take the first GPU's memory
        free_memory = int(free_memory_output.split('\n')[0])  # Take the first GPU's free memory

        return total_memory, free_memory
    except subprocess.CalledProcessError as e:
        print(f"Failed to get VRAM details through nvidia-smi for {name}: {e}")
        return None, None

def get_gpu_info():
    system = platform.system().lower()
    if system == "windows":
        try:
            gpu_name_output = subprocess.check_output(
                "wmic path win32_VideoController get name", shell=True
            ).decode().strip()
            gpu_names = gpu_name_output.split('\n')[1:]  # Skip the header line

            for name in gpu_names:
                if name:
                    if "nvidia" in name.lower():
                        total_vram, free_vram = get_nvidia_gpu_vram(name)
                        if total_vram is not None and free_vram is not None:
                            print(f"GPU Name: {name}, Total VRAM: {total_vram} MB, Available VRAM: {free_vram} MB")
                        else:
                            print(f"GPU Name: {name}, VRAM: [Could not determine]")
                    else:
                        print(f"GPU Name: {name}, VRAM: [Not an NVIDIA GPU or cannot determine VRAM]")
        except subprocess.CalledProcessError as e:
            print(f"Failed to get GPU details: {e}")
    # Add elif blocks here for Linux and Darwin if needed
    else:
        print("Unsupported OS or no additional details available for this OS.")

def get_cpu_info():
    info = cpuinfo.get_cpu_info()
    print("CPU Info:")
    print(f"Brand: {info['brand_raw']}")
    print(f"Arch: {info['arch']}")
    print(f"Bits: {info['bits']}")
    print(f"Count: {info['count']}")

if __name__ == "__main__":
    get_cpu_info()
    get_gpu_info()
