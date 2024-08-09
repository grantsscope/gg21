import duckdb

GATEWAY_URL = "https://grantsdataportal.xyz/data"

print('Starting')

QUERY = f"""
            SELECT *,
            CASE lower(d.round_id)
                WHEN '389' THEN 'Thriving Arbitrum Summer'
                WHEN '11' THEN 'Real World Builders'
                WHEN '388' THEN 'Climate Solutions Round'
                WHEN '385' THEN 'Web3 Grants Ecosystem Advancement'
                WHEN '44' THEN 'Asia Round'
                WHEN '57' THEN 'Token Engineering the Superchain'
                WHEN '14' THEN 'Regen Coordi-Nation Genesis'
                WHEN '386' THEN 'OpenCivics Collaborative Research Round'
                WHEN '387' THEN 'GG21 DeSci Round'
                WHEN '383' THEN 'Decentralized Science and Art in Psychedelics'
                WHEN '384' THEN 'CollabTech Round and Thresholds Experiment'
                ELSE 'Unknown Round'
            END AS round_name
        FROM '{GATEWAY_URL}/allo_donations.parquet' AS d
        WHERE lower(d.round_id) in 
            (
            '389', -- Thriving Arbitrum Summer
            '11', -- Real World Builders
            '388', -- Climate Solutions Round
            '385', -- Web3 Grants Ecosystem Advancement
            '44', -- Asia Round
            '57', -- Token Engineering the Superchain
            '14', -- Regen Coordi-Nation Genesis
            '386', -- OpenCivics Collaborative Research Round
            '387', -- GG21 DeSci Round
            '383', -- Decentralized Science and Art in Psychedelics
            '384' -- CollabTech Round and Thresholds Experiment
            )
        """

print('Executing')
query_all_result = duckdb.sql(QUERY).df()

query_all_result.to_csv('donations_21.csv')


