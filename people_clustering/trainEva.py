#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Thanks for the help of Wang Xuguang.
"""

import os
import subprocess


def run():
    ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    jar_path = os.path.join(ROOT, 'data/weps2007_data_1.1/scorer_1.1/wepsEvaluation.jar')

    truth_files_dir = os.path.join(ROOT, 'data/weps2007_data_1.1/traininig/truth_files/')

    my_result_dir = os.path.join(ROOT, 'result/myresult/')
    if not os.path.exists(my_result_dir):
        os.makedirs(my_result_dir)

    # The output evaluation result file must be in the same directory as jar_path in.
    output_dir = os.path.join(ROOT, 'data/weps2007_data_1.1/scorer_1.1/')

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    cmd = 'java -cp %s es.nlp.uned.weps.evaluation.SystemScorer %s %s %s -FMeasure_0.5_P-IP -P -IP -FMeasure_0.5_BEP-BER -BEP -BER  -AllInOne -OneInOne -Combined -overwrite -average' % (jar_path, truth_files_dir, my_result_dir, output_dir)

    cmd_list = cmd.split()

    subprocess.call(cmd_list)


def main():
    run()

if __name__ == '__main__':
    main()
