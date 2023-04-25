from flask import Flask, render_template, request, Markup
import llm

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        if request.method == 'POST':
            if "openApiKey" in request.form:
                print("POST - openApiKey")
                openApiKey = request.form['openApiKey']
                envApiResponse = llm.setOpenApiKey(openApiKey)
                if envApiResponse:
                    print("POST - openApiKey - envApiResponse: ", envApiResponse)
                    return render_template('index.html', output='', show_question_input=True)
                else:
                    return render_template('index.html', output='', show_question_input=False, error_message="Incorrect secret text.")
            else:
                if 'query' in request.form:
                    print("POST - query")
                    query = request.form['query']
                    output = llm.askQuestion(query)
                    output = Markup(f'<span class="underlined">Question</span> : <br>{query}<br><br>Anwser: <br>{output}')
                    return render_template('index.html', output=output, show_question_input=True)
                return render_template('index.html', output='', show_question_input=True)
        return render_template('index.html', output='', show_question_input=False)
    except Exception as e:
        print(e)
        print(request.form)
        return render_template('index.html', output='', show_question_input=False, error_message=e)

@app.after_request
def add_no_cache(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=5005)
