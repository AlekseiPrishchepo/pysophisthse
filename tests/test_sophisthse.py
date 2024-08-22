import pytest
import requests_mock
from sophisthse.sophisthse import sophisthse
from sophisthse.constants import tables_url

series_name_q = "HHI_Q_I"
series_name_m = "HHI_M_I"
series_name_y = "HHI_Y_DIRI"

data_path = "data"


@requests_mock.Mocker(kw="mock")
def test_list_tables(**kwargs):

    # Create an instance of sophisthse
    sophisthse_instance = sophisthse()

    # Mock the response
    with open(f"{data_path}/index.html", "r", encoding="cp1251") as f:
        result = f.read()
    kwargs["mock"].get(tables_url, text=result)

    # Test case 1: Check if the returned DataFrame has the expected columns
    df = sophisthse_instance.list_tables()
    expected_columns = ["date", "name"]
    assert all(col in df.columns for col in expected_columns)

    # Test case 2: Check if the returned DataFrame is not empty
    assert not df.empty

    # Test case 3: Check if the 'date' column is of datetime type
    assert df["date"].dtype == "datetime64[ns]"

    # Test case 4: Check if the 'name' column does not contain '.htm' extension
    assert not df["name"].str.contains(r"\.htm$").any()


@requests_mock.Mocker(kw="mock")
def test_get_table_q(**kwargs):

    # Create an instance of sophisthse
    sophisthse_instance = sophisthse()

    # Mock the response
    with open(f"{data_path}/{series_name_q}.htm", "r", encoding="cp1251") as f:
        result = f.read()
    table_url = sophisthse_instance.get_table_url(series_name_q)
    kwargs["mock"].get(table_url, text=result)

    # Test case 1: Check if the returned DataFrame is not empty
    df = sophisthse_instance.get_table(series_name_q)
    assert not df.empty

    # Test case 2: Check if the returned DataFrame has the expected columns
    expected_columns = ["HHI_Q_DIRI", "HHI_Q_DIRI_SA", "HHI_Q"]
    assert all(col in df.columns for col in expected_columns)

    # Test case 3: Check if the returned DataFrame is indexed by "T"
    assert df.index.name == "T"

    # Test case 4: Check if the verbose flag affects the output
    sophisthse_instance.verbose = True
    df = sophisthse_instance.get_table(series_name_q)
    assert not df.empty

    # Test case 5: Check if the function raises an exception for invalid series name
    with pytest.raises(Exception):
        sophisthse_instance.get_table("invalid_series_name")


@requests_mock.Mocker(kw="mock")
def test_get_table_m(**kwargs):

    # Create an instance of sophisthse
    sophisthse_instance = sophisthse()

    # Mock the response
    with open(f"{data_path}/{series_name_m}.htm", "r", encoding="cp1251") as f:
        result = f.read()
    table_url = sophisthse_instance.get_table_url(series_name_m)
    kwargs["mock"].get(table_url, text=result)

    # Test case 1: Check if the returned DataFrame is not empty
    df = sophisthse_instance.get_table(series_name_m)
    assert not df.empty

    # Test case 2: Check if the returned DataFrame has the expected columns
    expected_columns = ["HHI_M_DIRI", "HHI_M_DIRI_SA", "HHI_M"]
    assert all(col in df.columns for col in expected_columns)

    # Test case 3: Check if the returned DataFrame is indexed by "T"
    assert df.index.name == "T"

    # Test case 4: Check if the verbose flag affects the output
    sophisthse_instance.verbose = True
    df = sophisthse_instance.get_table(series_name_m)
    assert not df.empty

    # Test case 5: Check if the function raises an exception for invalid series name
    with pytest.raises(Exception):
        sophisthse_instance.get_table("invalid_series_name")

    # Test case 6: Check if decimal values are correctly parsed
    assert df.iloc[0, 1] == 85.4


@requests_mock.Mocker(kw="mock")
def test_get_table_y(**kwargs):

    # Create an instance of sophisthse
    sophisthse_instance = sophisthse()

    # Mock the response
    with open(f"{data_path}/{series_name_y}.htm", "r", encoding="cp1251") as f:
        result = f.read()
    table_url = sophisthse_instance.get_table_url(series_name_y)
    kwargs["mock"].get(table_url, text=result)

    # Test case 1: Check if the returned DataFrame is not empty
    df = sophisthse_instance.get_table(series_name_y)
    assert not df.empty

    # Test case 2: Check if the returned DataFrame has the expected columns
    expected_columns = ["HHI_C_Y", "HHI_R_Y"]
    assert all(col in df.columns for col in expected_columns)

    # Test case 3: Check if the returned DataFrame is indexed by "T"
    assert df.index.name == "T"

    # Test case 4: Check if the verbose flag affects the output
    sophisthse_instance.verbose = True
    df = sophisthse_instance.get_table(series_name_y)
    assert not df.empty

    # Test case 5: Check if the function raises an exception for invalid series name
    with pytest.raises(Exception):
        sophisthse_instance.get_table("invalid_series_name")
