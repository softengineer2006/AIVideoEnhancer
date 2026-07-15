import platform
from dataclasses import dataclass

import psutil
import torch


@dataclass(slots=True)
class DeviceInfo:
    device: str
    cuda_available: bool
    gpu_name: str | None
    gpu_memory_gb: float
    cpu_cores: int
    logical_cores: int
    system_ram_gb: float


class DeviceManager:

    @staticmethod
    def detect() -> DeviceInfo:

        cuda = torch.cuda.is_available()

        gpu_name = None
        gpu_memory = 0.0

        if cuda:
            gpu_name = torch.cuda.get_device_name(0)

            gpu_memory = (
                torch.cuda.get_device_properties(0).total_memory
                / 1024**3
            )

        ram = psutil.virtual_memory().total / 1024**3

        return DeviceInfo(
            device="cuda" if cuda else "cpu",
            cuda_available=cuda,
            gpu_name=gpu_name,
            gpu_memory_gb=round(gpu_memory, 2),
            cpu_cores=psutil.cpu_count(logical=False),
            logical_cores=psutil.cpu_count(logical=True),
            system_ram_gb=round(ram, 2),
        )

    @staticmethod
    def get_torch_device() -> torch.device:
        """
        Returns a torch.device object for use throughout the application.
        """
        return torch.device("cuda" if torch.cuda.is_available() else "cpu")

    @staticmethod
    def print_summary(info: DeviceInfo) -> None:

        print("\n========== Hardware ==========")

        print(f"Operating System : {platform.system()}")

        print(f"Device           : {info.device}")

        print(f"CUDA             : {info.cuda_available}")

        print(f"CPU Cores        : {info.cpu_cores}")

        print(f"Logical Cores    : {info.logical_cores}")

        print(f"System RAM       : {info.system_ram_gb} GB")

        if info.cuda_available:
            print(f"GPU              : {info.gpu_name}")
            print(f"GPU Memory       : {info.gpu_memory_gb} GB")

        print("==============================\n")
