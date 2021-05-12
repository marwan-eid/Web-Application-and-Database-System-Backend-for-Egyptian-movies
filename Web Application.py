import dash
import dash_table
import dash_html_components as html
import dash_core_components as dcc
import MySQLdb
import numpy as np
import pandas as pd
import webbrowser
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from threading import Timer

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

params_movies_reviews = ['m_name', 'user_email_address', 'review']
params_cast_movies = ['cm_name', 'm_name', 'm_duration', 'm_release_date', 'm_storyline']
params_genres = ['m_name', 'm_duration', 'm_release_date', 'm_storyline']
params_movie = ['m_name', 'm_duration', 'm_rating', 'm_release_date', 'm_storyline', 'm_revenue', 'm_director_name', 'm_writer_name']
params_cast_member = ['cm_name', 'cm_biography', 'cm_birthdate', 'cm_nationality']
params_top = ['m_name', 'm_duration', 'm_rating', 'm_release_date', 'm_revenue']
app.layout = html.Div([
    html.H1('Egyptian IMDB', style={'textAlign': 'center', 'margin': '48px 0', 'fontFamily': 'system-ui'}),
    html.H4('Fundamentals of Database Systems Project - Marwan Eid', style={'textAlign': 'center', 'fontFamily': 'system-ui'}),
    dcc.Tabs(id="tabs", children=[
        dcc.Tab(label='Register a user', children=[
            html.Div([
                html.Form(children=[
                    html.P(children=["Username: ", dcc.Input(type='text', id='user_username')], style={'marginLeft': '200'}),
                    html.P(children=["Email Address: ", dcc.Input(type='email', id='user_email_address', required=True)], style={'marginLeft': '800'}),
                    html.P(children=["Gender: ", dcc.Dropdown(id='gender-dropdown', options=[
                        {'label': 'Male', 'value': 'M'}, {'label': 'Female', 'value': 'F'}])], style={'marginLeft': '200', 'width': '50%'}),
                    html.P(children=["Birthdate: ", dcc.DatePickerSingle(id='user_birthdate')], style={'marginLeft': '800'}),
                    html.Button('Register', id='register', n_clicks_timestamp=0, style={'marginLeft': '200', 'marginTop': '20px'})]),
                    html.Div(id='out_trial')])
        ]),
        dcc.Tab(label='Find a movie', children=[
            html.Div([
                html.Form(children=[
                    html.P(children=["Movie ID: ", dcc.Input(type='number', id='movie_id')], style={'marginLeft': '200'}),
                    html.P(children=["Movie Name: ", dcc.Input(type='text', id='movie_name')], style={'marginLeft': '800'}),
                ]),
                html.Button('Search by movie ID', id='show-movie-by-id', n_clicks_timestamp=0, style={'marginLeft': '200', 'marginTop': '20px'}),
                html.Button('Search by movie Name', id='show-movie-by-name', n_clicks_timestamp=0, style={'marginLeft': '800', 'marginTop': '20px'}),
            dash_table.DataTable(id='movie-table',
            columns=([{'id': p, 'name': p} for p in params_movie]),
            data = [], editable=True, style_cell={'textAlign': 'left', 'whiteSpace': 'normal', 'height': 'auto'})
                ])
        ]),
        dcc.Tab(label='Find a cast member', children=[
            html.Div([
                html.Form(children=[
                    html.P(children=["Cast Member ID: ", dcc.Input(type='number', id='cast_member_id')], style={'marginLeft': '200'}),
                    html.P(children=["Cast Member Name: ", dcc.Input(type='text', id='cast_member_name')], style={'marginLeft': '800'}),
                ]),
                html.Button('Search by cast member ID', id='show-cast-member-by-id', n_clicks_timestamp=0, style={'marginLeft': '200', 'marginTop': '20px'}),
                html.Button('Search by cast member Name', id='show-cast-member-by-name', n_clicks_timestamp=0, style={'marginLeft': '800', 'marginTop': '20px'}),
            dash_table.DataTable(id='cast-member-table',
            columns=([{'id': p, 'name': p} for p in params_cast_member]),
            data = [], editable=True, style_cell={'textAlign': 'left', 'whiteSpace': 'normal', 'height': 'auto'})
                ])
        ]),
        dcc.Tab(label='Top 10 movies by total revenue', children=[
            html.Div([
                html.Button('Click to find the top 10 movies by revenue', id='show-top',style={'marginLeft': '565px', 'marginTop': '25px'}),
            dash_table.DataTable(id='top-table',
            columns=([{'id': 'No', 'name': 'No'}] + [{'id': p, 'name': p} for p in params_top]),
            data = [], editable=True, style_cell={'textAlign': 'left'})
            ])
        ]),
        dcc.Tab(label='Find movies by genre', children=[
            html.Div([dcc.Dropdown(id='genres-dropdown', options=[
            {'label': 'Action', 'value': 'Action'},
            {'label': 'Adventure', 'value': 'Adventure'},
            {'label': 'Animation', 'value': 'Animation'},
            {'label': 'Biography', 'value': 'Biography'},
            {'label': 'Comedy', 'value': 'Comedy'},
            {'label': 'Crime', 'value': 'Crime'},
            {'label': 'Documentary', 'value': 'Documentary'},
            {'label': 'Drama', 'value': 'Drama'},
            {'label': 'Family', 'value': 'Family'},
            {'label': 'Fantasy', 'value': 'Fantasy'},
            {'label': 'History', 'value': 'History'},
            {'label': 'Horror', 'value': 'Horror'},
            {'label': 'Musical', 'value': 'Musical'},
            {'label': 'Mystery', 'value': 'Mystery'},
            {'label': 'Religious', 'value': 'Religious'},
            {'label': 'Romance', 'value': 'Romance'},
            {'label': 'Science Fiction', 'value': 'Science Fiction'},
            {'label': 'Short', 'value': 'Short'},
            {'label': 'Sport', 'value': 'Sport'},
            {'label': 'Thriller', 'value': 'Thriller'},
            {'label': 'War', 'value': 'War'}
            ]),
            dash_table.DataTable(id='genres-table',
            columns=([{'id': 'No', 'name': 'No'}] + [{'id': p, 'name': p} for p in params_genres]),
            data = [], editable=True, style_cell={'textAlign': 'left', 'whiteSpace': 'normal', 'height': 'auto'})
            ])
        ]),
        dcc.Tab(label='Find movies of a cast member', children=[
            html.Div([
                html.Form(children=[
                    html.P(children=["Cast Member ID: ", dcc.Input(type='number', id='cast_member_movie_id')], style={'marginLeft': '200'}),
                    html.P(children=["Cast Member Name: ", dcc.Input(type='text', id='cast_member_movie_name')], style={'marginLeft': '800'}),
                ]),
                html.Button('Search by cast member ID', id='show-cast-member-movie-by-id', n_clicks_timestamp=0, style={'marginLeft': '200', 'marginTop': '20px'}),
                html.Button('Search by cast member Name', id='show-cast-member-movie-by-name', n_clicks_timestamp=0, style={'marginLeft': '800', 'marginTop': '20px'}),
                dash_table.DataTable(id='cast-member-movie-table',
                columns=([{'id': p, 'name': p} for p in params_cast_movies]),
                data = [], editable=True, style_cell={'textAlign': 'left', 'whiteSpace': 'normal', 'height': 'auto'})
                ])
        ]),
        dcc.Tab(label='Check movies reviews', children=[
            html.Div([
                html.P(children=["Movie ID: ", dcc.Input(type='number', id='find_review_movie_id')], style={'marginLeft': '200'}),
                html.P(children=["Movie Name: ", dcc.Input(type='text', id='find_review_movie_name')], style={'marginLeft': '800'})]),
                html.Button('Find using movie ID', id='find-review-movie-by-id', n_clicks_timestamp=0, style={'marginLeft': '200', 'marginTop': '20px'}),
                html.Button('Find using movie Name', id='find-review-movie-by-name', n_clicks_timestamp=0, style={'marginLeft': '800', 'marginTop': '20px'}),
                dash_table.DataTable(id='movies-reviews-table',
                columns=([{'id': 'No', 'name': 'No'}] + [{'id': p, 'name': p} for p in params_movies_reviews]),
                data = [], editable=True, style_cell={'textAlign': 'left', 'whiteSpace': 'normal', 'height': 'auto'})
        ]),
        dcc.Tab(label='Add a movie review', children=[
            html.Div([
                html.P(children=["Email Address: ", dcc.Input(type='email', id='add_review_email_address', required=True)], style={'marginLeft': '800'}),
                html.P(children=["Review: ", dcc.Input(type='text', id='add_review_review')], style={'marginLeft': '200'}),
                html.P(children=["Movie ID: ", dcc.Input(type='number', id='add_review_movie_id')], style={'marginLeft': '200'}),
                html.P(children=["Movie Name: ", dcc.Input(type='text', id='add_review_movie_name')], style={'marginLeft': '800'})]),
                html.Button('Add using movie ID', id='add-review-movie-by-id', n_clicks_timestamp=0, style={'marginLeft': '200', 'marginTop': '20px'}),
                html.Button('Add using movie Name', id='add-review-movie-by-name', n_clicks_timestamp=0, style={'marginLeft': '800', 'marginTop': '20px'}),
                html.Div(id='out_trial_1')
        ])
        ], style={'fontFamily': 'system-ui'})
    ])

@app.callback(
    Output('top-table', 'data'),
    Input(component_id='show-top', component_property='n_clicks'))
def top10_movies_by_revenue(n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    else:
        try:
            db_connection = MySQLdb.connect("sql11.freemysqlhosting.net", "sql11410479", "cSMqvaXALm", "sql11410479", charset = "utf8")
        except:
            print("Can't connect to database")
            return 0
        print("Connected")
        cursor = db_connection.cursor()
        cursor.execute("SELECT m_name, m_duration, m_rating, m_release_date, m_revenue FROM movie ORDER BY m_revenue DESC LIMIT 10")
        m = cursor.fetchall()
        df = pd.DataFrame(m, columns=params_top)
        df['No'] = [i for i in range(1, 11)]
        return df.to_dict('rows')

@app.callback(
    Output('movie-table', 'data'),
    [Input(component_id='show-movie-by-id', component_property='n_clicks_timestamp'),
    Input(component_id='show-movie-by-name', component_property='n_clicks_timestamp')],
    state=[State('movie_id', 'value'),
     State('movie_name', 'value')])
def find_movie(n_clicks_1, n_clicks_2, input1, input2):
    if int(n_clicks_1) > int(n_clicks_2):
        try:
            db_connection = MySQLdb.connect("sql11.freemysqlhosting.net", "sql11410479", "cSMqvaXALm", "sql11410479", charset = "utf8")
        except:
            print("Can't connect to database")
            return 0
        cursor = db_connection.cursor()
        cursor.execute("SELECT m_name, m_duration, m_rating, m_release_date, m_storyline, m_revenue, c1.cm_first_name, c1.cm_last_name, c2.cm_first_name, c2.cm_last_name FROM movie INNER JOIN cast_member c1 ON movie.m_director_ID = c1.cm_ID INNER JOIN cast_member c2 ON movie.m_writer_ID = c2.cm_ID WHERE movie.m_ID='%s'" % input1)
        m = cursor.fetchall()
        director = m[0][-2] + " " + m[0][-1] if m[0][-1] is not None else m[0][-2]
        writer = m[0][-4] + " " + m[0][-3] if m[0][-3] is not None else m[0][-4]
        l = m[0][:-4]
        l = list(l)
        l.append(director)
        l.append(writer)
        df = pd.DataFrame([l], columns=params_movie)
        n_clicks_1 = None
        return df.to_dict('rows')
    elif int(n_clicks_1) < int(n_clicks_2):
        try:
            db_connection = MySQLdb.connect("sql11.freemysqlhosting.net", "sql11410479", "cSMqvaXALm", "sql11410479", charset = "utf8")
        except:
            print("Can't connect to database")
            return 0
        cursor = db_connection.cursor()
        cursor.execute("SELECT m_name, m_duration, m_rating, m_release_date, m_storyline, m_revenue, c1.cm_first_name, c1.cm_last_name, c2.cm_first_name, c2.cm_last_name FROM movie INNER JOIN cast_member c1 ON movie.m_director_ID = c1.cm_ID INNER JOIN cast_member c2 ON movie.m_writer_ID = c2.cm_ID WHERE movie.m_name='%s'" % input2)
        m = cursor.fetchall()
        director = m[0][-2] + " " + m[0][-1] if m[0][-1] is not None else m[0][-2]
        writer = m[0][-4] + " " + m[0][-3] if m[0][-3] is not None else m[0][-4]
        l = m[0][:-4]
        l = list(l)
        l.append(director)
        l.append(writer)
        df = pd.DataFrame([l], columns=params_movie)
        n_clicks_2 = None
        return df.to_dict('rows')
    else:
        raise PreventUpdate

@app.callback(
    Output('cast-member-table', 'data'),
    [Input(component_id='show-cast-member-by-id', component_property='n_clicks_timestamp'),
    Input(component_id='show-cast-member-by-name', component_property='n_clicks_timestamp')],
    state=[State('cast_member_id', 'value'),
     State('cast_member_name', 'value')])
def find_cast_member(n1, n2, in1, in2):
    if int(n1) > int(n2):
        try:
            db_connection = MySQLdb.connect("sql11.freemysqlhosting.net", "sql11410479", "cSMqvaXALm", "sql11410479", charset = "utf8")
        except:
            print("Can't connect to database")
            return 0
        cursor = db_connection.cursor()
        cursor.execute("SELECT * FROM cast_member WHERE cm_ID='%s'" % in1)
        m = cursor.fetchall()
        name = m[0][1] + " " + m[0][2] if m[0][2] is not None else m[0][1]
        l = []
        l.append(name)
        l.append(m[0][3])
        l.append(m[0][4])
        l.append(m[0][5])
        df = pd.DataFrame([l], columns=params_cast_member)
        n1 = None
        return df.to_dict('rows')
    elif int(n1) < int(n2):
        try:
            db_connection = MySQLdb.connect("sql11.freemysqlhosting.net", "sql11410479", "cSMqvaXALm", "sql11410479", charset = "utf8")
        except:
            print("Can't connect to database")
            return 0
        first = in2.split(" ")[0]
        try:
            last = in2.split(" ")[1]
        except:
            last = None
        cursor = db_connection.cursor()
        cursor.execute("SELECT * FROM cast_member WHERE cm_first_name='%s'" % first + " AND cm_last_name='%s'" % last)
        m = cursor.fetchall()
        l = []
        l.append(in2)
        l.append(m[0][3])
        l.append(m[0][4])
        l.append(m[0][5])
        df = pd.DataFrame([l], columns=params_cast_member)
        n2 = None
        return df.to_dict('rows')
    else:
        raise PreventUpdate

@app.callback(
    Output('genres-table', 'data'),
    [Input('genres-dropdown', 'value')])
def find_genres(value):
    try:
        db_connection = MySQLdb.connect("sql11.freemysqlhosting.net", "sql11410479", "cSMqvaXALm", "sql11410479", charset = "utf8")
    except:
        print("Can't connect to database")
        return 0
    print("Connected")
    cursor = db_connection.cursor()
    cursor.execute("SELECT m_name, m_duration, m_release_date, m_storyline FROM movie INNER JOIN movies_genres ON movie.m_ID=movies_genres.m_ID WHERE movies_genres.genre='%s'" % value)
    m = cursor.fetchall()
    df = pd.DataFrame(m, columns=params_genres)
    df['No'] = [i for i in range(1, len(m)+1)]
    return df.to_dict('rows')

@app.callback(
    Output('cast-member-movie-table', 'data'),
    [Input(component_id='show-cast-member-movie-by-id', component_property='n_clicks_timestamp'),
    Input(component_id='show-cast-member-movie-by-name', component_property='n_clicks_timestamp')],
    state=[State('cast_member_movie_id', 'value'),
     State('cast_member_movie_name', 'value')])
def find_cast_member_movies(n1, n2, in1, in2):
    if int(n1) > int(n2):
        try:
            db_connection = MySQLdb.connect("sql11.freemysqlhosting.net", "sql11410479", "cSMqvaXALm", "sql11410479", charset = "utf8")
        except:
            print("Can't connect to database")
            return 0
        cursor = db_connection.cursor()
        cursor.execute("SELECT CM.cm_first_name, CM.cm_last_name, M.m_name, M.m_duration, M.m_release_date, M.m_storyline FROM movies_actors MA LEFT JOIN movie M ON MA.m_ID = M.m_ID LEFT JOIN cast_member CM ON MA.cm_ID = CM.cm_ID WHERE MA.cm_ID='%s'" % in1)
        m = cursor.fetchall()
        name = m[0][0] + " " + m[0][1] if m[0][1] is not None else m[0][0]
        t = []
        for i in range(len(m)):
            l = []
            l.append(name)
            l.append(m[i][2])
            l.append(m[i][3])
            l.append(m[i][4])
            l.append(m[i][5])
            t.append(l)
        t = np.array(t)
        df = pd.DataFrame(t, columns=params_cast_movies)
        n1 = None
        return df.to_dict('rows')
    elif int(n1) < int(n2):
        try:
            db_connection = MySQLdb.connect("sql11.freemysqlhosting.net", "sql11410479", "cSMqvaXALm", "sql11410479", charset = "utf8")
        except:
            print("Can't connect to database")
            return 0
        first = in2.split(" ")[0]
        try:
            last = in2.split(" ")[1]
        except:
            last = None
        cursor = db_connection.cursor()
        cursor.execute("SELECT M.m_name, M.m_duration, M.m_release_date, M.m_storyline FROM movies_actors MA LEFT JOIN movie M ON MA.m_ID = M.m_ID LEFT JOIN cast_member CM ON MA.cm_ID = CM.cm_ID WHERE CM.cm_first_name='%s'" % first + " AND CM.cm_last_name='%s'" % last)
        m = cursor.fetchall()
        t = []
        for i in range(len(m)):
            l = []
            l.append(in2)
            l.append(m[i][0])
            l.append(m[i][1])
            l.append(m[i][2])
            l.append(m[i][3])
            t.append(l)
        t = np.array(t)
        df = pd.DataFrame(t, columns=params_cast_movies)
        n2 = None
        return df.to_dict('rows')
    else:
        raise PreventUpdate

@app.callback(
    Output('out_trial', 'children'),
    [Input('register', component_property='n_clicks')],
    state=[State('user_username', 'value'),
     State('user_email_address', 'value'),
     State('gender-dropdown', 'value'),
     State('user_birthdate', 'date')])
def sign_up(n_clicks, v1, v2, v3, v4):
    if n_clicks is None:
        raise PreventUpdate
    else:
        try:
            db_connection = MySQLdb.connect("sql11.freemysqlhosting.net", "sql11410479", "cSMqvaXALm", "sql11410479", charset = "utf8")
        except:
            print("Can't connect to database")
            return 0
        print("Connected")
        cursor = db_connection.cursor()
        sql = "INSERT INTO user (email_address, username, gender, birthdate) VALUES (%s, %s, %s, %s)"
        val = (v2, v1, v3, v4)
        cursor.execute(sql, val)
        db_connection.commit()
        return "Registration Successful!"

@app.callback(
    Output('out_trial_1', 'children'),
    [Input(component_id='add-review-movie-by-id', component_property='n_clicks_timestamp'),
    Input(component_id='add-review-movie-by-name', component_property='n_clicks_timestamp')],
    state=[State('add_review_email_address', 'value'),
     State('add_review_review', 'value'),
     State('add_review_movie_id', 'value'),
     State('add_review_movie_name', 'value')])
def add_review(n1, n2, v1, v2, v3, v4):
    if int(n1) > int(n2):
        try:
            db_connection = MySQLdb.connect("sql11.freemysqlhosting.net", "sql11410479", "cSMqvaXALm", "sql11410479", charset = "utf8")
        except:
            print("Can't connect to database")
            return 0
        print("Connected")
        cursor = db_connection.cursor()
        sql = "INSERT INTO review (user_email_address, m_ID, textual_review) VALUES (%s, %s, %s)"
        val = (v1, v3, v2)
        cursor.execute(sql, val)
        db_connection.commit()
        return "Review added."
    elif int(n1) < int(n2):
        try:
            db_connection = MySQLdb.connect("sql11.freemysqlhosting.net", "sql11410479", "cSMqvaXALm", "sql11410479", charset = "utf8")
        except:
            print("Can't connect to database")
            return 0
        print("Connected")
        cursor = db_connection.cursor()
        cursor.execute("SELECT m_ID from movie where m_name='%s'" % v4)
        m = cursor.fetchall()
        sql = "INSERT INTO review (user_email_address, m_ID, textual_review) VALUES (%s, %s, %s)"
        val = (v1, m[0][0], v2)
        cursor.execute(sql, val)
        db_connection.commit()
        return "Review added."
    else:
        raise PreventUpdate

@app.callback(
    Output('movies-reviews-table', 'data'),
    [Input(component_id='find-review-movie-by-id', component_property='n_clicks_timestamp'),
    Input(component_id='find-review-movie-by-name', component_property='n_clicks_timestamp')],
    state=[State('find_review_movie_id', 'value'),
     State('find_review_movie_name', 'value')])
def check_review(n1, n2, v1, v2):
    if int(n1) > int(n2):
        try:
            db_connection = MySQLdb.connect("sql11.freemysqlhosting.net", "sql11410479", "cSMqvaXALm", "sql11410479", charset = "utf8")
        except:
            print("Can't connect to database")
            return 0
        print("Connected")
        cursor = db_connection.cursor()
        cursor.execute("SELECT m_name FROM movie WHERE m_ID='%s'" % v1)
        name = cursor.fetchall()
        cursor.execute("SELECT user_email_address, textual_review FROM review WHERE review.m_ID='%s'" % v1)
        m = cursor.fetchall()
        t = []
        for i in range(len(m)):
            l = []
            l.append(name)
            l.append(m[i][0])
            l.append(m[i][1])
            t.append(l)
        t = np.array(t)
        df = pd.DataFrame(t, columns=params_movies_reviews)
        n1 = None
        return df.to_dict('rows')
    elif int(n1) < int(n2):
        try:
            db_connection = MySQLdb.connect("sql11.freemysqlhosting.net", "sql11410479", "cSMqvaXALm", "sql11410479", charset = "utf8")
        except:
            print("Can't connect to database")
            return 0
        print("Connected")
        cursor = db_connection.cursor()
        cursor.execute("SELECT m_ID from movie where m_name='%s'" % v2)
        m = cursor.fetchall()
        cursor.execute("SELECT user_email_address, textual_review FROM review WHERE review.m_ID='%s'" % m[0][0])
        m = cursor.fetchall()
        t = []
        for i in range(len(m)):
            l = []
            l.append(v2)
            l.append(m[i][0])
            l.append(m[i][1])
            t.append(l)
        t = np.array(t)
        df = pd.DataFrame(t, columns=params_movies_reviews)
        n2 = None
        return df.to_dict('rows')
    else:
        raise PreventUpdate

def open_browser():
      webbrowser.open_new('http://127.0.0.1:8050/')

if __name__ == '__main__':
    Timer(1, open_browser).start()
    app.run_server()
