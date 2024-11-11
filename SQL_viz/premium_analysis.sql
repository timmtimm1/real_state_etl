WITH premium_properties AS (
                    SELECT *,
                        NTILE(10) OVER (ORDER BY price) as price_decile
                    FROM properties
                )
                SELECT 
                    COUNT(*) as total_premium_properties,
                    ROUND(AVG(area_util)::numeric, 2) as avg_area,
                    ROUND(AVG(bedrooms)::numeric, 1) as avg_bedrooms,
                    ROUND(AVG(bathrooms)::numeric, 1) as avg_bathrooms,
                    ROUND(AVG(parking_spots)::numeric, 1) as avg_parking_spots,
                    ROUND(AVG(price)::numeric, 2) as avg_price,
                    ROUND(AVG(price_per_m2)::numeric, 2) as avg_price_per_m2
                FROM premium_properties
                WHERE price_decile = 10;