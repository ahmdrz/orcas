from setuptools import setup

setup(
    name="orcas",
    version="0.0.1",
    description="Classify the images in your photo album into suitable destinations.",
    url="http://github.com/ahmdrz/orcas",
    author="Ahmadreza Zibaei",
    author_email="ahmadrezazibaei@hotmail.com",
    license='MIT',
    packages=["orcas"],
    entry_points={
        'console_scripts': [
            'orcas=orcas.cli:main'
        ]
    },
    install_requires=[
        'dlib',
        'scipy',
        'numpy'
    ],
    package_dir={'orcas': 'orcas'},
    package_data={
        'orcas': ['data/*.dat']
    },
    include_package_data=True,
    zip_safe=False
)
