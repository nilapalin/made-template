import os
from pathlib import Path
import sqlite3
import json
from urllib import request
from urllib.parse import urlencode
import pandas as pd

class Gdc1aPipeline:

    def requestPost(self, url, data = {}, headers = {}):
        data = urlencode(data).encode()
        req = request.Request(url, data = data, method="POST")   
        with request.urlopen(req) as response:
            the_page = response.read()
        if (response.reason == 'OK'):
            return json.dumps(the_page.decode("utf-8"), indent=2)
        else:
            raise Exception(f"Query failed to run with a {response.status}.")

    def runGraphQLQuery(self, url, query, variables = {}, headers = {}):
        #accessToken = "xxx"
        #headers = {"Authorization": f"Bearer {accessToken}"}
        data = self.requestPost(url, data = {"query": query, 'variables': variables}, headers = headers)
        return data

    def runGDCGraphQLQuery(self, first=None, after=None):
        url = "https://api.gdc.cancer.gov/v0/graphql"
        case_hit_first = "hits (filters: $filters_cases) "
        case_hit_next = """hits (filters: $filters_cases, first: {}, after: "{}") """.format(first, after)
        query1 = """
            query getgdcdata($filters_cases: FiltersArgument, $filters_diagnoses: FiltersArgument) {
            explore {
                cases {"""
        query2 = """{
                total
                pageInfo {
                    endCursor
                    hasNextPage
                }            
                edges {
                    node {
                        id,
                        index_date,
                        primary_site,
                        disease_type,
                        diagnoses {
                        hits (filters: $filters_diagnoses) {
                            edges {
                            node {
                                ajcc_clinical_t,
                                ajcc_clinical_n,
                                ajcc_clinical_m,
                                ajcc_clinical_stage,
                                ajcc_pathologic_t,
                                ajcc_pathologic_n,
                                ajcc_pathologic_m,
                                ajcc_pathologic_stage
                            }
                            }
                        }
                        },
                        demographic {
                        age_at_index,
                        days_to_birth,
                        days_to_death,
                        cause_of_death,
                        cause_of_death_source,
                        country_of_residence_at_enrollment,
                        state,
                        vital_status
                        }
                    }
                    }
                } 
                }
            }
            }
        """
        query = query1+case_hit_first+query2
        if (after):
            query = query1+case_hit_next+query2
        variables = """{"filters_cases": {"op": "in", "content": {"field": "primary_site", "value": ["Kidney"]}}, "filsters_diagnoses": {}}"""
        return self.runGraphQLQuery(url, query, variables)

    def prepareData(self, jsondata):
        js = json.loads(json.loads(jsondata))#TODO not clear yet why twice json.loads
        
        edges = js.get('data').get('explore').get('cases').get('hits').get('edges')
        diagnoses_data = []
        demographics_data = []
        case_data = []
        for edge in edges:
            id = edge.get('node').get('id')
            case_dict={}
            case_dict['id'] = id
            case_dict['index_date'] = edge.get('node').get('index_date')
            case_dict['primary_site'] = edge.get('node').get('primary_site')
            case_dict['disease_type'] = edge.get('node').get('disease_type')
            
            #{"node":{"demographic":{"age_
            demographic = edge.get('node').get('demographic')
            demographic_dict={}
            demographic_dict['case_id'] = id
            demographic_dict['age_at_index']=demographic.get('age_at_index')
            demographic_dict['days_to_birth']=demographic.get('days_to_birth')
            demographic_dict['days_to_death']=demographic.get('days_to_death')
            demographic_dict['cause_of_death']=demographic.get('cause_of_death')
            demographic_dict['cause_of_death_source']=demographic.get('cause_of_death_source')
            demographic_dict['country_of_residence_at_enrollment']=demographic.get('country_of_residence_at_enrollment')
            demographic_dict['state']=demographic.get('state')
            demographic_dict['vital_status']=demographic.get('vital_status')
            
            #{"node":{"diagnoses":{"hits":{"edges":[{"node":{"aj...
            diagnoses_edge = edge.get('node').get('diagnoses').get('hits').get('edges')
            for diagnosis_edge in diagnoses_edge:
                diagnosis_dict={}
                diagnosis = diagnosis_edge.get('node')
                diagnosis_dict['case_id'] = id
                diagnosis_dict['ajcc_clinical_m']=diagnosis.get('ajcc_clinical_m')
                diagnosis_dict['ajcc_clinical_t']=diagnosis.get('ajcc_clinical_t')
                diagnosis_dict['ajcc_clinical_n']=diagnosis.get('ajcc_clinical_n')
                diagnosis_dict['ajcc_clinical_m']=diagnosis.get('ajcc_clinical_m')
                diagnosis_dict['ajcc_clinical_stage']=diagnosis.get('ajcc_clinical_stage')
                diagnosis_dict['ajcc_pathologic_t']=diagnosis.get('ajcc_pathologic_t')
                diagnosis_dict['ajcc_pathologic_n']=diagnosis.get('ajcc_pathologic_n')
                diagnosis_dict['ajcc_pathologic_m']=diagnosis.get('ajcc_pathologic_m')
                diagnosis_dict['ajcc_pathologic_stage']=diagnosis.get('ajcc_pathologic_stage')
                                
            demographics_data.append(demographic_dict)
            diagnoses_data.append(diagnosis_dict)
            case_data.append(case_dict)
        total = js.get('data').get('explore').get('cases').get('hits').get('total')
        hasNextPage = js.get('data').get('explore').get('cases').get('hits').get('pageInfo').get('hasNextPage')
        endCursor = js.get('data').get('explore').get('cases').get('hits').get('pageInfo').get('endCursor')
        return case_data, demographics_data, diagnoses_data, total, hasNextPage, endCursor

    def loadToSink(self, path: str, data, tablename):
        con = sqlite3.connect(path)
        con.execute('drop table if exists {}'.format(tablename))
        df = pd.DataFrame(data)
        df.to_sql(tablename, con, if_exists='fail', index=False)
        con.commit()
        con.close()

    def runPipeline(self):
        response = self.runGDCGraphQLQuery(100) #run first 100 samples, get also pagination information, details see https://graphql.org/learn/pagination/
        cases, demographics, diagnoses, total, hasNextPage, endCursor = self.prepareData(response)
        while hasNextPage:
            response = self.runGDCGraphQLQuery(1000, endCursor)
            tmp_cases, tmp_demographics, tmp_diagnoses, total, hasNextPage, endCursor = self.prepareData(response)
            demographics = demographics + tmp_demographics
            diagnoses = diagnoses + tmp_diagnoses
            cases = cases + tmp_cases
            print("Total: {}".format(total))
            print("Aktuell: {}".format(len(demographics)))
            print("Noch Daten vorhanden: {}".format(hasNextPage))
        path = os.path.join(get_project_root(), 'data/gdc.sqlite')
        self.loadToSink(path, cases, 'cases')
        self.loadToSink(path, demographics, 'demographics')
        self.loadToSink(path, diagnoses, 'diagnoses')
        return total, path

def get_project_root() -> Path:
    return Path(__file__).parent.parent.parent

if __name__ == '__main__':
    pipeline = Gdc1aPipeline()
    pipeline.runPipeline()