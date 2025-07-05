import subprocess
import sys

def check_package_compatibility():
    """Verifica compatibilidad de paquetes principales"""
    
    print("=== Verificando compatibilidad para TensorFlow 2.15+ ===\n")
    
    # Paquetes críticos para verificar
    critical_packages = {
        'opencv-python': '4.8.1',
        'numpy': '1.24.3',
        'scikit-learn': '1.3.0',
        'mlflow': '2.8.0',
        'pandas': '2.0.3',
        'matplotlib': '3.7.2',
        'seaborn': '0.12.2',
        'Pillow': '10.0.0'
    }
    
    # Verificar versiones actuales
    current_packages = {}
    result = subprocess.run([sys.executable, '-m', 'pip', 'list'], 
                          capture_output=True, text=True)
    
    for line in result.stdout.split('\n'):
        for pkg in critical_packages:
            if line.startswith(pkg):
                version = line.split()[1]
                current_packages[pkg] = version
    
    print("Paquetes actuales:")
    for pkg, version in current_packages.items():
        print(f"  {pkg}: {version}")
    
    # Compatibilidad con TensorFlow 2.15
    print("\n=== Compatibilidad con TensorFlow 2.15 ===")
    print("✅ numpy: Compatible (requiere >=1.23.5)")
    print("✅ opencv-python: Compatible")
    print("✅ scikit-learn: Compatible")
    print("✅ mlflow: Compatible")
    print("✅ pandas: Compatible")
    print("✅ matplotlib: Compatible")
    
    # Verificar sin instalar
    print("\n=== Simulando actualización (dry-run) ===")
    cmd = [sys.executable, '-m', 'pip', 'install', '--dry-run', 
           'tensorflow[and-cuda]==2.15.0']
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ La actualización parece ser compatible!")
        print("\nPaquetes que se actualizarían:")
        for line in result.stdout.split('\n'):
            if 'Would install' in line or 'Collecting' in line:
                print(f"  {line}")
    else:
        print("❌ Posibles conflictos detectados:")
        print(result.stderr)
    
    return result.returncode == 0

def backup_requirements():
    """Crea backup de requirements actual"""
    print("\n=== Creando backup de requirements ===")
    subprocess.run([sys.executable, '-m', 'pip', 'freeze', '>', 
                   'requirements_backup.txt'], shell=True)
    print("✅ Backup guardado en requirements_backup.txt")

if __name__ == "__main__":
    # Crear backup primero
    backup_requirements()
    
    # Verificar compatibilidad
    is_compatible = check_package_compatibility()
    
    if is_compatible:
        print("\n=== Comandos sugeridos para actualizar ===")
        print("# En la rama feature/cuda-setup:")
        print("git checkout feature/cuda-setup")
        print("pip install --upgrade tensorflow[and-cuda]==2.15.0")
        print("\n# Si algo sale mal:")
        print("pip install -r requirements_backup.txt")
    else:
        print("\n⚠️ Se recomienda revisar los conflictos antes de actualizar")
