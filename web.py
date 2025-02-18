import streamlit as st
import random
import pyodbc

st.set_page_config(layout="wide")

st.title("Welcome :D")
    
def RPS(choise):
    rp = random.randint(1,3)
    if choise == "Rock":
        if rp == 1:
            return ("Tie !!!")
        elif rp == 2:
            return ("Lose !!!")
        elif rp == 3:
            return ("Win !!!")
    if choise == "Paper":
        if rp == 1:
            return ("Win !!!")
        elif rp == 2:
            return ("Tie !!!")
        elif rp == 3:
            return ("Lose !!!")
    if choise == "Scissors":
        if rp == 1:
            return ("Lose !!!")
        elif rp == 2:
            return ("Win !!!")
        elif rp == 3:
            return ("Tie !!!")

def numguess(guess):
    num = random.randint(1,10)
    if num == guess:
        return "You won (:"
    else:
        return "You lost ):"

def Guesshand(guess):
    hand = random.choice(['Right','Left'])
    if guess == hand:
        return "You won (:"
    else:
        return "You lost ):"
    
Game , News , BI , ML , Description = st.tabs(['Game' , 'News' , 'BI' , 'ML' , 'Description'])

with Game:
    
    RP, GN, GWH = st.columns(3)
    
    with RP:
        if st.button("Rock paper scissors"):
            st.session_state.show_rps_game = True  
            st.session_state.show_guess_number = False 
            st.session_state.show_guess_hand = False
    with GN:
        if st.button("Guess number"):
            st.session_state.show_rps_game = False 
            st.session_state.show_guess_number = True 
            st.session_state.show_guess_hand = False 
    with GWH:
        if st.button("Guess which hand"):
            st.session_state.show_rps_game = False  
            st.session_state.show_guess_number = False  
            st.session_state.show_guess_hand = True  
            
            
    if 'show_rps_game' in st.session_state and st.session_state.show_rps_game:
        st.title("Rock paper scissors")
        st.write("___")
        Rock, Paper, Scissors = st.columns(3)
        with Rock:
            if st.button("Rock"):
                st.write(RPS('Rock'))
        with Paper:
            if st.button("Paper"):
                st.write(RPS('Paper'))
        with Scissors:
            if st.button("Scissors"):
                st.write(RPS('Scissors'))
    if 'show_guess_number' in st.session_state and st.session_state.show_guess_number:
        st.title("Guess number")
        st.write("___")
        num = st.number_input("Guess a number between 1 and 10",1,10,step=1)
        if st.button("submit"):
            st.write(numguess(num))
    if 'show_guess_hand' in st.session_state and st.session_state.show_guess_hand:
        st.title("Guess which hand")
        st.write("___")
        Left, Right= st.columns(2)
        with Left:
            if st.button("Left"):
                st.write(Guesshand('Left'))
        with Right:
            if st.button("Right"):
                st.write(Guesshand('Right'))
                
with News:
    server = '.'
    driver = '{ODBC Driver 17 for SQL Server}'
    try:
        # Create News Database if not already exist
        connection = f'DRIVER={driver};SERVER={server};DATABASE=News;Trusted_Connection=yes;'
        conn = pyodbc.connect(connection, autocommit=True)
        cursor = conn.cursor()
        query = "SELECT Titles,Text FROM News"  # Replace with your table and column names
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            st.title(row.Titles)
            st.write(row.Text)
            st.write("___")
    except pyodbc.Error as e:
        print("An error occurred:", e)
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
    
    
    
                    
with BI:
    col1 , col2 ,col3 = st.columns(3)
    with col1:
        pass
    with col2:
        st.button("Power Bi report")
    with col3:
        pass


