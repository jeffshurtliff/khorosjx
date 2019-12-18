# -*- coding: utf-8 -*-
"""
:Module:        khorosjx.utils.df_utils
:Synopsis:      Useful tools and utilities to assist in importing, manipulating and exporting pandas dataframes
:Usage:         ``from khorosjx import df_utils``
:Example:       TBD
:Created By:    Jeff Shurtliff
:Last Modified: Jeff Shurtliff
:Modified Date: 18 Dec 2019
"""

import pandas as pd


# Define function to convert a list of dictionaries to a pandas dataframe
def convert_dict_list_to_dataframe(dict_list, column_names=[]):
    """This function converts a list of dictionaries into a pandas dataframe.

    :param dict_list: List of dictionaries
    :type dict_list: list
    :param column_names: The column names for the dataframe (Optional)
    :type column_names: list
    :returns: A pandas dataframe of the data
    """
    # Identify the dataframe column names
    if len(column_names) == 0:
        for field_name in dict_list[0].keys():
            column_names.append(field_name)

    # Identify the data for each column
    df_data = []
    for idx in range(0, len(dict_list)):
        row_data = []
        for field_value in dict_list[idx].values():
            row_data.append(field_value)
        df_data.append(row_data)

    # Create and return the dataframe
    dataframe = pd.DataFrame(df_data, columns=column_names)
    return dataframe


def import_csv(file_path, delimiter=",", column_names=[], columns_to_return=[], has_headers=True):
    """This function imports a CSV file to generate a dataframe.

    :param file_path: The absolute path to the CSV file to be imported
    :type file_path: str
    :param delimiter: The column delimiter utilized in the CSV
    :type delimiter: str
    :param column_names: The column names to use with the imported dataframe (Optional)
    :type column_names: list
    :param columns_to_return: Determines which of the columns should actually be returned (Default: all columns)
    :param has_headers: Defines whether or not the data in the file has column headers (Default: ``True``)
    :type has_headers: bool
    :returns: The imported data as a pandas dataframe
    :raises: FileNotFoundError, TypeError
    """
    # Determine the appropriate use case and then import and return the dataframe
    if has_headers is False and len(column_names) == 0:
        if len(columns_to_return) == 0:                                             # Use Case: Headless
            dataframe = pd.read_csv(file_path, sep=delimiter, header=None)
        else:                                                                       # Use Case: Headless Filtered
            dataframe = pd.read_csv(file_path, sep=delimiter, header=None, usecols=columns_to_return)
    else:
        if len(column_names) > 0 and len(columns_to_return) > 0:                    # Use Case: Custom Filtered
            dataframe = pd.read_csv(file_path, sep=delimiter, names=column_names)
            dataframe = dataframe[columns_to_return]
        elif len(column_names) > 0 and len(columns_to_return) == 0:                 # Use Case: Custom
            dataframe = pd.read_csv(file_path, sep=delimiter, names=column_names)
        elif len(column_names) == 0 and len(columns_to_return) > 0:                 # Use Case: Filtered
            dataframe = pd.read_csv(file_path, sep=delimiter, usecols=columns_to_return)
        else:                                                                       # Use Case: Default
            dataframe = pd.read_csv(file_path, sep=delimiter)
    return dataframe


def import_excel(file_path, excel_sheet='', use_first_sheet=False,
                 column_names=[], columns_to_return=[], has_headers=True):
    """This function imports a Microsoft Excel file to generate a dataframe.

    :param file_path: The absolute path to the Excel file to be imported
    :type file_path: str
    :param excel_sheet: The name of the specific sheet in the file to import
    :type excel_sheet: str
    :param use_first_sheet: Defines whether or not the first sheet in the file should be used (Default: ``False``)
    :type use_first_sheet: bool
    :param column_names: The column names to use with the imported dataframe (Optional)
    :type column_names: list
    :param columns_to_return: Determines which of the columns should actually be returned (Default: all columns)
    :param has_headers: Defines whether or not the data in the file has column headers (Default: ``True``)
    :type has_headers: bool
    :returns: The imported data as a pandas dataframe
    :raises: FileNotFoundError, TypeError
    """
    # Determine the appropriate use case and then import and return the dataframe
    if excel_sheet != "" and use_first_sheet is False:
        if has_headers is False and len(column_names) == 0:
            if columns_to_return == 0:                                                  # Use Case: Headless
                excel_data = pd.read_excel(file_path, sheet_name=excel_sheet, header=None)
            else:                                                                       # Use Case: Headless Filtered
                excel_data = pd.read_excel(file_path, sheet_name=excel_sheet, header=None, usecols=columns_to_return)
    else:
        if len(column_names) > 0 and len(columns_to_return) > 0:                        # Use Case: Custom Filtered
            excel_data = pd.read_excel(file_path, names=column_names)
            excel_data = excel_data[columns_to_return]
        elif len(column_names) > 0 and len(columns_to_return) == 0:                     # Use Case: Custom
            excel_data = pd.read_excel(file_path, names=column_names)
        elif len(column_names) == 0 and len(columns_to_return) > 0:                     # Use Case: Filtered
            excel_data = pd.read_excel(file_path, usecols=columns_to_return)
        else:                                                                           # Use Case: Default
            excel_data = pd.read_excel(file_path)
    if use_first_sheet:                                                                 # Use Case: Use First Sheet
        excel_data = excel_data[0]
    return excel_data
