class Codeblock:
    def __init__(self, title, description = "", footer = "", extra_title = "", style="asciidoc"):
        colours = {
            "pink": "\u001b[0;35m{TEXT}\u001b[0;0m",
            "red": "\u001b[0;31m{TEXT}\u001b[0;0m",
            "yellow": "\u001b[0;33m{TEXT}\u001b[0;0m",
            "green": "\u001b[0;32m{TEXT}\u001b[0;0m",
            "cyan": "\u001b[0;36m{TEXT}\u001b[0;0m",
            "blue": "\u001b[0;34m{TEXT}\u001b[0;0m"
        }

        self.title = title.replace("\n", "\n> ").replace("`", "'")
        self.description = description.replace("\n", "\n> ").replace("`", "'")
        self.footer = footer.replace("\n", "\n> ").replace("`", "'")
        self.extra_title = extra_title.replace("\n", "\n> ").replace("`", "'")
        self.style = style

        if self.extra_title != "":
            self.extra_title = f" {self.extra_title}"

    def __str__(self):
        if self.description == "":
            return f"> ```ini\n> [ {self.title} ]{self.extra_title}```"
        elif self.description != "" and self.footer == "":
            return f"> ```ini\n> [ {self.title} ]{self.extra_title}``````{self.style}\n> {self.description}```"
        else:
            return f"""> ```ini\n> [ {self.title} ]{self.extra_title}``````{self.style}\n> {self.description}``````ini\n> ; {self.footer}```"""
