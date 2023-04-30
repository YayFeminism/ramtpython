import ctypes
import sys
import os
from ctypes import wintypes

import security_dispatcher
from ctypes_structures import STARTUPINFOA, PROCESS_INFORMATIONA  # Добавьте импорт

urlmon = ctypes.windll.urlmon
kernel32 = ctypes.windll.kernel32

# Оригинальные функции
_original_URLDownloadToFile = urlmon.URLDownloadToFileW
_original_CreateProcessA = kernel32.CreateProcessA

# Создаем псевдонимы для оригинальных функций
OriginalURLDownloadToFileW = urlmon.URLDownloadToFileW
OriginalCreateProcessA = kernel32.CreateProcessA

# Типы аргументов и возвращаемого значения для URLDownloadToFile
urlmon.URLDownloadToFileW.argtypes = (
    wintypes.LPVOID,
    wintypes.LPCWSTR,
    wintypes.LPCWSTR,
    wintypes.DWORD,
    wintypes.LPVOID
)
urlmon.URLDownloadToFileW.restype = ctypes.HRESULT

# Типы аргументов и возвращаемого значения для CreateProcessA
kernel32.CreateProcessA.argtypes = (
    wintypes.LPCSTR,
    wintypes.LPSTR,
    wintypes.LPVOID,
    wintypes.LPVOID,
    wintypes.BOOL,
    wintypes.DWORD,
    wintypes.LPVOID,
    wintypes.LPCSTR,
    ctypes.POINTER(STARTUPINFOA),  # Замените ctypes.POINTER(ctypes.c_byte) на ctypes.POINTER(STARTUPINFOA)
    ctypes.POINTER(PROCESS_INFORMATIONA)  # Замените ctypes.POINTER(ctypes.c_byte) на ctypes.POINTER(PROCESS_INFORMATIONA)
)

kernel32.CreateProcessA.restype = wintypes.BOOL

# Функции-перехватчики
def _hooked_URLDownloadToFile(pCaller, szURL, szFileName, dwReserved, lpfnCB):
    print(f"_hooked_URLDownloadToFile called with URL {szURL} and FileName {szFileName}")
    if security_dispatcher.check_URLDownloadToFile(szURL, szFileName):
        result = _original_URLDownloadToFile(pCaller, szURL, szFileName, dwReserved, lpfnCB)
    else:
        result = 0x800C0008  # INET_E_DOWNLOAD_FAILURE
    return result

def _hooked_CreateProcessA(lpApplicationName, lpCommandLine, lpProcessAttributes, lpThreadAttributes,
                           bInheritHandles, dwCreationFlags, lpEnvironment, lpCurrentDirectory,
                           lpStartupInfo, lpProcessInformation):
    print(f"_hooked_CreateProcessA called with ApplicationName {lpApplicationName} and CommandLine {lpCommandLine}")
    if security_dispatcher.check_CreateProcessA(lpApplicationName, lpCommandLine):
        result = _original_CreateProcessA(lpApplicationName, lpCommandLine, lpProcessAttributes,
                                          lpThreadAttributes, bInheritHandles, dwCreationFlags,
                                          lpEnvironment, lpCurrentDirectory, lpStartupInfo,
                                          lpProcessInformation)
    else:
        result = False
    return result

# Функции для активации и деактивации перехватчиков
def initialize():
    urlmon.URLDownloadToFileW = _hooked_URLDownloadToFile
    kernel32.CreateProcessA = _hooked_CreateProcessA

def shutdown():
    urlmon.URLDownloadToFileW = _original_URLDownloadToFile
    kernel32.CreateProcessA = _original_CreateProcessA
