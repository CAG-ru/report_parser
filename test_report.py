#!/usr/bin/env python3
import unittest

from pandas import DataFrame

from report_parser.report import Report, Text

test_folder = 'test_data/'


class TestValidHTML(unittest.TestCase):
    """Тестирование парсинга файла с расширением HTML"""

    @classmethod
    def setUpClass(cls):
        """Set up for class"""
        print("setUpClass TestValidHTML")
        print("==========")

    def setUp(self):
        """Set up for test"""
        print("Set up for [" + self.shortDescription() + "]")
        self.report = Report(test_folder + 'valid_data.html')
        self.report.parse()
        self.texts = list(self.report.texts())
        self.tables = list(self.report.tables())
        self.text = self.texts[0]
        self.table = self.tables[0]

    def test_text_data_type_html(self):
        """Тип возвращаемого текста"""
        self.assertIsInstance(self.text, Text)

    def test_table_text_data_type_html(self):
        """Тип возвращаемой таблицы"""
        self.assertIsInstance(self.table, DataFrame)

    def test_number_of_texts_html(self):
        """Количество объектов типа Text"""
        self.assertEqual(len(self.texts), 1)

    def test_number_of_tables_html(self):
        """Количество объектов типа DataFrame"""
        self.assertEqual(len(self.tables), 1)

    def test_table_shape_rows_html(self):
        """Количество строк в итоговой таблице типа DataFrame"""
        self.assertEqual(self.table.shape[0], 3)

    def test_table_shape_cols_html(self):
        """Количество столбцов в итоговой таблице типа DataFrame"""
        self.assertEqual(self.table.shape[1], 3)

    def test_table_parse_colspan_html(self):
        """Содержимое ячеек первой колонки таблицы типа DataFrame одинаковое"""
        self.assertEqual((self.table.iloc[:, 0]).nunique(), 1)

    def test_table_parse_rowspan_html(self):
        """Содержимое ячеек второй и третьей колонок первой строки таблицы типа DataFrame одинаковое"""
        self.assertEqual((self.table.iloc[0, 1:3]).nunique(), 1)

    def tearDown(self):
        """Tear down for test"""
        print("Tear down for [" + self.shortDescription() + "]")
        print('')

    @classmethod
    def tearDownClass(cls):
        """Tear down for class"""
        print("==========")
        print("tearDownClass TestValidHTML")


class TestValidDOCX(unittest.TestCase):
    """Тестирование парсинга файла с расширением DOCX"""

    @classmethod
    def setUpClass(cls):
        """Set up for class"""
        print("setUpClass TestValidDOCX")
        print("==========")

    def setUp(self):
        """Set up for test"""
        print("Set up for [" + self.shortDescription() + "]")
        self.report = Report(test_folder + 'valid_data.docx')
        self.report.parse()
        self.texts = list(self.report.texts())
        self.tables = list(self.report.tables())
        self.text = self.texts[0]
        self.table = self.tables[0]

    def test_text_data_type_docx(self):
        """Тип возвращаемого текста"""
        self.assertIsInstance(self.text, Text)

    def test_table_text_data_type_docx(self):
        """Тип возвращаемой таблицы"""
        self.assertIsInstance(self.table, DataFrame)

    def test_number_of_texts_docx(self):
        """Количество объектов типа Text"""
        self.assertEqual(len(self.texts), 1)

    def test_number_of_tables_docx(self):
        """Количество объектов типа DataFrame"""
        self.assertEqual(len(self.tables), 1)

    def test_table_shape_rows_docx(self):
        """Количество строк в итоговой таблице типа DataFrame"""
        self.assertEqual(self.table.shape[0], 13)

    def test_table_shape_cols_docx(self):
        """Количество столбцов в итоговой таблице типа DataFrame"""
        self.assertEqual(self.table.shape[1], 6)

    def test_table_parse_colspan_first_docx(self):
        """Содержимое ячеек первой колонки в строках с первой по вторую таблицы типа DataFrame одинаковое"""
        self.assertEqual((self.table.iloc[0:2, 0]).nunique(), 1)

    def test_table_parse_colspan_second_docx(self):
        """Содержимое ячеек второй колонки в строках с первой по вторую таблицы типа DataFrame одинаковое"""
        self.assertEqual((self.table.iloc[0:2, 1]).nunique(), 1)

    def test_table_parse_rowspan_docx(self):
        """Содержимое ячеек в колонках с третьей по седьмую первой строки таблицы типа DataFrame одинаковое"""
        self.assertEqual((self.table.iloc[0, 2:6]).nunique(), 1)

    def tearDown(self):
        """Tear down for test"""
        print("Tear down for [" + self.shortDescription() + "]")
        print('')

    @classmethod
    def tearDownClass(cls):
        """Tear down for class"""
        print("==========")
        print("tearDownClass TestValidDOCX")


class TestValidXLSX(unittest.TestCase):
    """Тестирование парсинга файла с расширением XLSX"""

    @classmethod
    def setUpClass(cls):
        """Set up for class"""
        print("setUpClass TestValidXLSX")
        print("==========")

    def setUp(self):
        """Set up for test"""
        print("Set up for [" + self.shortDescription() + "]")
        self.report = Report(test_folder + 'valid_data.xlsx')
        self.report.parse()
        self.texts = list(self.report.texts())
        self.tables = list(self.report.tables())
        self.table = self.tables[0]

    def test_table_text_data_type_xlsx(self):
        """Тип возвращаемой таблицы"""
        self.assertIsInstance(self.table, DataFrame)

    def test_number_of_texts_xlsx(self):
        """Количество объектов типа Text"""
        self.assertEqual(len(self.texts), 0)

    def test_number_of_tables_xlsx(self):
        """Количество объектов типа DataFrame"""
        self.assertEqual(len(self.tables), 1)

    def test_table_shape_rows_xlsx(self):
        """Количество строк в итоговой таблице типа DataFrame"""
        self.assertEqual(self.table.shape[0], 27)

    def test_table_shape_cols_xlsx(self):
        """Количество столбцов в итоговой таблице типа DataFrame"""
        self.assertEqual(self.table.shape[1], 13)

    def test_table_parse_colspan_xlsx(self):
        """Содержимое ячеек первой строки таблицы типа DataFrame одинаковое"""
        self.assertEqual((self.table.iloc[0, :]).nunique(), 1)

    def test_table_parse_rowspan_xlsx(self):
        """Содержимое ячеек первой колонки в строках с пятой по двадцать шестую таблицы типа DataFrame одинаковое"""
        self.assertEqual((self.table.iloc[5:, 0]).nunique(), 1)

    def test_table_parse_rows_xlsx(self):
        """Содержимое ячеек с четвертой по седьмую второй строки таблицы типа DataFrame одинаковое"""
        self.assertEqual((self.table.iloc[1, 3:7]).nunique(), 1)

    def tearDown(self):
        """Tear down for test"""
        print("Tear down for [" + self.shortDescription() + "]")
        print('')

    @classmethod
    def tearDownClass(cls):
        """Tear down for class"""
        print("==========")
        print("tearDownClass TestValidXLSX")


class TestValidXLS(unittest.TestCase):
    """Тестирование парсинга файла с расширением XLS"""

    @classmethod
    def setUpClass(cls):
        """Set up for class"""
        print("setUpClass TestValidXLS")
        print("==========")

    def setUp(self):
        """Set up for test"""
        print("Set up for [" + self.shortDescription() + "]")
        self.report = Report(test_folder + 'valid_data.xls')
        self.report.parse()
        self.texts = list(self.report.texts())
        self.tables = list(self.report.tables())
        self.table = self.tables[0]

    def test_table_text_data_type_xls(self):
        """Тип возвращаемой таблицы"""
        self.assertIsInstance(self.table, DataFrame)

    def test_number_of_texts_xls(self):
        """Количество объектов типа Text"""
        self.assertEqual(len(self.texts), 0)

    def test_number_of_tables_xls(self):
        """Количество объектов типа DataFrame"""
        self.assertEqual(len(self.tables), 1)

    def test_table_shape_rows_xls(self):
        """Количество строк в итоговой таблице типа DataFrame"""
        self.assertEqual(self.table.shape[0], 11)

    def test_table_shape_cols_xls(self):
        """Количество столбцов в итоговой таблице типа DataFrame"""
        self.assertEqual(self.table.shape[1], 13)

    def test_table_parse_colspan_xls(self):
        """Содержимое ячеек первой строки таблицы типа DataFrame одинаковое"""
        self.assertEqual((self.table.iloc[0, :]).nunique(), 1)

    def test_table_parse_colspan_new_xls(self):
        """Содержимое ячеек второй строки таблицы типа DataFrame одинаковое"""
        self.assertEqual((self.table.iloc[1, :]).nunique(), 1)

    def test_table_parse_rowspan_xls(self):
        """Содержимое ячеек c третьей по шестую четвертой строки таблицы типа DataFrame одинаковое"""
        self.assertEqual((self.table.iloc[3, 3:7]).nunique(), 1)

    def test_table_parse_rowspan_new_xls(self):
        """Содержимое ячеек c седьмую по девятую четвертой строки таблицы типа DataFrame одинаковое"""
        self.assertEqual((self.table.iloc[3, 7:10]).nunique(), 1)

    def test_table_parse_rowspan_newspan_xls(self):
        """Содержимое ячеек в первой колонке в строках с седьмой по девятую таблицы типа DataFrame одинаковое"""
        self.assertEqual((self.table.iloc[6:9, 0]).nunique(), 1)

    def tearDown(self):
        """Tear down for test"""
        print("Tear down for [" + self.shortDescription() + "]")
        print('')

    @classmethod
    def tearDownClass(cls):
        """Tear down for class"""
        print("==========")
        print("tearDownClass TestValidXLS")


if __name__ == '__main__':
    unittest.main()
