#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Thanks for the help of Wang Xuguang.
"""

# DIR F:\ 
# cd F:\cloudPython\ml2\weps-2\data\test\scorer_1.2
# java -jar wepsScorer.jar F:\cloudPython\ml2\weps-2\data\test\metadata F:\cloudPython\ml2\weps-2\data\test\gold_standard F:\cloudPython\ml2\weps-2\data\test\my_answer testEva -P -IP -FMeasure_0.5_P-IP -FMeasure_0.2_P-IP -FMeasure_0.5_BEP-BER -FMeasure_0.2_BEP-BER -BEP -OneInOne -AllInOne -Combined  -overwrite -average
# pause


import os
import subprocess


def run():
    ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    jar_path = os.path.join(ROOT, 'data/weps-2/data/test/scorer_1.2/wepsEvaluation.jar')

    metadata_path = os.path.join(ROOT, 'data/weps-2/data/test/metadata/')

    truth_files_dir = os.path.join(ROOT, 'data/weps-2/data/test/gold_standard/')

    my_result_dir = os.path.join(ROOT, 'result/htest/')
    if not os.path.exists(my_result_dir):
        os.makedirs(my_result_dir)

    # The output evaluation result file must be in the same directory as jar_path in.
    output_dir = os.path.dirname(jar_path)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    cmd = 'java -jar %s %s %s %s %s -P -IP -FMeasure_0.5_P-IP -FMeasure_0.2_P-IP -FMeasure_0.5_BEP-BER -FMeasure_0.2_BEP-BER -BEP -OneInOne -AllInOne -Combined  -overwrite -average' % (jar_path, metadata_path, truth_files_dir, my_result_dir, output_dir)

    cmd_list = cmd.split()

    subprocess.call(cmd_list)


def main():
    run()

if __name__ == '__main__':
    main()
