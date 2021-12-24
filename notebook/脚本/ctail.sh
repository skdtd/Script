#!/bin/bash

# \e[1;33m$2\e[0m\e[1;31m$3\e[0m


STYLE_SET=(DEBUG=)

tail -f file | perl -pe 's/(?i)(DEBUG)/\e[1;34m$1\e[0m/g'