from .core.object import DataProcessor

def RAW_to_hdf(hdf_filename, RAW_path, date):
    processor = DataProcessor()
    processor.load(RAW = RAW_path)
    processor.set_date(date[0],date[1],date[2])
    processor.RAWtohdf(hdf_filename)



def npy_to_hdf(hdf_filename, npy):
    pass
