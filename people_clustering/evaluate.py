#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Thanks for the help of Wang Xuguang.
"""

import os
import subprocess


def eval_2007train():
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


def eval_2008test():
    ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    jar_path = os.path.join(ROOT, 'data/weps-2/data/test/scorer_1.2/wepsScorer.jar')

    metadata_path = os.path.join(ROOT, 'data/weps-2/data/test/metadata/')

    truth_files_dir = os.path.join(ROOT, 'data/weps-2/data/test/gold_standard/')

    my_result_dir = os.path.join(ROOT, 'pickle/2008test/result/')
    if not os.path.exists(my_result_dir):
        os.makedirs(my_result_dir)

    # The output evaluation result file must be in the same directory as jar_path in.
    output_dir = os.path.dirname(jar_path)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    cmd = 'java -jar %s %s %s %s %s -P -IP -FMeasure_0.5_P-IP -FMeasure_0.2_P-IP -FMeasure_0.5_BEP-BER -FMeasure_0.2_BEP-BER -BEP -OneInOne -AllInOne -Combined  -overwrite -average' % (jar_path, metadata_path, truth_files_dir, my_result_dir, output_dir)

    cmd_list = cmd.split()

    subprocess.call(cmd_list)


def run(version):
    if '2008test' == version:
        eval_2008test()
    else:
        print '!!!!!!!!!!!!!!!!!!! unknow evaluation version: %s !!!!!!!!!!!!!!!!!!!!!!!!' % version
    return None


def main():
    run('2008test')


if __name__ == '__main__':
    main()
