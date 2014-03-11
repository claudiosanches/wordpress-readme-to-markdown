import sublime_plugin
import os
import shutil
import re
from functools import partial


class WordpressReadmeToMarkdownCommand(sublime_plugin.TextCommand):

    def __init__(self, *args, **kwargs):
        super(WordpressReadmeToMarkdownCommand, self).__init__(*args, **kwargs) # Calls the parent constructor to maintain compatibilty
        # Dictionary of replaces
        titles = [
            ["""^(===)+(.+)+(===)\n""","""#\\2#\n"""],
            ["""^(==)+(.+)+(==)\n""","""##\\2##\n"""],
            ["""^(=)+(.+)+(=)\n""","""###\\2###\n"""]
        ]

        self.titles = []

        for search, replace in titles:
            # Compiles the Expression
            reg = re.compile(search,re.MULTILINE)

            # Saves a partial object with call to re.sub preparatted
            self.titles.append(partial(reg.sub, replace))

        other_replaces = {
            """^([^:\n#]+): (.+)$""": """**\\1:** \\2  """
        }

        self.other_replaces = {}
        for search, replace in other_replaces.iteritems():
            # Compiles the Expression
            reg = re.compile(search,re.MULTILINE)

            # Saves a partial object with call to re.sub preparatted
            self.other_replaces[search] = partial(reg.sub, replace)

        # Compile and save the regex
        self.plugin_slug = re.compile("""^=== (.+) ===\n""")
        self.plugin_screenshot = re.compile("""== Screenshots ==(.*?)==""", re.MULTILINE|re.DOTALL)
        self.plugin_information = re.compile("""=== (.+) ===(.*?)==""", re.MULTILINE|re.DOTALL)
        self.plugin_readme = re.compile("""(.+)/readme.txt$""")


    def getPluginSlug(self, content):
        """
        Gets the plugin slug
        """
        findName = self.plugin_slug.match(content)
        slug = findName.group(1).replace(" ", "-")

        return slug.lower()


    def parseScreenshots(self, content, slug):
        """
        Adds link to screenshots
        """

        images = self.plugin_screenshot.search(content)

        if images:
            for index, line in enumerate(images.group(1).strip().split("""\n""")):
                content = content.replace(line, \
                    """### %(name)s ###\n![%(name)s](http://s.wordpress.org/extend/plugins/%(slug)s/screenshot-%(index)s.png)\n""" \
                    % {"name": line, "slug": slug, "index": index + 1})

        return content


    def parseInformation(self, content):
        """
        Parse Information section
        """

        infos = self.plugin_information.search(content)
        func = self.other_replaces[ """^([^:\n#]+): (.+)$"""]
        for info in infos.group(2).strip().split("""\n"""):
            string = func(info)
            content = content.replace(info, string)

        return content


    def run(self, edit):
        # Get current file path
        oldFile = self.view.file_name()

        # Checks if the file is the readme.txt
        if self.plugin_readme.search(oldFile):

            # Generate the README.md path
            newFile = '%s/README.md' % (os.path.dirname(oldFile))

            # Create a new markdown file
            shutil.copy2(oldFile, newFile)

            getContent = open(newFile, 'r')
            content = getContent.read()

            # Gets the plugin slug
            slug = self.getPluginSlug(content)

            # Customizes the informations session
            content = self.parseInformation(content)

            # Parse Screenshots
            content = self.parseScreenshots(content, slug)

            # Replaces the headings
            for func in self.titles:
                content = func(content) #Simple, no?

            getContent.close()

            # Write the new content
            writeContent = open(newFile, 'w')
            writeContent.write(content)
            writeContent.close()
