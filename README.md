# fastAPI-learning-project

```mermaid
erDiagram
    Category {
      integer id PK "NN"
      char(100) name "NN"
      char(120) slug UK "NN"
      boolean is_active "NN DV(False)"
      integer level "NN DV(100)"
      integer parent_id FK
    }

    Product {
      integer id PK "NN"
      UUID pid UK "NN"
      string(200) name UK "NN"
      string(220) slug UK "NN"
      text description
      boolean is_digital "NN DF(False)"
      datetime created_at "NN"
      datetime updated_at "NN"
      boolean is_active "NN DF(False)"
      enum stock_status "NN DV(OutOfStock)"
      integer category_id FK "NN"
    }

    Category |o--o{ Category : "has parent"
    Product }o--|| Category: "belongs to"

```
