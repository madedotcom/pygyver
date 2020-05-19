import time
import asyncio
import logging
import unittest
from pygyver.etl.dw import BigQueryExecutor
import pygyver.etl.pipeline as pl


class TestExecute_parallel(unittest.TestCase):
    # def setUp(self):
    #     logging.basicConfig(level=logging.DEBUG)

    def sleep_2_sec(self, num):
        asyncio.sleep(2)
        return "ciao"

    def test_time_is_right(self):
        start_time = time.time()
        list_values = [
            {"num": "1"}, {"num": "2"}, {"num": "3"},
            {"num": "4"}, {"num": "5"}, {"num": "6"},
            {"num": "7"}, {"num": "8"}
            ]
        pl.execute_parallel(
                    self.sleep_2_sec,
                    list_values)

        end_time = time.time()
        self.assertLess(end_time-start_time, 3, "right execution time")

    def bug(self, **kwargs):
        for key, value in kwargs.items():
            if value == "error":
                raise Exception("error something")
            else:
                return 1

    def test_error_raised(self):
        with self.assertRaises(Exception):
            pl.execute_parallel(
                    self.bug,
                    [{"status": "ok"}, {"status": "ok"}, {"status": "error"}, {"status": "ok"}]
                )


class TestPipelineExecutorCreateTables(unittest.TestCase):

    def setUp(self):
        self.bq_client = BigQueryExecutor()
        self.p_ex = pl.PipelineExecutor("tests/yaml/test_run.yaml")

    def test_create_tables(self):
        batch = {
            "desc": "create table1 & table2 in staging",
            "tables":
            [
                {
                    "table_desc": "table1",
                    "create_table": {
                        "table_id": "table1",
                        "dataset_id": "test",              
                        "file": "tests/sql/table1.sql"
                    },
                    "pk": ["col1", "col2"],
                    "mock_data": "sql/table1_mocked.sql"
                },
                {
                    "table_desc": "table2",
                    "create_table": {
                        "table_id": "table2",
                        "dataset_id": "test",
                        "file": "tests/sql/table2.sql"
                    },
                    "pk": ["col1", "col2"],
                    "mock_data": "sql/table1_mocked.sql"
                }
            ]
        }
        self.p_ex.create_tables(batch)
        self.assertTrue(
            self.bq_client.table_exists(
                table_id='table1',
                dataset_id="test"),
            "Table1 exists")
        self.assertTrue(
            self.bq_client.table_exists(
                table_id='table2',
                dataset_id="test"
                ),
            "Table2 exists")

    def test_run_batch(self):
        batch = {
            "desc": "create table1 & table2 in staging",
            "tables":
            [
                {
                    "table_desc": "table1",
                    "create_table": {
                        "table_id": "table1",
                        "dataset_id": "test",              
                        "file": "tests/sql/table1.sql"
                    },
                    "pk": ["col1", "col2"],
                    "mock_data": "sql/table1_mocked.sql"
                },
                {
                    "table_desc": "table2",
                    "create_table": {
                        "table_id": "table2",
                        "dataset_id": "test",
                        "file": "tests/sql/table2.sql"
                    },
                    "pk": ["col1", "col2"],
                    "mock_data": "sql/table1_mocked.sql"
                }
            ]
        }
        self.p_ex.create_tables(batch)
        self.assertTrue(
            self.bq_client.table_exists(
                table_id='table1',
                dataset_id="test"),
            "Tables are created")
        self.assertTrue(
            self.bq_client.table_exists(
                table_id='table2',
                dataset_id="test"
                ),
            "Tables are created")

    def tearDown(self):
        if self.bq_client.table_exists(table_id='table1', dataset_id='test'):
            self.bq_client.delete_table(table_id='table1', dataset_id='test')
        if self.bq_client.table_exists(table_id='table2', dataset_id='test'):
            self.bq_client.delete_table(table_id='table2', dataset_id='test')
        if self.bq_client.table_exists(table_id='test_run_batch_table_1', dataset_id='test'):
            self.bq_client.delete_table(table_id='test_run_batch_table_1', dataset_id='test')
        if self.bq_client.table_exists(table_id='test_run_batch_table_2', dataset_id='test'):
            self.bq_client.delete_table(table_id='test_run_batch_table_2', dataset_id='test')


class TestPipelineExecutorRunChecks(unittest.TestCase):

    def setUp(self):
        self.bq_client = BigQueryExecutor()
        self.p_ex = pl.PipelineExecutor("tests/yaml/test_run.yaml")
        batch = {
            "desc": "create table1 & table2 in staging",
            "tables":
            [
                {
                    "table_desc": "table1",
                    "create_table": {
                        "table_id": "table1",
                        "dataset_id": "test",              
                        "file": "tests/sql/table1.sql"
                    },
                    "pk": ["col1", "col2"],
                    "mock_data": "sql/table1_mocked.sql"
                },
                {
                    "table_desc": "table2",
                    "create_table": {
                        "table_id": "table2",
                        "dataset_id": "test",
                        "file": "tests/sql/table2.sql"
                    },
                    "pk": ["col1", "col2"],
                    "mock_data": "sql/table1_mocked.sql"
                }
            ]
        }
        self.p_ex.create_tables(batch)

    def test_run_checks_raise_exception(self):
        batch = {
            "desc": "create table1 & table2 in staging",
            "tables":
            [
                {
                    "table_desc": "table1",
                    "create_table": {
                        "table_id": "table1",
                        "dataset_id": "test",              
                        "file": "tests/sql/table1.sql"
                    },
                    "pk": ["col1", "col2"],
                    "mock_data": "sql/table1_mocked.sql"
                },
                {
                    "table_desc": "table2",
                    "create_table": {
                        "table_id": "table2",
                        "dataset_id": "test",
                        "file": "tests/sql/table2.sql"
                    },
                    "pk": ["col1"],
                    "mock_data": "sql/table1_mocked.sql"
                }
            ]
        }
        with self.assertRaises(Exception):
            self.p_ex.run_checks(batch)

    def test_run_checks_success(self):
        batch = {
            "desc": "create table1 & table2 in staging",
            "tables":
            [
                {
                    "table_desc": "table1",
                    "create_table": {
                        "table_id": "table1",
                        "dataset_id": "test",              
                        "file": "tests/sql/table1.sql"
                    },
                    "pk": ["col1", "col2"],
                    "mock_data": "sql/table1_mocked.sql"
                },
                {
                    "table_desc": "table2",
                    "create_table": {
                        "table_id": "table2",
                        "dataset_id": "test",
                        "file": "tests/sql/table2.sql"
                    },
                    "pk": ["col1", "col2"],
                    "mock_data": "sql/table1_mocked.sql"
                }
            ]
        }
        try:
            self.p_ex.run_checks(batch)
        except AssertionError:
            self.fail("run_checks() raised AssertionError unexpectedly!")

    def tearDown(self):
        if self.bq_client.table_exists(table_id='table1', dataset_id='test'):
            self.bq_client.delete_table(table_id='table1', dataset_id='test')
        if self.bq_client.table_exists(table_id='table2', dataset_id='test'):
            self.bq_client.delete_table(table_id='table2', dataset_id='test')
        if self.bq_client.table_exists(table_id='test_run_batch_table_1', dataset_id='test'):
            self.bq_client.delete_table(table_id='test_run_batch_table_1', dataset_id='test')
        if self.bq_client.table_exists(table_id='test_run_batch_table_2', dataset_id='test'):
            self.bq_client.delete_table(table_id='test_run_batch_table_2', dataset_id='test')


class TestPipelineExecutorLoadGoogleSheets(unittest.TestCase):

    def setUp(self):
        self.bq_client = BigQueryExecutor()
        self.p_ex = pl.PipelineExecutor("tests/yaml/test_run.yaml")

    def test_LoadGoogleSheet(self):
        batch = {
            "desc": "load test spreadsheet into bigquery",
            "sheets": [
                {
                    "table_desc": "ref sheet1",
                    "load_google_sheet": {
                        "table_id": "ref_sheet1",
                        "dataset_id": "test",
                        "googlesheet_key": "19Jmapr9G1nrMcW2QTpY7sOvKYaFXnw5krK6dD0GwEqU",
                        "googlesheet_link": "https://docs.google.com/spreadsheets/d/19Jmapr9G1nrMcW2QTpY7sOvKYaFXnw5krK6dD0GwEqU/edit#gid=0"
                    }
                }
            ]
        }
        self.p_ex.load_google_sheets(batch)
        self.assertTrue(
            self.bq_client.table_exists(
                table_id='ref_sheet1',
                dataset_id="test"),
            "ref_sheet1 exists")

    

    def tearDown(self):
        if self.bq_client.table_exists(table_id='ref_sheet1', dataset_id='test'):
            self.bq_client.delete_table(table_id='ref_sheet1', dataset_id='test')


class TestPipelineExecutorRunBatch(unittest.TestCase):
    
    def setUp(self):
        self.bq_client = BigQueryExecutor()
        self.p_ex = pl.PipelineExecutor("tests/yaml/test_run.yaml")
    
    def test_run_batch_create_tables(self):
        batch = {
            "desc": "create table1 & table2 in staging",
            "tables":
            [
                {
                    "table_desc": "table1",
                    "create_table": {
                        "table_id": "table1",
                        "dataset_id": "test",              
                        "file": "tests/sql/table1.sql"
                    },
                    "pk": ["col1", "col2"],
                    "mock_data": "sql/table1_mocked.sql"
                },
                {
                    "table_desc": "table2",
                    "create_table": {
                        "table_id": "table2",
                        "dataset_id": "test",
                        "file": "tests/sql/table2.sql"
                    },
                    "pk": ["col1", "col2"],
                    "mock_data": "sql/table1_mocked.sql"
                }
            ]
        }
        self.p_ex.run_batch(batch)
        self.assertTrue(
            self.bq_client.table_exists(
                table_id='table1',
                dataset_id="test"),
            "Tables are created")
        self.assertTrue(
            self.bq_client.table_exists(
                table_id='table2',
                dataset_id="test"
                ),
            "Tables are created")

    def test_run_batch_load_google_sheets(self):
        batch = {
            "desc": "load test spreadsheet into bigquery",
            "sheets": [
                {
                    "table_desc": "ref sheet1",
                    "load_google_sheet": {
                        "table_id": "ref_sheet1",
                        "dataset_id": "test",
                        "googlesheet_key": "19Jmapr9G1nrMcW2QTpY7sOvKYaFXnw5krK6dD0GwEqU",
                        "googlesheet_link": "https://docs.google.com/spreadsheets/d/19Jmapr9G1nrMcW2QTpY7sOvKYaFXnw5krK6dD0GwEqU/edit#gid=0"
                    }
                }
            ]
        }
        self.p_ex.load_google_sheets(batch)
        self.assertTrue(
            self.bq_client.table_exists(
                table_id='ref_sheet1',
                dataset_id="test"),
            "ref_sheet1 exists")


    def tearDown(self):
        if self.bq_client.table_exists(table_id='table1', dataset_id='test'):
            self.bq_client.delete_table(table_id='table1', dataset_id='test')
        if self.bq_client.table_exists(table_id='table2', dataset_id='test'):
            self.bq_client.delete_table(table_id='table2', dataset_id='test')
        if self.bq_client.table_exists(table_id='test_run_batch_table_1', dataset_id='test'):
            self.bq_client.delete_table(table_id='test_run_batch_table_1', dataset_id='test')
        if self.bq_client.table_exists(table_id='test_run_batch_table_2', dataset_id='test'):
            self.bq_client.delete_table(table_id='test_run_batch_table_2', dataset_id='test')


class TestPipelineExecutorRun(unittest.TestCase):
    
    def setUp(self):
        self.bq_client = BigQueryExecutor()
        self.p_ex = pl.PipelineExecutor("tests/yaml/test_run.yaml")
        
    def test_run_completed_no_error(self):
        
        self.p_ex.run()

        self.assertTrue(
            self.bq_client.table_exists(
                table_id='ref_sheet1',
                dataset_id="test"),
            "googlesheet table1 exists")

        self.assertTrue(
            self.bq_client.table_exists(
                table_id='ref_sheet2',
                dataset_id="test"),
            "googlesheet table2 exists")
        
        self.assertTrue(
            self.bq_client.table_exists(
                table_id='table1',
                dataset_id="test"),
            "createtable table1 exists")

        self.assertTrue(
            self.bq_client.table_exists(
                table_id='table2',
                dataset_id="test"),
            "createtable table2 exists")
        
        
    def tearDown(self):
        if self.bq_client.table_exists(table_id='table1', dataset_id='test'):
            self.bq_client.delete_table(table_id='table1', dataset_id='test')
        if self.bq_client.table_exists(table_id='table2', dataset_id='test'):
            self.bq_client.delete_table(table_id='table2', dataset_id='test')
        if self.bq_client.table_exists(table_id='ref_sheet1', dataset_id='test'):
            self.bq_client.delete_table(table_id='ref_sheet1', dataset_id='test')
        if self.bq_client.table_exists(table_id='ref_sheet2', dataset_id='test'):
            self.bq_client.delete_table(table_id='ref_sheet2', dataset_id='test')


class TestPipelineUnitTests(unittest.TestCase):
    
    def setUp(self):
        self.bq_client = BigQueryExecutor()
        self.p_ex = pl.PipelineExecutor("tests/yaml/unit_tests.yaml")

    def test_extract_unit_tests(self):   
        list_batches = [
                        {
                            "batch": None,
                            "desc": "create table1 & table2 in staging",
                            "tables": [
                                {
                                "table_desc": "table1",
                                "create_table": {
                                    "table_id": "table1",
                                    "dataset_id": "test",
                                    "file": "tests/sql/unit_table1.sql"
                                },
                                "pk": [
                                    "col1",
                                    "col2"
                                ],
                                "mock_data": {
                                    "mock_file": "sql/unit_table1_mocked.sql"
                                }
                                },
                                {
                                "table_desc": "table2",
                                "create_table": {
                                    "table_id": "table2",
                                    "dataset_id": "test",
                                    "file": "tests/sql/unit_table2.sql"
                                },
                                "pk": [
                                    "col1",
                                    "col2"
                                ],
                                "mock_data": {
                                    "mock_file": "sql/unit_table2_mocked.sql"
                                }
                                }
                            ]
                            },
                            {
                            "batch": None,
                            "desc": "create table3 & table4 in staging",
                            "tables": [
                                {
                                "table_desc": "table3",
                                "create_table": {
                                    "table_id": "table3",
                                    "dataset_id": "test",
                                    "file": "tests/sql/unit_table3.sql"
                                },
                                "pk": [
                                    "col1",
                                    "col2"
                                ],
                                "mock_data": {
                                    "mock_file": "sql/unit_table3_mocked.sql"
                                }
                                },
                                {
                                "table_desc": "table4",
                                "create_table": {
                                    "table_id": "table4",
                                    "dataset_id": "test",
                                    "file": "tests/sql/unit_table4.sql"
                                },
                                "pk": [
                                    "col1",
                                    "col2"
                                ],
                                "mock_data": {
                                    "mock_file": "sql/unit_table4_mocked.sql",
                                    "output_table_name": "output_test_table"
                                }
                                }
                            ]
                            }
                        ]
                    
                          
        self.assertCountEqual( 
            self.p_ex.extract_unit_tests(list_batches), 
            [ 
                { "file" : "tests/sql/unit_table1.sql", "mock_file": "sql/unit_table1_mocked.sql"}, 
                { "file" : "tests/sql/unit_table2.sql", "mock_file": "sql/unit_table2_mocked.sql"},
                { "file" : "tests/sql/unit_table3.sql", "mock_file": "sql/unit_table3_mocked.sql"},
                { "file" : "tests/sql/unit_table4.sql", "mock_file": "sql/unit_table4_mocked.sql", "output_table_name": "output_test_table"},
            ], 
            "unit tests well extracted" )
       
    
    def test_extract_unit_test_value(self):
        self.assertCountEqual(
            self.p_ex.extract_unit_test_value(
                    [
                        { "file" : "tests/sql/unit_table1.sql", "mock_file": "tests/sql/unit_table1_mocked.sql"},
                        { "file" : "tests/sql/unit_table1.sql", "mock_file": "tests/sql/unit_table1_mocked.sql", "output_table_name": "output_test_table"},
                    ]
                ), 
            [
                { "sql" : "sql test 1", "cte": "mock_sql test 1",
                "file" : "tests/sql/unit_table1.sql", "mock_file": "tests/sql/unit_table1_mocked.sql"},
                { "sql" : "sql test 1", "cte": "mock_sql test 1", "output_table_name": "output_test_table",
                "file" : "tests/sql/unit_table1.sql", "mock_file": "tests/sql/unit_table1_mocked.sql", "output_table_name": "output_test_table"}
            ],
            "unit tests values well extracted" )

    def test_run_unit_tests_ok(self):        
        try:
            self.p_ex.run_unit_tests()
        except AssertionError:
            self.fail("run_unit_tests() raised AssertionError unexpectedly!")

    def tearDown(self):
        if self.bq_client.table_exists(table_id='table1', dataset_id='test'):
            self.bq_client.delete_table(table_id='table1', dataset_id='test')
        if self.bq_client.table_exists(table_id='table2', dataset_id='test'):
            self.bq_client.delete_table(table_id='table2', dataset_id='test')
        if self.bq_client.table_exists(table_id='test_run_batch_table_1', dataset_id='test'):
            self.bq_client.delete_table(table_id='test_run_batch_table_1', dataset_id='test')
        if self.bq_client.table_exists(table_id='test_run_batch_table_2', dataset_id='test'):
            self.bq_client.delete_table(table_id='test_run_batch_table_2', dataset_id='test')

class TestPipelineUnitTestsErrorRaised(unittest.TestCase):
    
    def setUp(self):
        self.bq_client = BigQueryExecutor()
        self.p_ex = pl.PipelineExecutor("tests/yaml/unit_tests_fail.yaml")

    def test_run_unit_tests_error(self):
        with self.assertRaises(AssertionError):
            self.p_ex.run_unit_tests()

class TestPipelineCopyTableStructure(unittest.TestCase):

    def setUp(self):
        self.bq_client = BigQueryExecutor()
        self.p_ex = pl.PipelineExecutor("tests/yaml/unit_tests_fail.yaml")    
        if self.bq_client.table_exists(dataset_id='reporting', table_id='out_product'):
            self.bq_client.delete_table(dataset_id='reporting', table_id='out_product')
        if self.bq_client.table_exists(dataset_id='reporting', table_id='out_saleorder'):
            self.bq_client.delete_table(dataset_id='reporting', table_id='out_saleorder')

    def test_copy_prod_structure(self):
        self.p_ex.copy_prod_structure(['reporting.out_product', 'reporting.out_saleorder'])
        self.assertTrue(
            self.bq_client.table_exists(dataset_id='reporting', table_id='out_product') and
            self.bq_client.table_exists(dataset_id='reporting', table_id='out_saleorder'),
            "all table's structure are copied"
        )

    
    


if __name__ == '__main__':
    unittest.main()
