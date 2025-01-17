from sqlalchemy import Integer


def test_model_structure_table_exists(db_inspector):
    assert db_inspector.has_table("product_product_type")


def test_model_structure_column_data_types(db_inspector):
    table = "product_product_type"
    columns = {column["name"]: column for column in db_inspector.get_columns(table)}

    assert isinstance(columns["id"]["type"], Integer)
    assert isinstance(columns["product_id"]["type"], Integer)
    assert isinstance(columns["product_type_id"]["type"], Integer)


def test_model_structure_nullable_constraints(db_inspector):
    table = "product_product_type"
    columns = db_inspector.get_columns(table)

    expected_nullables = {
        "id": False,
        "product_id": False,
        "product_type_id": False,
    }

    for column in columns:
        column_name = column["name"]
        assert column["nullable"] == expected_nullables[column_name], (
            f"Column '{column_name}' is not nullable as expected"
        )


def test_model_structure_unique_cosntraints(db_inspector):
    table = "product_product_type"
    constraints = db_inspector.get_unique_constraints(table)

    assert any(
        constraint["name"] == "uq_product_product_type" for constraint in constraints
    )


def test_model_structure_foreign_keys(db_inspector):
    table = "product_product_type"
    foreign_keys = db_inspector.get_foreign_keys(table)

    assert any(
        "product_id" in foreign_key["constrained_columns"]
        for foreign_key in foreign_keys
    )
    assert any(
        "product_type_id" in foreign_key["constrained_columns"]
        for foreign_key in foreign_keys
    )
