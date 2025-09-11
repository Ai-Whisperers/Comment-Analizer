#!/usr/bin/env python3
"""
🌩️ Streamlit Cloud Emulator
Script principal para gestionar el emulador local de Streamlit Cloud
"""

import os
import sys
import subprocess
import time
import json
import signal
from pathlib import Path
from datetime import datetime

class StreamlitCloudEmulator:
    def __init__(self):
        self.emulator_dir = Path(__file__).parent
        self.project_root = self.emulator_dir.parent
        self.compose_file = self.emulator_dir / "docker-compose.yml"
        self.container_name = "comment-analyzer-cloud-emulator"
        
    def _run_command(self, cmd, cwd=None, capture_output=False):
        """Execute a command safely"""
        try:
            if cwd is None:
                cwd = self.emulator_dir
            
            result = subprocess.run(
                cmd, shell=True, cwd=cwd, 
                capture_output=capture_output, text=True
            )
            return result
        except Exception as e:
            print(f"❌ Error ejecutando comando: {e}")
            return None
    
    def _is_docker_running(self):
        """Check if Docker is running"""
        result = self._run_command("docker info", capture_output=True)
        return result and result.returncode == 0
    
    def _is_container_running(self):
        """Check if emulator container is running"""
        result = self._run_command(
            f"docker ps --filter name={self.container_name} --format '{{{{.Names}}}}'",
            capture_output=True
        )
        return result and self.container_name in result.stdout
    
    def _get_container_stats(self):
        """Get real-time container resource usage"""
        if not self._is_container_running():
            return None
            
        result = self._run_command(
            f"docker stats {self.container_name} --no-stream --format "
            "\"{{{{.MemUsage}}}}|{{{{.CPUPerc}}}}|{{{{.NetIO}}}}\"",
            capture_output=True
        )
        
        if result and result.returncode == 0:
            parts = result.stdout.strip().split('|')
            if len(parts) >= 2:
                return {
                    'memory': parts[0],
                    'cpu': parts[1],
                    'network': parts[2] if len(parts) > 2 else 'N/A'
                }
        return None
    
    def start(self):
        """Start the Streamlit Cloud emulator"""
        print("🌩️ INICIANDO EMULADOR DE STREAMLIT CLOUD")
        print("=" * 50)
        
        # Check prerequisites
        if not self._is_docker_running():
            print("❌ Docker no está corriendo")
            print("💡 Inicia Docker Desktop y vuelve a intentar")
            return False
            
        if not self.compose_file.exists():
            print("❌ docker-compose.yml no encontrado")
            return False
            
        # Check if already running
        if self._is_container_running():
            print("⚠️ El emulador ya está corriendo")
            print("🌐 App disponible en: http://localhost:8501")
            self.status()
            return True
        
        print("🔄 Construyendo imagen Docker...")
        result = self._run_command("docker-compose build")
        if not result or result.returncode != 0:
            print("❌ Error construyendo la imagen")
            return False
        
        print("🚀 Iniciando contenedor con límites de Streamlit Cloud...")
        result = self._run_command("docker-compose up -d")
        if not result or result.returncode != 0:
            print("❌ Error iniciando el contenedor")
            return False
        
        # Wait for container to be ready
        print("⏳ Esperando que la aplicación esté lista...")
        for i in range(30):  # Wait max 30 seconds
            if self._is_container_running():
                time.sleep(2)  # Give it a moment to fully start
                break
            time.sleep(1)
            print(".", end="", flush=True)
        
        print("\n✅ ¡Emulador iniciado exitosamente!")
        print("\n📊 LÍMITES ACTIVOS (igual que Streamlit Cloud):")
        print("   • Memoria: 1GB máximo")
        print("   • CPU: 1 core")
        print("   • Python: 3.12")
        print("\n🌐 App disponible en: http://localhost:8501")
        print("📈 Monitor de recursos: python emulator.py --monitor")
        
        return True
    
    def stop(self):
        """Stop the emulator"""
        print("🛑 Deteniendo emulador...")
        
        if not self._is_container_running():
            print("⚠️ El emulador no está corriendo")
            return True
        
        result = self._run_command("docker-compose down")
        if result and result.returncode == 0:
            print("✅ Emulador detenido exitosamente")
            return True
        else:
            print("❌ Error deteniendo el emulador")
            return False
    
    def restart(self):
        """Restart the emulator (equivalent to Streamlit Cloud reboot)"""
        print("🔄 REINICIANDO EMULADOR (simulando reboot de Streamlit Cloud)")
        print("=" * 55)
        
        self.stop()
        time.sleep(2)
        return self.start()
    
    def status(self):
        """Show emulator status"""
        print("📊 ESTADO DEL EMULADOR")
        print("=" * 25)
        
        if not self._is_docker_running():
            print("❌ Docker no está corriendo")
            return
            
        if self._is_container_running():
            print("✅ Estado: CORRIENDO")
            print("🌐 URL: http://localhost:8501")
            
            # Get resource usage
            stats = self._get_container_stats()
            if stats:
                print(f"💾 Memoria: {stats['memory']}")
                print(f"🔥 CPU: {stats['cpu']}")
                print(f"🌐 Red: {stats['network']}")
            
            print("\n⚡ Acciones disponibles:")
            print("   • Monitor: python emulator.py --monitor")
            print("   • Logs: python emulator.py --logs")  
            print("   • Restart: python emulator.py --restart")
        else:
            print("❌ Estado: DETENIDO")
            print("🚀 Iniciar: python emulator.py --start")
    
    def logs(self):
        """Show emulator logs"""
        print("📋 LOGS DEL EMULADOR")
        print("=" * 20)
        
        if not self._is_container_running():
            print("❌ El emulador no está corriendo")
            return
        
        print("📝 Últimos logs (Ctrl+C para salir):")
        print("-" * 40)
        
        try:
            self._run_command("docker-compose logs -f")
        except KeyboardInterrupt:
            print("\n👋 Cerrando logs...")
    
    def monitor(self):
        """Real-time resource monitoring"""
        print("📈 MONITOR DE RECURSOS EN TIEMPO REAL")
        print("=" * 40)
        print("Límites Streamlit Cloud: 1GB RAM, 1 CPU")
        print("Presiona Ctrl+C para salir")
        print("-" * 40)
        
        if not self._is_container_running():
            print("❌ El emulador no está corriendo")
            return
        
        try:
            while True:
                stats = self._get_container_stats()
                if stats:
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    print(f"\r[{timestamp}] 💾 {stats['memory']} | 🔥 {stats['cpu']} | 🌐 {stats['network']}", end="")
                else:
                    print(f"\r❌ No se pudieron obtener estadísticas", end="")
                
                time.sleep(2)
        except KeyboardInterrupt:
            print("\n👋 Cerrando monitor...")
    
    def cleanup(self):
        """Clean up Docker resources"""
        print("🧹 Limpiando recursos Docker...")
        
        # Stop container
        self.stop()
        
        # Remove image
        result = self._run_command("docker-compose down --rmi all --volumes")
        if result and result.returncode == 0:
            print("✅ Recursos limpiados exitosamente")
        else:
            print("⚠️ Algunos recursos podrían no haberse limpiado completamente")

def main():
    emulator = StreamlitCloudEmulator()
    
    if len(sys.argv) < 2:
        print("🌩️ STREAMLIT CLOUD EMULATOR")
        print("=" * 30)
        print("Uso: python emulator.py [opción]")
        print("\nOpciones disponibles:")
        print("  --start     Iniciar el emulador")
        print("  --stop      Detener el emulador")
        print("  --restart   Reiniciar el emulador")
        print("  --status    Ver estado actual")
        print("  --logs      Ver logs en tiempo real")
        print("  --monitor   Monitor de recursos")
        print("  --cleanup   Limpiar recursos Docker")
        return
    
    action = sys.argv[1]
    
    if action == "--start":
        emulator.start()
    elif action == "--stop":
        emulator.stop()
    elif action == "--restart":
        emulator.restart()
    elif action == "--status":
        emulator.status()
    elif action == "--logs":
        emulator.logs()
    elif action == "--monitor":
        emulator.monitor()
    elif action == "--cleanup":
        emulator.cleanup()
    else:
        print(f"❌ Opción desconocida: {action}")
        print("💡 Usa: python emulator.py para ver opciones disponibles")

if __name__ == "__main__":
    main()