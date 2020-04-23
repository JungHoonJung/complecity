from setuptools import setup

setup(name='taxidata',
		version='0.2.0',
		description='Taxidata Analyzer',
		author='Junghoon Jung',
		author_email='jh.gnuaz@gamil.com',
		packages=['taxidata', 'taxidata.tdarray','taxidata.core', 'taxidata.core.lib'],
		py_modules=['taxidata.core.lib.taxipoint'],
		data_files=[('core/lib',['taxidata/core/lib/district.DAT'])],
		include_package_data=True,
		#package_data={'taxidata':['taxidata/lib/TL_SCCO_SIG_W.gml']},
		python_requires = '>=3',
		install_requires=['numpy', 'networkx', 'h5py', 'matplotlib','pyproj']

	 )
