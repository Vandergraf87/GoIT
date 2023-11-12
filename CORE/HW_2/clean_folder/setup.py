from setuptools import setup, find_packages

setup(
    name='clean_folder',
    version='0.0.2',
    description='cleaning up my closet, good and noice',
    url='https://github.com/Vandergraf87/GoIT',
    author='Dmytro Komarov',
    author_email='komarov.dmytro@gmail.com',
    license='MIT',
    packages=find_packages(),
    entry_points={"console_scripts":["clean-folder = clean_folder.clean:main"]},
    #install_requires=["numpy", "Pillow",],
)
