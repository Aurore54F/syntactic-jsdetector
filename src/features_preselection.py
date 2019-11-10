# Copyright (C) 2019 Aurore Fass
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
    Preselection of (AST-based + variables' name info) features for malicious JS detection:
    ALL features appearing in a corpus.
"""

import os
import pickle
import logging
import timeit
from multiprocessing import Process, Queue
import queue  # For the exception queue.Empty which is not in the multiprocessing package

import features_extraction
import utility


def handle_features_1file(unique_features_dict, all_features_dict):
    """ Fills a dict with the encountered features + the number of files they have been seen in.
    Case one file. """

    for feature in unique_features_dict:
        if feature not in all_features_dict:
            all_features_dict[feature] = 1
        else:
            all_features_dict[feature] += 1


def handle_features_1dir(samples_dir, label, analysis_path):
    """ handle_features_1file for ALL files from a directory.
    Case one folder. """

    if not os.path.exists(analysis_path):
        os.makedirs(analysis_path)

    pickle_path = os.path.join(analysis_path, '_all_features_' + label)

    if os.path.isfile(pickle_path):
        all_features_dict = pickle.load(open(pickle_path, 'rb'))
    else:
        all_features_dict = dict()

    analyses = get_features_all_files_multiproc(samples_dir)

    start = timeit.default_timer()

    for analysis in analyses:
        features_dict = analysis.features
        if features_dict is not None:
            try:
                handle_features_1file(features_dict, all_features_dict)
            except:
                logging.exception('Something went wrong with %s', analysis.file_path)

    pickle.dump(all_features_dict, open(pickle_path, 'wb'))
    utility.micro_benchmark('Total elapsed time:', timeit.default_timer() - start)


def handle_features_all(js_dirs, labels, analysis_path):
    """ handle_features_1dir for a list of directories; TO CALL. """

    for i, _ in enumerate(js_dirs):
        print('Currently handling ' + js_dirs[i])
        handle_features_1dir(js_dirs[i], labels[i], analysis_path)


class Analysis:

    def __init__(self, file_path, label=None):
        self.file_path = file_path
        self.features = None
        self.label = label

    def set_features(self, features):
        self.features = features


def worker_get_features(my_queue, out_queue, except_queue):
    """ Worker to get the features."""

    while True:
        try:
            analysis = my_queue.get(timeout=2)
            try:
                features_dict, _ = features_extraction.get_features(analysis.file_path)
                analysis.set_features(features_dict)
                out_queue.put(analysis)  # To share modified analysis object between processes
            except Exception as e:  # Handle exception occurring in the processes spawned
                logging.error('Something went wrong with %s', analysis.file_path)
                print(e)
                except_queue.put([analysis.file_path, e])
        except queue.Empty:  # Empty queue exception
            break


def get_features_all_files_multiproc(samples_dir):
    """ Gets the features of all files from samples_dir."""

    start = timeit.default_timer()

    my_queue = Queue()
    out_queue = Queue()
    except_queue = Queue()
    workers = list()

    for sample in os.listdir(samples_dir):
        sample_path = os.path.join(samples_dir, sample)
        analysis = Analysis(file_path=sample_path)
        my_queue.put(analysis)

    for i in range(utility.NUM_WORKERS):
        p = Process(target=worker_get_features, args=(my_queue, out_queue, except_queue))
        p.start()
        workers.append(p)

    analyses = list()

    while True:
        try:
            analysis = out_queue.get(timeout=0.01)
            analyses.append(analysis)
        except queue.Empty:
            pass
        all_exited = True
        for w in workers:
            if w.exitcode is None:
                all_exited = False
                break
        if all_exited & out_queue.empty():
            break

    utility.micro_benchmark('Total elapsed time for features production:',
                            timeit.default_timer() - start)

    return analyses
