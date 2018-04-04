import codecs
from html.parser import HTMLParser


class Colors:
    """ Generates ANSI escape codes for tags """

    # Reset color
    RESET = '\u001b[0m'

    def __init__(self):
        self.i = 0
        self.j = 1

    def get_color(self):
        """ Rotates through 256 colors """

        code = str(self.i * 16 + self.j)
        color = "\u001b[48;5;" + code + "m"
        if(self.i < 16):
            self.i = self.i + 1
        else:
            self.i = 0
        if(self.j < 16):
            self.j = self.j + 1
        else:
            self.j = 0
        return color


class Tag:
    """ Data structure used for tag contains the name and the color of the tag """

    def __init__(self, name, color):
        self.name = name
        self.color = color

    def __repr__(self):
        return self.color + self.name + Colors.RESET

    def __str__(self):
        return self.color + self.name + Colors.RESET


# Init variables
colors = Colors()
tags = []


def findTagIndex(name):
    """ Find the tag index, if not found then create one 

    Args:
        name (str): tag name

    Returns:
        The return value. index number of the found tag name.

    """
    for i in range(len(tags)):
        if(tags[i].name == name):
            return i

    createdTag = Tag(name, colors.get_color())
    tags.append(createdTag)
    return -1


# Parser Class which we will feed the html
class MyHTMLParser(HTMLParser):
    # numTags is used to identify how much tabs to put in
    numTags = 0
    # output is the output string from the parser
    output = ''
    # currentColor is the text color that is being outputed
    currentColor = ''

    def generateTabs(self):
        for x in range(0, self.numTags):
            self.output += '\t'

    def handle_starttag(self, tag, attrs):
        """ Handles start of the tag """

        # Finds the index of the tag
        index = findTagIndex(tag)
        self.output += '\n'
        self.output += tags[index].color
        # currentColor is used for data output later
        self.currentColor += tags[index].color
        self.generateTabs()
        self.output += '<'
        self.output += tag

        # Loop through the attributes of the tag
        for attr, value in attrs:
            self.output += ' '
            self.output += attr.strip()
            self.output += '="' + value.strip() + '"'

        self.output += '>'
        self.output += Colors.RESET
        self.numTags = self.numTags + 1

    def handle_endtag(self, tag):
        """ Handles when the end tag is reached """

        index = findTagIndex(tag)
        self.numTags = self.numTags - 1
        self.output += '\n'
        self.generateTabs()
        self.output += tags[index].color
        self.output += '</' + tag + '>'
        self.output += Colors.RESET

    def handle_data(self, data):
        """ Handles data from the tag being processed """

        text = data.strip()
        if text:
            self.output += '\n'
            self.generateTabs()
            self.output += self.currentColor + text + Colors.RESET

    def handle_comment(self, data):
        """ Handles comments from the html file """

        self.output += '\n'
        self.generateTabs()
        self.output += "<!--" + data + "-->"


def main():
    """ Main Function """

    # File names
    inputFileName = "test.html"
    outputFileName = "output.txt"

    # Read the file
    f = codecs.open(inputFileName, 'r', 'utf-8')
    file = f.read()
    f.close()

    # Create HTML Parser and feed the file to parser
    parser = MyHTMLParser()
    parser.feed(file)

    # Output file generate
    f = open(outputFileName, 'w')
    f.write(parser.output)
    f.close()


main()
