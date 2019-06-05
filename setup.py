import setuptools

setuptools.setup(
    name='runcible_vyos_driver',
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    author='Grayson Head',
    author_email='grayson@graysonhead.net',
    packages=setuptools.find_packages(),
    license='GPL V3',
    install_requires=[
        'runcible>=0.0.4'
    ],
    long_description=open('README.md').read(),
    entry_points={'runcible.drivers': 'vyos = runcible_vyos.driver:VyosDriver'}
)