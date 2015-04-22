#!/usr/bin/env python
#coding=utf-8 
from generator import SignalGenerator,SingleToneSignalGenerator ,DualToneSignalGenerator
import pytest
import math
from Tkinter import *  
import wave
import numpy as np  



global fg
fg=SingleToneSignalGenerator()
global tb
tb=DualToneSignalGenerator()

def variance(s):
	narray=np.array(s)
	sum1=narray.sum()
	narray2=narray*narray
	sum2=narray2.sum()
	mean=sum1/len(s)
	var=sum2/len(s)-mean**2
	return var

@pytest.fixture(scope="module")  



def setUp(request):
	print("setup")
	def teardown():
		print("teardown")
	request.addfinalizer(teardown)

def testsignal(setUp):
		 fg.setsignal(1000)
		
		
def testamplitude(setUp):
		 fg.setamp(0.5)
		
		 
		
def testpath1(setUp):
		 fg.setpath1("/home/yun/gqrx.wav")

def test_setTone(setUp):
		f1=wave.open(r'/home/yun/gqrx-20150320-085746.wav','rb')
		#read the wave's format infomation,and return a tuple  
	   	params = f1.getparams()
		#get the info  
		nchannels, sampwidth, framerate, nframes = params[:4]  
		#Reads and returns nframes of audio, as a string of bytes.   
		expectedfile = f1.readframes(nframes)  
		#close the stream  
		expected_data = np.fromstring(expectedfile, dtype = np.short)
  		f1.close() 
		
		f2=wave.open(r'/home/yun/gqrx.wav','rb')
	   	params = f2.getparams()
		nchannels, sampwidth, framerate, nframes = params[:4]     
		wavefile = f2.readframes(nframes)  
		wave_data = np.fromstring(wavefile, dtype = np.short)
  		f2.close() 
		print expected_data,wave_data

		variance_deviation1=variance(wave_data)
		variance_deviation2=variance(expected_data)
		assert variance_deviation1-variance_deviation2<5

		


        


def testsignal1(setUp):
		tb.setsignal1(1000)

		
def testamplitude1(setUp):
	  	tb.setamp1(0.5)
		
def testsignal2(setUp):
		tb.setsignal2(2000)
		
def testamplitude2(setUp):
		tb.setamp2(2)
		
def testpath2(setUp):
		tb.setpath2("/home/yun/gqrx.wav")
		
def test_setTone(setUp):
		f1=wave.open(r'/home/yun/gqrx-20150320-085746.wav','rb')
		#read the wave's format infomation,and return a tuple  
	   	params = f1.getparams()
		#get the info  
		nchannels, sampwidth, framerate, nframes = params[:4]  
		#Reads and returns nframes of audio, as a string of bytes.   
		expectedfile = f1.readframes(nframes)  
		#close the stream  
		expected_data = np.fromstring(expectedfile, dtype = np.short)
  		f1.close() 
		
		f2=wave.open(r'/home/yun/gqrx.wav','rb')
	   	params = f2.getparams()
		nchannels, sampwidth, framerate, nframes = params[:4]     
		wavefile = f2.readframes(nframes)  
		wave_data = np.fromstring(wavefile, dtype = np.short)
  		f2.close() 
 

		variance_deviation1=variance(wave_data)
		variance_deviation2=variance(expected_data)
		assert variance_deviation1-variance_deviation2<5

		


