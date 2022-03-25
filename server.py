"""
Written by Lucas Jensen for BeaverHacks Spring 2022
Last updated 3/24/2022
A very basic server for playing a game locally
"""
import subprocess

PORT = 3000


def serve():
    subprocess.Popen(f"python -m http.server {PORT}")
