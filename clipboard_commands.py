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

def relative_path(full_path):
  folder = False
  for f in sublime.active_window().folders():
    if full_path.startswith(f):
      folder = f
      break
  if not folder: return False

  folder, folder_name = os.path.split(folder)
  relative_path = full_path.replace(folder+"\\", "", 1)
  relative_path = relative_path.replace("\\", "/")
  return relative_path

def copy(text):
  sublime.set_clipboard(text)
  sublime.status_message("Copied "+text)


class ClipboardCommand(sublime_plugin.TextCommand):
  def is_enabled(self):
    return not not full_file_path(self.view)


class CopyPathCommand(ClipboardCommand):
  def run(self, edit):
    fp = full_file_path(self.view)
    copy(fp)


class CopyFileNameCommand(ClipboardCommand):
  def run(self, edit):
    fp = full_file_path(self.view)
    dir_path, file_name = os.path.split(fp)
    copy(file_name)


class CopyDirPathCommand(ClipboardCommand):
  def run(self, edit):
    fp = full_file_path(self.view)
    dir_path, file_name = os.path.split(fp)
    copy(dir_path)


class CopyRelativePathCommand(ClipboardCommand):
  def run(self, edit):
    fp = full_file_path(self.view)
    rp = relative_path(fp)
    if not rp: rp = fp
    copy(rp)


class CopyRelativePathWithLineNumberCommand(ClipboardCommand):
  def run(self, edit):
    fp = full_file_path(self.view)
    rp = relative_path(fp)
    if not rp: rp = fp
    copy(rp + ":" + str(get_row(self.view)))
