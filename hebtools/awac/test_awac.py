# -*- coding: utf-8 -*-
"""
author: James Morrison
"""
import unittest
import os
import pandas as pd
from hebtools.awac import parse_wad
from hebtools.awac import parse_wap
from hebtools.awac import awac_stats

awac_folder_path = '../../awac_data'
number_of_records = 998
wad_records = 100
number_of_awac_stats = 1

# class TestParseWad(unittest.TestCase):

    # def setUp(self):
        # try:        
            # parse_wad.ParseWad(awac_folder_path + 'test_data.wad')
        # except WindowsError:
            # print "Load Wad Files failed"

    # def test_wad_dataframe(self):
        # wad_dataframe = pd.load('test_data_wad_df')
        # self.assertEqual(len(wad_dataframe),number_of_records)
        
# class TestParseWap(unittest.TestCase):

    # def setUp(self):
        # try:        
            # parse_wap.load('../../awac_data/test_data.wap')
        # except WindowsError:
            # print "Load wap Files failed"

    # def test_wap_dataframe(self):
        # wap_dataframe = pd.load('test_data_wap_df')
        # self.assertEqual(len(wap_dataframe),wad_records)

class TestAwacStats(unittest.TestCase):

    def setUp(self):
        try:        
            awac_stats.process_wave_height('../../awac_data/awac_wave_height_df')
        except WindowsError:
            print "Load wap Files failed"

    def test_awac_stats(self):
        wave_height_dataframe = pd.load('wave_h_half_hour_set_test_awac')
        self.assertEqual(len(wave_height_dataframe),number_of_awac_stats)          
        
if __name__=='__main__':
    unittest.main()   