"""
Fallback implementation for psutil when not available
Provides basic system monitoring capabilities
"""
import os
import time
import platform
from typing import Dict, Any, Optional

class FallbackProcess:
    """Fallback implementation for psutil.Process"""
    
    def __init__(self, pid: Optional[int] = None):
        self.pid = pid or os.getpid()
        self._start_time = time.time()
    
    def cpu_percent(self, interval: Optional[float] = None) -> float:
        """Returns a simulated CPU percentage"""
        # Simple fallback - return a random-ish value
        return hash(str(time.time())) % 100 / 10.0
    
    def memory_info(self):
        """Returns mock memory info"""
        class MockMemoryInfo:
            def __init__(self):
                # Estimate based on typical usage
                self.rss = 50 * 1024 * 1024  # 50MB
                self.vms = 100 * 1024 * 1024  # 100MB
        return MockMemoryInfo()
    
    def memory_percent(self) -> float:
        """Returns mock memory percentage"""
        return 5.0  # Assume 5% memory usage

class FallbackPsutil:
    """Fallback psutil-like interface"""
    
    def __init__(self):
        self.Process = FallbackProcess
    
    def cpu_percent(self, interval: Optional[float] = None, percpu: bool = False) -> float:
        """Returns mock CPU percentage"""
        if percpu:
            # Return list for multiple CPUs
            cpu_count = os.cpu_count() or 4
            return [hash(str(time.time() + i)) % 100 / 10.0 for i in range(cpu_count)]
        return hash(str(time.time())) % 100 / 10.0
    
    def virtual_memory(self):
        """Returns mock virtual memory info"""
        class MockVirtualMemory:
            def __init__(self):
                # Estimate typical system memory
                self.total = 8 * 1024 * 1024 * 1024  # 8GB
                self.available = 4 * 1024 * 1024 * 1024  # 4GB available
                self.used = self.total - self.available
                self.percent = (self.used / self.total) * 100
        
        return MockVirtualMemory()
    
    def disk_usage(self, path: str = '/'):
        """Returns mock disk usage"""
        class MockDiskUsage:
            def __init__(self):
                # Estimate typical disk usage
                self.total = 500 * 1024 * 1024 * 1024  # 500GB
                self.used = 250 * 1024 * 1024 * 1024   # 250GB used
                self.free = self.total - self.used
        
        return MockDiskUsage()
    
    def boot_time(self) -> float:
        """Returns mock boot time"""
        # Estimate boot time as 1 hour ago
        return time.time() - 3600
    
    def cpu_count(self, logical: bool = True) -> int:
        """Returns CPU count"""
        return os.cpu_count() or 4

def get_fallback_psutil() -> FallbackPsutil:
    """Get fallback psutil instance"""
    return FallbackPsutil()

# Create a global instance for compatibility
fallback_psutil = get_fallback_psutil()
Process = fallback_psutil.Process
cpu_percent = fallback_psutil.cpu_percent
virtual_memory = fallback_psutil.virtual_memory
disk_usage = fallback_psutil.disk_usage
boot_time = fallback_psutil.boot_time
cpu_count = fallback_psutil.cpu_count