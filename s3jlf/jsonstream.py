#! /usr/bin/env python

import boto3, json, logtool, tempfile

class JsonStream (object):

  @logtool.log_call
  def __init__ (self, bucket, keylist, validate = False):
    self.keylist = keylist if keylist else []
    self.s3 = boto3.resource ("s3")
    self.bucket = self.s3.Bucket (bucket)
    self.validate = validate

  @logtool.log_call
  def __iter__ (self):
    return self

  @logtool.log_call
  def __next__ (self):
    return self.next ()

  @logtool.log_call
  def next (self):
    for key in self.keylist:
      with tempfile.NamedTemporaryFile (prefix = "s3jlf_in__") as f:
        self.bucket.download_file (key, f.name)
        for line in f: # pylint: disable=not-an-iterable
          try:
            if self.validate:
              json.loads (line)
            return line
          except ValueError:
            continue
    raise StopIteration
