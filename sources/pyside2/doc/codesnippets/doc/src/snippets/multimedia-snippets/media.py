****************************************************************************
**
** Copyright (C) 2019 The Qt Company Ltd.
** Contact: http//www.qt.io/licensing/
**
** This file is part of the Qt for Python examples of the Qt Toolkit.
**
** $QT_BEGIN_LICENSE:BSD$
** You may use this file under the terms of the BSD license as follows:
**
** "Redistribution and use in source and binary forms, with or without
** modification, are permitted provided that the following conditions are
** met:
**   * Redistributions of source code must retain the above copyright
**     notice, this list of conditions and the following disclaimer.
**   * Redistributions in binary form must reproduce the above copyright
**     notice, this list of conditions and the following disclaimer in
**     the documentation and/or other materials provided with the
**     distribution.
**   * Neither the name of The Qt Company Ltd nor the names of its
**     contributors may be used to endorse or promote products derived
**     from this software without specific prior written permission.
**
**
** THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
** "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
** LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
** A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
** OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
** SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
** LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
** DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
** THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
** (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
** OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
**
** $QT_END_LICENSE$
**
****************************************************************************/

import sys
from PySide2.QtMultimedia import (QMediaPlayerControl, QAudioEncoderSettings,
                                  QVideoEncoderSettings, QImageEncoderSettings,
                                  QMediaPlayer, QRadioTuner, QAudioEncoderSettings,
                                  QVideoProbe, QAudioProbe, QAudioRecorder,
                                  QCamera)
from PySide2.QtCore import (QObject, QUrl, QByteArray, QIODevice, QBuffer)
from PySide2.QtMultimediaWidgets import (QVideoWidget, QCameraViewfinder)
from PySide2.QtGui import QImage

class MediaExample(QObject):
    def __init__(self):
        QObject.__init__(self)

        self.yourRadioStationFrequency = 11

    def MediaControl(self):
        //! [Request control]
        self.control = QMediaPlayerControl()
        //didnt ge tthe rest
        self.qobject_cast = QMediaPlayerControl()
        self.qobject_cast.requestControl("org.qt-project.qt.mediaplayercontrol/5.0")
        //! [Request control]

        //! [Request control templated]
        self.control = QMediaPlayerControl()
        self.mediaService.requestControl()
        //! [Request control templated]

    def EncoderSettings(self):
        //! [Audio encoder settings]
        self.audioSettings = QAudioEncoderSettings()
        self.audioSettings.setCodec("audio/mpeg")
        self.audioSettings.setChannelCount(2)

        self.recorder.setAudioSettings(self.audioSettings)
        //! [Audio encoder settings]

        //! [Video encoder settings]
        self.videoSettings = QVideoEncoderSettings()
        self.videoSettings.setCodec("video/mpeg2")
        self.videoSettings.setResolution(640, 480)

        self.recorder.setVideoSettings(self.videoSettings)
        //! [Video encoder settings]

    def ImageEncoderSettings(self):
        //! [Image encoder settings]
        self.imageSettings = QImageEncoderSettings()
        self.imageSettings.setCodec("image/jpeg")
        self.imageSettings.setResolution(1600, 1200)

        self.imageCapture.setEncondingSettings(self.imageSettings)
        //! [Image encoder settings]

    def MediaPlayer(self):
        //! [Player]
        self.player = QMediaPlayer()
        self.player.positionChange.connect(self.positionChange)
        self.player.setMedia(QUrl.fromLocalFile("/Users/me/Music/coolsong.mp3"))
        self.player.setVolume(50)
        self.player.play()
        //! [Player]

        //! [Local playback]
        self.player = QMediaPlayer()
        # ...
        self.player.setMedia(QUrl.fromLocalFile("/Users/me/Music/coolsong.mp3"))
        self.player.setVolume(50)
        self.player.play()
        //! [Local playback]

        //! [Audio playlist]
        self.player = QMediaPlayer()

        self.playlist = QMediaPlayer(self.player)
        self.playlist.addMedia(QUrl("http//example.com/myfile1.mp3"))
        self.playlist.addMedia(QUrl("http//example.com/myfile2.mp3"))
        #...
        self.playlist.setCurrentIndex(1)
        self.player()
        //! [Audio playlist]

        //! [Movie playlist]
        self.playlist = QMediaPlayList()
        self.playlist.addMedia(QUrl("http//example.com/movie1.mp4"))
        self.playlist.addMedia(QUrl("http//example.com/movie2.mp4"))
        self.playlist.addMedia(QUrl("http//example.com/movie3.mp4"))
        self.playlist.setCurrentIndex(1)

        self.player = QMediaPlayer()
        self.player.setPlayList(self.playlist)

        self.videoWidget = QVideoWidget()
        self.player.setVideoOutput(self.videoWidget)
        self.videoWidget.show()

        self.player.play()
        //! [Movie playlist]

        //! [Pipeline]
        self.player = QMediaPlayer()
        self.player.setMedia(QUrl("gst-pipeline: videotestsrc ! autovideosink"))
        self.player.play()
        //! [Pipeline]

        //! [Pipeline appsrc]
        self.img = QImage("images/qt-logo.png")
        self.img.convertToFormat(QImage.Format_ARGB32)
        ba = QByteArray(self.img.bits(), self.img.sizeInBytes())
        self.buffer = QBuffer(ba)
        self.buffer.open(QIODevice.ReadOnly)
        self.player = QMediaPlayer()
        self.player.setMedia(QUrl("gst-pipeline: appsrc blocksize=4294967295 ! \
        video/x-raw,format=BGRx,framerate=30/1,width=200,height=147 ! \
        coloreffects preset=heat ! videoconvert ! video/x-raw,format=I420 ! jpegenc ! rtpjpegpay ! \
        udpsink host=127.0.0.1 port=5000"), buffer)
        self.player.play()

        self.receiver = QMediaPlayer()
        self.videoWidget = QVideoWidget()
        self.receiver.setVideoOutput(self.videoWidget)
        self.receiver.setMedia(QUrl("gst-pipeline: udpsrc port=5000 ! \
        application/x-rtp,encoding-name=JPEG,payload=26 ! rtpjpegdepay ! jpegdec ! \
        xvimagesink name=qtvideosink"))
        receiver.play()
        # Content will be shown in this widget.
        videoWidget.show()
        //! [Pipeline appsrc]

    def MediaRecorder(self):
        //! [Media recorder]
        self.recorder = QMediaRecorder(self.camera)

        self.audioSettings = QAudioEncoderSettings()
        self.audioSettings.setCodec("audio/amr")
        self.audioSettings.setQuality(self.audioSettings.HighQuality)

        self.recorder.setAudioSettings(audioSettings)

        self.recorder.setOutputLocation(QUrl.fromLocalFile(fileName))
        self.recorder.record()
        //! [Media recorder]

    def AudioRecorder(self):
        //! [Audio recorder]
        self.audioRecorder = QAudioRecorder()

        self.audioSettings = QAudioEncoderSettings()
        self.audioSettings.setCodec("audio/amr")
        self.audioSettings.setQuality(self.audioSettings.HighQuality)

        self.audioRecorder.setEncodingSettings(audioSettings)

        self.audioRecorder.setOutputLocation(QUrl.fromLocalFile("test.amr"))
        self.audioRecorder.record()
        //! [Audio recorder]

        //! [Audio recorder inputs]
        self.inputs = audioRecorder.audioInputs()
        self.selectedInput = audioRecorder.defaultAudioInputself()

        for audioInput in self.inputs:
            self.description = audioRecorder.audioInputDescription(audioInput)
            // show descriptions to user and allow selection
            self.selectedInput = audioInput

        self.audioRecorder.setAudioInput(selectedInput)
        //! [Audio recorder inputs]

    def RadioTuna(self):
        //! [Radio tuner]
        self.radio = QRadioTuner()
        self.radio.frequencyChange().connect(freqChanged())
        if self.radio.isBandSupported(self.radio.FM):
            self.radio.setBand(self.radio.FM)
            self.radio.setFrequency(self.yourRadioStationFrequency)
            self.radio.setVolume(100)
            self.radio.start()
        //! [Radio tuner]

        //! [Radio data setup]
        self.radio = QRadioTuner()
        self.radioData = self.radio.radioData()
        //! [Radio data setup]

    def AudioProbe(self):
        //! [Audio probe]
        self.audioRecorder = QAudioRecorder()

        self.audioSettings = QAudioEncoderSettings()
        self.audioSettings.setCodec("audio/amr")
        self.audioSettings.setQuality(self.audioSettings.HighQuality)

        self.audioRecorder.setEncodingSettings(self.audioSettings)

        self.audioRecorder.setOutputLocation(QUrl.fromLocalFile("test.amr"))

        self.audioProbe = QAudioProbe()
        if self.audioProbe.setSource(self.audioRecorder):
             Probing succeeded, self.audioProbe.isValid() should be true.
            self.audioProbe.audioBufferProbed[QAudioBuffer].connect(calculateLevel(QAudioBuffer))

        self.audioRecorder.record()
         # Now audio buffers being recorded should be signaled
         # by the probe, so we can do things like calculating the
         # audio power level, or performing a frequency transform
        //! [Audio probe]

    def VideoProbe(self):
        //! [Video probe]
        self.camera = QCamera()
        self.viewfinder = QCameraViewfinder()
        self.camera.setViewfinder(self.viewfinder)

        self.camera.setCaptureMode(self.camera.CaptureVideo)

        self.videoProbe = QVideoProbe()

        if self.videoProbe.setSource(self.camera):
             Probing succeeded, self.videoProbe.isValid() should be true.
            self.videoProbe.videoFrameProbed[QVideoFrame].connect(detectBarcodes(QVideoFrame))

        self.camera.start()
         # Viewfinder frames should now also be emitted by
         # the video probe, even in still image capture mode.
         # Another alternative is to install the probe on a
         # QMediaRecorder connected to the camera to get the
         # recorded frames, if they are different from the
         # viewfinder frames.

        //! [Video probe]
