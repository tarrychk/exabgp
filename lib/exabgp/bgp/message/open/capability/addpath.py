# encoding: utf-8
"""
addpath.py

Created by Thomas Mangin on 2012-07-17.
Copyright (c) 2009-2013 Exa Networks. All rights reserved.
"""

from struct import pack
from exabgp.protocol.family import AFI
from exabgp.protocol.family import SAFI
from exabgp.bgp.message.open.capability import Capability
from exabgp.bgp.message.open.capability.id import CapabilityID

# ====================================================================== AddPath
#

class AddPath (Capability,dict):
	ID = CapabilityID.ADD_PATH

	string = {
		0 : 'disabled',
		1 : 'receive',
		2 : 'send',
		3 : 'send/receive',
	}

	def __init__ (self,families=[],send_receive=0):
		for afi,safi in families:
			self.add_path(afi,safi,send_receive)

	def add_path (self,afi,safi,send_receive):
		self[(afi,safi)] = send_receive

	def __str__ (self):
		return 'AddPath(' + ','.join(["%s %s %s" % (self.string[self[aafi]],xafi,xsafi) for (aafi,xafi,xsafi) in [((afi,safi),str(afi),str(safi)) for (afi,safi) in self]]) + ')'

	def extract (self):
		rs = []
		for v in self:
			if self[v]:
				rs.append(v[0].pack() +v[1].pack() + pack('!B',self[v]))
		return rs

	@staticmethod
	def unpack (capability,instance,data):
		# XXX: FIXME: should check that we have not yet seen the capability
		while data:
			afi = AFI.unpack(data[:2])
			safi = SAFI.unpack(data[2])
			sr = ord(data[3])
			instance.add_path(afi,safi,sr)
			data = data[4:]
		return instance

AddPath.register_capability()
