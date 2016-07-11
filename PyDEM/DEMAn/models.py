'''
Created on July 1, 2016
@author: Andrew Abi-Mansour

Center for Materials Sci. & Eng.,
Merck Inc., West Point
'''

# !/usr/bin/python
# -*- coding: utf8 -*- 
# -------------------------------------------------------------------------
#
#   Python module for analyzing contact models for DEM simulations
#
# --------------------------------------------------------------------------
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.

#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.

#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

# -------------------------------------------------------------------------

import numpy as np


class Model:
	def __init__(self, **params):

		self.materials = {}

		for item in params['materials']:
			if params['materials'][item][2] == '2':
				self.materials[params['materials'][item][0]] = np.array([np.float(it) for \
					it in params['materials'][item][3:]]).mean()
			else:	
				self.materials[params['materials'][item][0]] = np.array([np.float(it) for \
					it in params['materials'][item][2:]]).mean()

		self.SS = params['SS']
		self.radius = np.array([radius[1] for radius in params['radius']])
		self.mass = np.array([4.0/3.0 * np.pi * self.radius[i]**3 * self.SS[i]['density'] for \
								i in range(len(self.SS))])

	def contactTime(self):
		pass

	def overlap(self):
		pass

	def contactForce(self):
		pass

	def normalForce(self):
		pass

	def tangForce(self):
		pass

class LinearSpring(Model):
	"""
	A class that implements the linear spring model for granular materials
	"""

	def __init__(self, **params):
		Model.__init__(self, **params)

	def springStiff(self, radius = None, yMod = None, mass = None, v0 = None):
		""" Computes the spring constant kn for 
			F = - kn * \delta
		"""
		if yMod is None:
			yMod = self.materials['youngsModulus']

		if v0 is None:
			v0 = self.materials['characteristicVelocity']

		if mass is None:
			mass = self.mass

		if radius is None:
			radius = self.radius

		return 16.0/15.0 * np.sqrt(radius) * yMod * (15.0 * mass \
			* v0 **2.0 / (16.0 * np.sqrt(radius) * yMod))**(1.0/5.0)

	def contactTime(self, mass = None, cR = None, kn = None):

		if kn is None:
			 kn = self.springStiff()

		if mass is None:
			mass = self.mass

		if cR is None:
			cR = self.materials['coefficientRestitution']

		return np.sqrt(mass * (np.pi**2.0 + np.log(cR)) / kn) 

	def normalForce(self, ):
		return - self.springStiff