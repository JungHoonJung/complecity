import pkg_resources
import os
import platform
import ctypes
import gc
import numpy as np

__all__ = ['c_ext']

#cpp header
cpp_header = """
    DCURVE_API float d_pp(float x1, float y1, float x2, float y2);
    DCURVE_API float d_ls_p(float* line_points, int line_length, float px, float py, int line_start = 0);
    DCURVE_API float d_curve_single(float* seg_points, int seg_length, float* traj_points, int traj_length, int index, int seg_index, float& prefix, int seg_start = 0);
    DCURVE_API void d_curve(float* segments, int* segment_lengths, int* segment_start_point, int total_seg_num, float* traj_points, int traj_length, int index, float* prefix, float* d_c, int thr_num = 1);
    DCURVE_API void k_segments(int* edges, int* edge_start_indices, int* degrees, int max_number, int* start_node, int n_num, float* length, float* angle, float k, float threshold, int thr_num=1);
"""


c_to_py ={
    'int'       : ctypes.c_int,
    'float'     : ctypes.c_float,
    'float&'     : ctypes.c_float,
    'double'    : ctypes.c_double,
    'float*'    : np.ctypeslib.ndpointer(dtype=np.float32),
    'int*'      : np.ctypeslib.ndpointer(dtype=np.int32),
    'double*'   : np.ctypeslib.ndpointer(dtype=np.float64),
    'void'      : None
}


def c_import(c_ext):
    if platform.system() == 'Windows':
        _cdll = ctypes.windll.LoadLibrary(pkg_resources.resource_filename(__name__,f"{c_ext}.dll"))
    elif platform.system() == 'Linux':
        _cdll = ctypes.cdll.LoadLibrary(pkg_resources.resource_filename(__name__,f"{c_ext}.so.1"))
    else:
        raise OSError("this OS is not supported.")
    return _cdll


def cdll_types(header):
    ans = {}
    for line in header.splitlines():
        if line.lstrip():
            if len(line.split("("))<2: continue
            func_name = line.split("(")[0].split()[-2:]
            #print(func_name)
            restype     = (func_name[0])
            name        = func_name[1]
            func_args   = line.split("(")[1].split(")")[0].split(",")
            argtypes    = [(func_arg.split()[0]) for func_arg in func_args]

            ans[name] = (argtypes, restype)
    return ans
                

def c_interface(_cdll, func_name, argtypes, restype = None):
    func = eval(f'_cdll.{func_name}')
    func.argtypes = argtypes
    if restype is not None:
        func.restype = restype

def interface_from_header(cdll, header, py_dict, include = None, exclude = None):
    cdll.header = header
    c_funcs = cdll_types(header)
    if exclude is None:
        exclude = []
    for f_name in c_funcs:
        if f_name in exclude: continue
        if include is not None and not f_name in include: continue
        args, res = c_funcs[f_name]
        args = [py_dict[arg] for arg in args]
        res  = py_dict[res]
        c_interface(cdll, f_name, args, res)

c_ext = c_import('d_curve')
#print(c_ext)
interface_from_header(c_ext, cpp_header, c_to_py)


"""
#   DCURVE_API float d_pp(float x1, float y1, float x2, float y2);
c_interface('d_pp', 
[
    float_,
    float_,
    float_,
    float_
],
float_
)

# DCURVE_API float d_ls_p(float* line_points, int line_length, float px, float py, int line_start = 0);
c_interface('d_ls_p', 
[
    np_float,
    int_,
    float_,
    float_,
    int_
],
float_
)

# DCURVE_API float d_curve_single(float* seg_points, int seg_length, float* traj_points, int traj_length, int index, int seg_index, float& prefix, int seg_start = 0);
c_interface('d_curve_single', 
[
    np_float,
    int_,
    np_float,
    int_,
    int_,
    int_,
    float_,
    int_
],
float_
)

# DCURVE_API void d_curve(float* segments, int* segment_lengths, int* segment_start_point, int total_seg_num, float* traj_points, int traj_length, int index, float* prefix, float* d_c, int thr_num = 1);
c_interface('d_curve', 
[
    np_float,   # float*    segments
    np_int,     # int*      segment_lengths
    np_int,     # int*      segment_start_point
    int_,       # int       total_seg_num
    np_float,   # float*    traj_points
    int_,       # int       traj_length
    int_,       # int       index
    np_float,   # float*    prefix
    np_float,   # float*    d_c
    int_        # int       thr_num = 1
]
)
"""