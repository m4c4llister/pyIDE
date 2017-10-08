from flask import Flask,session,redirect,request,render_template,url_for
import commands

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(
    SECRET_KEY="A0Zr98j/3yX R~XHH!jmN]LWX/,?RT",
))

#Change these in setup
DEFAULT_USERNAME = "pyadmin"
DEFAULT_PASSWORD = "!#s3mp3rP4R4TU5#!"

def process_command(codeblock):
		tokens = codeblock.split("\n")

		command = ""
		for token in tokens:

				token = token.replace("\r","")
				#token = token.replace("\"","'")
				command += token + ";"

		wrap = "python -c '" + command + "'"
		result = commands.getoutput(wrap)
		return result


@app.route('/')
def hello_world():
	return redirect('/login')


@app.route("/login",methods=["GET","POST"])
def login():
		error = None
		if request.method == "POST":
				form_username = request.form["username"]
				form_password = request.form["password"]

				if (form_username == DEFAULT_USERNAME) and (form_password == DEFAULT_PASSWORD):
						user = {"id":1,"username":DEFAULT_USERNAME}
						session["logged_in"] = True
						session["user"] = user
						return redirect(url_for("ide"))
				else:
						error = "Wrong username or password"
						return render_template("login.html",error=error)
		else:
				return render_template("login.html")


@app.route("/ide",methods=["GET","POST"])
def ide():
		if not session.get("logged_in"):
				return "not allowed"

		user = session.get("user")

		if request.method == "GET":
				return render_template("ide.html",username=user["username"])

		if request.method == "POST":
				codeblock = request.form["code"]
				result = process_command(codeblock)
				return render_template("ide.html",username=user["username"],result=result)


@app.route('/logout')
def logout():
		session.pop('logged_in', None)
		session.pop('user', None)
		return redirect(url_for('login'))


if __name__ == '__main__':
	app.run("0.0.0.0")
