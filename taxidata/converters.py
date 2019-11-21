from .core.object import DataProcessor

def RAW_to_hdf(hdf_filename, RAW_path):
    processor = DataProcessor()
    processor.load(hdf = hdf_filename, RAW = RAW_path)
    processor.RAWtohdf()

def npy_to_hdf(hdf_filename, npy):
    pass
