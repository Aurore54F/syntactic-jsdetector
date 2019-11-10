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
    Main module to classify JavaScript files using a given model.
"""

import os
import pickle
import argparse
import logging

import machine_learning
import utility
import analysis


def test_model(names, labels, attributes, model, print_res=True, print_score=True):
    """
        Use an existing model to classify new JS inputs.

        -------
        Parameters:
        - names: list
            Name of the data files used to be tested using the following model.
        - labels: list
            Labels (i.e. 'benign', 'malicious', or '?') of the test data using the model.
        - attributes: csr_matrix
            Features of the data used to be tested using the following model.
        - model
            Model to be used to classify new observations. Beware: the model must have been
            constructed using the same parameters as for the current classification process.
        - print_res: bool
            Indicates whether to print or not the classifier's predictions.
        - print_score: bool
            Indicates whether to print or not the classifier's performance.

        -------
        Returns:
        - list:
            List of labels predicted.
    """

    if isinstance(model, str):
        model = pickle.load(open(model, 'rb'))

    labels_predicted_test = model.predict(attributes)

    if print_res:
        machine_learning.get_classification_results(names, labels_predicted_test)

    if print_score:
        machine_learning.get_score(labels, labels_predicted_test)

    return labels_predicted_test


def parsing_commands():
    """
        Creation of an ArgumentParser object, holding all the information necessary to parse
        the command line into Python data types.
    """

    parser = argparse.ArgumentParser(description='Given a list of directory or file paths,\
    detects the malicious JS inputs.')

    parser.add_argument('--d', metavar='DIR', type=str, nargs='+',
                        help='directories containing the JS files to be analyzed')
    parser.add_argument('--l', metavar='LABEL', type=str, nargs='+',
                        choices=['benign', 'malicious', '?'],
                        help='labels of the JS directories to evaluate the model from')
    parser.add_argument('--f', metavar='FILE', type=str, nargs='+', help='files to be analyzed')
    parser.add_argument('--lf', metavar='LABEL', type=str, nargs='+',
                        choices=['benign', 'malicious', '?'],
                        help='labels of the JS files to evaluate the model from')
    parser.add_argument('--m', metavar='MODEL', type=str, nargs=1,
                        help='path of the model used to classify the new JS inputs')
    utility.parsing_commands(parser)

    return vars(parser.parse_args())


arg_obj = parsing_commands()
utility.control_logger(arg_obj['v'][0])


def main_classification(js_dirs=arg_obj['d'], js_files=arg_obj['f'], labels_f=arg_obj['lf'],
                        labels_d=arg_obj['l'], model=arg_obj['m'],
                        analysis_path=arg_obj['analysis_path'][0]):
    """
        Main function, performs a static analysis (syntactic) of JavaScript files given as input
        before predicting if the executables are benign or malicious.

        -------
        Parameters:
        - js_dirs: list of strings
            Directories containing the JS files to be analysed.
        - js_files: list of strings
            Files to be analysed.
        - labels_f: list of strings
            Indicates the label's name of the files considered: either benign or malicious.
        - labels_d: list of strings
            Indicates the label's name of the directories considered: either benign or malicious.
        - model: str
            Path to the model used to classify the new files
        - analysis_path: str
            Folder to store the features' analysis results in.
        Default values are the ones given in the command lines or in the
        ArgumentParser object (function parsingCommands()).

        -------
        Returns:
        The results of the static analysis of the files given as input:
        either benign or malicious
    """

    if js_dirs is None and js_files is None:
        logging.error('Please, indicate a directory or a JS file to be analyzed')

    elif js_dirs is not None and labels_d is not None and len(js_dirs) != len(labels_d):
        logging.error('Please, indicate either as many directory labels as the number %s of '
                      + 'directories to analyze or no directory label at all', str(len(js_dirs)))

    elif js_files is not None and labels_f is not None and len(js_files) != len(labels_f):
        logging.error('Please, indicate either as many file labels as the number %s of files to '
                      + 'analyze or no file label at all', str(len(js_files)))

    elif model is None:
        logging.error('Please, indicate a model to be used to classify new files.\n'
                      + '(see >$ python3 <path-of-learner.py> -help) to build a model)')

    else:
        features2int_dict_path = os.path.join(analysis_path, 'Features', '_selected_features_')

        names, attributes, labels =\
            analysis.main_analysis(js_dirs=js_dirs, labels_dirs=labels_d,
                                   js_files=js_files, labels_files=labels_f,
                                   features2int_dict_path=features2int_dict_path)

        if names:
            test_model(names, labels, attributes, model=model[0])

        else:
            logging.warning('No file found for the analysis.')


if __name__ == "__main__":  # Executed only if run as a script
    main_classification()
