import time
import asyncio
import logging
import unittest
from pygyver.etl.dw import BigQueryExecutor
import pygyver.etl.pipeline as pl


# class TestExecute_parallel(unittest.TestCase):
#     # def setUp(self):
#     #     logging.basicConfig(level=logging.DEBUG)

#     def sleep_2_sec(self, num):
#         asyncio.sleep(2)
#         return "ciao"

#     def test_time_is_right(self):
#         start_time = time.time()
#         list_values = [
#             {"num": "1"}, {"num": "2"}, {"num": "3"},
#             {"num": "4"}, {"num": "5"}, {"num": "6"},
#             {"num": "7"}, {"num": "8"}
#             ]
#         pl.execute_parallel(
#                     self.sleep_2_sec,
#                     list_values)

#         end_time = time.time()
#         self.assertLess(end_time-start_time, 3, "right execution time")

#     def bug(self, **kwargs):
#         for key, value in kwargs.items():
#             if value == "error":
#                 raise Exception("error something")
#             else:
#                 return 1

#     def test_error_raised(self):
#         with self.assertRaises(Exception):
#             pl.execute_parallel(
#                     self.bug,
#                     [{"status": "ok"}, {"status": "ok"}, {"status": "error"}, {"status": "ok"}]
#                 )


# class TestPipelineExecutorCreateTables(unittest.TestCase):

#     def setUp(self):
#         self.bq_client = BigQueryExecutor()
#         self.p_ex = pl.PipelineExecutor("tests/yaml/mock_run_batch.yaml")

#     def test_create_tables(self):
#         batch = {
#             "desc": "create table1 & table2 in staging",
#             "tables":
#             [
#                 {
#                     "table_desc": "table1",
#                     "create_table": {
#                         "table_id": "table1",
#                         "dataset_id": "test",              
#                         "file": "tests/sql/table1.sql"
#                     },
#                     "pk": ["col1", "col2"],
#                     "mock_data": "sql/table1_mocked.sql"
#                 },
#                 {
#                     "table_desc": "table2",
#                     "create_table": {
#                         "table_id": "table2",
#                         "dataset_id": "test",
#                         "file": "tests/sql/table2.sql"
#                     },
#                     "pk": ["col1", "col2"],
#                     "mock_data": "sql/table1_mocked.sql"
#                 }
#             ]
#         }
#         self.p_ex.create_tables(batch)
#         self.assertTrue(
#             self.bq_client.table_exists(
#                 table_id='table1',
#                 dataset_id="test"),
#             "Table1 exists")
#         self.assertTrue(
#             self.bq_client.table_exists(
#                 table_id='table2',
#                 dataset_id="test"
#                 ),
#             "Table2 exists")

#     def test_run_batch(self):
#         batch = {
#             "desc": "create table1 & table2 in staging",
#             "tables":
#             [
#                 {
#                     "table_desc": "table1",
#                     "create_table": {
#                         "table_id": "table1",
#                         "dataset_id": "test",              
#                         "file": "tests/sql/table1.sql"
#                     },
#                     "pk": ["col1", "col2"],
#                     "mock_data": "sql/table1_mocked.sql"
#                 },
#                 {
#                     "table_desc": "table2",
#                     "create_table": {
#                         "table_id": "table2",
#                         "dataset_id": "test",
#                         "file": "tests/sql/table2.sql"
#                     },
#                     "pk": ["col1", "col2"],
#                     "mock_data": "sql/table1_mocked.sql"
#                 }
#             ]
#         }
#         self.p_ex.create_tables(batch)
#         self.assertTrue(
#             self.bq_client.table_exists(
#                 table_id='table1',
#                 dataset_id="test"),
#             "Tables are created")
#         self.assertTrue(
#             self.bq_client.table_exists(
#                 table_id='table2',
#                 dataset_id="test"
#                 ),
#             "Tables are created")

#     def tearDown(self):
#         if self.bq_client.table_exists(table_id='table1', dataset_id='test'):
#             self.bq_client.delete_table(table_id='table1', dataset_id='test')
#         if self.bq_client.table_exists(table_id='table2', dataset_id='test'):
#             self.bq_client.delete_table(table_id='table2', dataset_id='test')
#         if self.bq_client.table_exists(table_id='test_run_batch_table_1', dataset_id='test'):
#             self.bq_client.delete_table(table_id='test_run_batch_table_1', dataset_id='test')
#         if self.bq_client.table_exists(table_id='test_run_batch_table_2', dataset_id='test'):
#             self.bq_client.delete_table(table_id='test_run_batch_table_2', dataset_id='test')


# class TestPipelineExecutorRunChecks(unittest.TestCase):

#     def setUp(self):
#         self.bq_client = BigQueryExecutor()
#         self.p_ex = pl.PipelineExecutor("tests/yaml/mock_run_batch.yaml")
#         batch = {
#             "desc": "create table1 & table2 in staging",
#             "tables":
#             [
#                 {
#                     "table_desc": "table1",
#                     "create_table": {
#                         "table_id": "table1",
#                         "dataset_id": "test",              
#                         "file": "tests/sql/table1.sql"
#                     },
#                     "pk": ["col1", "col2"],
#                     "mock_data": "sql/table1_mocked.sql"
#                 },
#                 {
#                     "table_desc": "table2",
#                     "create_table": {
#                         "table_id": "table2",
#                         "dataset_id": "test",
#                         "file": "tests/sql/table2.sql"
#                     },
#                     "pk": ["col1", "col2"],
#                     "mock_data": "sql/table1_mocked.sql"
#                 }
#             ]
#         }
#         self.p_ex.create_tables(batch)

#     def test_run_checks_raise_exception(self):
#         batch = {
#             "desc": "create table1 & table2 in staging",
#             "tables":
#             [
#                 {
#                     "table_desc": "table1",
#                     "create_table": {
#                         "table_id": "table1",
#                         "dataset_id": "test",              
#                         "file": "tests/sql/table1.sql"
#                     },
#                     "pk": ["col1", "col2"],
#                     "mock_data": "sql/table1_mocked.sql"
#                 },
#                 {
#                     "table_desc": "table2",
#                     "create_table": {
#                         "table_id": "table2",
#                         "dataset_id": "test",
#                         "file": "tests/sql/table2.sql"
#                     },
#                     "pk": ["col1"],
#                     "mock_data": "sql/table1_mocked.sql"
#                 }
#             ]
#         }
#         with self.assertRaises(Exception):
#             self.p_ex.run_checks(batch)

#     def test_run_checks_success(self):
#         batch = {
#             "desc": "create table1 & table2 in staging",
#             "tables":
#             [
#                 {
#                     "table_desc": "table1",
#                     "create_table": {
#                         "table_id": "table1",
#                         "dataset_id": "test",              
#                         "file": "tests/sql/table1.sql"
#                     },
#                     "pk": ["col1", "col2"],
#                     "mock_data": "sql/table1_mocked.sql"
#                 },
#                 {
#                     "table_desc": "table2",
#                     "create_table": {
#                         "table_id": "table2",
#                         "dataset_id": "test",
#                         "file": "tests/sql/table2.sql"
#                     },
#                     "pk": ["col1", "col2"],
#                     "mock_data": "sql/table1_mocked.sql"
#                 }
#             ]
#         }
#         try:
#             self.p_ex.run_checks(batch)
#         except AssertionError:
#             self.fail("run_checks() raised AssertionError unexpectedly!")

#     def tearDown(self):
#         if self.bq_client.table_exists(table_id='table1', dataset_id='test'):
#             self.bq_client.delete_table(table_id='table1', dataset_id='test')
#         if self.bq_client.table_exists(table_id='table2', dataset_id='test'):
#             self.bq_client.delete_table(table_id='table2', dataset_id='test')
#         if self.bq_client.table_exists(table_id='test_run_batch_table_1', dataset_id='test'):
#             self.bq_client.delete_table(table_id='test_run_batch_table_1', dataset_id='test')
#         if self.bq_client.table_exists(table_id='test_run_batch_table_2', dataset_id='test'):
#             self.bq_client.delete_table(table_id='test_run_batch_table_2', dataset_id='test')


# class TestPipelineExecutorRunBatch(unittest.TestCase):

#     def setUp(self):
#         self.bq_client = BigQueryExecutor()
#         self.p_ex = pl.PipelineExecutor("tests/yaml/mock_run_batch.yaml")

#     def test_run_batch(self):
#         batch = {
#             "desc": "create table1 & table2 in staging",
#             "tables":
#             [
#                 {
#                     "table_desc": "table1",
#                     "create_table": {
#                         "table_id": "table1",
#                         "dataset_id": "test",              
#                         "file": "tests/sql/table1.sql"
#                     },
#                     "pk": ["col1", "col2"],
#                     "mock_data": "sql/table1_mocked.sql"
#                 },
#                 {
#                     "table_desc": "table2",
#                     "create_table": {
#                         "table_id": "table2",
#                         "dataset_id": "test",
#                         "file": "tests/sql/table2.sql"
#                     },
#                     "pk": ["col1", "col2"],
#                     "mock_data": "sql/table1_mocked.sql"
#                 }
#             ]
#         }
#         try:
#             self.p_ex.run_batch(batch)
#         except AssertionError:
#             self.fail("run_checks() raised AssertionError unexpectedly!")

#     def tearDown(self):
#         if self.bq_client.table_exists(table_id='table1', dataset_id='test'):
#             self.bq_client.delete_table(table_id='table1', dataset_id='test')
#         if self.bq_client.table_exists(table_id='table2', dataset_id='test'):
#             self.bq_client.delete_table(table_id='table2', dataset_id='test')
#         if self.bq_client.table_exists(table_id='test_run_batch_table_1', dataset_id='test'):
#             self.bq_client.delete_table(table_id='test_run_batch_table_1', dataset_id='test')
#         if self.bq_client.table_exists(table_id='test_run_batch_table_2', dataset_id='test'):
#             self.bq_client.delete_table(table_id='test_run_batch_table_2', dataset_id='test')


class TestPipelineUnitTests(unittest.TestCase):
    
    def setUp(self):
        self.bq_client = BigQueryExecutor()
        self.p_ex = pl.PipelineExecutor("tests/yaml/unit_tests.yaml")

    def test_extract_unit_tests(self):     
        
        self.assertCountEqual( 
            self.p_ex.extract_unit_tests(), 
            [ 
                ("tests/sql/table1.sql", "sql/table1_mocked.sql"), 
                ("tests/sql/table2.sql", "sql/table2_mocked.sql"), 
                ("tests/sql/table3.sql", "sql/table3_mocked.sql"), 
                ("tests/sql/table4.sql", "sql/table4_mocked.sql")
            ], 
            "unit tests well extracted" )

    def tearDown(self):
        if self.bq_client.table_exists(table_id='table1', dataset_id='test'):
            self.bq_client.delete_table(table_id='table1', dataset_id='test')
        if self.bq_client.table_exists(table_id='table2', dataset_id='test'):
            self.bq_client.delete_table(table_id='table2', dataset_id='test')
        if self.bq_client.table_exists(table_id='test_run_batch_table_1', dataset_id='test'):
            self.bq_client.delete_table(table_id='test_run_batch_table_1', dataset_id='test')
        if self.bq_client.table_exists(table_id='test_run_batch_table_2', dataset_id='test'):
            self.bq_client.delete_table(table_id='test_run_batch_table_2', dataset_id='test')

if __name__ == '__main__':
    unittest.main()
