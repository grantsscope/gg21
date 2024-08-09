SELECT
  "public"."donations"."id" AS "id",
  "public"."donations"."chain_id" AS "chain_id",
  "public"."donations"."round_id" AS "round_id",
  "public"."donations"."application_id" AS "application_id",
  "public"."donations"."donor_address" AS "donor_address",
  "public"."donations"."recipient_address" AS "recipient_address",
  "public"."donations"."project_id" AS "project_id",
  "public"."donations"."transaction_hash" AS "transaction_hash",
  "public"."donations"."block_number" AS "block_number",
  "public"."donations"."token_address" AS "token_address",
  "public"."donations"."timestamp" AS "timestamp",
  "public"."donations"."amount" AS "amount",
  "public"."donations"."amount_in_usd" AS "amount_in_usd",
  "public"."donations"."amount_in_round_match_token" AS "amount_in_round_match_token",
  CASE lower("public"."donations"."round_id")
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
  "public"."donations"
where lower(round_id) in 
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
