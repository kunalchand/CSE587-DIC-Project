import streamlit as st
import pickle
import sqlite3
import pandas as pd

# Intallation Guide
# First install Python in the system
# Put files in a project folder
# Go inside project folder
# pip install streamlit
# pip install scikit-learn
# pip install pysqlite3
# git bash or open cmd in the same directory
# chmod +x run.sh
# ./run.sh {Deletes game_review_database.db and executes "streamlit run app.py"}

def warning():
    st.warning("Game already exists!")
    st.session_state.flag = 'none'

def success():
    st.success("Game added successfully!")
    st.session_state.flag = 'none'

def warning_game_deletion():
    st.warning("Please select some games to delete!")
    st.session_state.flag = 'none'

def success_game_deletion():
    st.success("Game and its reviews successfully deleted!")
    st.session_state.flag = 'none'

def warning_review_deletion():
    st.warning("Please select some reviews to delete!")
    st.session_state.flag = 'none'

def success_review_deletion():
    st.success("Reviews successfully deleted!")
    st.session_state.flag = 'none'

def dropdown_game_warning():
    st.warning("Please select a game!")
    st.session_state.flag = 'none'

def dropdown_review_warning():
    st.warning("Please write a review!")
    st.session_state.flag = 'none'

def dropdown_success():
    st.success("Review successfully added!")
    st.session_state.flag = 'none'

def score_update(game_name):
    c.execute("SELECT COUNT(*) FROM reviews WHERE game_name = ? AND game_review_prediction = 'Positive'", (game_name,))
    p_c = c.fetchall()
    positive_count = int(p_c[0][0])

    c.execute("SELECT COUNT(*) FROM reviews WHERE game_name = ? AND game_review_prediction = 'Negative'", (game_name,))
    n_c = c.fetchall()
    negative_count = int(n_c[0][0])

    new_score = positive_count - (negative_count * 0.5)
    
    c.execute('UPDATE games SET game_score = ? WHERE game_name = ?',(new_score, game_name))
    conn.commit()

def table_setup():
    if not c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='games'").fetchone():
        c.execute("CREATE TABLE games (id INTEGER PRIMARY KEY, game_name TEXT, game_score REAL)")
        c.execute("INSERT INTO games (game_name, game_score) VALUES (?, ?)", ('GTA Vice City', 0.5))
        c.execute("INSERT INTO games (game_name, game_score) VALUES (?, ?)", ('Freedom Fighters', 1))
        c.execute("INSERT INTO games (game_name, game_score) VALUES (?, ?)", ('Paladins', 0))
        conn.commit()

    if not c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='reviews'").fetchone():
        c.execute("CREATE TABLE reviews (id INTEGER PRIMARY KEY, game_name TEXT, game_review TEXT, game_review_prediction TEXT)")
        c.execute("INSERT INTO reviews (game_name, game_review, game_review_prediction) VALUES (?, ?, ?)", ('GTA Vice City', 'This game is amazing!', 'Positive'))
        c.execute("INSERT INTO reviews (game_name, game_review, game_review_prediction) VALUES (?, ?, ?)", ('GTA Vice City', 'Extremely disappointed. It did not meet my expectations at all.', 'Negative'))
        c.execute("INSERT INTO reviews (game_name, game_review, game_review_prediction) VALUES (?, ?, ?)", ('Freedom Fighters', 'Love this Game', 'Positive'))
        conn.commit()

def display_client_games():
    c.execute("SELECT * FROM games ORDER BY game_score DESC")
    data = c.fetchall()
    
    # Degine headers
    df = pd.DataFrame(data, columns=['ID', 'Game Name', 'Game Score'])
    df = df.set_index('ID')
    df.index.name = None

    st.write("### Games")
    
    # Display Table
    table_html = df.to_html(escape=False, index=False)
    table_html = table_html.replace('<table', '<table style="width:100%;"')
    st.write(table_html, unsafe_allow_html=True)

    st.markdown("""
        <style>
            table td {
                text-align: center;
            }
            table th {
                text-align: center;
                background-color: #003380;
            }
        </style>
    """, unsafe_allow_html=True)

def display_client_reviews():
    c.execute("""
        SELECT games.id, games.game_name, reviews.game_review, reviews.game_review_prediction 
        FROM games 
        INNER JOIN reviews 
        ON games.game_name = reviews.game_name 
        ORDER BY games.game_score DESC, reviews.game_review_prediction DESC;
    """)
    data = c.fetchall()
    
    # Degine headers
    df = pd.DataFrame(data, columns=['ID', 'Game Name', 'Game Review', 'Game Review Prediction'])
    df = df.set_index('ID')
    df.index.name = None

    st.write("### Reviews")
    
    # Display Table
    table_html = df.to_html(escape=False, index=False)
    table_html = table_html.replace('<table', '<table style="width:100%;"')
    st.write(table_html, unsafe_allow_html=True)

    st.markdown("""
        <style>
            table td {
                text-align: center;
            }
            table th {
                text-align: center;
                background-color: #803300;
            }
        </style>
    """, unsafe_allow_html=True)

def display_reviews():
    c.execute("SELECT * FROM reviews")
    data = c.fetchall()
    
    # Degine headers
    df = pd.DataFrame(data, columns=['ID', 'Game Name', 'Game Review', 'Game Review Prediction'])
    df = df.set_index('ID')
    df.index.name = None

    st.write("### Reviews")
    
    # Display Table
    table_html = df.to_html(escape=False, index=False)
    table_html = table_html.replace('<table', '<table style="width:100%;"')
    st.write(table_html, unsafe_allow_html=True)

    st.markdown("""
        <style>
            table td {
                text-align: center;
            }
            table th {
                text-align: center;
                background-color: #99003d;
            }
        </style>
    """, unsafe_allow_html=True)

def header(url):
    st.markdown(f'<p style="background-color: #008080; color: #ffffff; font-weight: bold; font-size: 20px; border-radius: 2%; text-align: center;"> {url}</p>', unsafe_allow_html=True)
    return url

def cell(url):
    st.markdown(f'<p style="background-color: #FFC87C; color: #000000; font-size: 17px; border-radius: 2%; text-align: center; padding: 5px;"> {url}</p>', unsafe_allow_html=True)
    return url

def display_games_adv():
    c.execute("SELECT * FROM games")
    data = c.fetchall()
    
    # Degine headers
    df = pd.DataFrame(data, columns=['ID', 'Game Name', 'Game Score'])
    df = df.set_index('ID')
    df.index.name = None

    st.write("### Games")
    
    # Define a list of options
    options = []
    
    counter = 1
    for row in data:
        with st.container():
            col0, col1, col2 = st.columns(3)
            with col0:
                label = "Game {}".format(counter)
                options.append(st.checkbox(label))
            with col1:
                header("Game Name")
                cell("{}".format(*row[1:]))
            with col2: 
                header("Game Score")
                cell("{}".format(*row[2:]))
            st.markdown("---")
        counter = counter + 1
        # options.append(st.checkbox("GAME NAME ----------------------- [ {} ]\n\nGAME SCORE ----------------------- [ {} ]".format(*row[1:])))

    # Define an empty list to hold the selected options
    selected_options = []
    for i in range(len(options)):
        if options[i]:
            selected_options.append(data[i][0])

    if st.button("Delete Selected Games"):
        if(len(selected_options) > 0):
            selected_ids = ','.join(map(str, selected_options))

            # Delete from reviews
            c.execute(f"SELECT game_name FROM games WHERE id IN ({selected_ids})")
            game_names = c.fetchall()
            for game_name in game_names:
                c.execute("DELETE FROM reviews WHERE game_name = ?", game_name)
                conn.commit()
            
            # Delete from games
            c.execute(f"DELETE FROM games WHERE id IN ({selected_ids})")
            conn.commit()

            st.session_state.flag = 'delete_game_success'

            st.session_state.page = 'admin'
            st.experimental_rerun()

        else:
            st.session_state.flag = 'delete_game_warning'
    
    
    if st.session_state.flag == 'delete_game_success':
        st.session_state.page = 'home'
        st.experimental_rerun()
    elif st.session_state.flag == 'delete_game_warning':
        warning_game_deletion()
    
    new_game = st.text_input("Enter the name of new game:")
    if st.button("Add New Game"):
        if new_game == '':
            st.warning("Please enter a game name to add")
            st.session_state.flag = 'none'
        else:
            c.execute("SELECT COUNT(*) FROM games WHERE game_name=?", (new_game,))
            if c.fetchone()[0] > 0:
                # Game already exists
                st.session_state.flag = 'add_game_warning'
            else:
                # Insert new game
                c.execute("INSERT INTO games (game_name, game_score) VALUES (?, ?)", (new_game,0))
                conn.commit()
                st.session_state.flag = 'add_game_success'

            st.session_state.page = 'admin'
            st.experimental_rerun()

    if st.session_state.flag == 'add_game_warning':
        warning()
    elif st.session_state.flag == 'add_game_success':
        success()

def display_reviews_adv():
    c.execute("SELECT * FROM reviews")
    data = c.fetchall()

    # Define headers
    df = pd.DataFrame(data, columns=['ID', 'Game Name', 'Game Review', 'Game Review Prediction'])
    df = df.set_index('ID')
    df.index.name = None

    st.write("### Reviews")

    # Define a list of options
    options = []
    
    counter = 1
    for row in data:
        with st.container():
            col0, col1, col2, col3 = st.columns(4)
            with col0:
                label = "Review {}".format(counter)
                options.append(st.checkbox(label))
            with col1:
                header("Game Name")
                cell("{}".format(*row[1:]))
            with col2: 
                header("Game Review")
                cell("{}".format(*row[2:]))
            with col3: 
                header("Game Review Prediction")
                cell("{}".format(*row[3:]))
            st.markdown("---")
        counter = counter + 1
        # options.append(st.checkbox("GAME NAME ----------------------- [ {} ]\n\nGAME REVIEW -------------------- [ {} ]\n\nGAME REVIEW PREDICTION --- [ {} ]".format(*row[1:])))

    # Define an empty list to hold the selected options
    selected_options = []
    for i in range(len(options)):
        if options[i]:
            selected_options.append(data[i][0])

    if st.button("Delete Selected Reviews"):
        if(len(selected_options) > 0):
            c.execute(f'SELECT game_name FROM reviews WHERE id IN (?)', (selected_options[0],))
            game_name = c.fetchall()

            selected_ids = ','.join(map(str, selected_options))
            c.execute(f"DELETE FROM reviews WHERE id IN ({selected_ids})")
            conn.commit()

            score_update(game_name[0][0])

            st.session_state.flag = 'delete_review_success'

            st.session_state.page = 'admin'
            st.experimental_rerun()

        else:
            st.session_state.flag = 'delete_review_warning'
    
    if st.session_state.flag == 'delete_review_success':
        st.session_state.page = 'home'
        st.experimental_rerun()
    elif st.session_state.flag == 'delete_review_warning':
        warning_review_deletion()

def home_page():

    if st.session_state.flag == 'delete_game_success':
        success_game_deletion()
    
    if st.session_state.flag == 'delete_review_success':
        success_review_deletion()
    
    st.title("Game Review App")

    # Add custom CSS to style the buttons
    st.markdown(
        """
        <style>
            .stButton>button {
                width: 100%;
                height: 175px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Add buttons to select user type
    with st.container():
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Admin", key='admin'):
                st.session_state.page = 'admin'
                st.experimental_rerun() 
        with col2:
            if st.button("Tester", key='tester'):
                st.session_state.page = 'tester'
                st.experimental_rerun()
        with col3:
            if st.button("Client", key='client'):
                st.session_state.page = 'client'
                st.experimental_rerun()   

def admin_page():
    # Add a home button to go back to the main page
    if st.button("Home"):
        st.session_state.page = 'home'
        st.experimental_rerun() 

    st.title("Admin Page")
    st.markdown("---")

    display_games_adv()
    st.markdown("---")
    display_reviews_adv()

def tester_page():
    # Add a home button to go back to the main page
    if st.button("Home"):
        st.session_state.page = 'home'
        st.experimental_rerun() 

    st.title("Tester Page")
    st.markdown("---")

    options = ['Select a game']

    c.execute("SELECT game_name FROM games")
    game_list = c.fetchall()

    for game in game_list:
        options.append(game[0])

    selected_option = st.selectbox('Choose a game to give review about:', options)

    # Add an input field for the tester to enter text review
    review = st.text_input("Enter your review:")

    # Add a button to trigger the analysis
    if st.button("Submit and Analyze"):
        if selected_option == 'Select a game':
            st.session_state.flag = 'dropdown_game_warning'
        else:
            if review == '':
                st.session_state.flag = 'dropdown_review_warning'
            else:
                # Use the loaded model to predict the sentiment of the input review
                file_name = open("vectorizer.pkl", "rb")
                vectorizer = pickle.load(file_name)
                prediction = model.predict(vectorizer.transform([review]))

                c.execute("INSERT INTO reviews (game_name, game_review, game_review_prediction) VALUES (?, ?, ?)", (selected_option, review, prediction[0]))
                conn.commit()

                st.session_state.flag = 'dropdown_success'

        st.session_state.page = 'tester'
        st.experimental_rerun()
    
    if st.session_state.flag == 'dropdown_game_warning':
        dropdown_game_warning()
    elif st.session_state.flag == 'dropdown_review_warning':
        dropdown_review_warning()
    elif st.session_state.flag == 'dropdown_success':
        score_update(selected_option)
        dropdown_success()

    display_reviews()

def client_page():
    # Add a home button to go back to the main page
    if st.button("Home"):
        st.session_state.page = 'home'
        st.experimental_rerun() 

    st.title("Client Page")
    st.markdown("---")

    display_client_games()
    display_client_reviews()

if __name__ == '__main__':
    # Reload on any code changes
    st.set_option('deprecation.showfileUploaderEncoding', False)

    # Load the pre-trained model
    file_name = open("knn.pkl", "rb")
    model = pickle.load(file_name)

    # Database setup
    conn = sqlite3.connect('game_review_database.db')
    c = conn.cursor()

    # Table setup
    table_setup()

    # Initialize the page state
    if 'page' not in st.session_state:
        st.session_state.page = 'home'

    # Initialize the flag state
    if 'flag' not in st.session_state:
        st.session_state.flag = 'none'

    # Execute the appropriate page function based on the current page
    if st.session_state.page == 'home':
        home_page()
    elif st.session_state.page == 'admin':
        admin_page()
    elif st.session_state.page == 'tester':
        tester_page()
    elif st.session_state.page == 'client':
        client_page()
    
    