from setuptools import setup, find_packages

setup(
    name='companyDetails',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
        'scrapy',
        'playwright',
        'pandas',
        'cx-Oracle',
    ],
    entry_points={
        'console_scripts': [
            'run_flask_app = companyDetails.api:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
