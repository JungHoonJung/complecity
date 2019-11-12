from setuptools import setup

setup(name='taxidata',
		version='0.1.7',
		description='Taxidata Analyzer',
		author='Junghoon Jung',
		author_email='jh.gnuaz@gamil.com',
		packages=['taxidata','taxidata.tdarray','taxidata.lib'],
		py_modules=['taxidata.lib.taxipoint'],
		data_files=[('lib',['taxidata/lib/district.DAT'])],
		include_package_data=True,
		#package_data={'taxidata':['taxidata/lib/TL_SCCO_SIG_W.gml']},
		setup_requires=['numpy']
	
	 )
