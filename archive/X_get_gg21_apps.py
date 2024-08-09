import duckdb
import json
import pandas as pd

GATEWAY_URL = "https://grantsdataportal.xyz/data/"

print('Starting')

QUERY = f"""
            SELECT  id,
                    metadata,
                    chain_id,
                    round_id,
                    project_id,
                    status,    
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
            FROM '{GATEWAY_URL}/allo_applications.parquet' AS d
            WHERE    
                (
                    (round_id = '389' AND chain_id = '42161') OR -- Thriving Arbitrum Summer
                    (round_id = '11' AND chain_id = '42220') OR -- Real World Builders
                    (round_id = '388' AND chain_id = '42161') OR  -- Climate Solutions Round
                    (round_id = '385' AND chain_id = '42161') OR -- Web3 Grants Ecosystem Advancement
                    (round_id = '44' AND chain_id = '10') OR -- Asia Round
                    (round_id = '57' AND chain_id = '10') OR -- Token Engineering the Superchain
                    (round_id = '14' AND chain_id = '42220') OR  -- Regen Coordi-Nation Genesis
                    (round_id = '386' AND chain_id = '42161') OR -- OpenCivics Collaborative Research Round
                    (round_id = '387' AND chain_id = '42161') OR -- GG21 DeSci Round
                    (round_id = '383' AND chain_id = '42161') OR -- Decentralized Science and Art in Psychedelics
                    (round_id = '384' AND chain_id = '42161')    -- CollabTech Round and Thresholds Experiment
                ) AND
                status = 'APPROVED';
        """

print('Executing')
query_all_result = duckdb.sql(QUERY).df()

# Function to extract description and recipient from the metadata JSON string
def extract_info(metadata):
    try:
        # Parse the JSON string
        metadata_dict = json.loads(metadata)
        
        # Extract the title
        title = metadata_dict['application']['project']['title']
        
        # Extract the description
        description = metadata_dict['application']['project']['description']
        
        # Extract the recipient
        recipient = metadata_dict['application']['recipient']
        
        return title, description, recipient
    
    except (json.JSONDecodeError, KeyError):
        return None, None, None  # Handle cases where JSON parsing fails or keys are missing

# Apply the function to the 'metadata' column to create new 'description' and 'recipient' columns
query_all_result['project_title'], query_all_result['description'], query_all_result['recipient'] = zip(*query_all_result['metadata'].apply(extract_info))

query_all_result['recipient'] = query_all_result['recipient'].str.lower()

# Write the updated DataFrame to a CSV file
query_all_result.to_csv('./data/apps_21.csv', index=False)