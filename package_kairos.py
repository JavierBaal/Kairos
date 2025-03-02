#!/usr/bin/env python3
"""
Script para empaquetar Kairos como un ejecutable independiente usando PyInstaller.
Este script crea un ejecutable que no requiere que el usuario tenga Python instalado.
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

def check_pyinstaller():
    """Verifica si PyInstaller está instalado y lo instala si es necesario."""
    try:
        import PyInstaller
        print("✓ PyInstaller está instalado")
        return True
    except ImportError:
        print("✗ PyInstaller no está instalado")
        print("Instalando PyInstaller...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("✓ PyInstaller instalado correctamente")
            return True
        except subprocess.CalledProcessError:
            print("✗ Error al instalar PyInstaller")
            return False

def create_spec_file(use_langchain=True):
    """Crea un archivo .spec para PyInstaller."""
    app_name = "Kairos_LangChain" if use_langchain else "Kairos"
    main_script = "main_simple.py"  # Usamos la versión simplificada para mayor compatibilidad
    
    # Determinar los datos adicionales a incluir
    datas = [
        ("ui", "ui"),
        ("models", "models"),
        ("config", "config"),
    ]
    
    if use_langchain:
        datas.append(("langchain_prototype", "langchain_prototype"))
    
    # Convertir datas a formato de PyInstaller
    datas_str = ", ".join([f"('{src}', '{dst}')" for src, dst in datas])
    
    # Crear contenido del archivo .spec
    spec_content = f"""# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['{main_script}'],
    pathex=[],
    binaries=[],
    datas=[{datas_str}],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='{app_name}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='ui/icons/kairos.ico' if os.path.exists('ui/icons/kairos.ico') else None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='{app_name}',
)
"""
    
    # Escribir archivo .spec
    spec_file = f"{app_name}.spec"
    with open(spec_file, "w") as f:
        f.write(spec_content)
    
    print(f"✓ Archivo .spec creado: {spec_file}")
    return spec_file

def run_pyinstaller(spec_file):
    """Ejecuta PyInstaller con el archivo .spec especificado."""
    print(f"Ejecutando PyInstaller con {spec_file}...")
    try:
        subprocess.check_call([sys.executable, "-m", "PyInstaller", spec_file, "--clean"])
        print("✓ PyInstaller completado correctamente")
        return True
    except subprocess.CalledProcessError:
        print("✗ Error al ejecutar PyInstaller")
        return False

def create_installer(app_name):
    """Crea un instalador para Windows usando NSIS."""
    if platform.system() != "Windows":
        print("La creación de instaladores solo está disponible en Windows")
        return False
    
    # Verificar si NSIS está instalado
    nsis_path = shutil.which("makensis")
    if not nsis_path:
        print("✗ NSIS no está instalado o no está en el PATH")
        print("Por favor, instala NSIS desde https://nsis.sourceforge.io/Download")
        return False
    
    # Crear script NSIS
    nsis_script = f"""
; Instalador para {app_name}
!include "MUI2.nsh"

Name "{app_name}"
OutFile "{app_name}_Setup.exe"
InstallDir "$PROGRAMFILES\\{app_name}"
InstallDirRegKey HKCU "Software\\{app_name}" ""

!define MUI_ABORTWARNING
!define MUI_ICON "dist\\{app_name}\\{app_name}.exe"

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

!insertmacro MUI_LANGUAGE "Spanish"

Section "Instalar"
  SetOutPath "$INSTDIR"
  File /r "dist\\{app_name}\\*.*"
  
  CreateDirectory "$SMPROGRAMS\\{app_name}"
  CreateShortcut "$SMPROGRAMS\\{app_name}\\{app_name}.lnk" "$INSTDIR\\{app_name}.exe"
  CreateShortcut "$DESKTOP\\{app_name}.lnk" "$INSTDIR\\{app_name}.exe"
  
  WriteUninstaller "$INSTDIR\\Uninstall.exe"
  WriteRegStr HKCU "Software\\{app_name}" "" $INSTDIR
  WriteRegStr HKCU "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{app_name}" "DisplayName" "{app_name}"
  WriteRegStr HKCU "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{app_name}" "UninstallString" "$INSTDIR\\Uninstall.exe"
SectionEnd

Section "Uninstall"
  RMDir /r "$SMPROGRAMS\\{app_name}"
  Delete "$DESKTOP\\{app_name}.lnk"
  
  RMDir /r "$INSTDIR"
  
  DeleteRegKey HKCU "Software\\{app_name}"
  DeleteRegKey HKCU "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{app_name}"
SectionEnd
"""
    
    # Escribir script NSIS
    nsis_file = f"{app_name}_installer.nsi"
    with open(nsis_file, "w") as f:
        f.write(nsis_script)
    
    # Ejecutar NSIS
    print(f"Creando instalador con NSIS...")
    try:
        subprocess.check_call(["makensis", nsis_file])
        print(f"✓ Instalador creado: {app_name}_Setup.exe")
        return True
    except subprocess.CalledProcessError:
        print("✗ Error al crear el instalador")
        return False

def create_portable_version(app_name):
    """Crea una versión portable de la aplicación."""
    dist_dir = Path(f"dist/{app_name}")
    portable_dir = Path(f"portable/{app_name}")
    
    # Crear directorio portable
    portable_dir.mkdir(parents=True, exist_ok=True)
    
    # Copiar archivos
    print(f"Creando versión portable en {portable_dir}...")
    try:
        # Copiar todos los archivos de dist a portable
        for item in dist_dir.glob("**/*"):
            if item.is_file():
                relative_path = item.relative_to(dist_dir)
                target_path = portable_dir / relative_path
                target_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(item, target_path)
        
        # Crear archivo README.txt
        with open(portable_dir / "README.txt", "w") as f:
            f.write(f"""
{app_name} - Versión Portable

Esta es una versión portable de {app_name} que no requiere instalación.
Para ejecutar la aplicación, simplemente haz doble clic en {app_name}.exe.

Nota: No muevas ni elimines ningún archivo o carpeta dentro de este directorio,
ya que son necesarios para el funcionamiento de la aplicación.
""")
        
        # Crear archivo batch para ejecutar la aplicación
        with open(portable_dir / f"Ejecutar_{app_name}.bat", "w") as f:
            f.write(f"""@echo off
echo Iniciando {app_name}...
start {app_name}.exe
""")
        
        print(f"✓ Versión portable creada en {portable_dir}")
        
        # Crear archivo ZIP
        zip_file = f"{app_name}_Portable.zip"
        shutil.make_archive(app_name + "_Portable", "zip", "portable")
        print(f"✓ Archivo ZIP creado: {zip_file}")
        
        return True
    except Exception as e:
        print(f"✗ Error al crear la versión portable: {str(e)}")
        return False

def main():
    """Función principal."""
    print("=== Empaquetador de Kairos ===")
    
    # Verificar PyInstaller
    if not check_pyinstaller():
        print("No se puede continuar sin PyInstaller")
        return
    
    # Preguntar qué versión empaquetar
    print("\n¿Qué versión de Kairos deseas empaquetar?")
    print("1. Kairos con LangChain (recomendado)")
    print("2. Kairos básico (sin LangChain)")
    
    choice = input("Ingresa el número de tu elección (1-2): ")
    use_langchain = choice == "1"
    
    app_name = "Kairos_LangChain" if use_langchain else "Kairos"
    
    # Crear archivo .spec
    spec_file = create_spec_file(use_langchain)
    
    # Ejecutar PyInstaller
    if not run_pyinstaller(spec_file):
        print("No se puede continuar debido a errores en PyInstaller")
        return
    
    # Preguntar qué tipo de distribución crear
    print("\n¿Qué tipo de distribución deseas crear?")
    print("1. Instalador para Windows")
    print("2. Versión portable (ZIP)")
    print("3. Ambos")
    
    dist_choice = input("Ingresa el número de tu elección (1-3): ")
    
    if dist_choice in ["1", "3"]:
        create_installer(app_name)
    
    if dist_choice in ["2", "3"]:
        create_portable_version(app_name)
    
    print("\n=== Proceso de empaquetado completado ===")
    print(f"Los archivos generados se encuentran en:")
    print(f"- Ejecutable: dist/{app_name}")
    
    if dist_choice in ["1", "3"]:
        print(f"- Instalador: {app_name}_Setup.exe")
    
    if dist_choice in ["2", "3"]:
        print(f"- Versión portable: {app_name}_Portable.zip")

if __name__ == "__main__":
    main()
