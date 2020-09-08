import pkg_resources
import os
import platform
import ctypes
import gc
import numpy as np

if platform.system() == 'Windows':
    _cdll = ctypes.windll.LoadLibrary(pkg_resources.resource_filename(__name__,"d_curve.dll"))
elif platform.system() == 'Linux':
    _cdll = ctypes.cdll.LoadLibrary(pkg_resources.resource_filename(__name__,"d_curve.so.1"))
else:
    raise OSError("this OS is not supported.")

def d_curve():
    return _cdll.d_curve