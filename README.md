# syntactic-jsdetector

This repository contains our reimplementation of the concept presented by [Curtsinger et al. with Zozzle](https://www.usenix.org/legacy/events/sec11/tech/full_papers/Curtsinger.pdf) (static part only).
Please note that in its current state, the code is a Poc and not a fully-fledged production-ready API.


## Summary
In our reimplementation, we combined an AST-based analysis of JavaScript inputs with variables' name information and with machine learning algorithms to automatically and accurately detect malicious samples. 

## Setup

```
install python3
install python3-pip
pip3 install -r requirements.txt

install nodejs
install npm
cd src
npm install esprima
cd ..
```


## Usage

### Learning: Building a Model

To build a model from the folders BENIGN and MALICIOUS, containing JS files, use the option --d BENIGN MALICIOUS and add their corresponding ground truth with --l benign malicious.

Select the features appearing in the training set with chi2 on 2 independent datasets with the option --vd BENIGN-VALIDATE MALICIOUS-VALIDATE with their corresponding ground truth --vl benign malicious.

Choose the classifier to use to train your model with. Possible choices: 'RF' (Random Forest), 'MNB' (Multinomial Naive Bayes), and 'BNB' (Bernoulli Naive Bayes) (option --clf).

You can choose the model's name with --mn (default being 'model') and its directory with --md (default syntactic-jsdetector/Analysis).

```
$ python3 src/learner.py --d  BENIGN MALICIOUS --l benign malicious --vd BENIGN-VALIDATE MALICIOUS-VALIDATE --vl benign malicious --clf BNB --mn MODEL-NAME --md MODEL-DIR
```


### Classification of JS Samples

The process is similar for the classification process.

To classify JS samples from the folders BENIGN2 and MALICIOUS2, use the option --d BENIGN2 MALICIOUS2. To load an existing model MODEL-DIR/MODEL-NAME to be used for the classification process, use the option --m MODEL-DIR/MODEL-NAME:

```
$ python3 src/classifier.py --d  BENIGN2 MALICIOUS2 --m MODEL-DIR/MODEL-NAME
```

If you know the ground truth of the samples you classify and would like to evaluate the accuracy of your classifier, use the option --l with the corresponding ground truth: 

```
$ python3 src/classifier.py --d  BENIGN2 MALICIOUS2 --l benign malicious --m MODEL-DIR/MODEL-NAME
```

Currently, we are using 2 CPUs for the learning and classification processes; this can be changed by modifying the variable NUM\_WORKERS from src/utility.py.


## License

This project is licensed under the terms of the AGPL3 license, which you can find in ```LICENSE```.
