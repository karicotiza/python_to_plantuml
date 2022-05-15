import io
import os
from antlr4 import *
from antlr4.error.ErrorListener import *
from gen.Python3Lexer import Python3Lexer
from gen.Python3Parser import Python3Parser
from gen.Python3Visitor import Python3Visitor


class Python3ErrorListener(ErrorListener):
    def __init__(self, output):
        self.output = output
        self._symbol = ''

    def syntaxError(self, recognizer, offending_symbol, line, column, msg, e):
        self.output.write(msg)
        self._symbol = offending_symbol.text
        stack = recognizer.getRuleInvocationStack()
        stack.reverse()
        print(
            "error at {}:{} - {}".format(
                str(line),
                str(column),
                msg
            )
        )

    @property
    def symbol(self):
        return self._symbol


class MyParser:
    def __init__(self):
        self.output = io.StringIO()
        self.error = io.StringIO()
        self.errorListener = Python3ErrorListener(self.error)

    def setup(self, path):
        my_input = FileStream(path, encoding="utf-8")
        lexer = Python3Lexer(my_input)
        stream = CommonTokenStream(lexer)

        stream.fill()
        parser = Python3Parser(stream)
        parser.removeErrorListeners()
        parser.addErrorListener(self.errorListener)
        return parser

    def make_uml(self, path_to_input: str, path_to_output: str):
        if os.path.isdir(path_to_input):
            files = os.listdir(path_to_input)
            with open(f"{path_to_output}", mode="w", encoding="utf-8") as output_file:
                for file in files:
                    with open(f"{os.path.join(path_to_input, file)}", mode="r", encoding="utf-8") as code:
                        for line in code:
                            output_file.write(line)
            path_to_input = path_to_output

        parser = self.setup(path_to_input)
        tree = parser.file_input()
        visitor = MyVisitor()
        visitor.visit(tree)
        visitor.get_plant_uml()

        with open(f"{path_to_output}", mode="a", encoding="utf-8") as output_file:
            output_file.truncate(0)
            for line in visitor.plant_uml_text:
                output_file.write(line + "\n")


class MyVisitor(Python3Visitor):
    plant_uml_text = ["@startuml"]
    classes = []

    def visitClassdef(self, ctx):
        if self.plant_uml_text[-1] == "@startuml":
            self.plant_uml_text.append(f"class {ctx.NAME()}" + " {")
            self.classes.append(str(ctx.NAME()))
        else:
            self.plant_uml_text.append("}")
            self.plant_uml_text.append("")
            self.plant_uml_text.append(f"class {ctx.NAME()}" + " {")
            self.classes.append(str(ctx.NAME()))
        self.visitChildren(ctx)

    def visitArglist(self, ctx):
        if str(ctx) == "[1039 610 412 180]":
            if ctx.getText() == "ABC":
                class_position = []
                for index in range(len(self.plant_uml_text)):
                    if "class" in self.plant_uml_text[index]:
                        class_position.append(index)
                class_position = class_position[-1]
                class_name = self.plant_uml_text[class_position].split(" ")[1]
                self.plant_uml_text[class_position] = f"abstract class {class_name}" + " {"
            else:
                class_name = []
                for element in self.plant_uml_text:
                    if "class" in element:
                        class_name.append(element)
                class_name = class_name[-1].split(" ")[1]
                self.plant_uml_text.insert(-1, f"class {class_name} implements {ctx.getText()}")
            self.visitChildren(ctx)

    def visitFuncdef(self, ctx):
        if str(ctx)[-12:] == "610 412 180]":
            name = str(ctx.NAME())
            name = self.__visibility(name)
            self.plant_uml_text.append("{method} " + name)
            self.visitChildren(ctx)

    def visitParameters(self, ctx):
        function_position = self.__function_position()

        arguments = str(ctx.getText())
        arguments = arguments.replace("self,", "")
        arguments = arguments.replace("self", "")

        if "=" in arguments:
            arguments = arguments.split("=")
            for index in range(len(arguments)):
                if index == 0:
                    arguments[index] += ", "
                    continue
                if "," in arguments[index]:
                    arguments[index] = arguments[index].split(",")[1] + ", "
            arguments = "".join(arguments[:-1])[:-2] + ")"

        if ":" in arguments:
            arguments = arguments.split(":")
            for index in range(len(arguments)):
                if "," in arguments[index]:
                    arguments[index] = arguments[index].split(",")[0] + ", "
            arguments = "(" + "".join(arguments[1:])

        arguments = arguments.replace(",", ", ")
        self.plant_uml_text[function_position] += f"{arguments}"
        self.visitChildren(ctx)

    def visitTest(self, ctx):
        if str(ctx) == "[226 609 412 714 1046 610 412 180]":
            function_position = self.__function_position()
            self.plant_uml_text[function_position] += ": " + str(ctx.getText())
            self.visitChildren(ctx)
        elif str(ctx) == "[226 215 611 412 714 1046 610 412 180]":
            function_position = self.__function_position()
            self.plant_uml_text[function_position] += ": " + str(ctx.getText())
            self.visitChildren(ctx)

    def visitSimple_stmt(self, ctx):
        if str(ctx) == "[411 714 1046 610 412 180]":
            field = ctx.getText().rstrip()
            variable, value, annotation = self.__separate_field(field)
            variable = variable.split(",")
            for element in variable:
                element = self.__visibility(element)
                if annotation:
                    self.plant_uml_text.append("{field} " + element + ": " + annotation)
                else:
                    self.plant_uml_text.append("{field} " + element + ": " + value)
            self.visitChildren(ctx)
        elif str(ctx) == "[411 714 230 609 412 714 1046 610 412 180]":
            if ctx.getText()[:5] == "self.":
                if "=" in ctx.getText():
                    field = ctx.getText().rstrip()
                    variable, value, annotation = self.__separate_field(field)
                    variable = variable.split(",")
                    for element in variable:
                        element = self.__visibility(element[5:])
                        if annotation:
                            self.plant_uml_text.append("{field} " + element + ": " + annotation)
                        else:
                            self.plant_uml_text.append("{field} " + element + ": " + value)
                    self.visitChildren(ctx)

            if ctx.getText()[:6] == "return":
                function_position = self.__function_position()
                if not (":" in self.plant_uml_text[function_position]):
                    self.plant_uml_text[function_position] += ": " + str(ctx.getText().rstrip())[6:]
        elif "411 714 230 215 611 412 714 1046 610 412 180" in str(ctx):
            if ctx.getText()[:6] == "return":
                function_position = self.__function_position()
                if not (":" in self.plant_uml_text[function_position]):
                    self.plant_uml_text[function_position] += ": " + str(ctx.getText().rstrip())[6:]
        elif "411 714" in str(ctx) and "412 714 1046 610 412 180" in str(ctx):
            if ctx.getText()[:6] == "return":
                function_position = self.__function_position()
                if not (":" in self.plant_uml_text[function_position]):
                    self.plant_uml_text[function_position] += ": " + str(ctx.getText().rstrip())[6:]

    def __function_position(self):
        function_position = []
        for index in range(len(self.plant_uml_text)):
            if "{method}" in self.plant_uml_text[index]:
                function_position.append(index)
        return function_position[-1]

    @staticmethod
    def __visibility(name):
        if name[0:2] == "__":
            if name[-2:] == "__":
                name = "-" + name
            else:
                name = "-" + name[2:]
        elif name[0] == "_" and name[1] != "_":
            name = "#" + name[1:]
        else:
            name = "+" + name
        return name

    @staticmethod
    def __separate_field(field):
        field = field.split("=")

        if field[1] == "[]":
            field[1] = "List"
        elif field[1] == "{}":
            field[1] = "Dict"
        elif field[1] == "()":
            field[1] = "Tuple"

        annotation = None

        if ":" in field[0]:
            field[0], annotation = field[0].split(":")

        return field[0], field[1], annotation

    def __check_functions(self):
        for index in range(len(self.plant_uml_text)):
            if "{method}" in self.plant_uml_text[index] and not (":" in self.plant_uml_text[index]):
                self.plant_uml_text[index] += ": None"

    def __link_classes(self):
        associations = []

        index = -1
        for line in self.plant_uml_text:
            if "class" in line and not("implements" in line):
                index += 1
            elif not("implements" in line):
                for element in self.classes:
                    if element in line:
                        associations.append(element + " <-- " + self.classes[index])
        associations = list(set(associations))

        self.plant_uml_text.append("")
        for element in associations:
            self.plant_uml_text.append(element)

    def get_plant_uml(self):
        self.plant_uml_text.insert(1, "")
        self.plant_uml_text.append("}")
        self.__check_functions()
        self.__link_classes()
        self.plant_uml_text.append("")
        self.plant_uml_text.append("@enduml")
        return self.plant_uml_text


if __name__ == '__main__':
    result = MyParser()
    input_path = str(input("Path to file / project: "))
    output_file = str(input("Path to text file with PlantUML code: "))
    result.make_uml(input_path, output_file)
