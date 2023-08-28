from setuptools import setup

setup(name='clean_folder',
      version='0.0.1',
      packages=['clean_folder'],
      author='aftermath112',
      description='clean folder from garbage',
      entry_points={
            'console_scripts': ['clean-folder = clean_folder.clean:process']


      }
)