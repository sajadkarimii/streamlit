import streamlit as st
import random
import pyodbc
import pandas as pd
import joblib

st.set_page_config(layout="wide")

st.title("Welcome :D")
    
model = joblib.load('random_forest_model.pkl')
    
work = pd.read_csv('Working Professional or Student.csv')
pro = pd.read_csv('Profession.csv')
deg = pd.read_csv('Degree.csv')
sui = pd.read_csv('Have you ever had suicidal thoughts _.csv')

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
        st.link_button("Power Bi report","http://sajad/Reports/powerbi/Epl")
    with col3:
        pass

with ML:
    with st.form('ML'):
        col1 , col2 ,col3 ,col4,col5= st.columns(5)
        with col1:
            age = st.number_input("Enter your age :",0,120,step=1)
        with col2:
            working = st.selectbox("Select your status :",options=(work['Working Professional or Student'].unique()))
        with col3:
            profession = st.selectbox("Are you student :",options=(pro['Profession'].unique()))
        with col4:
            wpressure = st.number_input("Enter your working pressure (1 , 5):",1,5,step=1)
        with col5:
            degree = st.selectbox("What's your Degree :",options=(deg['Degree'].unique()))
        col6 , col7 ,col8 ,col9= st.columns(4)
        with col6:
            JSatisfaction = st.number_input("Enter your Job Satisfaction (1 , 5):",1,5,step=1)
        with col7:
            suicide = st.selectbox("Have you ever had suicidal thoughts ? :",options=(sui['Have you ever had suicidal thoughts ?'].unique()))
        with col8:
            WSHours = st.number_input("Enter your Work/Study Hours :",0,24,step=1)
        with col9:
            FStress = st.number_input("Enter your Financial Stress (1 , 5):",1,5,step=1)
        data = [[age,work['encoded'][work['Working Professional or Student'] == working].iloc[0],pro['encoded'][pro['Profession'] == profession].iloc[0]
                ,wpressure,deg['encoded'][deg['Degree'] == degree].iloc[0],JSatisfaction,sui['encoded'][sui['Have you ever had suicidal thoughts ?'] == suicide].iloc[0],WSHours,FStress]]
        if st.form_submit_button("Submit"):
            predict = model.predict(data)
            if predict:
                st.title("You are most likely depressed :(((")
            else : 
                st.title("Fortunately, you are not depressed :)))")

with Description:
    st.title("توضیحات")
    st.write("صفحه اول سه بازی برای سرگرمی درست شده است")
    st.write("صفحه دوم اخبار به روز ایرانو جهان را میتوانید مشاهده کنید")
    st.write("صفحه سوم دارای یک لینک برای مشاهده یک داشبورد مدیریتی پاور بی ای است")
    st.write('صفحه چهارم دارای یک هوش مصنوعی برای دریافت اطلاعات مورد نیاز است')             