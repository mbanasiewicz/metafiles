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

        stems = first_line.split('\t')
        stem = ""
        if len(stems) < 2:
            stem = input_word
        else:
            stem = stems[1]

        print(input_word + " ~> " + stem)

        if stem != '-':
            return stem
        else:
            return input_word
    else:
        return input_word

def stem_list(stems_list):
    fn = os.path.join(os.path.dirname(__file__))
    process_call = 'java -jar ' + str(fn) +'/morfologik-tools-1.9.0-standalone.jar plstem -ie utf-8 -oe utf-8'
    output = instream(", ".join(stems_list)).p(process_call).stdout().split("\n")[:-2]
    set_of_stems = set()
    for stem_line in output:
        set_of_stems.add(stem_line.split("\t")[1])
    return [stem for stem in set_of_stems]
