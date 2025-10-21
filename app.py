from flask import Flask, render_template, request
from forms import RegistrationForm
from flask_wtf.csrf import CSRFProtect

'''
# To generate a secret key, run the following code once in a Python shell:
import secrets 
print(secrets.token_hex(16))
'''
app = Flask(__name__)

# ✅ Add a secret key (required for CSRF)
app.config['SECRET_KEY'] = '6d3552184a04f416e7c240dc7f0fe13a'  # use a random value in real apps

# ✅ Enable CSRF protection
csrf = CSRFProtect(app)

@app.route("/", methods=["GET"])
def welcome():
    #return "Welcome to Wholly Roasters!"
    return render_template("home.html", name = "Parker")

@app.route("/about", methods=["GET"])
def about():
    #return "This is the 'About Us' page."
    return render_template("about.html")

@app.route("/inventory", methods=["GET"])
def inventory():
    return render_template("inventory.html", 
                           count = 5,
                           beans = ["Arabica", 
                                    "Robusta", 
                                    "Liberica", 
                                    "Excelsa", 
                                    "Maragogype", 
                                    "Typica", 
                                    "Bourbon", 
                                    "Caturra", 
                                    "Gesha", 
                                    "Pacamara", 
                                    "SL28", 
                                    "SL34"])

@app.route("/shop", methods=["GET"])
def shop():
    return render_template("shop.html", 
                           cart = ["12oz Medium Roast", 
                                   "24oz French Roast", 
                                   "96oz Whole Beans"])

'''
@app.route("/register", methods=["GET", "POST"])
def register():
    message = ""
    errors = []   
    if request.method == "POST":
        username = request.form["uname"]
        password = request.form["pword"]
        confirm = request.form["confirm"]
        # Here you would typically save the user info to a database
        message = f"Successfully registered user: {username}!"
        
        if not username:
            errors.append("Username can't be blank!")
        
        if not password:
            errors.append("Password can't be blank!")
            
        if not confirm:
            errors.append("Password can't cannot be blank!")
            
        if len(username) < 3:
            errors.append("Username must be greater than 3 characters!")
            
        if password != confirm:
            errors.append("Passwords don't match!")
        
        if errors:
            message = "Registration failed! See errors below:"
        else:
            message = f"Successfully registered {username}."
    
    return render_template("register.html",
                           message=message,
                           errors=errors)
'''
@app.route("/register", methods=["GET", "POST"])
def register():
    message = ""
    form = RegistrationForm()

    if request.method == "POST":
        if form.validate_on_submit():
            username = form.data["uname"]
            password = form.data["pword"]
            confirm = form.data["confirm"]
            message = f"Successfully registered {username}!"
        else:
            message = "Registration failed."

    return render_template("register.html",
                           message=message,
                           form=form)

if __name__ == "__main__":
    app.run(debug=True)