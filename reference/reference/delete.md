+++
title = "delete"
+++

## delete, keyword

The `delete` statement removes a secondary dimension from a table.

```envision
table Products = with
  [| as Product, as Category |]
  [| "Tomato", "Fresh" |]
  [| "Ships", "Dry" |]
  [| "Apple", "Dry" |]

table Categories[c] = by Products.Category

delete Products.c

// 'where' has no effect on 'Products' as dimension 'c' has been removed
where c == "Fresh" 
  show table "Products" a1b3 with // 3 lines displayed
    Products.Product
    Products.Category
```
