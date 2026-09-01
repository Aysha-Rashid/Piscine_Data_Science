
DROP TABLE IF EXISTS customers_fused;

CREATE TABLE customers_fused AS

WITH ranked_items AS (
    SELECT *,
        ROW_NUMBER() OVER (
            PARTITION BY product_id
            ORDER BY
                (
                    (category_id IS NOT NULL)::int +
                    (category_code IS NOT NULL)::int +
                    (brand IS NOT NULL)::int
                ) DESC,
                category_id NULLS LAST,
                category_code NULLS LAST,
                brand NULLS LAST
        ) AS rn
    FROM item
)

SELECT
    c.event_time,
    c.event_type,
    c.product_id,
    c.price,
    c.user_id,
    c.user_session,
    i.category_id,
    i.category_code,
    i.brand
FROM customers AS c
LEFT JOIN ranked_items AS i
    ON c.product_id = i.product_id
   AND i.rn = 1;

DROP TABLE customers;

ALTER TABLE customers_fused
RENAME TO customers;

SELECT COUNT(*) FROM customers;