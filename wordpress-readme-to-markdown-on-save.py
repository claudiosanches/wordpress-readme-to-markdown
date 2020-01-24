import sublime
import sublime_plugin
import re

class WordpressReadmeToMarkdownOnSave(sublime_plugin.EventListener):

    def __init__(self):
        self.plugin_readme = re.compile("""(.+)/readme.txt$""")

    def on_post_save(self, view):
        name = view.file_name()

        if self.get_settings(view).get('on-save') and self.plugin_readme.search(name):
            view.window().run_command('wordpress_readme_to_markdown')

    @staticmethod
    def get_settings(view):
        settings = view.settings().get('WordPressReadmeToMarkdown')

        if settings is None:
            settings = sublime.load_settings('WordPressReadmeToMarkdown.sublime-settings')

        return settings
