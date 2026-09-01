WITH remove_duplicates AS(
	SELECT ctid, 
		lag(event_time) 
			over (PARTITION BY event_type, product_id, price, user_id, user_session
			ORDER BY event_time) AS previous_time, 
		event_time - lag(event_time) 
			over (PARTITION BY event_type, product_id, price, user_id, user_session
			ORDER BY event_time) as time_difference
	FROM customers
),

duplicates AS(
	SELECT ctid FROM remove_duplicates
	WHERE time_difference <= INTERVAL '1 seconds'
)

DELETE FROM customers
WHERE ctid IN (
	SELECT ctid
	FROM duplicates
)

-- SELECT COUNT(*) FROM customers;
