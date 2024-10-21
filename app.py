import pickle
import streamlit as st
import requests

st.header("Game Recommendation System Using ML")

# Fetch Images, Ratings, and Download Links
def fetch_game_details(game_name):
    api_key = '914683eabfe04e9c91db9da15f6348ac'  # Replace with your actual RAWG API key
    url = f"https://api.rawg.io/api/games?key={api_key}&search={game_name}"
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            # Get the first result
            game_info = data['results'][0]
            image_url = game_info.get('background_image', 'Image not available')
            rating = game_info.get('rating', 'No rating available')
            return image_url, rating
        else:
            return "Image not available", "No rating available"
    else:
        return "Error fetching data", "No rating available"

# Load the pickled data
game = pickle.load(open("artifacts/Game_list.pkl", 'rb'))
link = pickle.load(open("artifacts/Link_list.pkl", 'rb'))
similarity = pickle.load(open("artifacts/similarity.pkl", 'rb'))

# List of game titles
game_list = game['Game_ID'].values
selected_game = st.selectbox("Select The Game", game_list)

# Recommendation function
def recommend(selected_game):
    index = game[game['Game_ID'] == selected_game].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_game_names = []
    recommended_game_posters = []
    recommended_game_ratings = []
    recommended_game_links = []
    
    for i in distances[1:6]:
        recommended_game_names.append(game.iloc[i[0]].Game_ID)
        # Fetch image, rating using the actual game name
        image_url, rating = fetch_game_details(game.iloc[i[0]].Game_ID)
        recommended_game_posters.append(image_url)
        recommended_game_ratings.append(rating)
        
        # Create a Google search link for the download
        game_id = game.iloc[i[0]].Game_ID.strip()  # Strip whitespace from the game name
        google_search_url = f"https://www.google.com/search?q={'+'.join(game_id.split())}+download"
        recommended_game_links.append(google_search_url)

    return recommended_game_names, recommended_game_posters, recommended_game_ratings, recommended_game_links

# Display recommendations
if st.button("Show Recommendation"):
    recommended_game_names, recommended_game_posters, recommended_game_ratings, recommended_game_links = recommend(selected_game)
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.text(recommended_game_names[0])
        st.image(recommended_game_posters[0])
        st.markdown(f"**Rating:** {recommended_game_ratings[0]}")
        st.link_button("Download Game",f"{recommended_game_links[0]})")
        
    with col2:
        st.text(recommended_game_names[1])
        st.image(recommended_game_posters[1])
        st.markdown(f"**Rating:** {recommended_game_ratings[1]}")
        st.link_button("Download Game",f"{recommended_game_links[1]})")
        
    with col3:
        st.text(recommended_game_names[2])
        st.image(recommended_game_posters[2])
        st.markdown(f"**Rating:** {recommended_game_ratings[2]}")
        st.link_button("Download Game",f"{recommended_game_links[2]})")
        
    with col4:
        st.text(recommended_game_names[3])
        st.image(recommended_game_posters[3])
        st.markdown(f"**Rating:** {recommended_game_ratings[3]}")
        st.link_button("Download Game",f"{recommended_game_links[3]})")
        
    with col5:
        st.text(recommended_game_names[4])
        st.image(recommended_game_posters[4])
        st.markdown(f"**Rating:** {recommended_game_ratings[4]}")
        st.link_button("Download Game",f"{recommended_game_links[4]})")
