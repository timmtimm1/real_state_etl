WITH neighborhood_stats AS (
                    SELECT 
                        l.city,
                        l.state,
                        l.neighborhood,
                        COUNT(*) as listing_count,
                        ROUND(AVG(p.price)::numeric, 2) as avg_price,
                        ROUND(AVG(p.price_per_m2)::numeric, 2) as avg_price_per_m2,
                        ROUND(AVG(p.area_util)::numeric, 2) as avg_area
                    FROM properties p
                    JOIN locations l ON p.location_id = l.location_id
                    WHERE l.neighborhood IS NOT NULL
                    GROUP BY l.city, l.state, l.neighborhood
                    HAVING COUNT(*) > 5
                )
                SELECT *,
                    ROUND(100.0 * listing_count / SUM(listing_count) OVER (PARTITION BY city), 2) 
                    as market_share
                FROM neighborhood_stats
                ORDER BY listing_count DESC
                LIMIT 20;