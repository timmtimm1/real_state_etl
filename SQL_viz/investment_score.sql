WITH investment_metrics AS (
                    SELECT 
                        l.city,
                        l.state,
                        COUNT(*) as total_listings,
                        AVG(p.price_per_m2) as avg_price_per_m2,
                        STDDEV(p.price_per_m2) as price_std,
                        percentile_cont(0.5) WITHIN GROUP (ORDER BY p.price_per_m2) as median_price_per_m2,
                        AVG(p.area_util) as avg_area,
                        AVG(p.bedrooms) as avg_bedrooms,
                        AVG(p.bathrooms) as avg_bathrooms,
                        AVG(p.parking_spots) as avg_parking,
                        COUNT(*) / MAX(COUNT(*)) OVER () as market_density_score
                    FROM properties p
                    JOIN locations l ON p.location_id = l.location_id
                    GROUP BY l.city, l.state
                    HAVING COUNT(*) > 20
                )
                SELECT 
                    city,
                    state,
                    total_listings,
                    ROUND(avg_price_per_m2::numeric, 2) as avg_price_per_m2,
                    ROUND(median_price_per_m2::numeric, 2) as median_price_per_m2,
                    ROUND((
                        (0.4 * (avg_price_per_m2 / MAX(avg_price_per_m2) OVER ())) +
                        (0.2 * (1 - (price_std / avg_price_per_m2))) +
                        (0.2 * market_density_score) +
                        (0.2 * (
                            (avg_bedrooms / 4) + 
                            (avg_bathrooms / 3) + 
                            (avg_parking / 2)
                        ) / 3)
                    ) * 100::numeric, 2) as investment_score
                FROM investment_metrics
                WHERE city IS NOT NULL
                ORDER BY investment_score DESC
                LIMIT 20;