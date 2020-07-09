#!/usr/bin/env python
"""
This module queries the GDC API to build data for mapping between UUIDs
and TCGA barcodes
"""

import requests
import json


class GdcIdMapping():
    """
    This class maintains the mapping.  It queries the GDC to get the mapping
    data, and provides functions that map from barcode to UUID, and from UUID
    to barcode, and that print out the UUID / barcode mapping
    """
    def __init__(self, project_id=None, maxsize=10000):
        self.case_uuid_to_barcode = dict()
        self.barcode_to_case_uuid = dict()
        self.aliquot_uuid_to_barcode = dict()
        cases_endpoint = 'https://api.gdc.cancer.gov/cases'
        fields = [
            "case_id",
            "aliquot_ids",
            "submitter_id"
        ]
        fields = ','.join(fields)
        filters = {
            "op": "in",
            "content":{
                "field": "project.project_id",
                "value": project_id
                }
            }
        start_record = 0
        received = 0
        all_received = False
        while not all_received:
            params = {
                "filters": json.dumps(filters),
                "fields": fields,
                "format": "JSON",
                "from": start_record,
                "size": maxsize
            }
            response = requests.get(cases_endpoint, params = params)
            self.project_id = project_id
            content = json.loads(response.content.decode("utf-8"))
            for hit in content['data']['hits']:
                case_uuid = hit['id']
                case_barcode = hit['submitter_id']
                self.case_uuid_to_barcode[case_uuid] = case_barcode
                self.barcode_to_case_uuid[case_barcode] = case_uuid
                for aliquot_uuid in hit['aliquot_ids']:
                    self.aliquot_uuid_to_barcode[aliquot_uuid] = case_barcode
            received += content['data']['pagination']['size']
            if received < content['data']['pagination']['total']:
                start_record += content['data']['pagination']['size']
            else:
                all_received = True


    def barcode(self, uuid, check_aliquots=True):
        if uuid in self.case_uuid_to_barcode:
            return self.case_uuid_to_barcode[uuid]
        elif check_aliquots and uuid in self.aliquot_uuid_to_barcode:
            return self.aliquot_uuid_to_barcode[uuid]
        else:
            return None

    def uuid(self, barcode):
        if barcode in self.barcode_to_case_uuid:
            return self.barcode_to_case_uuid[barcode]
        else:
            return None

def main():
    mapping = GdcIdMapping("TCGA-BRCA")
    print("UUID\tBarcode")
    for case_uuid in mapping.case_uuid_to_barcode.keys():
        print("%s\t%s" % (case_uuid, mapping.case_uuid_to_barcode[case_uuid]))
    for aliquot_uuid in mapping.aliquot_uuid_to_barcode.keys():
        print("%s\t%s" % (aliquot_uuid,
                          mapping.aliquot_uuid_to_barcode[aliquot_uuid]))

if __name__ == '__main__':
    main()

