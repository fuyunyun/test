#!/usr/bin/env python
##################################################

from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.wxgui import fftsink2
from gnuradio.wxgui import scopesink2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
from timer import StoppableThread
import wx
import time
import threading 
import os
import wave
import pylab as pl
import numpy as np
import signal


class SignalGenerator(grc_wxgui.top_block_gui):
	def __init__(self):
		self.path=""
		self.DEVICE_FILE=0
		self.DEVICE_USRP=0
		grc_wxgui.top_block_gui.__init__(self, title="Top Block")
		_icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
                self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

	################filepath##################	
 	def setDevice(self,path):
		self.path=path
		if os.path.exists(os.path.dirname(path)):
			pass
		else:
			raise ValueError,"illeage path"
	#################wavefile,audiofile...############################
	def setDeviceType(self,Type):
		self.type=Type
		

	def Run(self, start=True, max_nouts=0):
		"""
		Setup the wx gui elements.
		Start the gr top block.
		Block with the wx main loop.
		"""
		#blocking main loop
                self.Start(start, max_nouts)
		self._app.MainLoop()
	def RunFor(self,seconds):
		self.seconds=seconds
		self._app.MainLoop()
		time.sleep(seconds)
		self._quit()
        def Wait(self):
		self._app.MainLoop()
	def getsecond(self):
		return self.seconds
	def setsecond(self,seconds):
		if second<0:
			raise ValueError,"illeage value"		


class SingleToneSignalGenerator(SignalGenerator):
	def __init__(self):
		SignalGenerator.__init__(self)
		self.samp_rate = samp_rate = 1000000
		self.signal=0
		self.amp=0
		self.path=""
	def setTone(self,freq,amplitude):
		self.signal=freq
		self.amp=amplitude
		self.analog_sig_source_x_0 = analog.sig_source_c(self.samp_rate, analog.GR_COS_WAVE, self.signal, self.amp, 0)
	        ##################################################
       	        # Variables
       	        ##################################################
     	        self.samp = samp = 192000
    	        self.rational_samp = rational_samp = 48000
              	self.rational_resampler_xxx_0 = filter.rational_resampler_fff(
          	        interpolation=samp,
                        decimation=rational_samp,
                        taps=None,
                        fractional_bw=None,
                )
        	self.blocks_wavfile_sink_0 = blocks.wavfile_sink(self.path, 1, rational_samp, 16)
        	self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp,True)
      		self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
      		self.blocks_complex_to_real_0 = blocks.complex_to_real(1)
       		self.analog_sig_source_x_2 = analog.sig_source_c(samp, analog.GR_COS_WAVE, samp/2, 1, 0)
       		 ##################################################
        		# Connections
      		  ##################################################
       		self.connect((self.analog_sig_source_x_2, 0), (self.blocks_multiply_xx_0, 1))
        	self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 0))
       	 	self.connect((self.blocks_throttle_0, 0), (self.blocks_complex_to_real_0, 0))
        	self.connect((self.blocks_complex_to_real_0, 0), (self.rational_resampler_xxx_0, 0))
        	self.connect((self.rational_resampler_xxx_0, 0), (self.blocks_wavfile_sink_0, 0))
        	self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_throttle_0, 0))

	def getsignal(self):
		return self.freq
	def setsignal(self,freq):
		if freq<10:
			raise ValueError,"illeage value"
		elif freq>1000000000:
			raise ValueError,"illeage value"
	def getamp(self):
		return self.amp
	def setamp(self,amplitude):
		if amplitude<0:
			raise ValueError,"illeage value"
	def getpath1(self):
		return self.path
	def setpath1(self,path):
		if os.path.exists(os.path.dirname(path)):
			pass
		else:
			raise ValueError,"illeage path"	
		
	


class DualToneSignalGenerator(SignalGenerator):
	def __init__(self):
		SignalGenerator.__init__(self)
		self.samp_rate = samp_rate = 1000000
		self.signal1=0
		self.signal2=0
		self.amp1=0
		self.amp2=0
		self.path=""
	def setTone(self,freq1,freq2,amplitude1,amplitude2):
		self.signal1=freq1
		self.signal2=freq2
		self.amp1=amplitude1		
		self.amp2=amplitude2
		self.analog_sig_source_x_0 = analog.sig_source_c(self.samp_rate, analog.GR_COS_WAVE, self.signal1, self.amp1, 0)
                self.analog_sig_source_x_1 = analog.sig_source_c(self.samp_rate, analog.GR_COS_WAVE, self.signal2, self.amp2, 0)
		
	        ##################################################
       	        # Variables
       	        ##################################################
       	 	self.samp_rate = samp_rate = 1000000
        	self.samp = samp = 192000
        	self.rational_samp = rational_samp = 48000
  	        ##################################################
  	        # Blocks
  	        ##################################################
  	        self.wxgui_scopesink2_0 = scopesink2.scope_sink_c(
         		self.GetWin(),
        	 	title="Scope Plot",
        		sample_rate=samp_rate,
        		v_scale=0,
        		v_offset=0,
        		t_scale=0,
        		ac_couple=False,
        		xy_mode=False,
        		num_inputs=1,
        		trig_mode=wxgui.TRIG_MODE_AUTO,
        		y_axis_label="Counts",
      		  )
      	        self.Add(self.wxgui_scopesink2_0.win)
  	        self.wxgui_fftsink2_0 = fftsink2.fft_sink_f(
        		self.GetWin(),
        		baseband_freq=0,
        		y_per_div=10,
        		y_divs=10,
        		ref_level=0,
        		ref_scale=2.0,
        		sample_rate=rational_samp,
        		fft_size=1024,
        		fft_rate=15,
        		average=False,
        		avg_alpha=None,
        		title="FFT Plot",
    	    		peak_hold=False,
   	        	)
       	      	self.Add(self.wxgui_fftsink2_0.win)
              	self.rational_resampler_xxx_0 = filter.rational_resampler_fff(
          	        interpolation=samp,
                        decimation=rational_samp,
                        taps=None,
                        fractional_bw=None,
     		   )
        	self.blocks_wavfile_sink_0 = blocks.wavfile_sink(self.path, 1, rational_samp, 16)
        	self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp,True)
      		self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
      		self.blocks_complex_to_real_0 = blocks.complex_to_real(1)
       		self.blocks_add_xx_0 = blocks.add_vcc(1)
       		self.analog_sig_source_x_2 = analog.sig_source_c(samp, analog.GR_COS_WAVE, samp/2, 1, 0)
       		 ##################################################
        		# Connections
      		 ##################################################
       		self.connect((self.analog_sig_source_x_1, 0), (self.blocks_add_xx_0, 1))
        	self.connect((self.analog_sig_source_x_0, 0), (self.blocks_add_xx_0, 0))
       		self.connect((self.analog_sig_source_x_2, 0), (self.blocks_multiply_xx_0, 1))
        	self.connect((self.blocks_add_xx_0, 0), (self.blocks_multiply_xx_0, 0))
       	 	self.connect((self.blocks_throttle_0, 0), (self.blocks_complex_to_real_0, 0))
        	self.connect((self.blocks_complex_to_real_0, 0), (self.rational_resampler_xxx_0, 0))
        	self.connect((self.rational_resampler_xxx_0, 0), (self.blocks_wavfile_sink_0, 0))
        	self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_throttle_0, 0))
        	self.connect((self.rational_resampler_xxx_0, 0), (self.wxgui_fftsink2_0, 0))
        	self.connect((self.blocks_add_xx_0, 0), (self.wxgui_scopesink2_0, 0))

	def getsignal1(self):
		return self.signal1
	def getsignal2(self):
		return self.signal2
	def getamp1(self):
		return self.amp1
	def getamp2(self):
		return self.amp2
	def getpath2(self):
		return self.path
	def setsignal1(self,freq1):
		if freq1<10:
			raise ValueError,"illeage value"
		elif freq1>1000000000:
			raise ValueError,"illeage value"	
	def setsignal2(self,freq2):
		if freq2<10:
			raise ValueError,"illeage value"
		elif freq2>1000000000:
			raise ValueError,"illeage value"
	def setamp1(self,amplitude1):
		if amplitude1<0:
			raise ValueError,"illeage value"
	def setamp2(self,amplitude2):
		if amplitude2<0:
			raise ValueError,"illeage value"
	def setpath2(self,path):
		if os.path.exists(os.path.dirname(path)):
			pass
		else:
			raise ValueError,"illeage path"

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    fg1 = DualToneSignalGenerator()

    #def my_generator():
    fg1.setDevice("/home/yun/gqrx.wav")
    fg1.setTone(2500,2000,2,0.5)     	
    fg1.Start(True)
    time.sleep(5)
    fg1.stop()


    #t=threading.Thread(target=my_generator)
    #t.setDaemon(True)
    #t.start()
    #start_time=time.time()
    #while True:      
	#print "susccess"
	#print time.time()   
	#if  int(time.time()-start_time)>=2:       
         	#print('Warning: Timeout!!'*2)
		
		
		#t=StoppableThread()
		#t.stop()
		#os.kill(os.getpid(), signal.SIGKILL) 
		



