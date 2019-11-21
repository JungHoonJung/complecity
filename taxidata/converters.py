from .core.object import DataProcessor

def RAW_to_hdf(hdf_filename, RAW_path):
    processor = DataProcessor()
    processor.load(RAW = RAW_path)
    processor.RAWtohdf(hdf_filename)

def npy_to_hdf(hdf_filename, npy):
    pass
