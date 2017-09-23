#! /usr/bin/env python

import boto3, json, logtool, tempfile

@logtool.log_call
def jsonstream (keylist, cb = None, validate = False):
    keylist = keylist
    s3 = boto3.resource ("s3")
    for ndx, key in enumerate (keylist):
      if cb is not None:
        cb (ndx)
      with tempfile.NamedTemporaryFile (prefix = "s3jlf_in__") as f:
        f.write (key.get ()["Body"].read ())
        f.seek (0)
        for line in file (f.name): # pylint: disable=not-an-iterable
          try:
            if validate:
              json.loads (line)
            yield line
          except ValueError:
            continue
    raise StopIteration
