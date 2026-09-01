"""
Módulo de portapapeles seguro para ChronoLock.
Copia texto al portapapeles de Windows sin que aparezca en el historial
de portapapeles (Win+V), usando el formato ExcludeClipboardContentFromMonitorProcessing.
"""
import ctypes
from ctypes import wintypes

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

# Configurar tipos de retorno y argumentos
kernel32.GlobalAlloc.argtypes = [wintypes.UINT, ctypes.c_size_t]
kernel32.GlobalAlloc.restype = wintypes.HGLOBAL
kernel32.GlobalLock.argtypes = [wintypes.HGLOBAL]
kernel32.GlobalLock.restype = wintypes.LPVOID
kernel32.GlobalUnlock.argtypes = [wintypes.HGLOBAL]
kernel32.GlobalUnlock.restype = wintypes.BOOL
kernel32.GlobalFree.argtypes = [wintypes.HGLOBAL]
kernel32.GlobalFree.restype = wintypes.HGLOBAL

user32.SetClipboardData.argtypes = [wintypes.UINT, wintypes.HANDLE]
user32.SetClipboardData.restype = wintypes.HANDLE
user32.RegisterClipboardFormatW.argtypes = [wintypes.LPCWSTR]
user32.RegisterClipboardFormatW.restype = wintypes.UINT

CF_UNICODETEXT = 13
GMEM_MOVEABLE = 0x0002
GMEM_ZEROINIT = 0x0040


def secure_copy(text):
    """
    Copia texto al portapapeles SIN que aparezca en el historial de Windows.
    Usa el formato 'ExcludeClipboardContentFromMonitorProcessing' para
    indicarle a Windows que no registre esta entrada en el clipboard history.
    
    Returns True si se copió correctamente, False en caso de error.
    """
    # Registrar el formato especial de exclusión
    exclude_format = user32.RegisterClipboardFormatW(
        "ExcludeClipboardContentFromMonitorProcessing"
    )

    if not user32.OpenClipboard(0):
        return False

    try:
        user32.EmptyClipboard()

        # 1) Establecer la flag de exclusión del historial
        h_exclude = kernel32.GlobalAlloc(GMEM_MOVEABLE | GMEM_ZEROINIT, 1)
        if h_exclude:
            p_exclude = kernel32.GlobalLock(h_exclude)
            if p_exclude:
                ctypes.memmove(p_exclude, b'\x00', 1)
                kernel32.GlobalUnlock(h_exclude)
            user32.SetClipboardData(exclude_format, h_exclude)

        # 2) Establecer el texto real como CF_UNICODETEXT
        text_bytes = (text + '\0').encode('utf-16-le')
        h_mem = kernel32.GlobalAlloc(GMEM_MOVEABLE | GMEM_ZEROINIT, len(text_bytes))
        if h_mem:
            p_mem = kernel32.GlobalLock(h_mem)
            if p_mem:
                ctypes.memmove(p_mem, text_bytes, len(text_bytes))
                kernel32.GlobalUnlock(h_mem)
            user32.SetClipboardData(CF_UNICODETEXT, h_mem)

        return True
    except Exception:
        return False
    finally:
        user32.CloseClipboard()


def clear_clipboard():
    """Limpia el portapapeles de Windows."""
    if user32.OpenClipboard(0):
        user32.EmptyClipboard()
        user32.CloseClipboard()
