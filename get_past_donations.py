import duckdb

GATEWAY_URL = "https://grantsdataportal.xyz/data/"

print('Starting')

QUERY = f"""
            SELECT *
            FROM '{GATEWAY_URL}/allo_donations.parquet' AS d
            WHERE lower(d.round_id) in 
                (
                '25',
                '23',
                '24',
                '27',
                '26',
                '9',
                '31',
                '29',
                '28',
                '36',
                '39',
                '0xa1d52f9b5339792651861329a046dd912761e9a9',
                '0x98720dd1925d34a2453ebc1f91c9d48e7e89ec29',
                '0xd4cc0dd193c7dc1d665ae244ce12d7fab337a008',
                '0x5eb890e41c8d2cff75ea942085e406bb90016561',
                '0x0f0b9d9f72c1660905c57864e79ceb409ada0c9e',
                '0xe60a569ec8aac2045d9fda306dc2a16cc1e52a90',
                '0x6726fe9c89fb04eaef388c11cf55be6aa0a62fb9',
                '0xe168ac27b7c32db85478a6807640c8bca1220d15',
                '0x79115c9114055f16bb5b0e9bbfa450844d0fcb3a',
                '0x3ac78e1ae5086904d53b41c747188216789f59a7',
                '0xc34745b3852df32d5958be88df2bee0a83474001',
                '0xa7608d95a93cc684f2719323d40cbd0f59afe7d4',
                '0x4727e3265706c59dbc31e7c518960f4f843bb4da',
                '0x7f9415761afbd82e3fe2fd9e878fa643184bc729',
                '0x36f548e082b09b0cec5b3f5a7b78953c75de5e74',
                '0xc08008d47e3deb10b27fc1a75a96d97d11d58cf8',
                '0x40511f88b87b69496a3471cdbe1d3d25ac68e408',
                '0xc9a01d3d2505d9d2418dd2da64d06cf53fd403a0',
                '0xd309defd59c0b8792b14197eaa40043d9625b22b',
                '0xb5c0939a9bb0c404b028d402493b86d9998af55e',
                '0x911ae126be7d88155aa9254c91a49f4d85b83688',
                '0x8de918f0163b2021839a8d84954dd7e8e151326d',
                '0xb6be0ecafdb66dd848b0480db40056ff94a9465d',
                '0x2871742b184633f8dc8546c6301cbc209945033e',
                '0x222ea76664ed77d18d4416d2b2e77937b76f0a35',
                '0x10be322de44389ded49c0b2b73d8c3a1e3b6d871',
                '0x5b95acf46c73fd116f0fedadcbedf453530e35d0',
                '0xc5fdf5cff79e92fac1d6efa725c319248d279200',
                '0xf591e42fdfe8e62c2085ccaadfe05f84d89d0c6',
                '0x9331fde4db7b9d9d1498c09d30149929f24cf9d5',
                '0x30c381033aa2830ceb0aa372c2e4d28f004b3db9',
                '0x69e423181f1d3e6bebf8ab88030c36da73785f26'
                )
        """

print('Executing')
query_all_result = duckdb.sql(QUERY).df()

query_all_result.to_csv('donations_18_to_20.csv')