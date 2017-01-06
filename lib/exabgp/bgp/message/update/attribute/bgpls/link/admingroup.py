# encoding: utf-8
"""
admingroup.py

Created by Evelio Vila on 2016-12-01.
Copyright (c) 2014-2016 Exa Networks. All rights reserved.
"""

import binascii

from exabgp.dep.bitstring import BitArray

from exabgp.bgp.message.notification import Notify

from exabgp.bgp.message.update.attribute.bgpls.linkstate import LINKSTATE

@LINKSTATE.register()
class AdminGroup(object):
	TLV = 1088
	def __init__ (self, colormask):
		self.colormask = colormask

	def __repr__ (self):
		return "Admin Group mask: %s" % (self.colormask)

	@classmethod
	def unpack (cls,data,length):
		if length != 4:
			raise Notify(3,5, "Unable to decode attribute. Incorrect Size")
		else:
			b = BitArray(bytes=data)
			colormask = b.unpack('uintbe:32')
			return cls(colormask=colormask)

	def json (self,compact=None):
		return '"admin-group-mask": %s' % self.colormask