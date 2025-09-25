"""Simulation adapter for testing without hardware."""

from __future__ import annotations

import random
import time
from typing import Dict, List

from i2ctool_core.interfaces import I2CAdapter, I2CError


class SimulationAdapter(I2CAdapter):
    """Simulation adapter for testing UI without real hardware."""

    _SUPPORTED_SPEEDS = (50, 100, 400, 1000)

    def __init__(self) -> None:
        self._connected = False
        self._speed_khz = 100
        self._buses: Dict[str, Dict[int, bytearray]] = self._create_buses()
        self._active_bus = next(iter(self._buses))

    # ------------------------------------------------------------------
    # Adapter lifecycle
    # ------------------------------------------------------------------
    def open(self) -> bool:
        """Open simulated connection."""
        time.sleep(0.05)  # tiny delay for realism
        self._connected = True
        return True

    def close(self) -> None:
        """Close simulated connection."""
        self._connected = False

    def is_connected(self) -> bool:
        """Check if simulated device is connected."""
        return self._connected

    # ------------------------------------------------------------------
    # Bus management helpers (simulation specific)
    # ------------------------------------------------------------------
    def list_buses(self) -> List[str]:
        """Return available simulated I2C buses."""
        return list(self._buses.keys())

    def set_bus(self, bus: str) -> None:
        """Select active simulated bus."""
        if bus not in self._buses:
            raise I2CError(f"Bus '{bus}' not available in simulation")
        self._active_bus = bus

    def get_bus(self) -> str:
        """Return the currently selected bus."""
        return self._active_bus

    # ------------------------------------------------------------------
    # I2CAdapter implementation
    # ------------------------------------------------------------------
    def scan(self) -> List[int]:
        """Scan for simulated I2C devices."""
        self._ensure_connected()
        devices = self._buses[self._active_bus]
        # Deterministic order for UI display
        return sorted(devices.keys())

    def read(
        self,
        device_addr: int,
        mem_addr: int,
        length: int,
        addr_width: int = 1,
    ) -> bytes:
        """Read from simulated device memory."""
        self._ensure_connected()
        memory = self._get_device_memory(device_addr)

        if mem_addr < 0:
            raise I2CError("Negative memory address is invalid")
        if mem_addr >= len(memory):
            raise I2CError(f"Memory address 0x{mem_addr:04X} out of range")

        end = min(mem_addr + max(length, 0), len(memory))
        time.sleep(self._read_delay(length))
        return bytes(memory[mem_addr:end])

    def write(
        self,
        device_addr: int,
        mem_addr: int,
        data: bytes,
        addr_width: int = 1,
    ) -> None:
        """Write to simulated device memory."""
        self._ensure_connected()
        memory = self._get_device_memory(device_addr)

        if mem_addr < 0:
            raise I2CError("Negative memory address is invalid")
        if mem_addr >= len(memory):
            raise I2CError(f"Memory address 0x{mem_addr:04X} out of range")

        end = mem_addr + len(data)
        if end > len(memory):
            raise I2CError("Write would exceed device memory")

        time.sleep(self._write_delay(len(data)))
        memory[mem_addr:end] = data

    def set_speed(self, khz: int) -> None:
        """Set simulated I2C speed."""
        if khz not in self._SUPPORTED_SPEEDS:
            raise I2CError(
                f"Unsupported speed: {khz} kHz. Supported: {', '.join(map(str, self._SUPPORTED_SPEEDS))}"
            )
        self._speed_khz = khz

    def supports_eeprom_page_write(self) -> bool:
        """Simulation supports page write."""
        return True

    def get_info(self) -> str:
        """Get adapter information."""
        bus = self._active_bus
        return f"Simulation Adapter on {bus} ({self._speed_khz} kHz)"

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _ensure_connected(self) -> None:
        if not self._connected:
            raise I2CError("Adapter not connected")

    def _get_device_memory(self, device_addr: int) -> bytearray:
        devices = self._buses[self._active_bus]
        if device_addr not in devices:
            raise I2CError(f"Device 0x{device_addr:02X} not found on {self._active_bus}")
        return devices[device_addr]

    @staticmethod
    def _read_delay(length: int) -> float:
        # small deterministic delay based on length
        return min(0.002 + length * 0.00005, 0.02)

    @staticmethod
    def _write_delay(length: int) -> float:
        return min(0.005 + length * 0.00008, 0.05)

    def _create_buses(self) -> Dict[str, Dict[int, bytearray]]:
        """Create simulated buses with deterministic pseudo-random data."""
        buses: Dict[str, Dict[int, bytearray]] = {
            "/dev/i2c-0": self._create_device_map({0x40: 2048, 0x50: 1024}),
            "/dev/i2c-1": self._create_device_map({0x50: 32768, 0x51: 1024}),
            "/dev/i2c-2": self._create_device_map({0x20: 256, 0x68: 4096}),
        }
        return buses

    def _create_device_map(self, devices: Dict[int, int]) -> Dict[int, bytearray]:
        result: Dict[int, bytearray] = {}
        for addr, size in devices.items():
            memory = bytearray(size)
            for offset in range(size):
                memory[offset] = self._pattern_byte(addr, offset)
            result[addr] = memory
        return result

    @staticmethod
    def _pattern_byte(addr: int, offset: int) -> int:
        seed = (addr << 16) | offset
        random.seed(seed)
        return random.randint(0, 255)


__all__ = ["SimulationAdapter"]