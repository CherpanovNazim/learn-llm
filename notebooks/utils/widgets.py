from collections import defaultdict
import html
import uuid

from IPython.display import display, HTML


class LLMCallVisualiser:
    """
    Visualises the LLM call displaying tabs like "Prompt",
      "LLM Output", "Generated Code", ..., "Hide All"
    """

    WIDGET_HTML_TEMPLATE: str = """
<html>
<head>
  <style>
    .tab {
      display: none;
    }

    .tablink {
      border: 1px solid transparent;
      transition: border-color 0.2s;
      margin-left: 3px;
    }

    .tablink.active {
      background-color: rgb(230, 230, 230);
    }

    .tablink.active::before {
      content: '';
    }
  </style>
</head>
<body>
<div style="border: 1px solid lightgray; margin: 8px;">

<button class="tablink" onclick="openTab_[Visualiser_ID_Placeholder]('Prompt')"
   id="Prompt_Button_[Visualiser_ID_Placeholder]">Prompt</button>
<button class="tablink" onclick="openTab_[Visualiser_ID_Placeholder]('LLM Output')"
   id="LLMOutput_Button_[Visualiser_ID_Placeholder]">LLM Output</button>
<button class="tablink" onclick="openTab_[Visualiser_ID_Placeholder]('Generated Code')"
   id="GeneratedCode_Button_[Visualiser_ID_Placeholder]" style="display: none;">Generated Code</button>
<button class="tablink" onclick="openTab_[Visualiser_ID_Placeholder]('Code Issues')"
   id="CodeIssues_Button_[Visualiser_ID_Placeholder]" style="display: none;">Code Issues</button>
<button class="tablink" onclick="openTab_[Visualiser_ID_Placeholder]('Hide All')"
   id="HideAll_Button_[Visualiser_ID_Placeholder]">Hide All</button>

<div style="padding: 8px;">
<div class="tabcontent" id="Prompt_Div_[Visualiser_ID_Placeholder]">
    <pre style="margin-bottom: 0em" id="DynamicText"></pre>
</div>

<div class="tabcontent" id="LLMOutput_Div_[Visualiser_ID_Placeholder]">
    <pre style="margin-bottom: 0em"></pre>
</div>

<div class="tabcontent" id="GeneratedCode_Div_[Visualiser_ID_Placeholder]">
    <pre style="margin-bottom: 0em"></pre>
</div>

<div class="tabcontent" id="CodeIssues_Div_[Visualiser_ID_Placeholder]">
    <pre style="margin-bottom: 0em"></pre>
</div>

<div class="tabcontent" id="HideAll_Div_[Visualiser_ID_Placeholder]">
</div>
</div>

</div>

<script>
function openTab_[Visualiser_ID_Placeholder](tabName) {
    var i, tabcontent, tablinks;
    tabcontent = document.querySelectorAll('[id*="_Div_[Visualiser_ID_Placeholder]"]');
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.querySelectorAll('[id*="_Button_[Visualiser_ID_Placeholder]"]');
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].classList.remove("active");
    }
    var tabId = tabName.replace(" ", "");
    document.getElementById(tabId + "_Div_[Visualiser_ID_Placeholder]").style.display = "block";
    var button = document.getElementById(tabId + "_Button_[Visualiser_ID_Placeholder]");
    button.classList.add("active");
}
openTab_[Visualiser_ID_Placeholder]("Prompt");

function updateTab_[Visualiser_ID_Placeholder](tabName, append, text) {
    // Update tab text
    var tabId = tabName.replace(" ", "");
    var divElement = document.getElementById(tabId + "_Div_[Visualiser_ID_Placeholder]");
    var preElements = divElement.getElementsByTagName("pre");
    if (preElements.length == 1) {
        if (append) preElements[0].innerHTML += text;
        else preElements[0].innerHTML = text;
    }
    // Once we changed any tab content, we make its tablink visible
    var button = document.getElementById(tabId + "_Button_[Visualiser_ID_Placeholder]");
    button.removeAttribute("style");
}
</script>

</body>
</html>
"""

    def __init__(
        self,
        prompt: str,
    ):
        self.html_content = None
        self.js_runner = None
        self.visualiser_id = str(uuid.uuid4()).replace("-", "")[:8]
        self.widget_visualised = False

        self.tabs_that_had_streaming = set()
        self.tabs_texts = defaultdict(str)
        self.tabs_texts["Prompt"] = prompt
    
    def display(self):
        """Starts visualising LLM call and sets Prompt"""

        if not self.widget_visualised:
            self.widget_visualised = True

            prepared_widget_html = LLMCallVisualiser.WIDGET_HTML_TEMPLATE.replace(
                "[Visualiser_ID_Placeholder]",
                self.visualiser_id)
            display(HTML(prepared_widget_html))
            self.js_runner_for_stream = display(
                HTML(""),
                display_id=f"js_for_stream_{self.visualiser_id}")

            self.update_content(tab_name="Prompt", text=self.tabs_texts["Prompt"])

    def open_tab(
        self,
        tab_name: str,  # One of: "Prompt", "LLM Output", "Generated Code" or "Code Issues"
    ):
        """Opens specific tab by its name"""

        script = f"<script>openTab_{self.visualiser_id}('{tab_name}')</script>"
        display(HTML(script))

    def update_content(
        self,
        tab_name: str,  # One of: "Prompt", "LLM Output", "Generated Code" or "Code Issues"
        text: str,
        append: bool = False,  # To append the text rather than replace
        change_tab: bool = False,  # To change tab after content update
    ):
        """Updates the content of specific tab"""

        escaped_text = html.escape(text)
        escaped_text = repr(escaped_text)

        if append:
            self.tabs_texts[tab_name] += text
            script = f"<script>updateTab_{self.visualiser_id}("\
                     f"'{tab_name}', true, {escaped_text})</script>"
            self.js_runner_for_stream.update(HTML(script))
        else:
            self.tabs_texts[tab_name] = text
            script = f"<script>updateTab_{self.visualiser_id}("\
                     f"'{tab_name}', false, {escaped_text})</script>"
            display(HTML(script))

        if change_tab:
            self.open_tab(tab_name)

    def append_streamed_text(
        self,
        text_to_append: str,
        tab_name: str = "LLM Output",
    ):
        """Callback for updating tab with stream of text from LLM"""

        self.update_content(
            tab_name=tab_name,
            text=text_to_append,
            append=True)

        if tab_name not in self.tabs_that_had_streaming:
            self.tabs_that_had_streaming.add(tab_name)
            self.open_tab(tab_name)

    def finalize_streamed_text(
        self,
        tab_name: str = "LLM Output",
    ):
        """Finalizes streamed text from LLM"""

        self.update_content(
            tab_name=tab_name,
            text=self.tabs_texts[tab_name],
            append=False)
