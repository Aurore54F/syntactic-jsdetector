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
    Production of (AST-based + variables' name info) features for malicious JS detection.
"""

import sys

import ast_generation
import ast_units

UNITS_DICT = ast_units.AST_UNITS_DICT
sys.setrecursionlimit(400000)


def get_the_ast(input_file):
    """
        Produces the AST of a given file.

        -------
        Parameter:
        - input_file: str
            Path of the file to study.

        -------
        Returns:
        - Node
            AST of the file
        - or None.
    """

    if input_file.endswith('.js'):
        esprima_json = input_file.replace('.js', '.json')
    else:
        esprima_json = input_file + '.json'
    extended_ast = ast_generation.get_extended_ast(input_file, esprima_json)
    if extended_ast is not None:
        ast = extended_ast.get_ast()
        ast_nodes = ast_generation.ast_to_ast_nodes(ast, ast_nodes=ast_generation.Node('Program'))
        return ast_nodes
    return None


def search_identifier(node, tab_id):
    """ Search and return the first Identifier Node found. Or None. """

    for child in node.children:
        if child.name == 'Identifier':
            tab_id.append(child)
        else:
            search_identifier(child, tab_id)
        if tab_id:
            return tab_id[0]
    return None


def build_features(ast, features_list):
    """ Build features with a context and the associated value. The features list is
    in features_list. """

    for child in ast.children:
        if UNITS_DICT[child.name] == 'Literal':  # Case Literal (String, Int, Regex etc.)
            context = child.literal_type()
            if 'value' in child.attributes:
                value = child.attributes['value']
                features_list.append((context, value))
            elif 'value' in child.attributes:
                value = child.attributes['regex']
                features_list.append((context, value))

        elif UNITS_DICT[child.name] != 0:  # Case Statements or Expressions, cf ast_units.py
            if not (child.name == 'ExpressionStatement' and child.children
                    and UNITS_DICT[child.children[0].name] != 0):
                # To avoid duplicates as ExpressionStatement is not informative, and it may have a
                # more informative child

                context = UNITS_DICT[child.name]
                identifier_node = search_identifier(child, [])
                if identifier_node is not None:
                    value = identifier_node.attributes['name']
                    if child.name == 'MemberExpression' and child.children:
                        if child.children[0].name == 'ThisExpression':
                            context = 'This'  # To differentiate This and Object
                    features_list.append((context, value))

        build_features(child, features_list)


def get_features(input_file):
    """ Returns (AST-based + variables' name info) features + the total number of features. """

    ast = get_the_ast(input_file)
    if ast is not None:
        features_list = list()
        unique_features_dict = dict()
        build_features(ast, features_list)
        for feature in features_list:
            if feature not in unique_features_dict:
                unique_features_dict[feature] = 1
            else:
                unique_features_dict[feature] += 1
        # print(features_list)
        return unique_features_dict, len(features_list)
    return None, None
