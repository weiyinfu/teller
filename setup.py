from setuptools import setup, find_packages

setup(
    name="teller",
    version="1.0",
    package_data={
        "": ["res/*"]
    },
    packages=find_packages(),
    install_requires=['requests', 'flask', 'Pillow'],
    zip_safe=False,
    entry_points={
        'console_scripts': {
            'tell=teller.client:main',
            'telld=teller.server:main',
        }
    }
)
