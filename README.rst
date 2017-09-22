S3jlf
=====

Reads a series of files from S3 and pipes them into a series of files
in S3 under a destination key template.  

::
s3jlf: Stream and chump JSONL files in chumks

Usage: s3jlf {{arguments}} {{options}}

Arguments:
  from [text]  S3 URL prefix to clump
    to [text]    S3 URL for target clump ('{}' will be the count)
    
    Options:
      -h, --help             Show this help message and exit
      -H, --HELP             Help for all sub-commands
      -c, --check            Don't check for target (may over-write)
      -C, --nocolour         Suppress colours in reports
      -D, --debug            Enable debug logging
      -d, --delete           Don't delete source files
      -q, --quiet            Be quiet, be vewy vewy quiet
      -v, --verbose          Verbose output
      -V, --version          Report installed version
      -z, --compress         Don't compress the target
      -b, --blocksize [int]  Size of pre-compressed output files in bytes. (default: 1048576)
