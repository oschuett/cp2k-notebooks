import ipywidgets as ipw
import difflib

# author: Ole Schuett

class CodePreviewer(ipw.Box):
    def __init__(self):
        self._value = None
        css = """@keyframes changed_animation {
                     from {color: red;   font-weight: bold;}
                     to   {color: black; font-weight: normal;}
                 }
                 .changed {
                     animation-name: changed_animation; animation-duration: 4s;
                 }"""
        style = ipw.HTML("<style>" + css + "</style>")
        self.html = ipw.HTML()
        super().__init__([style, self.html])

    @property
    def value(self):
        return self._value

    def _render(self, markup):
        inner_html = markup.strip().replace("\n", "<br>\n").replace(" ", "&nbsp;")
        inner_html = inner_html.replace("<changed>","<span class='changed'>")
        inner_html = inner_html.replace("</changed>","</span>")
        full_html = "<div style='font-family:monospace; line-height:1.3; border:1px solid black; padding: 10px'>"
        full_html += inner_html
        full_html += "</div>"
        self.html.value = full_html

    @value.setter
    def value(self, new_value):
        if not self._value:
            self._render(new_value)
            self._value = new_value
            return

        differ = difflib.Differ()
        diff = differ.compare(self._value.split("\n"), new_value.split("\n"))
        markup_lines = []
        changed_line = None
        for line in diff:
            line = line.strip("\n")
            if line.startswith("  "):
                markup_lines.append(line[2:])
            elif line.startswith("+ "):
                changed_line = line

            elif line.startswith("? ") and changed_line:
                d = len(changed_line) - len(line)
                line = line + " " * d
                markup_lines.append("")
                for annotation, char in zip(line[2:], changed_line[2:]):
                    if annotation == " ":
                        markup_lines[-1] += char
                    else:
                        markup_lines[-1] += "<changed>" + char + "</changed>"
                changed_line = None

        self._render("\n".join(markup_lines))
        self._value = new_value

#EOF
