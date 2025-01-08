import sys
import os

libs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../libs/python"))

if libs_path not in sys.path and os.path.exists(libs_path):
    sys.path.append(libs_path)