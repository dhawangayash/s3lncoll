#! /usr/bin/env python

import logtool, tempfile

class RotatingFile_Ctx (object):

  @logtool.log_call
  def __init__ (self, if_cb, of_cb, block = 1024, start = 0):
    self.if_cb = if_cb
    self.of_cb = of_cb
    self.count = start
    self.fh = None
    self.block = block
    self.length = 0

  @logtool.log_call
  def _file_done (self):
    if self.fh is not None:
      self.fh.close ()
      self.of_cb (self.count, self.fh.name)
      self.count += 1
      self.fh.delete ()
      self.fh = None
    self.fh = tempfile.NamedTemporaryFile (
      prefix = "s3jlf__", delete = False)
    self.length = 0

  @logtool.log_call
  def write (self, data):
    if self.fh is None or self.length + len (data) > self.block:
      self._file_done ()
    self.fh.write (data)
    self.length += len (data)
    return self.length

  @logtool.log_call
  def __enter__ (self):
    return self

  @logtool.log_call
  def __exit__ (self, *_):
    if self.fh is not None:
      self._file_done ()
