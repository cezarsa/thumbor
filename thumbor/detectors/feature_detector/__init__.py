#!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/globocom/thumbor/wiki

# Licensed under the MIT license: 
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 globo.com timehome@corp.globo.com

import cv

from thumbor.detectors import BaseDetector
from thumbor.point import FocalPoint


class Detector(BaseDetector):

    def detect(self, context):
        engine = context['engine']
        sz = engine.size
        image = cv.CreateImageHeader(sz, cv.IPL_DEPTH_8U, 3)
        cv.SetData(image, engine.get_image_data())

        gray_image = cv.CreateImage(engine.size, 8, 1);
        convert_mode = getattr(cv, 'CV_%s2GRAY' % engine.get_image_mode())
        cv.CvtColor(image, gray_image, convert_mode)
        image = gray_image
        rows = sz[0]
        cols = sz[1]

        eig_image = cv.CreateMat(rows, cols, cv.CV_32FC1)
        temp_image = cv.CreateMat(rows, cols, cv.CV_32FC1)
        points = cv.GoodFeaturesToTrack(image, eig_image, temp_image, 20, 0.04, 1.0, useHarris = False)

        if points:
            for x, y in points:
                context['focal_points'].append(FocalPoint(x, y, 1))
        else:
            self.next(context)
