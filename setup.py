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
        'runcible>=0.0.6',
        'VyattaConfParser>=0.5.1'

    ],
    long_description=open('README.md').read(),
    # This is what Runcible looks at to decide if this is a driver candidate or not
    entry_points={'runcible.drivers': 'vyos = runcible_vyos.driver:VyosDriver'}
)
