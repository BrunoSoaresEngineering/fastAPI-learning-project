from sqlalchemy import Integer


def test_model_structure_table_exists(db_inspector):
    assert db_inspector.has_table("product_line_attribute_value")


def test_model_structure_column_data_types(db_inspector):
    table = "product_line_attribute_value"
    columns = {column["name"]: column for column in db_inspector.get_columns(table)}

    assert isinstance(columns["id"]["type"], Integer)
    assert isinstance(columns["attribute_value_id"]["type"], Integer)
    assert isinstance(columns["product_line_id"]["type"], Integer)


def test_model_structure_nullable_constraints(db_inspector):
    table = "product_line_attribute_value"
    columns = db_inspector.get_columns(table)

    expected_nullables = {
        "id": False,
        "attribute_value_id": False,
        "product_line_id": False,
    }

    for column in columns:
        column_name = column["name"]
        assert column["nullable"] == expected_nullables[column_name], (
            f"Column '{column_name}' is not nullable as expected"
        )


def test_model_structure_unique_cosntraints(db_inspector):
    table = "product_line_attribute_value"
    constraints = db_inspector.get_unique_constraints(table)

    assert any(
        constraint["name"] == "uq_product_line_attribute_value"
        for constraint in constraints
    )


def test_model_structure_foreign_keys(db_inspector):
    table = "product_line_attribute_value"
    foreign_keys = db_inspector.get_foreign_keys(table)

    assert any(
        "product_line_id" in foreign_key["constrained_columns"]
        for foreign_key in foreign_keys
    )
    assert any(
        "attribute_value_id" in foreign_key["constrained_columns"]
        for foreign_key in foreign_keys
    )
