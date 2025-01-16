from sqlalchemy import Integer, String


def test_model_structure_table_exists(db_inspector):
    assert db_inspector.has_table("product_image")


def test_model_structure_column_data_types(db_inspector):
    table = "product_image"
    columns = {column["name"]: column for column in db_inspector.get_columns(table)}

    assert isinstance(columns["id"]["type"], Integer)
    assert isinstance(columns["alternative_text"]["type"], String)
    assert isinstance(columns["url"]["type"], String)
    assert isinstance(columns["order"]["type"], Integer)
    assert isinstance(columns["product_line_id"]["type"], Integer)


def test_model_structure_nullable_constraints(db_inspector):
    table = "product_image"
    columns = db_inspector.get_columns(table)

    expected_nullable = {
        "id": False,
        "alternative_text": False,
        "url": False,
        "order": False,
        "product_line_id": False,
    }

    for column in columns:
        column_name = column["name"]
        assert expected_nullable[column_name] == column["nullable"], (
            f"column '{column_name}' is not nullable as expected"
        )


def test_model_structure_foreign_keys(db_inspector):
    table = "product_image"
    foreign_keys = db_inspector.get_foreign_keys(table)

    assert any("product_line_id" in fk["constrained_columns"] for fk in foreign_keys)


def test_model_structure_column_constraints(db_inspector):
    table = "product_image"
    constraints = db_inspector.get_check_constraints(table)

    assert any(
        constraint["name"] == "product_image_order_range" for constraint in constraints
    )
    assert any(
        constraint["name"] == "product_image_alternative_length"
        for constraint in constraints
    )
    assert any(
        constraint["name"] == "product_image_url_length" for constraint in constraints
    )


def test_model_structure_column_lengths(db_inspector):
    table = "product_image"
    columns = {column["name"]: column for column in db_inspector.get_columns(table)}

    columns["alternative_text"]["type"].length == 100
    columns["url"]["type"].length == 100


def test_model_structure_unique_constraints(db_inspector):
    table = "product_image"
    constraints = db_inspector.get_unique_constraints(table)

    assert any(
        constraint["name"] == "uq_product_image_order_product_line_id"
        for constraint in constraints
    )
