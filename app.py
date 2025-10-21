from flask import Flask, render_template

app = Flask(__name__)

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

@app.route("/register", methods=["GET"])
def register():
    return render_template("register.html")

if __name__ == "__main__":
    app.run(debug=True)