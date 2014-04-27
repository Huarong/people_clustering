#!/usr/bin/python

import subprocess
cmd =  ['java','-cp','../result/wepsEvaluation.jar', 'es.nlp.uned.weps.evaluation.SystemScorer',\
'../result/truth_official/','../result/test_system/','../result/','-ALLMEASURES','-AllInOne',\
 '-OneInOne', '-Combined', '-average','-true']

subprocess.call(cmd)