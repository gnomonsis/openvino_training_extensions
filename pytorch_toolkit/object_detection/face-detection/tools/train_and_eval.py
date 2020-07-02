# Copyright (C) 2020 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions
# and limitations under the License.

# pylint: disable=C0301,W0622,R0914

import argparse
import subprocess
import os

from mmcv.utils import Config

from eval import eval


def parse_args():
    """ Parses input args. """

    args = argparse.ArgumentParser()
    args.add_argument('config',
                      help='A path to model training configuration file (.py).')
    args.add_argument('gpu_num',
                      help='A number of GPU to use in training.')
    args.add_argument('out',
                      help='A path to output file where models metrics will be saved (.yml).')
    args.add_argument('--wider_dir',
                      help='Specify this  path if you would like to test your model on WiderFace dataset.',
                      default='data/wider_dir')
    args.add_argument(
        '--update_config',
        help='Update configuration file by parameters specified here.'
             'Use quotes if you are going to change several params.',
        default='')

    return args.parse_args()


def main():
    """ Main function. """

    args = parse_args()

    mmdetection_tools = f'{os.path.dirname(__file__)}/../../../../external/mmdetection/tools'

    update_config = f'--update_config {args.update_config}' if args.update_config else ''
    subprocess.run(f'{mmdetection_tools}/dist_train.sh'
                   f' {args.config}'
                   f' {args.gpu_num}'
                   f' {update_config}'.split(' '), check=True)

    cfg = Config.fromfile(args.config)

    overrided_work_dir = [p.split('=') for p in args.update_config.strip().split(' ') if p.startswith('work_dir=')]
    if overrided_work_dir:
        cfg.work_dir = overrided_work_dir[0][1]

    eval(args.config, os.path.join(cfg.work_dir, "latest.pth"), args.out, args.update_config, args.wider_dir)


if __name__ == '__main__':
    main()
