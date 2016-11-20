#!/usr/bin/env python

from distutils.core import setup

setup(name='Leap',
      version='0.1',
      description='Demo for 3D CAD',
      author='K. Tyagi, P. Paruchuri',
      author_email='kunaltyagi@iitb.ac.in',
      url='https://www.example.com',
      package_dir = {'': 'src'}
      packages=['Leap.ogl', 'Leap.leap', 'Leap'],
     )
