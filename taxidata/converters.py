from .core.object import DataProcessor

def RAW_to_hdf(hdf_filename, RAW_path, date):
    processor = DataProcessor()
    processor.load(RAW = RAW_path)
    processor.set_date(int(date[0]),int(date[1]),int(date[2]))
    processor.RAWtohdf(hdf_filename)



def npy_to_hdf(hdf_filename, npy):
    """Test.

    Parameters
    ----------
    hdf_filename : ``string``
        Description of parameter `hdf_filename`.
    npy : type
        Description of parameter `npy`.

    Returns
    -------
    type
        Description of returned object.


    # NOTE: this is making note

    ..note::
        This is also making note
    """
    pass
