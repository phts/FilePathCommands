import sublime, sublime_plugin
import os.path

def full_file_path(view):
  fp = view.file_name()
  if not fp or len(fp) == 0: return False
  return fp

def get_row(view):
  sel = view.sel()[0]
  point = sel.begin()
  row, col = view.rowcol(point)
  return row+1

def relative_path(full_path, with_project_folder=False):
  folder = False
  for f in sublime.active_window().folders():
    if full_path.startswith(f):
      folder = f
      break
  if not folder: return False

  if with_project_folder:
    folder, project_folder = os.path.split(folder)

  relative_path = conform_path(full_path).replace(conform_path(folder+"/"), "", 1)
  return relative_path

def relative_path_to_file(full_path, another_file_path):
  relpath = os.path.relpath(another_file_path, os.path.dirname(full_path))
  if relpath.find("/") == -1:
    relpath = "./" + relpath
  return relpath

def copy(text):
  sublime.set_clipboard(text)
  sublime.status_message("Copied "+text)

def conform_path(path):
  if sublime.platform() == "windows":
    path = path.replace("\\", "/")
  return path


class FilePathCommand(sublime_plugin.TextCommand):
  def is_enabled(self):
    return not not full_file_path(self.view)


class CopyFileNameCommand(FilePathCommand):
  def run(self, edit, without_ext=False):
    fp = full_file_path(self.view)
    dir_path, file_name = os.path.split(fp)
    if without_ext:
      file_name = os.path.splitext(file_name)[0]
    copy(file_name)


class CopyDirPathCommand(FilePathCommand):
  def run(self, edit):
    fp = full_file_path(self.view)
    dir_path, file_name = os.path.split(fp)
    copy(dir_path)


class CopyRelativePathCommand(FilePathCommand):
  def run(self, edit, with_project_folder=False, with_line_number=False):
    fp = full_file_path(self.view)
    rp = relative_path(fp, with_project_folder)
    if not rp: rp = fp
    if with_line_number:
      rp += ":" + str(get_row(self.view))
    copy(rp)

class InsertRelativePathOfAnotherFileCommand(FilePathCommand):
  def run(self, edit):
    self.view.window().show_input_panel("Another file's full path:", "", self.on_done, None, None)

  def on_done(self, text):
    try:
      another_file_path = text
      this_file_path = full_file_path(self.view)
      result = relative_path_to_file(this_file_path, another_file_path)
      self.view.run_command("insert_text", {"text": result})
    except ValueError:
      pass

class InsertTextCommand(sublime_plugin.TextCommand):
  def run(self, edit, text):
    for s in self.view.sel():
      self.view.insert(edit, s.begin(), text)
