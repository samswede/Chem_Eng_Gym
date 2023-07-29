from setuptools import setup, find_packages

setup(
    name='Chem_Eng_Gym',
    version='0.1.0',
    url='https://github.com/yourusername/Chem_Eng_Gym',
    author='Samuel Martin Andersson',
    author_email='youremail@gmail.com',
    description='Description of your package',
    packages=find_packages(where="src"),  # automatically find all packages and subpackages in 'src' directory
    package_dir={"": "src"},  # tell setuptools that packages are under 'src' directory
    install_requires=[
        'numpy>=1.21.0',
        'pandas>=1.2.5',
        # ... rest of your dependencies
    ],  # list all dependencies here
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
    ],
)
