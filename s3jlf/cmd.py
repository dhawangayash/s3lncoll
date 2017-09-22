#!/usr/bin/env python

from __future__ import absolute_import
import boto3, botocore, clip, logging, logtool, os
import retryp, StringIO, threading, urlparse
from collections import namedtuple
from progress.bar import Bar
from .cmdio import CmdIO
from .jsonstream import JsonStream
from .rotatingfile_ctx import RotatingFile_Ctx

LOG = logging.getLogger (__name__)

class _ProgressPercentage (object):

  # pylint: disable=too-few-public-methods

  @logtool.log_call
  def __init__ (self, filename, quiet):
    self._filename = filename
    self._size = float (os.path.getsize (filename))
    self._lock = threading.Lock ()
    self.quiet = quiet
    self.progress = Bar ("Sending", max = 100) if not quiet else None

  @logtool.log_call
  def __enter__ (self):
    return self

  @logtool.log_call
  def __exit__ (self, *args):
    if not self.quiet:
      self.progress.finish ()

  @logtool.log_call
  def __call__ (self, bytes_amount):
    if not self.quiet:
      with self._lock:
        self.progress.next (n = int (100 * bytes_amount / self._size))

class Action (CmdIO):

  @logtool.log_call
  def __init__ (self, args):
    CmdIO.__init__ (self, conf = args)
    self.args = args
    self.p_from = self._parse_url ("Source", args.url_from)
    self.p_to = self._parse_url ("Destination", args.url_to)
    self.compress = args.compress
    self.check = args.check
    self.s3 = boto3.resource ("s3")
    self.keys = None

  @logtool.log_call
  def _parse_url (self, typ, url):
    _urlspec = namedtuple ("_UrlSpec", ["protocol", "bucket", "key"])
    p = urlparse.urlparse (url)
    rc = _urlspec (protocol = p.scheme, bucket = p.netloc,
                   key = p.path[1:] if p.path.startswith ("/") else p.path)
    if rc.protocol != "s3":
      self.error ("%s protocol is not s3: %s" % (typ, url))
      clip.exit (err = True)
    return rc

  @retryp.retryp (expose_last_exc = True, log_faults = True)
  @logtool.log_call
  def _cleanup (self):
    if not self.args.delete:
      for key in (Bar ("Deleting").iter (self.keys)
                  if not self.args.quiet else self.keys):
        key.delete ()

  @retryp.retryp (expose_last_exc = True, log_faults = True)
  @logtool.log_call
  def _send (self, ndx, fname):
    client = boto3.client("s3")
    out_f = self.p_to.key.format (ndx)
    with _ProgressPercentage (out_f, self.args.quiet) as cb:
      client.upload_file (fname, self.p_to.bucket, out_f, Callback = cb)

  @retryp.retryp (expose_last_exc = True, log_faults = True)
  @logtool.log_call
  def _list_from (self):
    bucket = self.s3.Bucket (self.p_from.bucket)
    self.keys = [k for k in bucket.objects.filter (
      Prefix = self.p_from.key)]

  @logtool.log_call
  def _pipedata (self):
    with _ProgressPercentage ("Reading", self.args.quiet) as cb:
      with RotatingFile_Ctx (cb, self._send, block = self.args.block) as rf:
        for line in JsonStream (self.p_from.bucket, self.keys):
          rf.write (line)

  @retryp.retryp (expose_last_exc = True, log_faults = True)
  @logtool.log_call
  def _check (self):
    if self.check:
      return False
    try:
      boto3.client ("s3").head_object (
        Bucket = self.p_to.bucket,
        Key = self.p_to.key)
      self.error ("Target exists: %s" % self.args.url_to)
      return True
    except botocore.exceptions.ClientError as e:
      if int (e.response["Error"]["Code"]) == 404:
        client = boto3.client("s3")
        client.upload_fileobj (
          StringIO.StringIO (), self.p_to.bucket, self.p_to.key)
        return False
      raise

  @logtool.log_call
  def run (self):
    if self._check ():
      clip.exit (err = True)
    self._list_from ()
    self._pipedata ()
    self._cleanup ()
    if not self.args.quiet:
      print ""
