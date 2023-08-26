import ctypes, os
from ctypes import c_char_p, c_int, c_void_p, POINTER

class LabelMgr:
    def __init__(self, dll_path='./isat_utils.dll'):
        # 加载动态链接库
        self.dll_path = dll_path
        self.your_lib = ctypes.CDLL(dll_path)
        
        # 定义函数原型
        self.isat_write = self.your_lib.isat_write
        self.isat_write.argtypes = [c_char_p, c_char_p, c_int]
        self.isat_write.restype = c_int

        self.isat_read = self.your_lib.isat_read
        self.isat_read.argtypes = [c_char_p, POINTER(c_int)]
        self.isat_read.restype = c_void_p

        self.isat_free_buf = self.your_lib.isat_free_buf
        self.isat_free_buf.argtypes = [c_void_p]
        self.isat_free_buf.restype = None
        
        self.your_lib.isat_set_path.argtypes = [c_char_p]
        self.your_lib.isat_set_path(os.getcwd().encode('utf-8'))
    
    def write(self, file_name, data):
        result = self.isat_write(file_name.encode('utf-8'), data.encode('utf-8'), len(data))
        return result > 0
    
    def read(self, file_name):
        decrypted_len = c_int(0)
        decrypted_data_ptr = self.isat_read(file_name.encode('utf-8'), ctypes.byref(decrypted_len))
        
        if decrypted_len.value > 0:
            decrypted_data = ctypes.string_at(decrypted_data_ptr, decrypted_len.value).decode('utf-8')
            self.isat_free_buf(decrypted_data_ptr)  # 释放缓冲区
            return decrypted_data
        else:
            self.isat_free_buf(decrypted_data_ptr)  # 释放缓冲区，以防万一
            return None  # 或者你可以抛出一个异常