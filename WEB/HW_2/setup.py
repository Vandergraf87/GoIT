from setuptools import setup, find_namespace_packages

setup(name='Phoenix',
      version='0.0.1',
      description='Your personal assistant',
      url='https://github.com/AlyaVKravchenko/Phoenix',
      author='project-group-12',
      packages=find_namespace_packages(),
      license='MIT',
      entry_points={"console_scripts":["Ineedhelp = Phoenix.main:main"]},
      install_requires=[],
      include_package_data=True,
      )