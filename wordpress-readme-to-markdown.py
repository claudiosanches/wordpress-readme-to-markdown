import sublime
import sublime_plugin
import os
import shutil
import re

class WordpressReadmeToMarkdownCommand(sublime_plugin.TextCommand):

    def replaceAll(self, search, replace, content):
        """
        Finds in all lines and replaces
        """
        find = re.compile(search, re.MULTILINE)

        return find.sub(replace, content)

    def getPluginSlug(self, content):
        """
        Gets the plugin slug
        """
        findName = re.match("""^=== (.+) ===\n""", content)
        slug = findName.group(1).replace(" ", "-")

        return slug.lower()

    def parseScreenshots(self, content, slug):
        """
        Adds link to screenshots
        """
        find = re.compile("""== Screenshots ==(.*?)==""", re.MULTILINE|re.DOTALL)

        images = find.search(content)

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
        find = re.compile("""=== (.+) ===(.*?)==""", re.MULTILINE|re.DOTALL)

        infos = find.search(content)

        for info in infos.group(2).strip().split("""\n"""):
            string = self.replaceAll("""^([^:\n#]+): (.+)$""", """**\\1:** \\2  """, info)
            content = content.replace(info, string)

        return content

    def run(self, edit):
        # Get current file path
        oldFile = self.view.file_name()

        # Checks if the file is the readme.txt
        if re.search("""(.+)/readme.txt$""", oldFile):

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
            content = self.replaceAll("""^(===)+(.+)+(===)\n""", """#\\2#\n""", content)
            content = self.replaceAll("""^(==)+(.+)+(==)\n""", """##\\2##\n""", content)
            content = self.replaceAll("""^(=)+(.+)+(=)\n""", """###\\2###\n""", content)

            getContent.close()

            # Write the new content
            writeContent = open(newFile, 'w')
            writeContent.write(content)
            writeContent.close()
