#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Dictado Español — Servidor HTTP simplificado
==============================================
Inicia un servidor HTTP, detecta la IP local y muestra un código QR
en la terminal para acceder desde iPad sin instalar nada.

Uso:
    python server.py [puerto]

Por defecto usa el puerto 8080.
"""

import socket
import sys
import os
import io
from http.server import HTTPServer, SimpleHTTPRequestHandler

# Fix encoding for Windows console (GBK can't handle Spanish chars)
if hasattr(sys.stdout, 'buffer'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'buffer'):
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8080


def get_local_ip():
    """Obtiene la IP local en la red LAN (no 127.0.0.1)."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Conectamos a una IP externa (no envía datos reales)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip


def show_qr_ascii(url):
    """Muestra un código QR como arte ASCII en la terminal."""
    try:
        import qrcode
        qr = qrcode.QRCode(border=2, box_size=1)
        qr.add_data(url)
        qr.make(fit=True)
        qr.print_ascii(invert=True)
    except ImportError:
        print('\n  [!] Instala qrcode para ver el QR: pip install qrcode[pil]\n')
        print(f'  Escanea este texto como QR en: https://qr-code.io/')
        print(f'  O simplemente abre la URL en Safari.\n')


def main():
    # Cambiar al directorio del script para servir index.html
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    ip = get_local_ip()
    url = f'http://{ip}:{PORT}'

    print()
    print('=' * 60)
    print('  Dictado Español — 西班牙语语音听写')
    print('=' * 60)
    print()
    print(f'  [PC]  URL local:  http://localhost:{PORT}')
    print(f'  [iPad] URL iPad:   {url}')
    print()
    print('  Escanea el codigo QR con la camara del iPad:')
    print()
    show_qr_ascii(url)
    print('  [*] Asegurate de que el iPad y este PC esten en la misma WiFi.')
    print('  [*] Si el microfono no funciona, revisa:')
    print('     Ajustes -> Safari -> Microfono -> Permitir')
    print()
    print('  Pulsa Ctrl+C para detener el servidor.')
    print('=' * 60)
    print()

    # Iniciar servidor
    handler = SimpleHTTPRequestHandler
    # Suprimir logs de peticiones para una salida más limpia
    import logging
    logging.getLogger('http.server').setLevel(logging.WARNING)

    with HTTPServer(('0.0.0.0', PORT), handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print('\n\n  Servidor detenido. Hasta luego!\n')


if __name__ == '__main__':
    main()
