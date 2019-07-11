from setuptools import find_packages, setup

setup(
    name='flagwaver',
    version='1.0.0',
    python_requires='>=3',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'flask_socketio',
        'pyserial',
        'numpy',
        'matplotlib',
        'requests',

    ],
)