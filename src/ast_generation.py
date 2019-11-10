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
    From the JS source code to the Esprima AST exported in JSON.
    From JSON to ExtendedAst and Node objects.
"""

import logging
import json
import os
from subprocess import run, PIPE


SRC_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__)))


class ExtendedAst:
    """
    Class ExtendedAst: corresponds to the output of Esprima's parse function with the arguments:
    {range: true, tokens: true, comment: true}.
    """

    def __init__(self):
        self.type = None
        self.body = []
        self.source_type = None
        self.range = []
        self.comments = []
        self.tokens = []
        self.leading_comments = []

    def get_body(self):
        return self.body

    def get_type(self):
        return self.type

    def get_ast(self):
        return {'type': self.get_type(), 'body': self.get_body()}

    def set_type(self, root):
        self.type = root

    def set_body(self, body):
        self.body = body

    def set_source_type(self, source_type):
        self.source_type = source_type

    def set_range(self, ast_range):
        self.range = ast_range

    def set_comments(self, comments):
        self.comments = comments

    def set_tokens(self, tokens):
        self.tokens = tokens

    def set_leading_comments(self, leading_comments):
        self.leading_comments = leading_comments


class Node:
    """
    Class Node: converts an Esprima AST into Node objects.
    """
    id = 0

    def __init__(self, name, parent=None):
        self.name = name
        self.id = Node.id
        Node.id += 1
        self.attributes = {}
        self.body = None
        self.body_list = False
        self.parent = parent
        self.children = []

    def set_attribute(self, attribute_type, node_attribute):
        self.attributes[attribute_type] = node_attribute

    def set_body(self, body):
        self.body = body

    def set_body_list(self, bool_body_list):
        self.body_list = bool_body_list

    def set_child(self, child):
        self.children.append(child)

    def literal_type(self):
        if 'value' in self.attributes:
            literal = self.attributes['value']
            if isinstance(literal, str):
                return 'String'
            elif isinstance(literal, int):
                return 'Int'
            elif isinstance(literal, float):
                return 'Numeric'
            elif isinstance(literal, bool):
                return 'Bool'
            elif literal == 'null' or literal is None:
                return 'Null'
        if 'regex' in self.attributes:
            return 'RegExp'
        if self.name != 'Literal':
            logging.warning('The node %s is not a Literal', self.name)
        else:
            logging.warning('The literal %s has an unknown type', self.attributes['raw'])
        return None


def get_extended_ast(input_file, json_path='1', remove_json=True):
    """
        JavaScript AST production.

        -------
        Parameters:
        - input_file: str
            Path of the file to produce an AST from.
        - json_path: str
            Path of the JSON file to temporary store the AST in.
        - remove_json: bool
            Indicates whether to remove or not the JSON file containing the Esprima AST.
            Default: True.

        -------
        Returns:
        - ExtendedAst
            The extended AST (i.e., contains type, body, sourceType, range, comments, tokens and
            possibly leadingComments) of input_file.
        - None if an error occurred.
    """

    produce_ast = run(['node', os.path.join(SRC_PATH, 'js_ast.js'), input_file, json_path],
                      stdout=PIPE)
    if produce_ast.returncode == 0:
        if json_path == '1':
            ast = produce_ast.stdout.decode('utf-8').replace('\n', '')
            return ast.split('##!!**##')
        else:
            with open(json_path) as json_data:
                esprima_ast = json.loads(json_data.read())
            if remove_json:
                os.remove(json_path)

            extended_ast = ExtendedAst()
            extended_ast.set_type(esprima_ast['type'])
            extended_ast.set_body(esprima_ast['body'])
            extended_ast.set_source_type(esprima_ast['sourceType'])
            extended_ast.set_range(esprima_ast['range'])
            extended_ast.set_tokens(esprima_ast['tokens'])
            extended_ast.set_comments(esprima_ast['comments'])
            if 'leadingComments' in esprima_ast:
                extended_ast.set_leading_comments(esprima_ast['leadingComments'])

            return extended_ast
    logging.error('Esprima could not produce an AST for %s', input_file)
    return None


def create_node(dico, node_body, parent_node, cond=False):
    """ Node creation. """

    if 'type' in dico:
        node = Node(name=dico['type'], parent=parent_node)
        parent_node.set_child(node)
        node.set_body(node_body)
        if cond:
            node.set_body_list(True)
        ast_to_ast_nodes(dico, node)


def ast_to_ast_nodes(ast, ast_nodes=Node('Program')):
    """
        Convert an AST to Node objects.

        -------
        Parameters:
        - ast: dict
            Output of get_extended_ast(<input_file>, <json_path>).get_ast().
        - ast_nodes: Node
            Current Node to be built. Default: ast_nodes=Node('Program'). Beware, always call the
            function indicating the default argument, otherwise the last value will be used
            (because the default parameter is mutable).

        -------
        Returns:
        - Node
            The AST in format Node object.
    """

    for k in ast:
        if k == 'range' or (k != 'type' and not isinstance(ast[k], list)
                            and not isinstance(ast[k], dict)) or k == 'regex':
            ast_nodes.set_attribute(k, ast[k])  # range is a list but stored as attributes
        if isinstance(ast[k], dict):
            if k == 'range':  # Case leadingComments as range: {0: begin, 1: end}
                ast_nodes.set_attribute(k, ast[k])
            else:
                create_node(dico=ast[k], node_body=k, parent_node=ast_nodes)
        elif isinstance(ast[k], list):
            if not ast[k]:  # Case with empty list, e.g. params: []
                ast_nodes.set_attribute(k, ast[k])
            for el in ast[k]:
                if isinstance(el, dict):
                    create_node(dico=el, node_body=k, parent_node=ast_nodes, cond=True)
    return ast_nodes
