import json
import os
import sqlite3
import unittest
from unittest.mock import MagicMock, patch
from urllib import request

from data.gdc1a import Gdc1aPipeline

class Test_gdc1a(unittest.TestCase):
    def setUp(self):
        self.classUnderTest = Gdc1aPipeline()

    def test_system_pipeline(self):
        #arrange
        #act
        total, path = self.classUnderTest.runPipeline()
        #assert
        self.assertTrue(os.path.exists(path))
        con = sqlite3.connect(path)
        cursor = con.execute('select count(*) from cases')
        actual_total = cursor.fetchone()[0]
        self.assertEqual(total, actual_total, "The number of cases in the database {} is not the downloaded sample number {}".format(actual_total, total))
        con.close()

    @patch('urllib.request.urlopen')
    @patch('urllib.request.Request')
    def test_component_request_post(self, mock_urlopen, mock_request):
        #arrange
        expected_json = "{name='test', weather='sunny'}"
        expected_json_encoded = expected_json.encode("UTF-8")
        mock_urlopen.return_value = MagicMock()
        mock_urlopen.reason.return_value = 'OK'
        mock_urlopen.return_value.__enter__.return_value.reason = 'OK'
        mock_urlopen.read.return_value = expected_json_encoded
        mock_urlopen.return_value.__enter__.return_value.read.return_value = expected_json_encoded
        mock_request.return_value = ""
        request.Request = mock_request
        request.urlopen = mock_urlopen
        #act
        jsonResponse = self.classUnderTest.requestPost(url="testurl", data={"query": "", 'variables': ""})
        #assert
        self.assertEqual(jsonResponse, json.dumps(expected_json, indent=2))

    def test_component_prepare_data(self):
        #arrange
        json_data = '''{
                            "data": {
                                "explore": {
                                    "cases": {
                                        "hits": {
                                            "edges": [
                                                {
                                                    "node": {
                                                        "demographic": {
                                                            "age_at_index": 7,
                                                            "cause_of_death": "Cancer Related",
                                                            "cause_of_death_source": null,
                                                            "country_of_residence_at_enrollment": null,
                                                            "days_to_birth": -2775,
                                                            "days_to_death": 450,
                                                            "state": "released",
                                                            "vital_status": "Dead"
                                                        },
                                                        "diagnoses": {
                                                            "hits": {
                                                                "edges": [
                                                                    {
                                                                        "node": {
                                                                            "ajcc_clinical_m": "11",
                                                                            "ajcc_clinical_n": "12",
                                                                            "ajcc_clinical_stage": "13",
                                                                            "ajcc_clinical_t": "14",
                                                                            "ajcc_pathologic_m": "15",
                                                                            "ajcc_pathologic_n": "16",
                                                                            "ajcc_pathologic_stage": "17",
                                                                            "ajcc_pathologic_t": "18"
                                                                        }
                                                                    },
                                                                    {
                                                                        "node": {
                                                                            "ajcc_clinical_m": "21",
                                                                            "ajcc_clinical_n": "22",
                                                                            "ajcc_clinical_stage": "23",
                                                                            "ajcc_clinical_t": "24",
                                                                            "ajcc_pathologic_m": "25",
                                                                            "ajcc_pathologic_n": "26",
                                                                            "ajcc_pathologic_stage": "27",
                                                                            "ajcc_pathologic_t": "28"
                                                                        }
                                                                    }
                                                                ]
                                                            }
                                                        },
                                                        "disease_type": "Complex Mixed and Stromal Neoplasms",
                                                        "id": "RUNhc2U6ODg0YjQ0NmItMzNhYy01MGJhLThlNmQtN2FhOWQ4NThhMWI3",
                                                        "index_date": "Diagnosis",
                                                        "primary_site": "Kidney"
                                                    }
                                                }
                                            ],
                                            "pageInfo": {
                                                "endCursor": "OToxNzFjOGExNDk3MmY2MjI0YjRkNTFkODk3ZmJhMzdhMA==",
                                                "hasNextPage": true
                                            },
                                            "total": 3506
                                        }
                                    }
                                }
                            }
                        }
            '''
        expected_case_dict={}
        expected_case_dict['id'] = "RUNhc2U6ODg0YjQ0NmItMzNhYy01MGJhLThlNmQtN2FhOWQ4NThhMWI3"
        expected_case_dict['index_date'] = "Diagnosis"
        expected_case_dict['primary_site'] = "Kidney"
        expected_case_dict['disease_type'] = "Complex Mixed and Stromal Neoplasms"
        expected_cases = [expected_case_dict]

        expected_demographic_dict={}
        expected_demographic_dict['case_id'] = "RUNhc2U6ODg0YjQ0NmItMzNhYy01MGJhLThlNmQtN2FhOWQ4NThhMWI3"
        expected_demographic_dict['age_at_index']=7
        expected_demographic_dict['days_to_birth']=-2775
        expected_demographic_dict['days_to_death']=450
        expected_demographic_dict['cause_of_death']="Cancer Related"
        expected_demographic_dict['cause_of_death_source']=None
        expected_demographic_dict['country_of_residence_at_enrollment']=None
        expected_demographic_dict['state']="released"
        expected_demographic_dict['vital_status']="Dead"
        expected_demographics = [expected_demographic_dict]

        expected_diagnosis_dict1={}
        expected_diagnosis_dict1['case_id'] = "RUNhc2U6ODg0YjQ0NmItMzNhYy01MGJhLThlNmQtN2FhOWQ4NThhMWI3"
        expected_diagnosis_dict1['ajcc_clinical_m']="11"
        expected_diagnosis_dict1['ajcc_clinical_t']="14"
        expected_diagnosis_dict1['ajcc_clinical_n']="12"
        expected_diagnosis_dict1['ajcc_clinical_stage']="13"
        expected_diagnosis_dict1['ajcc_pathologic_t']="18"
        expected_diagnosis_dict1['ajcc_pathologic_n']="16"
        expected_diagnosis_dict1['ajcc_pathologic_m']="15"
        expected_diagnosis_dict1['ajcc_pathologic_stage']="17"
        expected_diagnosis_dict2={}
        expected_diagnosis_dict2['case_id'] = "RUNhc2U6ODg0YjQ0NmItMzNhYy01MGJhLThlNmQtN2FhOWQ4NThhMWI3"
        expected_diagnosis_dict2['ajcc_clinical_m']="21"
        expected_diagnosis_dict2['ajcc_clinical_t']="24"
        expected_diagnosis_dict2['ajcc_clinical_n']="22"
        expected_diagnosis_dict2['ajcc_clinical_stage']="23"
        expected_diagnosis_dict2['ajcc_pathologic_t']="28"
        expected_diagnosis_dict2['ajcc_pathologic_n']="26"
        expected_diagnosis_dict2['ajcc_pathologic_m']="25"
        expected_diagnosis_dict2['ajcc_pathologic_stage']="27"
        expected_diagnoses = [expected_diagnosis_dict1, expected_diagnosis_dict2]
        #act
        cases, demographics, diagnoses, total, hasNextPage, endCursor = self.classUnderTest.prepareData(json.dumps(json_data))
        #assert
        self.assertEqual(len(cases), 1)
        self.assertEqual(cases, expected_cases)
        self.assertEqual(len(demographics), 1)
        self.assertEqual(demographics, expected_demographics)
        self.assertEqual(len(diagnoses), 2)
        self.assertEqual(diagnoses, expected_diagnoses)
        self.assertEqual(total, 3506)
        self.assertEqual(hasNextPage, True)
        self.assertEqual(endCursor, "OToxNzFjOGExNDk3MmY2MjI0YjRkNTFkODk3ZmJhMzdhMA==")        