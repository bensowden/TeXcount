import sublime, sublime_plugin
from subprocess import PIPE, Popen

class TexcountCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		filename = self.view.file_name()

		# Check a file is selected
		if filename == None:
			sublime.error_message("No file selected")
			return

		# Save if file has been edited since last save
		if (self.view.is_dirty()):
			self.view.run_command('save')

		# Cleanse name and make shell command
		filename = filename.replace(" ","\ ")
		cmd = "texcount " + filename

		# MacTex fix
		cmd = "PATH=$PATH:/usr/texbin; " + cmd

		# Test to see if texcount is installed and in available PATH
		testcmdprocess = Popen("PATH=$PATH:/usr/texbin; which texcount", shell=True, stdout=PIPE, stderr=PIPE)
		testout, testerr = testcmdprocess.communicate()
		if (testout == ""):
			sublime.error_message("TeXcount not installed in PATH \nDownload from: http://app.uio.no/ifi/texcount/")
			return

		# Excecute texcount and collect output
		p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
		out, err = p.communicate()

		# Display Sublime console and print texcount output to console
		sublime.active_window().run_command("show_panel", {"panel": "console", "toggle": True})
		out = out.strip()
		print(out)
		return
