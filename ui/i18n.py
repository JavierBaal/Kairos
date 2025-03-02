"""
Kairos Intelligence System - Internacionalización
Este módulo proporciona funciones para la internacionalización de la aplicación.
"""

import json
import os
from typing import Dict, Any

class I18n:
    """Clase para gestionar la internacionalización."""
    
    _instance = None
    _translations = {}
    _current_locale = "es"  # Idioma predeterminado
    
    @classmethod
    def get_instance(cls):
        """Obtener la instancia singleton."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def __init__(self):
        """Inicializar el sistema de internacionalización."""
        if I18n._instance is not None:
            raise Exception("Esta clase es un singleton. Usa get_instance() en su lugar.")
        
        self._load_translations()
    
    def _load_translations(self):
        """Cargar las traducciones desde los archivos JSON."""
        locales_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "locales")
        
        if not os.path.exists(locales_dir):
            os.makedirs(locales_dir)
        
        # Cargar cada archivo de traducción
        for locale in ["es", "en"]:
            locale_file = os.path.join(locales_dir, f"{locale}.json")
            
            # Si el archivo no existe, crear uno vacío
            if not os.path.exists(locale_file):
                with open(locale_file, "w", encoding="utf-8") as f:
                    json.dump({}, f, ensure_ascii=False, indent=2)
            
            # Cargar las traducciones
            try:
                with open(locale_file, "r", encoding="utf-8") as f:
                    self._translations[locale] = json.load(f)
            except Exception as e:
                print(f"Error al cargar las traducciones para {locale}: {e}")
                self._translations[locale] = {}
    
    def set_locale(self, locale: str):
        """Establecer el idioma actual."""
        if locale in self._translations:
            self._current_locale = locale
            return True
        return False
    
    def get_locale(self) -> str:
        """Obtener el idioma actual."""
        return self._current_locale
    
    def translate(self, key: str, default: str = None) -> str:
        """Traducir una clave al idioma actual."""
        if key in self._translations.get(self._current_locale, {}):
            return self._translations[self._current_locale][key]
        
        # Si no se encuentra la traducción, devolver el valor predeterminado o la clave
        return default if default is not None else key
    
    def add_translation(self, key: str, value: str, locale: str = None):
        """Añadir una traducción."""
        if locale is None:
            locale = self._current_locale
        
        if locale not in self._translations:
            self._translations[locale] = {}
        
        self._translations[locale][key] = value
        
        # Guardar las traducciones en el archivo
        self._save_translations(locale)
    
    def _save_translations(self, locale: str):
        """Guardar las traducciones en el archivo JSON."""
        locales_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "locales")
        locale_file = os.path.join(locales_dir, f"{locale}.json")
        
        try:
            with open(locale_file, "w", encoding="utf-8") as f:
                json.dump(self._translations[locale], f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error al guardar las traducciones para {locale}: {e}")