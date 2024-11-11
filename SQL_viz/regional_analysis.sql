WITH regional_stats AS (
                    SELECT 
                        CASE 
                            WHEN l.state IN ('sp', 'rj', 'mg', 'es') THEN 'Sudeste'
                            WHEN l.state IN ('pr', 'sc', 'rs') THEN 'Sul'
                            WHEN l.state IN ('ba', 'ce', 'pe', 'pb', 'ma', 'pi', 'rn', 'se', 'al') THEN 'Nordeste'
                            WHEN l.state IN ('mt', 'ms', 'go', 'df') THEN 'Centro-Oeste'
                            ELSE 'Norte'
                        END as region,
                        COUNT(*) as total_properties,
                        ROUND(AVG(price)::numeric, 2) as avg_price,
                        ROUND(AVG(price_per_m2)::numeric, 2) as avg_price_per_m2,
                        ROUND(AVG(area_util)::numeric, 2) as avg_area
                    FROM properties p
                    JOIN locations l ON p.location_id = l.location_id
                    GROUP BY region
                )
                SELECT 
                    region,
                    total_properties,
                    avg_price,
                    avg_price_per_m2,
                    avg_area,
                    ROUND(100.0 * total_properties / SUM(total_properties) OVER (), 2) as market_share_percentage
                FROM regional_stats
                ORDER BY avg_price DESC;