SELECT 
    warehouse_block, 
    COUNT(id) as total_shipments, 
    ROUND(AVG(cost_of_the_product)) AS avg_cost,

    -- Equivalent to sla_status in SQL:
    SUM(CASE WHEN reached_on_time = 0 THEN 1 ELSE 0 END) AS delayed_shipments,

    -- Calculate the percentage of delayed shipments:
    ROUND(
        (SUM(CASE WHEN reached_on_time = 0 THEN 1.0 ELSE 0.0 END) * 100.0 / COUNT(id)), 
        2
    ) AS delay_rate_pct

FROM shipments
GROUP BY warehouse_block
ORDER BY delay_rate_pct DESC;