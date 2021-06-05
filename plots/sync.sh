#!/bin/bash
# anytime jpgs are added push to bucket
find *.jpg -type f |\
  entr sh -c 'echo 'update' & gsutil cp *.jpg gs://plotsxvzf/'
