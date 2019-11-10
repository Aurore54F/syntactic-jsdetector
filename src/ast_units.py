#!/usr/bin/python

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
    Configuration file storing the dictionary AST_UNITS_DICT.
        Key: Esprima syntactic unit;
        Value: Features name.
"""


AST_UNITS_DICT = {
    'ArrayExpression': 'Array',
    'ArrayPattern': 'Array',
    'ArrowFunctionExpression': 'Expression',
    'AssignmentExpression': 'Assign',
    'AssignmentPattern': 'Assign',
    'AwaitExpression': 'Await',
    'BinaryExpression': 'Expression',
    'Block': 'Comment',
    'BlockStatement': 0,
    'BreakStatement': 0,
    'CallExpression': 'Call',
    'CatchClause': 'Catch',
    'ClassBody': 0,
    'ClassDeclaration': 'Class',
    'ClassExpression': 'Expression',
    'ConditionalExpression': 'If',
    'ContinueStatement': 0,
    'DebuggerStatement': 'Debug',
    'DoWhileStatement': 'While',
    'EmptyStatement': 0,
    'ExportAllDeclaration': 0,
    'ExportDefaultDeclaration': 0,
    'ExportNamedDeclaration': 0,
    'ExportSpecifier': 0,
    'ExpressionStatement': 'ExpressionStatement',
    'ForInStatement': 'For',
    'ForOfStatement': 'For',
    'ForStatement': 'For',
    'FunctionDeclaration': 'Function',
    'FunctionExpression': 'Function',
    'Identifier': 0,
    'IfStatement': 'If',
    'Import': 'Import',
    'ImportDeclaration': 'Import',
    'ImportDefaultSpecifier': 0,
    'ImportNamespaceSpecifier': 0,
    'ImportSpecifier': 0,
    'LabeledStatement': 'Label',
    'Line': 'Comment',
    'Literal': 'Literal',
    'LogicalExpression': 'Expression',
    'MemberExpression': 'Object',
    'MetaProperty': 0,
    'MethodDefinition': 0,
    'NewExpression': 'New',
    'ObjectExpression': 'Object',
    'ObjectPattern': 'Object',
    'Program': 0,
    'Property': 'Property',
    'RestElement': 0,
    'ReturnStatement': 'Return',
    'SequenceExpression': 'Expression',
    'SpreadElement': 0,
    'Super': 'Super',
    'SwitchCase': 'SwitchCase',
    'SwitchStatement': 'Switch',
    'TaggedTemplateExpression': 'Expression',
    'TemplateElement': 0,
    'TemplateLiteral': 0,
    'ThisExpression': 'This',
    'ThrowStatement': 'Throw',
    'TryStatement': 'Try',
    'UnaryExpression': 'Expression',
    'UpdateExpression': 'Expression',
    'VariableDeclaration': 'Variable',
    'VariableDeclarator': 0,
    'WhileStatement': 'While',
    'WithStatement': 'With',
    'YieldExpression': 'Yield'
}
