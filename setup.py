from setuptools import setup, find_packages

setup(
    name="bitstream_generator",
    version='0.0.1',
    author='FANGS',
    description='Utility to quickly make a bitstream containing certain features',
    package_dir={'bitstream_generator':'bitstream_generator'},
    packages=find_packages(),
    include_package_data=True,
    install_requires=["dearpygui","setuptools-git"],
    entry_points={
        'console_scrupts': ['main=bitstream_generator:main']
        }
)
