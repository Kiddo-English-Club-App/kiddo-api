import json
from jinja2 import Environment, FileSystemLoader
from carbonpage.helpers.contexts import ProcessedContext
from carbonpage.helpers.processors import CLI, SnakeCased, Get, CamelCased
from carbonpage.helpers.factories import TemplateFactory
from carbonpage.interfaces import TemplateEngine, FileFactory, ContextBase


class JinjaEngine(TemplateEngine):

    def __init__(self):
        self.env = Environment(loader=FileSystemLoader("dev/templates")) 

    def render_string(self, content: str, context: dict) -> str:
        return self.env.from_string(content).render(context)
    
    def render_template(self, template: str, context: dict) -> str:
        return self.env.get_template(template).render(context)

class SaveModule:

    def __init__(self, path: str, exclude: list[str] = []):
        self.path = path
        self.exclude = exclude

    def process(self,current, name, context: dict):
        modules = []
        with open(self.path, "r", encoding="utf-8") as f:
            content = json.load(f)
            if isinstance(content, list):
                modules = content
            else:
                modules.append(content)
        context = context.copy()
        context[name] = current
        for e in self.exclude:
            if e in context:
                context.pop(e, None)
        
        modules.append(context)

        with open(self.path, "w", encoding="utf-8") as f:
            content = json.dumps(modules, indent=4)
            f.write(content)
        return current

engine = JinjaEngine()

def f(path: str, template: str = None, content: str = ""):
    return TemplateFactory(engine, path, template, content)

module_files = [
    f("{{ base }}src/{{ module }}/__init__.py", template="init2.py"),
    f("{{ base }}src/{{ module }}/domain/__init__.py"),
    f("{{ base }}src/{{ module }}/domain/{{ module }}.py",
          content="# Domain model\n\nclass {{ class }}:\n    pass\n"),
    f("{{ base }}src/{{ module }}/domain/{{ module }}_repository.py", 
          template="repository.py"),
    f("{{ base }}src/{{ module }}/application/__init__.py"),
    f("{{ base }}src/{{ module }}/application/{{ module }}_service.py", template="app_service.py"),
    f("{{ base }}src/{{ module }}/application/dto.py"),
    f("{{ base }}src/{{ module }}/infrastructure/__init__.py"),
    f("{{ base }}src/{{ module }}/controller.py", 
          template="controller.py"),
    ]

module_template = {    
    "context": ProcessedContext(
        processed={
            "module": [CLI(str, "Module name"), SnakeCased()],
            "plural": [CLI(str, "Plural module name"), SnakeCased()],
            "class": [Get("module"), CamelCased(), SaveModule("dev/module.json", ["base"])]
        },
        context={
            "base": ""
        }
    ),
    "files": module_files
}

class MultiContextFile(FileFactory):

    def __init__(
            self,
            context: list[dict|ContextBase],
            factories: list[FileFactory]
            ):
        self.context = context
        self.factories = factories

    def render(self, context: dict):
        for c in self.context:
            if isinstance(c, dict):
                processed = c
            else:
                processed = c.process(context)

            processed.update(context)
            for f in self.factories:
                f.render(processed)

modules = json.load(open("dev/module.json", "r", encoding="utf-8"))

project = {
    "context": {
        "base": "./",
        "modules": modules,
    },
    "files": [
        MultiContextFile(
            context=modules,
            factories=module_files
        ),
        f("{{ base }}src/settings/__init__.py", template="settings.py"),
        f("{{ base }}src/settings/environment.py", template="init.py"),
        f("{{ base }}src/settings/dependencies.py", template="init.py"),
        f("{{ base }}src/settings/error_handlers.py", template="init.py"),
        f("{{ base }}src/app.py", template="app.py"),
        f("{{ base }}src/main.py", template="main.py"),
        f("{{ base }}src/shared/utils.py"),
        f("{{ base }}src/shared/exceptions.py"),
        f("{{ base }}.env"),
        f("{{ base }}.flaskenv", template="flaskenv.txt"),
    ]
}