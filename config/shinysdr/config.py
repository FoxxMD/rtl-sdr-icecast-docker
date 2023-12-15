# This is a ShinySDR configuration file. For more information about what can
# be put here, read the manual section on it, available from the running
# ShinySDR server at: http://localhost:8100/manual/configuration

from shinysdr.devices import AudioDevice
from shinysdr.plugins.osmosdr import OsmoSDRDevice
from shinysdr.plugins.simulate import SimulatedDevice

# OsmoSDR generic driver; handles USRP, RTL-SDR, FunCube Dongle, HackRF, etc.
# To select a specific device, replace '' with 'rtl=0' etc.
#config.devices.add(u'osmo', OsmoSDRDevice('rtl=0'))
config.devices.add(u'osmo', OsmoSDRDevice('rtl_tcp=rtl_tcp'))

# For hardware which uses a sound-card as its ADC or appears as an
# audio device.
# config.devices.add(u'audio', AudioDevice(rx_device=''))

# Locally generated RF signals for test purposes.
config.devices.add(u'sim', SimulatedDevice())


config.features.enable('stereo');

config.serve_web(
    # These are in Twisted endpoint description syntax:
    # <http://twistedmatrix.com/documents/current/api/twisted.internet.endpoints.html#serverFromString>
    # Note: ws_endpoint must currently be 1 greater than http_endpoint; if one
    # is SSL then both must be. These restrictions will be relaxed later.
    http_endpoint='tcp:8100',
    ws_endpoint='tcp:8101',

    # A secret placed in the URL as simple access control. Does not
    # provide any real security unless using HTTPS. The default value
    # in this file has been automatically generated from 128 random bits.
    # Set to None to not use any secret.
    root_cap=None,

    # Page title / station name
    title='ShinySDR')