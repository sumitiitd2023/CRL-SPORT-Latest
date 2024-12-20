# app.py
# from flask import Flask, render_template, request, jsonify, redirect, url_for,flash
# #from flask import Flask, render_template, request, redirect, url_for, flash
# import json
# import os
from fpdf import FPDF
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, send_file,redirect, url_for,flash
import pandas as pd
from io import BytesIO
import json
import os

# Install openpyxl
# Install xlrd

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flash messages


user_data_file = os.path.join('static', 'user_data.json')
staff_data_file = os.path.join('static', 'staff_data.json')

# Function to load users from a JSON file
def load_users():
    try:
        with open('users.json', 'r') as file:
            return json.load(file)  # Load the data from the JSON file
    except FileNotFoundError:
        print("users.json not found.")
        return []
    except json.JSONDecodeError:
        print("Error reading the JSON file.")
        return []


# Route for the default page, which serves mainlogin.html
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()

        # Check if username and password match
        for user in users:
            if user['username'] == username and user['password'] == password:
                flash("Login successful!", "success")
                return redirect(url_for('registration'))  # Redirect to index.html

        # If login fails, render the same page with an error message
        error_message = "Invalid username or password. Please try again."
        return render_template('mainlogin.html', error_message=error_message)
    else:
        # Render the login page for GET requests
        return render_template('mainlogin.html')

# Route for the index page (after login)
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/games')
def games():
    return render_template('games.html')


@app.route('/gallery')
def gallery():
    return render_template('gallery.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


# def append_to_json_file(file_name, new_data):
#     with open(file_name, 'r') as file:
#         existing_data = json.load(file)
#
#     # Step 2: Parse JSON data into Python object
#     existing_data_list = existing_data['data']
#
#     # Step 3: Append new JSON data to existing data
#     # new_data = {'name': 'John', 'age': 25}
#     existing_data_list.append(new_data)
#
#     # Step 4: Write updated JSON data back to file
#     with open(file_name, 'w') as file:
#         json.dump(existing_data, file, indent=4)
#
#     return existing_data
#     # try:
#     #     # Try to open the existing JSON file
#     #     with open(file_name, 'r') as file:
#     #         # Load existing JSON data
#     #         existing_data = json.load(file)
#     #
#     # except FileNotFoundError:
#     #     # If the file doesn't exist, create an empty dictionary
#     #     existing_data = {}
#     #
#     # # Append new data to the existing data
#     # data = existing_data['data']
#     # data.append(new_data)
#     # # existing_data.update(new_data)
#     #
#     # # Write the updated data back to the JSON file
#     # with open(file_name, 'a') as file:
#     #     json.dump(data, file, indent=2)
#
#
# @app.route('/submit', methods=['POST'])
# def submit():
#     data = {
#         'user_name': request.form['user_name'],
#         'staff_id': request.form['staff_id'],
#         'selected_options': request.form.getlist('options')
#     }
#     # Save data to a JSON file or database (in this example, we'll just print it)
#     print("Received data:", data)
#     # Example usage:
#     file_name = './static/registration_data.json'
#     # new_data = {'key1': 'value1', 'key2': 'value2'}
#     updated_data = append_to_json_file(file_name, data)
#
#     return jsonify({'message': updated_data})


file_name = "./static/staff_data.json"
# Load staff data from JSON file
with open(staff_data_file, 'r') as f:
    staff_data = json.load(f)
    print(staff_data)

def save_data():
    # Save staff data to JSON file
    with open(file_name, 'w') as f:
        json.dump(staff_data, f, indent=2)

@app.route('/register')
def register():
    return render_template('form.html')
@app.route('/download-schedule', methods=['GET'])
def download_schedule():
    # Create a simple PDF schedule
    pdf = FPDF()  # Correctly instantiate the FPDF class
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Your Schedule", ln=True, align="C")
    pdf.cell(200, 10, txt="Monday: 9 AM - 5 PM", ln=True, align="L")
    pdf.cell(200, 10, txt="Tuesday: 9 AM - 5 PM", ln=True, align="L")

    pdf_path = "schedule.pdf"
    pdf.output(pdf_path)

    return send_file(pdf_path, as_attachment=True)


@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    staff_id = request.form.get('staff_id')
    indoor_games = request.form.getlist('indoor_games')
    outdoor_games = request.form.getlist('outdoor_games')

    # Store the submitted data in the staff_data dictionary
    staff_data[staff_id] = {
        'name': name,
        'indoor_games': indoor_games,
        'outdoor_games': outdoor_games
    }

    # Save updated data
    save_data()
    return redirect(url_for('view', staff_id=staff_id))




TEXT_FILE_FOLDER = './static/uploads/rules/'

@app.route('/badminton', methods=['GET'])
def badminton():
    text_file_path = TEXT_FILE_FOLDER + 'badminton.txt'
    print("txt file name: ", id)
    with open(text_file_path, 'r') as file:
        lines = file.readlines()
    return render_template('rules.html', lines=lines)

@app.route('/cricket_men', methods=['GET'])
def cricket_men():
    text_file_path = TEXT_FILE_FOLDER +'cricket_men.txt'
    print("txt file name: ", id)
    with open(text_file_path, 'r') as file:
        lines = file.readlines()
    return render_template('rules.html', lines=lines)

@app.route('/cricket_women', methods=['GET'])
def cricket_women():
    text_file_path = TEXT_FILE_FOLDER +'cricket_women.txt'
    print("txt file name: ", id)
    with open(text_file_path, 'r') as file:
        lines = file.readlines()
    return render_template('rules.html', lines=lines)

@app.route('/throwball', methods=['GET'])
def throwball():
    text_file_path = TEXT_FILE_FOLDER +'throwball.txt'
    print("txt file name: ", id)
    with open(text_file_path, 'r') as file:
        lines = file.readlines()
    return render_template('rules.html', lines=lines)

@app.route('/tugofwar', methods=['GET'])
def tugofwar():
    text_file_path = TEXT_FILE_FOLDER +'tugofwar.txt'
    print("txt file name: ", id)
    with open(text_file_path, 'r') as file:
        lines = file.readlines()
    return render_template('rules.html', lines=lines)

@app.route('/volleyball', methods=['GET'])
def volleyball():
    text_file_path = TEXT_FILE_FOLDER +'volleyball.txt'
    print("txt file name: ", id)
    with open(text_file_path, 'r') as file:
        lines = file.readlines()
    return render_template('rules.html', lines=lines)

@app.route('/table_tennis', methods=['GET'])
def table_tennis():
    text_file_path = TEXT_FILE_FOLDER +'table_tennis.txt'
    print("txt file name: ", id)
    with open(text_file_path, 'r') as file:
        lines = file.readlines()
    return render_template('rules.html', lines=lines)

@app.route('/fun_games', methods=['GET'])
def fun_games():
    text_file_path = TEXT_FILE_FOLDER +'fun_games.txt'
    print("txt file name: ", id)
    with open(text_file_path, 'r') as file:
        lines = file.readlines()
    return render_template('rules.html', lines=lines)

############# Admin Code ###########################
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS_IMAGES = {'png', 'jpg', 'jpeg', 'gif'}
ALLOWED_EXTENSIONS_VIDEOS = {'mp4'}
ALLOWED_EXTENSIONS_TEXT = {'txt', 'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

@app.route('/admin')
def admin():
    # List of sample text file names for the dropdown
    text_file_options = ["table_tennis", "fun_game", "cricket_men", "cricket_women", "throwball", "volleyball", "badminton",
             "tug_of_war"]

    return render_template('admin.html', text_file_options=text_file_options)

@app.route('/upload', methods=['POST'])
def upload():
    # Create uploads folders if not exists
    for folder in ['images', 'videos', 'rules']:
        folder_path = os.path.join(app.config['UPLOAD_FOLDER'], folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

    # Handle image uploads
    images = request.files.getlist('images')
    for image in images:
        if image and allowed_file(image.filename, ALLOWED_EXTENSIONS_IMAGES):
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], 'images', filename))

    # Handle video uploads
    videos = request.files.getlist('videos')
    for video in videos:
        if video and allowed_file(video.filename, ALLOWED_EXTENSIONS_VIDEOS):
            filename = secure_filename(video.filename)
            video.save(os.path.join(app.config['UPLOAD_FOLDER'], 'videos', filename))

    # Handle text file upload
    text_file = request.files.get('text_file')
    text_file_name = request.form.get('text_file_name')
    if text_file and allowed_file(text_file.filename, ALLOWED_EXTENSIONS_TEXT):
        filename = f"{text_file_name}.{text_file.filename.split('.')[-1]}"
        text_file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'rules', filename))

    return "Files uploaded successfully!"


# In-memory user for demo purposes
admin_user = "admin"
admin_password = "crl"

@app.route('/admin_login_page')
def admin_login_page():
    print("In side login page")
    return render_template('login.html')

@app.route('/admin_login', methods=['POST'])
def admin_login():
    username = request.form['username']
    password = request.form['password']

    if username == admin_user and password == admin_password:
        # Redirect to success page
        return redirect(url_for('admin'))
    else:
        # Show login credentials are not valid
        return redirect(url_for('success'))

@app.route('/success')
def success():
    return 'Login Username/password is wrong !!!!'


########### Registration Login ##############
##############################  Login Integration ####################


# Function to read users data from users.json
def get_user_data():
    try:
        with open('users.json', 'r') as file:
            user_data = json.load(file)
        return user_data
    except FileNotFoundError:
        return []

# def get_user_data():
#     # Load user data from JSON file
#     with open(user_data_file, 'r') as file:
#         user_data = json.load(file)
#     return user_data

def get_user_data_old():
    # Load user data from JSON file
    with open(user_data_file, 'r') as file:
        user_data = json.load(file)
    return user_data

def get_staff_names():
    # Get staff names from user data
    user_data = get_user_data_old()
    staff_names = [(staff['staff_num'], staff['name']) for staff in user_data]
    return staff_names


# Get staff numbers (from username field)
def get_staff_numbers():
    user_data = get_user_data()
    staff_numbers = [user['username'] for user in user_data if 'username' in user]
    return staff_numbers


def store_staff_data(user_info):
    # Load staff data from JSON file
    try:
        with open(staff_data_file, 'r') as file:
            staff_data = json.load(file)
    except FileNotFoundError:
        # If file does not exist, create an empty list
        staff_data = []

    print(staff_data)
    # Check if staff number already exists in staff data
    existing_staff = next((staff for staff in staff_data if staff['staff_number'] == user_info['staff_number']), None)

    if existing_staff:
        # If staff number already exists, update the entry
        existing_staff.update(user_info)
    else:
        # Add the new staff information
        staff_data.append(user_info)

    # Save updated staff data back to the JSON file
    try:
        with open(staff_data_file, 'w') as file:
            json.dump(staff_data, file, indent=2)  # Write data with indentation
    except IOError as e:
        # Handle any IO errors, such as file permission issues
        print(f"Error writing to file: {e}")


def get_staff_name_for_number(staff_number):
    staff_list =get_user_data_old()
    # print(staff_number)
    # print("==============================")
    # print(staff_list)
    # print("==============================")
    for staff in staff_list:
         if staff["staff_num"] == int(staff_number):
            return staff["name"]
    return None

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        staff_number = request.form.get('staff_number')
        indoor_games = request.form.getlist('indoor_games') or []
        outdoor_games = request.form.getlist('outdoor_games') or []

        submit_action = request.form.get('action')

        if submit_action == 'action1':
            print("Action-1")
            print("staff_number=> "+ staff_number)
            staff_name = get_staff_name_for_number(staff_number)

            user_info = {
                'staff_number': staff_number,
                'name': staff_name,
                'indoor_games': indoor_games,
                'outdoor_games': outdoor_games
            }

            # You could store user_info to a database or file here if needed
            print(user_info)
            store_staff_data(user_info)
            return render_template('registration.html', user_info=user_info, updated=False, staff_numbers=get_staff_numbers())

        if submit_action == 'action2':
            print("Action-2")
            print(staff_number)
            # print(staff_data)
            with open(staff_data_file, 'r') as f:
                staff_data = json.load(f)
            print(staff_data)
            # staff_list =get_user_data_old()
            view_info=None
            for staff in staff_data:
                # print(staff["staff_number"])
                if staff["staff_number"] == staff_number:
                    # print("Staff Num: ",staff["staff_number"])
                    # print("Staff Name: ", staff["name"])
                    # print("Indoor Games: ", staff["indoor_games"])
                    # print("Outdoor Games:",staff["outdoor_games"])
                    view_info = {
                        'staff_number': staff["staff_number"],
                        'name': staff["name"],
                        'indoor_games': staff["indoor_games"],
                        'outdoor_games': staff["outdoor_games"]
                    }
            print(view_info)
            return render_template('registration.html', view_info=view_info)

    return render_template('registration.html', user_info=None, view_info=None)



# @app.route('/view')
# def view():
#     return render_template('view.html')

# @app.route('/view')
# def view():
#     if request.method == 'POST':
#         staff_id = request.form.get('staff_number')
#         if staff_id in staff_data:
#             return render_template('view.html', staff_id=staff_id, data=staff_data[staff_id])
#         else:
#             return render_template('view.html', not_found=True)


@app.route('/update', methods=['POST'])
def update_registration():
    staff_number = request.form['staff_number']
    # Here, you can retrieve the staff info based on the staff_number if needed

    # For this example, we'll simply pass the staff number
    return render_template('registration.html', user_info={'staff_number': staff_number}, updated=True)

    ########## Download ##################################
@app.route('/download', methods=['GET', 'POST'] )
def download():
    # sports = list(data.keys())
    games = ["table_tennis", "fun_game", "cricket_men", "cricket_women", "throwball", "volleyball", "badminton",
             "tug_of_war"]
    # print(sports)
    return render_template('fetch.html', sports=games)

def get_user_data_dwonload():
    # Load user data from JSON file
    with open(staff_data_file, 'r') as file:
        user_data = json.load(file)
    return user_data

def filter_by_game(json_data, game_to_search):
    filtered_results = [staff for staff in json_data if
                        game_to_search in staff["indoor_games"] or game_to_search in staff["outdoor_games"]]
    return filtered_results

@app.route('/episodes', methods=['POST'])
def episodes():
    sport = request.form['sport']
    episodes_data = get_user_data_dwonload()
    # Example usage
    game_to_search = sport
    filtered_results = filter_by_game(episodes_data, game_to_search)
    print(filtered_results)
    print(sport)
    print(episodes_data)
    print(get_user_data_dwonload())
    return render_template('download.html', episodes=filtered_results, sport=sport)

@app.route('/download_excel', methods=['POST'])
def download_excel():
    sport = request.form['sport']
    episodes_data = get_user_data_dwonload()
    game_to_search = sport
    filtered_results = filter_by_game(episodes_data, game_to_search)
    print(filtered_results)

    # Creating a DataFrame from the data
    df = pd.DataFrame(filtered_results)

    # Save DataFrame to Excel in memory
    excel_file = BytesIO()
    df.to_excel(excel_file, index=False)
    excel_file.seek(0)

    return send_file(excel_file, download_name=f"{sport}_Game.xlsx", as_attachment=True)


######################### Integration for Tea Create ###########################
@app.route('/team')
def team():
    return render_template('teamcreate.html')

@app.route('/process', methods=['POST'])
def process():
    # Check if a file is provided in the form
    if 'file' not in request.files:
        return redirect(url_for('teamcreate'))

    file = request.files['file']

    # Check if the file is empty
    if file.filename == '':
        return redirect(url_for('index'))

    # Read the Excel file
    df = pd.read_excel(file)

    # Get the number of teams from the form
    num_teams = int(request.form['num_teams'])

    # Shuffle the data randomly
    df = df.sample(frac=1).reset_index(drop=True)

    # Create random teams based on the number provided
    teams = [df.iloc[i:i + len(df) // num_teams] for i in range(0, len(df), len(df) // num_teams)]

    # Create a new DataFrame to store team information
    team_info = pd.DataFrame(columns=['Team', 'Staff Number', 'Name'])
    for i, team in enumerate(teams):
        team_info = pd.concat([team_info, pd.DataFrame({'Team': [f'Team {i + 1}'] * len(team),
                                                         'Staff Number': team['staff_number'].tolist(),
                                                         'Name': team['name'].tolist()})])

    # Save team information to Excel in memory
    excel_file = BytesIO()
    team_info.to_excel(excel_file, index=False)
    excel_file.seek(0)

    return send_file(excel_file, download_name='team_info.xlsx', as_attachment=True)


##################### Create Team ############################
if __name__ == "__main__":
    app.run(debug=True)


