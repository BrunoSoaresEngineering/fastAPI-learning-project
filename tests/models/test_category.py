from sqlalchemy import Boolean, Integer, String


def test_model_structure_table_exists(db_inspector):
    assert db_inspector.has_table("category")


def test_model_structure_column_data_types(db_inspector):
    table = "category"
    columns = {column["name"]: column for column in db_inspector.get_columns(table)}

    assert isinstance(columns["id"]["type"], Integer)
    assert isinstance(columns["name"]["type"], String)
    assert isinstance(columns["slug"]["type"], String)
    assert isinstance(columns["is_active"]["type"], Boolean)
    assert isinstance(columns["level"]["type"], Integer)
    assert isinstance(columns["parent_id"]["type"], Integer)


def test_model_structure_nullable_constraints(db_inspector):
    table = "category"
    columns = db_inspector.get_columns(table)

    expected_nullable = {
        "id": False,
        "name": False,
        "slug": False,
        "is_active": False,
        "level": False,
        "parent_id": True,
    }

    for column in columns:
        column_name = column["name"]
        assert column["nullable"] == expected_nullable.get(
            column_name
        ), f"column '{column_name}' nullable not set as expected"


def test_model_structure_column_constraints(db_inspector):
    table = "category"
    constraints = db_inspector.get_check_constraints(table)

    assert any(constraint["name"] == "name_length_check" for constraint in constraints)
    assert any(constraint["name"] == "slug_length_check" for constraint in constraints)
