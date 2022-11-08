#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Designin Filter Taps
# Author: jachall
# GNU Radio version: 3.10.4.0

from packaging.version import Version as StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import analog
from gnuradio import blocks
from gnuradio import filter
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.qtgui import Range, GrRangeWidget
from PyQt5 import QtCore
import numpy as np



from gnuradio import qtgui

class designingFilterTaps(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Designin Filter Taps", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Designin Filter Taps")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "designingFilterTaps")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 32000
        self.lowPassFilterTaps = lowPassFilterTaps = firdes.low_pass(1.0, samp_rate, samp_rate/8,samp_rate/16, window.WIN_HAMMING, 6.76)
        self.n = n = np.arange(0, len(lowPassFilterTaps))
        self.bandpassCenterFrequency = bandpassCenterFrequency = samp_rate/4
        self.frequencyShift = frequencyShift = np.exp(2j*np.pi*(bandpassCenterFrequency/samp_rate)*n)
        self.frequency = frequency = 0
        self.boxcarFilter = boxcarFilter = np.ones(8)/8
        self.bandPassTaps = bandPassTaps = lowPassFilterTaps*frequencyShift

        ##################################################
        # Blocks
        ##################################################
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            'Sinusoid', #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0.set_fft_window_normalized(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_win)
        self._frequency_range = Range(-samp_rate/2, samp_rate/2, 1, 0, 200)
        self._frequency_win = GrRangeWidget(self._frequency_range, self.set_frequency, "Frequency Slider", "counter_slider", float, QtCore.Qt.Horizontal, "value")

        self.top_layout.addWidget(self._frequency_win)
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_fcc(1, bandPassTaps, 0, samp_rate)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.analog_fastnoise_source_x_0 = analog.fastnoise_source_f(analog.GR_GAUSSIAN, 1, 0, 8192)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_fastnoise_source_x_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.blocks_throttle_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "designingFilterTaps")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_bandpassCenterFrequency(self.samp_rate/4)
        self.set_frequencyShift(np.exp(2j*np.pi*(self.bandpassCenterFrequency/self.samp_rate)*self.n))
        self.set_lowPassFilterTaps(firdes.low_pass(1.0, self.samp_rate, self.samp_rate/8, self.samp_rate/16, window.WIN_HAMMING, 6.76))
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate)

    def get_lowPassFilterTaps(self):
        return self.lowPassFilterTaps

    def set_lowPassFilterTaps(self, lowPassFilterTaps):
        self.lowPassFilterTaps = lowPassFilterTaps
        self.set_bandPassTaps(self.lowPassFilterTaps*self.frequencyShift)
        self.set_n(np.arange(0, len(self.lowPassFilterTaps)))

    def get_n(self):
        return self.n

    def set_n(self, n):
        self.n = n
        self.set_frequencyShift(np.exp(2j*np.pi*(self.bandpassCenterFrequency/self.samp_rate)*self.n))

    def get_bandpassCenterFrequency(self):
        return self.bandpassCenterFrequency

    def set_bandpassCenterFrequency(self, bandpassCenterFrequency):
        self.bandpassCenterFrequency = bandpassCenterFrequency
        self.set_frequencyShift(np.exp(2j*np.pi*(self.bandpassCenterFrequency/self.samp_rate)*self.n))

    def get_frequencyShift(self):
        return self.frequencyShift

    def set_frequencyShift(self, frequencyShift):
        self.frequencyShift = frequencyShift
        self.set_bandPassTaps(self.lowPassFilterTaps*self.frequencyShift)

    def get_frequency(self):
        return self.frequency

    def set_frequency(self, frequency):
        self.frequency = frequency

    def get_boxcarFilter(self):
        return self.boxcarFilter

    def set_boxcarFilter(self, boxcarFilter):
        self.boxcarFilter = boxcarFilter

    def get_bandPassTaps(self):
        return self.bandPassTaps

    def set_bandPassTaps(self, bandPassTaps):
        self.bandPassTaps = bandPassTaps
        self.freq_xlating_fir_filter_xxx_0.set_taps(self.bandPassTaps)




def main(top_block_cls=designingFilterTaps, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
