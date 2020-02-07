import sublime
import sublime_plugin
import os.path

class WordpressReadmeToMarkdownOnSave(sublime_plugin.EventListener):

    def on_post_save(self, view):
        if self.get_settings(view).get('on-save') == False:
            return

        file = view.file_name()

        if 'README.md' == file[-9:]:
            file_txt = file.replace("README.md", "readme.txt")

            if os.path.isfile(file_txt):
                sublime.error_message("You are saving a README.md file directly, but autosave is ON. \nYour changes will be lost if you save readme.txt.")
                return

            return

        view.window().run_command('wordpress_readme_to_markdown')

    @staticmethod
    def get_settings(view):
        settings = view.settings().get('WordPressReadmeToMarkdown')

        if settings is None:
            settings = sublime.load_settings('WordPressReadmeToMarkdown.sublime-settings')

        return settings
