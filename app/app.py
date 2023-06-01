import json
import requests
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

API_KEY = ""
API_ENDPOINT = "https://api.openai.com/v1/chat/completions"

def generate_chat_completion(messages, model="gpt-4", temperature=1, max_tokens=None):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    }
    
    data = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
    }
    
    if max_tokens is not None:
        data["max_tokens"] = max_tokens
    
    response = requests.post(API_ENDPOINT, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])

app.layout = html.Div(
    style={
        "width": "50%",
        "margin": "auto",
        "padding": "20px",
    },
    children=[
        html.H1("Use GPT-4 or 3.5", style={"textAlign": "center"}),
        html.Div(
            style={"marginBottom": "20px"},
            children=[
                html.Label("Place API key here"),
                dcc.Input(
                    id="api-key-input",
                    type="text",
                    value="",
                    style={"width": "100%", "padding": "10px", "fontSize": "16px", "borderRadius": "10px"}
                ),
            ]
        ),
        html.Div(
            style={"marginBottom": "20px"},
            children=[
                dcc.Dropdown(
                    id="model-dropdown",
                    options=[
                        {"label": "GPT-4", "value": "gpt-4"},
                        {"label": "GPT-3.5-turbo", "value": "gpt-3.5-turbo"}
                    ],
                    value="gpt-4",
                    style={"width": "100%", "padding": "10px", "fontSize": "16px", "borderRadius": "10px"},
                    searchable = False
                )
            ]
        ),
        html.Div(
            style={"marginBottom": "20px"},
            children=[
                dcc.Textarea(
                    id="prompt-input",
                    placeholder="Enter a prompt",
                    value="",
                    style={"width": "100%", "height": "200px", "padding": "10px", "fontSize": "16px", "borderRadius": "10px"}
                )
            ]
        ),
        html.Button(
            "Generate",
            id="generate-button",
            n_clicks=0,
            style={
                "backgroundColor": "#4CAF50",
                "color": "white",
                "border": "none",
                "padding": "10px 20px",
                "fontSize": "16px",
                "cursor": "pointer",
                "marginTop": "10px",
                "borderRadius": "20px"
            }
        ),
        html.Div(id="error-message", style={"color": "red", "marginTop": "10px"}),
        html.Div(id="output-div"),
    ]
)

@app.callback(
    [Output("output-div", "children"), Output("error-message", "children")],
    [Input("generate-button", "n_clicks")],
    [
        dash.dependencies.State("prompt-input", "value"),
        dash.dependencies.State("api-key-input", "value"),
        dash.dependencies.State("model-dropdown", "value")
    ]
)
def generate_output(n_clicks, prompt, api_key, model):
    global API_KEY

    if n_clicks == 0:
        return "", ""  # Initially, no output and error message are shown

    if not api_key:
        return "", "Please enter an API key."  # Show error message for missing API key

    API_KEY = api_key

    if prompt:
        messages = [
            {"role": "system", "content": "Hello! How may I help you?"},
            {"role": "user", "content": prompt}
        ]
        try:
            response_text = generate_chat_completion(messages, model=model)
            return dcc.Markdown(response_text), ""  # Return output and no error message
        except Exception as e:
            return "", str(e)  # Show error message for invalid API key or other errors

    return "", "Please enter a prompt."  # Show error message for missing prompt


if __name__ == '__main__':
    app.run_server(debug=False)