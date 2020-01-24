import sublime
import sublime_plugin
import re

class WordpressReadmeToMarkdownOnSave(sublime_plugin.EventListener):

    def __init__(self):
        self.plugin_readme = re.compile("""(.+)/readme.txt$""")

    def on_post_save(self, view):
        name = view.file_name()

        if self.plugin_readme.search(name):
            view.window().run_command('wordpress_readme_to_markdown')
