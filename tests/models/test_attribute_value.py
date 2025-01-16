from sqlalchemy import Integer, String


def test_model_structure_table_exists(db_inspector):
    assert db_inspector.has_table("attribute_value")


def test_model_structure_column_data_types(db_inspector):
    table = "attribute_value"
    columns = {column["name"]: column for column in db_inspector.get_columns(table)}

    assert isinstance(columns["id"]["type"], Integer)
    assert isinstance(columns["attribute_value"]["type"], String)
    assert isinstance(columns["attribute_id"]["type"], Integer)


def test_model_structure_nullable_constraints(db_inspector):
    table = "attribute_value"
    columns = db_inspector.get_columns(table)

    expected_nullables = {"id": False, "attribute_value": False, "attribute_id": False}

    for column in columns:
        column_name = column["name"]
        assert expected_nullables[column_name] == column["nullable"]


def test_model_structure_foreign_keys(db_inspector):
    table = "attribute_value"
    foreign_keys = db_inspector.get_foreign_keys(table)

    assert any(
        "attribute_id" in foreign_key["constrained_columns"]
        for foreign_key in foreign_keys
    )


def test_model_structure_column_constraints(db_inspector):
    table = "attribute_value"
    constraints = db_inspector.get_check_constraints(table)
    print(constraints)

    assert any(
        constraint["name"] == "attribute_value_length" for constraint in constraints
    )


def test_model_structure_unique_constraints(db_inspector):
    table = "attribute_value"
    constraints = db_inspector.get_unique_constraints(table)

    assert any(
        constraint["name"] == "uq_attribute_value_attribute_id"
        for constraint in constraints
    )


def test_model_structure_column_length(db_inspector):
    table = "attribute_value"
    columns = {column["name"]: column for column in db_inspector.get_columns(table)}

    assert columns["attribute_value"]["type"].length == 100
