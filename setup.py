from setuptools import setup, find_packages

requires = [
    'Pillow',
    'RPi.GPIO',
    'picamera',
    'pygame',
]

test_requires = [
]

setup(
    name='SpeakersCorner',
    version='0.0',
    description='',
    classifiers=[
        "Programming Language :: Python",
    ],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    tests_require=test_requires
)
