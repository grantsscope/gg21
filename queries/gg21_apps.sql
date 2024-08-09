SELECT
  "public"."applications"."id" AS "id",
  (
    "public"."applications"."metadata" #>> array [ 'application',
    'project',
    'title' ] :: text [ ]
  ) :: text AS "project_title",
  lower(
    "public"."applications"."metadata" #>> array [ 'application',
    'recipient' ] :: text [ ]
  ) :: text AS "recipient",
  (
    "public"."applications"."metadata" #>> array [ 'application',
    'project',
    'description' ] :: text [ ]
  ) :: text AS "description",
  "public"."applications"."chain_id" AS "chain_id",
  "public"."applications"."round_id" AS "round_id",
  "public"."applications"."project_id" AS "project_id",
  "public"."applications"."status" AS "status",
  CASE lower("public"."applications"."round_id")
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
FROM
  "public"."applications"
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
        ) 
    AND "public"."applications"."status" = 'APPROVED'