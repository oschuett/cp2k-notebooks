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
                     animation-name: changed_animation; animation-duration: 3s;
                 }
                 .codepreview {
                     padding: 10px;
                     line-height: 1.3;
                     font-family: monospace;
                     border: 1px solid black;
                 }
                 """
        style = ipw.HTML("<style>" + css + "</style>")
        self.html = ipw.HTML()
        super().__init__([style, self.html])

    @property
    def value(self):
        return self._value

    def _render(self, markup):
        """Turn text with <changed> tags into HTML."""
        inner_html = markup.strip().replace("\n", "<br>\n").replace(" ", "&nbsp;")
        inner_html = inner_html.replace("<changed>","<span class='changed'>")
        inner_html = inner_html.replace("</changed>","</span>")
        full_html = "<div class='codepreview'>" + inner_html + "</div>"
        self.html.value = full_html

    def _markup(self, line, annotations):
        """Parse annotations and wrap all changed tokens into <changed> tags."""
        d = len(line) - len(annotations)
        annotations = annotations + " " * d
        markup, token, changed = "", "", False
        for char, anno in zip(line, annotations):
            if char.isspace():
                markup += "<changed>" + token + "</changed>" if changed else token
                markup += char
                token, changed = "", False
            else:
                token += char
                changed |= (anno != " ")

        markup += "<changed>" + token + "</changed>" if changed else token
        return(markup)

    @value.setter
    def value(self, new_value):
        """Update content and highligh changed tokens."""
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
                markup_lines.append(self._markup(changed_line[2:], line[2:]))
                changed_line = None
            else:
                pass  # ignore removed lines

        if changed_line:
            markup_lines.append("<changed>" + changed_line[2:] + "</changed>")
        self._render("\n".join(markup_lines))
        self._value = new_value

#EOF