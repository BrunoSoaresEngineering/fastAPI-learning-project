from sqlalchemy import Integer, String


def test_model_structure_table_exists(db_inspector):
    assert db_inspector.has_table("product_type")


def test_model_structure_column_data_types(db_inspector):
    table = "product_type"
    columns = {column["name"]: column for column in db_inspector.get_columns(table)}

    assert isinstance(columns["id"]["type"], Integer)
    assert isinstance(columns["name"]["type"], String)
    assert isinstance(columns["level"]["type"], Integer)
    assert isinstance(columns["parent"]["type"], Integer)


def test_model_structure_nullable_constraints(db_inspector):
    table = "product_type"
    columns = db_inspector.get_columns(table)

    expected_nullables = {"id": False, "name": False, "level": False, "parent": True}

    for column in columns:
        column_name = column["name"]
        assert expected_nullables[column_name] == column["nullable"], (
            f"Column '{column_name}' is not nullable as expected"
        )


def test_model_structure_column_constraints(db_inspector):
    table = "product_type"
    constraints = db_inspector.get_check_constraints(table)

    assert any(
        constraint["name"] == "product_type_name_length" for constraint in constraints
    )


def test_model_structure_unique_constraints(db_inspector):
    table = "product_type"
    constraints = db_inspector.get_unique_constraints(table)

    assert any(
        constraint["name"] == "uq_product_type_name_level" for constraint in constraints
    )


def test_model_structure_foreign_keys(db_inspector):
    table = "product_type"
    foreign_keys = db_inspector.get_foreign_keys(table)

    assert any(
        "parent" in foreign_key["constrained_columns"] for foreign_key in foreign_keys
    )


def test_model_structure_column_lengths(db_inspector):
    table = "product_type"
    columns = {column["name"]: column for column in db_inspector.get_columns(table)}

    columns["name"]["type"].length == 100
