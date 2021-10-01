import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
        name='alacritty-circadian',
        version='0.9.8',
        author='Leonardo \"drd\" Idone',
        author_email='idone.leonardo@gmail.com',
        description='Alacritty time/sun based theme switch daemon',
        long_description=long_description,
        long_description_content_type='text/markdown',
        url='https://github.com/Dr-Dd/alacritty-circadian',
        license_files=('LICENSE'),
        classifiers=[
            "Programming Language :: Python :: 3 :: Only",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "License :: OSI Approved :: Apache Software License",
            "Operating System :: Unix",
            "Operating System :: MacOS",
            "Operating System :: Microsoft :: Windows"
            ],
        package_dir={"": "src"},
        packages=setuptools.find_packages(where="src"),
        python_requires=">=3.6",
        install_requires=[ 
            "ruamel.yaml",
            "astral",
            "tzlocal"
        ],
        entry_points={
            'console_scripts': [
                'alacritty-circadian = alacritty_circadian.alacritty_circadian:main',
            ],
        },
        include_package_data=True
)

