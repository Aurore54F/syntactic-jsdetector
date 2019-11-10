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
    Additional functions to classify JS files, print the predictions, their accuracy...
"""

import logging

from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import BernoulliNB
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix


def classifier_choice(clf_choice='MNB', estimators=500):
    """ Selecting the classifier to be used: Random Forest, Bernoulli Naive Bayes
    or Multinomial Naive Bayes. """

    if clf_choice == 'RF':
        return RandomForestClassifier(n_estimators=estimators, max_depth=50,
                                      random_state=0, n_jobs=-1)
    elif clf_choice == 'BNB':
        return BernoulliNB()
    elif clf_choice == 'MNB':
        return MultinomialNB()
    logging.error("Please choose your classifier and indicate: 'RF', 'BNB', or 'MNB")
    return None


def get_classification_results(names, labels_predicted):
    """
        Print in stdout the classification results of the files 'names' after our analysis.
        Format: 'Name: labelPredicted (trueLabel)'

        -------
        Parameters:
        - names: list
            Contains the path of the files being analysed.
        - labels_predicted: list
            Contains the predicted labels of the files being analysed.
    """

    for i, _ in enumerate(names):
        print(str(names[i]) + ': ' + str(labels_predicted[i]))
    print('> Name: labelPredicted')


def get_score(labels, labels_predicted):
    """
        Print in stdout the accuracy results of our classification (i.e. detection accuracy,
        true positives, false positives, false negatives and true negatives).

        -------
        Parameters:
        - labels: list
            Contains the labels (real classification or '?') of the files being analysed.
        - labels_predicted: list
            Contains the predicted labels of the files being analysed.
    """

    if '?' in labels:
        logging.info("No ground truth given: unable to evaluate the accuracy of the "
                     + "classifier's predictions")
    else:
        try:
            tn, fp, fn, tp = confusion_matrix(labels, labels_predicted,
                                              labels=['benign', 'malicious']).ravel()
            print("Detection: " + str((tp + tn) / (tp + tn + fp + fn)))
            print("TP: " + str(tp) + ", FP: " + str(fp) + ", FN: " + str(fn) + ", TN: "
                  + str(tn))

        except ValueError as error_message:  # In the case of a binary classification
            # (i.e. benign or malicious), if the confusion_matrix only contains one element, it
            # means that only one of the class was tested and all samples correctly classified.
            logging.exception(error_message)
