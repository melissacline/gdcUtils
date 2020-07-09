#!/usr/bin/env python

import gdc_id_mapping
import unittest

class TestIdMapping(unittest.TestCase):

    def setUp(self):
        self.mapping = gdc_id_mapping.GdcIdMapping("TCGA-BRCA")
    
    def test_case_uuid_to_barcode(self):
        case_uuid = "418c11e8-2670-48d5-bbf5-95b46bff1201"
        target_barcode = "TCGA-A2-A4S3"
        self.assertEqual(self.mapping.barcode(case_uuid), target_barcode)

    def test_aliquot_uuid_to_barcode(self):
        aliquot_uuid = "00741e84-d5ca-4d90-9b67-328e808705ae"
        target_barcode = "TCGA-AR-A0TX"
        self.assertEqual(self.mapping.barcode(aliquot_uuid), target_barcode)

    def test_barcode_to_case_uuid(self):
        barcode = "TCGA-A2-A4S3"
        target_case_uuid = "418c11e8-2670-48d5-bbf5-95b46bff1201"
        self.assertEqual(self.mapping.uuid(barcode), target_case_uuid)
        
if __name__ == '__main__':
    unittest.main()
