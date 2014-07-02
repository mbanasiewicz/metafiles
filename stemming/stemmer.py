__author__ = 'maciejbanasiewicz'
# -*- coding: utf-8 -*-

import subprocess
from shlex import split
from shell import instream
from defines import project_root
import os

def get_stem(input_word):
    fn = os.path.join(os.path.dirname(__file__))
    if input_word:
        process_call = 'java -jar ' + str(fn) +'/morfologik-tools-1.9.0-standalone.jar plstem -ie utf-8 -oe utf-8'
        output = instream(input_word).p(process_call).stdout()

        first_line = output.split("\n")[0]
        stem = first_line.split('\t')[1]
        if stem != '-':
            return stem
        else:
            return None