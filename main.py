import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import re
import numpy as np
from database import fetch_data
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import logging

# Set up logging
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def log_dataframe(df, name):
    logging.info(f"DataFrame: {name}")
    logging.info(f"Shape: {df.shape}")
    logging.info(f"Columns: {df.columns.tolist()}")
    logging.info(f"Head:\n{df.head().to_string()}")
    logging.info(f"--- End of {name} ---\n")

def read_query_from_file(file_path):
    with open(file_path, 'r') as file:
        query = file.read()
    return query

st.set_page_config(layout="wide")
tcol1,tcol2,tcol3 = st.columns([1,8,1])

gg21_donations_query_path = './gg21/queries/gg21_donations.sql'
gg21_apps_query_path = './gg21/queries/gg21_apps.sql'


# Add header
tcol2.title("GrantsScope for GG21")
tcol2.markdown("### Get one-click personalized grantee recommendations based on your Gitcoin donation history")
tcol2.markdown('We\'re excited to offer you curated recommendations to enhance your contribution experience. Here\'s what you can expect:')
tcol2.markdown('1. **Cherished Allies:** Re-discover the grantees you\'ve supported in the past.' + '\n' \
            '2. **Community Favorites:** Explore grantees backed by the community who also champion your favorite grantees.' + '\n' \
            '3. **Likeminded Visionaries:** We\'ll introduce you to grantees similar to those you\'ve previously supported.'  + '\n' \
            '4. **New Perspectives:** Throw a light on the corners of public goods you have peeked the least.')
tcol2.link_button("Support GrantsScope in GG21", "https://explorer.gitcoin.co/#/round/42161/385/39",type="primary")


tcol2.markdown("\n \n \n")


# Get address
address = tcol2.text_input('Enter your Ethereum address below (starting "0x"):', 
							help='ENS not supported, please enter 42-character hexadecimal address starting with "0x"')

# Convert to lower case for ease of comparison
address = address.lower()

if address and address != 'None':
        
        if not re.match(r'^(0x)?[0-9a-f]{40}$', address, flags=re.IGNORECASE):
            tcol2.error('Not a valid address. Please enter a valid 42-character hexadecimal Ethereum address starting with "0x"')
        else:

            logging.info(f"User entered address: {address}")
            #STEP 0: Get historical donations, GG21 donations, and GG21 applications

            # Load historical donations from GG18 through GG20
            hist_donations_df = pd.read_csv('./gg21/data/donations_18_to_20.csv')

            # Load latest donations for GG21
            query = read_query_from_file(gg21_donations_query_path)


            # Fetch data using the query
            
            try:
                gg21_donations_df = fetch_data(query)
            except Exception as e:
                tcol2.error(f"Error fetching data: {e}",icon="🚨")            
            

            # Load latest applications for GG21
            query = read_query_from_file(gg21_apps_query_path)

            # Fetch data using the query
            try:
                gg21_apps_df = fetch_data(query)
            except Exception as e:
                tcol2.error(f"Error fetching data: {e}",icon="🚨")   

            # STEP 1: Display projects previously supported by user that are participating in GG21

            # 1.1 - Get list of projects supported by user in the past
            supported_by_user = hist_donations_df[hist_donations_df['donor_address'] == address].drop_duplicates(subset=['recipient_address'])

            # 1.2 - Filter those participating in GG21 
            filtered_gg21_apps_df = gg21_apps_df[gg21_apps_df['recipient'].isin(supported_by_user['recipient_address'])]

            # 1.3 Build the page URL
            filtered_gg21_apps_df['url'] = filtered_gg21_apps_df.apply(lambda row: f"https://explorer.gitcoin.co/#/round/{row['chain_id']}/{row['round_id']}/{row['id']}", axis=1)

            # 1.4 Identigy GG21 projects user has already donated to
            
            
            user_gg21_donations_df = gg21_donations_df[gg21_donations_df['donor_address'] == address]
            
            merged_gg21_user_df = filtered_gg21_apps_df.merge(
                user_gg21_donations_df[['recipient_address', 'round_id']],
                left_on=['recipient', 'round_id'],
                right_on=['recipient_address', 'round_id'],
                how='left',
                indicator=True
            )

            merged_gg21_user_df['donation_found'] = merged_gg21_user_df['_merge'].apply(lambda x: '✅' if x == 'both' else '')
            merged_gg21_user_df.drop(columns=['recipient_address', '_merge'], inplace=True)
            merged_gg21_user_df = merged_gg21_user_df.sort_values(by='project_title')    
            

            tcol2.markdown("#### 1. Cherished Allies: List of grantees in GG21 who you have contributed in the past")
            tcol2.markdown(f"Out of the {len(supported_by_user)} grantees you supported since GG18, here are those participating in GG21. Show them some love again in this round!")

            tcol2.dataframe(merged_gg21_user_df, hide_index=True, use_container_width=True,
                column_order=("project_title", "round_name", "url", "donation_found"),   
                column_config = {
                    "project_title": "Grantee Name",
                    "round_name": "Round",
                    "url": st.column_config.LinkColumn(label = "Donation Link", display_text = "Add to cart"),
                    "donation_found": "Donated in GG21?"
                    } 
                )
            log_dataframe(merged_gg21_user_df, '1. Cherished Allies')            

            # STEP 2: Display recommendations using contributor graph

            # 2.1 - Find the top most contributed projects by the user
            top_recipients = supported_by_user.nlargest(5, 'amount_in_usd')[['recipient_address', 'amount_in_usd']]

            # 2.2 - Find list of other donors who also contribute to user's fav projects
            donors_to_top_recipients = hist_donations_df[hist_donations_df['recipient_address'].isin(top_recipients['recipient_address'])]['donor_address'].unique()

            # 2.3 Remove user from this list
            donors_to_top_recipients = [donor for donor in donors_to_top_recipients if donor != address]

            # 2.4 Find projects most supported by this cohort that the user has never donated to
            other_recipients = hist_donations_df[
                (hist_donations_df['donor_address'].isin(donors_to_top_recipients)) &
                (~hist_donations_df['recipient_address'].isin(supported_by_user['recipient_address']))
            ]    

            # 2.5 Sort these never-before-donated projects by donation amounts from the cohort
            other_recipients_sorted = other_recipients.groupby('recipient_address').sum().sort_values(by='amount_in_usd', ascending=False)
            other_recipients_sorted = other_recipients_sorted.reset_index()
            reco_recipient_address = other_recipients_sorted['recipient_address']

            # 2.6 Find if they are participating in GG21
            cohort_df = gg21_apps_df[gg21_apps_df['recipient'].isin(reco_recipient_address)]
            cohort_df['url'] = cohort_df.apply(lambda row: f"https://explorer.gitcoin.co/#/round/{row['chain_id']}/{row['round_id']}/{row['id']}", axis=1)
            cohort_df = cohort_df.head(30)

            # 2.7 Display
            tcol2.markdown("#### 2. Community Favorites: Recommendations based on your donation history")    
            tcol2.markdown(f"{len(donors_to_top_recipients)} donors have supported the top 5 grantees you have contributed, since GG18. \
                Here are their most supported grantees in GG21 that you have not previously donated to.")
            
            tcol2.dataframe(cohort_df, hide_index=True, use_container_width=True,
                column_order=("project_title", "round_name", "url"),   
                column_config = {
                    "project_title": "Grantee Name",
                    "round_name": "Round",
                    "url": st.column_config.LinkColumn(label = "Donation Link", display_text = "Add to cart")
                    } 
                )
            log_dataframe(cohort_df, '2. Community Favorites')            

            # STEP 3: Show projects similar to user's previous contributions and recommendations in Step 2 using clustering

            # Load a pre-trained sentence transformer model
            model = SentenceTransformer('all-MiniLM-L6-v2')

            # Set a similarity threshold (e.g., 0.7)
            similarity_threshold = 0.5

            # Create embeddings for user's favorite projects from the past

            past_projects = pd.read_csv('./gg21/data/apps_18_to_20.csv')

            top_20_recipients = supported_by_user.nlargest(20, 'amount_in_usd')[['recipient_address']]

            # Filter past_projects to get the rows where the recipient is in the top 20 recipients
            user_donated_projects = past_projects[past_projects['recipient'].isin(top_20_recipients['recipient_address'])]

            user_donated_embeddings = model.encode(user_donated_projects['description'].tolist())

            # Calculate similarities with GG21 projects for top past favorites
                
            # Load embeddings for GG21 projects
            gg21_app_embeddings = np.load('./gg21/data/gg21_embeddings.npy')
            gg21_apps = pd.read_csv('./gg21/data/gg21_apps.csv')


            ##
            # Aggregate the embeddings of the user's donated projects into a single cluster embedding
            # Here we use the mean of the embeddings as the cluster representation

            # Calculate the cluster embedding by averaging the embeddings of the user's donated projects
            cluster_embedding = np.mean(user_donated_embeddings, axis=0)

            # Calculate similarity scores between the cluster embedding and all GG21 project embeddings
            similarity_scores = cosine_similarity([cluster_embedding], gg21_app_embeddings).flatten()

            ##
            # Find indices of GG21 projects that meet the similarity threshold
            similar_indices = [index for index, score in enumerate(similarity_scores) if score > similarity_threshold ]

            # Get the projects that meet the threshold
            similar_projects = gg21_apps.iloc[similar_indices]
            similar_projects['similarity_score'] = similarity_scores[similar_indices]

            # Sort similar projects by similarity score in descending order
            similar_projects = similar_projects.sort_values(by='similarity_score', ascending=False)

            # Store the recommendations as a DataFrame
            recommendations_df = similar_projects if not similar_projects.empty else pd.DataFrame()

            # Remove records from recommendations if the user has donated to the project in the past
            recommendations_df = recommendations_df[~recommendations_df['recipient'].isin(past_projects['recipient'])]

            recommendations_df['url'] = recommendations_df.apply(lambda row: f"https://explorer.gitcoin.co/#/round/{row['chain_id']}/{row['round_id']}/{row['id']}", axis=1)

            # Output the recommendations if any exist
            if not recommendations_df.empty:
                tcol2.markdown("#### 3. Likeminded Visionaries: Discover grantees similar to your past donations")
                tcol2.markdown("We looked at the cluster of top grantees you have supported and found out similar grantees in GG21 using Large Language Models (LLMs)")

                recommendations_df = recommendations_df.sort_values(by=['similarity_score', 'project_title'], ascending=[False, True])
                tcol2.dataframe(recommendations_df.head(20), hide_index=True, use_container_width=True,
                    column_order=("project_title", "round_name", "url", "similarity_score"),   
                    column_config = {
                        "project_title": "Grantee Name",
                        "round_name": "Round",
                        "url": st.column_config.LinkColumn(label = "Donation Link", display_text = "Add to cart"),
                        "similarity_score": st.column_config.ProgressColumn(
                            "Similarity Score",
                            help="Range 0 to 1",
                            format="%.1f",
                            min_value=0.0,
                            max_value=1.0,
                        )
                    } 
                )   
                log_dataframe(recommendations_df.head(20), '3. Likeminded Visionaries')


            ##
            # Find indices of GG21 projects that meet the similarity threshold
            similar_indices = [index for index, score in enumerate(similarity_scores) if score <= similarity_threshold ]

            # Get the projects that meet the threshold
            similar_projects = gg21_apps.iloc[similar_indices]
            similar_projects['similarity_score'] = similarity_scores[similar_indices]

            # Sort similar projects by similarity score in descending order
            similar_projects = similar_projects.sort_values(by='similarity_score', ascending=False)

            # Store the recommendations as a DataFrame
            recommendations_df = similar_projects if not similar_projects.empty else pd.DataFrame()

            # Remove records from recommendations if the user has donated to the project in the past
            recommendations_df = recommendations_df[~recommendations_df['recipient'].isin(past_projects['recipient'])]

            recommendations_df['url'] = recommendations_df.apply(lambda row: f"https://explorer.gitcoin.co/#/round/{row['chain_id']}/{row['round_id']}/{row['id']}", axis=1)

            # Output the recommendations if any exist
            if not recommendations_df.empty:
                tcol2.markdown("#### 4. Discover New Perspectives: Projects least similar to your favorites")
                tcol2.markdown("Here are GG21 projects that differ the most from your usual picks.")

                recommendations_df = recommendations_df.sort_values(by=['similarity_score', 'project_title'], ascending=[True, True])
                tcol2.dataframe(recommendations_df.head(20), hide_index=True, use_container_width=True,
                    column_order=("project_title", "round_name", "url", "similarity_score"),   
                    column_config = {
                        "project_title": "Grantee Name",
                        "round_name": "Round",
                        "url": st.column_config.LinkColumn(label = "Donation Link", display_text = "Add to cart"),
                        "similarity_score": st.column_config.ProgressColumn(
                            "Similarity Score",
                            help="Range 0 to 1",
                            format="%.1f",
                            min_value=0.0,
                            max_value=1.0,
                        )
                    } 
                )   
                log_dataframe(recommendations_df.head(20), '4. Discover New Perspectives')    

                



                



