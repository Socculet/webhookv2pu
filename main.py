from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

HTML_TEMPLATE = """
<!doctype html>
<title>Discord Webhook Sender</title>
<h1>Send a Discord Webhook</h1>
<form method="post">
    Webhook URL: <input type="text" name="webhook_url" required><br>
    Message: <textarea name="message" required></textarea><br>
    Number of Times: <input type="number" name="count" min="1" required><br>
    <button type="submit">Send</button>
</form>
{% if result %}
<h2>Results</h2>
<ul>
    {% for res in result %}
    <li>{{ res }}</li>
    {% endfor %}
</ul>
{% endif %}
"""

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        webhook_url = request.form.get("webhook_url")
        message = request.form.get("message")
        count = int(request.form.get("count"))
        payload = {"content": message}
        result = []
        for i in range(count):
            response = requests.post(webhook_url, json=payload)
            if response.status_code == 204:
                result.append(f"Message {i + 1}: Sent successfully.")
            else:
                result.append(f"Message {i + 1}: Failed with status code {response.status_code}.")
    return render_template_string(HTML_TEMPLATE, result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
