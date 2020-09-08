from setuptools import setup, find_packages

setup(name='taxidata',
		version='0.2.0',
		description='Taxidata Analyzer',
		author='Junghoon Jung',
		author_email='jh.gnuaz@gamil.com',
		packages=find_packages()       # ['taxidata', 'taxidata.tdarray','taxidata.core', 'taxidata.core.lib','taxidata.core.lib'],
		py_modules=['taxidata.core.lib.taxipoint'],
		data_files=[('core/lib',['taxidata/core/lib/district.DAT'])]#,('core/network/nodelink',['taxidata/core/network/nodelink/'+filename for filename in ['Seoul_Edgelist.csv','Seoul_Links.shp']])],
		include_package_data=True, # include MANIFEST.in
		#package_data={'taxidata':['taxidata/lib/TL_SCCO_SIG_W.gml']},
		python_requires = '>=3',
		install_requires=['numpy', 'networkx', 'h5py', 'matplotlib','pyproj','tqdm','geopandas']

	 )
