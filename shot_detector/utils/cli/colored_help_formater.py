# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

import argparse
import re as _re
from gettext import gettext as _

from .cli_help_painter import (
    CliPainterString as pstr,
    cli_help_painter as chp
)


class ColoredHelpFormatter(argparse.HelpFormatter):
    """
        ...
    """

    class _Section(argparse.HelpFormatter._Section):
        # noinspection PyPep8
        """
            ...
        """

        def __init__(self, *args, **kwargs):
            super(ColoredHelpFormatter._Section, self).__init__(
                *args,
                **kwargs
            )
            self.heading = chp.section(self.heading)

    def __init__(self,
                 prog,
                 indent_increment=2,
                 max_help_position=8,
                 width=72):

        super(ColoredHelpFormatter, self).__init__(
            prog=chp.prog(prog),
            indent_increment=indent_increment,
            max_help_position=max_help_position,
            width=width,
        )

        self._whitespace_matcher = _re.compile(r'\s+')
        self._long_break_matcher = _re.compile(r'\n\n+')

    def _format_usage(self, usage, actions, groups, prefix):
        if prefix is None:
            prefix = _(chp.section('usage: '))

            # if usage is specified, use that
            if usage is not None:
                usage %= dict(prog=self._prog)

            # if no optionals or positionals
            # are available, usage is just prog
            elif usage is None and not actions:
                usage = '%(prog)s' % dict(prog=self._prog)

            # if optionals and positionals
            # are available, calculate usage
            elif usage is None:
                prog = '%(prog)s' % dict(prog=self._prog)

                prog = pstr(prog)

                # split optionals from positionals
                optionals = []
                positionals = []
                for action in actions:
                    if action.option_strings:
                        optionals.append(action)
                    else:
                        positionals.append(action)

                # build full usage string
                form = self._format_actions_usage
                action_usage = form(optionals + positionals, groups)
                usage = ' '.join([s for s in [prog, action_usage] if s])

                prefix = pstr(prefix)
                usage = pstr(usage)

                # wrap the usage parts if it's too long
                text_width = self._width - self._current_indent
                if len(prefix) + len(usage) > text_width:

                    # break usage into wrappable parts
                    part_regexp = r'\(.*?\)+|\[.*?\]+|\S+'
                    opt_usage = form(optionals, groups)
                    pos_usage = form(positionals, groups)
                    opt_parts = _re.findall(part_regexp, opt_usage)
                    pos_parts = _re.findall(part_regexp, pos_usage)

                    c_opt_parts = pstr.clean(' '.join(opt_parts))
                    c_pos_parts = pstr.clean(' '.join(pos_parts))

                    assert c_opt_parts == pstr.clean(opt_usage)
                    assert c_pos_parts == pstr.clean(pos_usage)

                    # helper for wrapping lines
                    # noinspection PyShadowingNames
                    def get_lines(parts, indent, prefix=None):
                        """
                        
                        :param str or pstr parts: 
                        :param indent: 
                        :param prefix: 
                        :return: 
                        """
                        # noinspection PyShadowingNames
                        lines = []
                        line = []

                        if prefix is not None:
                            line_len = len(prefix) - 1
                        else:
                            line_len = len(indent) - 1
                        for part in parts:
                            part = pstr(part)

                            if line_len + 1 + len(
                                    part) > text_width and line:
                                lines.append(indent + ' '.join(line))
                                line = []
                                line_len = len(indent) - 1
                            line.append(part)
                            line_len += len(part) + 1
                        if line:
                            lines.append(indent + ' '.join(line))
                        if prefix is not None:
                            lines[0] = lines[0][len(indent):]
                        return lines

                    # if prog is short,
                    # follow it with optionals or positionals
                    if float(len(prefix) + len(
                            prog)) <= 0.75 * text_width:
                        indent = ' ' * (len(prefix) + len(prog) + 1)
                        if opt_parts:
                            # noinspection PyTypeChecker
                            lines = get_lines([prog] + opt_parts,
                                              indent, prefix)
                            # noinspection PyTypeChecker
                            lines.extend(get_lines(pos_parts, indent))
                        elif pos_parts:
                            # noinspection PyTypeChecker
                            lines = get_lines([prog] + pos_parts,
                                              indent, prefix)
                        else:
                            lines = [prog]

                    # if prog is long, put it on its own line
                    else:
                        indent = ' ' * len(prefix)
                        parts = opt_parts + pos_parts
                        # noinspection PyTypeChecker
                        lines = get_lines(parts, indent)
                        if len(lines) > 1:
                            lines = []
                            # noinspection PyTypeChecker
                            lines.extend(get_lines(opt_parts, indent))
                            # noinspection PyTypeChecker
                            lines.extend(get_lines(pos_parts, indent))
                        lines = [prog] + lines

                    # join lines into usage
                    usage = '\n'.join(lines)

            # prefix with 'usage:'
            return '%s|%s\n\n' % (prefix, usage)

    def _format_actions_usage(self, actions, groups):
        # find group indices and identify actions in groups
        group_actions = set()
        inserts = {}
        for group in groups:
            try:
                # noinspection PyProtectedMember
                start = actions.index(group._group_actions[0])
            except ValueError:
                continue
            else:
                # noinspection PyProtectedMember
                end = start + len(group._group_actions)
                # noinspection PyProtectedMember
                if actions[start:end] == group._group_actions:
                    # noinspection PyProtectedMember
                    for action in group._group_actions:
                        group_actions.add(action)
                    if not group.required:
                        if start in inserts:
                            inserts[start] += ' ['
                        else:
                            inserts[start] = '['
                        inserts[end] = ']'
                    else:
                        if start in inserts:
                            inserts[start] += ' ('
                        else:
                            inserts[start] = '('
                        inserts[end] = ')'
                    for i in range(start + 1, end):
                        inserts[i] = '|'

        # collect all actions format strings
        parts = []
        for i, action in enumerate(actions):

            # suppressed arguments are marked with None
            # remove | separators for suppressed arguments
            if action.help is argparse.SUPPRESS:
                parts.append(None)
                if inserts.get(i) == '|':
                    inserts.pop(i)
                elif inserts.get(i + 1) == '|':
                    inserts.pop(i + 1)

            # produce all arg strings
            elif not action.option_strings:
                default = self._get_default_metavar_for_positional(
                    action)
                part = self._format_args(action, default)

                # if it's in a group, strip the outer []
                if action in group_actions:
                    if part[0] == '[' and part[-1] == ']':
                        part = part[1:-1]

                # add the action string to the list

                part = chp.optional_short_name(part)

                parts.append(part)

            # produce the first way to invoke the option in brackets
            else:
                option_string = action.option_strings[0]

                # if the Optional doesn't take a value, format is:
                #    -s or --long
                if action.nargs == 0:
                    part = '%s' % option_string
                    part = chp.optional_flag_short_name(part)


                # if the Optional takes a value, format is:
                #    -s ARGS or --long ARGS
                else:
                    default = self._get_default_metavar_for_optional(
                        action)
                    args_string = self._format_args(action, default)
                    option_string = chp.optional_short_name(
                        option_string
                    )
                    part = '%s %s' % (option_string, args_string)
                # make it look optional
                # if it's not required or in a group
                if not action.required and action not in group_actions:
                    part = '[%s]' % part

                # add the action string to the list
                parts.append(part)

        # insert things at the necessary indices
        for i in sorted(inserts, reverse=True):
            parts[i:i] = [inserts[i]]

        # join all the action items with spaces
        text = ' '.join([item for item in parts if item is not None])

        # clean up separators for mutually exclusive groups
        op = r'[\[(]'
        close = r'[\])]'
        text = _re.sub(r'(%s) ' % op, r'\1', text)
        text = _re.sub(r' (%s)' % close, r'\1', text)
        text = _re.sub(r'%s *%s' % (op, close), r'', text)
        text = _re.sub(r'\(([^|]*)\)', r'\1', text)
        text = text.strip()

        # return the text
        return text

    def _format_text(self, text):
        text = chp.text(text)
        result = super(ColoredHelpFormatter, self)._format_text(text)
        return result

    def _format_action(self, action):
        # determine the required width and the entry label
        help_position = self._max_help_position
        help_width = self._width - help_position
        action_width = help_position
        action_header = pstr(
            self._format_action_invocation(action)
        )

        # no help; start on same line and add a final newline
        if not action.help:
            tup = self._current_indent, '', action_header
            action_header = '%*s%s\n' % tup

        # short action name; start on the same line and pad two spaces
        elif len(pstr.clean(action_header)) <= action_width:
            tup = self._current_indent, '', action_header
            action_header = '%*s%s\n' % tup

        # long action name; start on the next line
        else:
            tup = self._current_indent, '', action_header
            action_header = '%*s%s\n' % tup

        parts = [action_header]

        default = self._format_default(action)

        if default:
            default_lines = self._split_lines(default, help_width)

            for i, line in enumerate(default_lines):
                parts.append('%*s%s\n' % (help_position + i, '', line))

        # if there was help for the action, add lines of help text
        if action.help:
            help_text = self._expand_help(action)

            help_lines = self._split_lines(help_text, help_width)

            for line in help_lines:
                line = chp.action_help(line)
                parts.append('%*s%s\n' % (help_position, '', line))

        # or add a newline if the description doesn't end with one
        elif not action_header.endswith('\n'):
            parts.append('\n')

        # if there are any sub-actions, add their help as well
        for subaction in self._iter_indented_subactions(action):
            parts.append(self._format_action(subaction))

        # return a single string
        return self._join_parts(parts)

    def _get_help_string(self, action):
        help = action.help
        return help

    @staticmethod
    def _format_default(action):
        default = None

        if not action.default:
            return None
        if action.default is not argparse.SUPPRESS:
            defaulting_nargs = [
                argparse.OPTIONAL,
                argparse.ZERO_OR_MORE
            ]
            if (
                        action.option_strings
                    or (action.nargs in defaulting_nargs)
            ):
                default = "{name} is '{value}'.".format(
                    name=chp.default_name('Default'),
                    value=chp.default_value(str(action.default))
                )
                default = pstr(default)

        return default

    def _format_action_invocation(self, action):
        if action.option_strings:
            string = self._format_action_option_invocation(action)
            string = pstr(string)
            return string

        else:
            default = self._get_default_metavar_for_positional(action)
            metavar, = self._metavar_formatter(action, default)(1)
            return pstr(metavar)

    def _metavar_formatter(self, action, default_metavar):
        if action.metavar is not None:
            result = chp.metavar_action(action.metavar)
        elif action.choices is not None:
            mc = chp.metavar_choices('').obj

            choice_strs = [
                ('%s%s' % (mc.start, choice)) for choice in
                action.choices
            ]

            obj = chp.metavar_choices_wrap('=').obj()
            result = '%s{%s%s}%s' % (
                obj.start,
                ','.join(choice_strs),
                obj.start,
                obj.stop
            )

        else:
            result = chp.metavar_default(default_metavar)

        result = pstr(result)

        def format_(tuple_size):
            """

            :param tuple_size: 
            :return: 
            """
            if isinstance(result, tuple):
                return result
            else:
                return (result,) * tuple_size

        return format_

    def _format_action_option_invocation(self, action):
        seq = self._format_action_option_invocation_seq(action)
        return ', '.join(seq)

    def _format_action_option_invocation_seq(self, action):

        # if the Optional doesn't take a value, format is:
        #    -s, --long
        if action.nargs == 0:
            for option_string in action.option_strings:
                option_arg = "{name}".format(
                    name=chp.optional_flag_name(option_string),
                )

                yield pstr(option_arg)

        # if the Optional takes a value, format is:
        #    -s ARGS, --long ARGS
        else:
            default = self._get_default_metavar_for_optional(action)
            args_string = self._format_args(action, default)
            for option_string in action.option_strings:
                option_arg = "{name} : {lbr}{value}{rbr}".format(
                    name=chp.optional_name(option_string),
                    lbr=chp.optional_value_wrap('('),
                    value=chp.optional_value(args_string),
                    rbr=chp.optional_value_wrap(')'),
                )
                yield pstr(option_arg)

                # default = self._format_default(action)
                # if default:
                #     yield pstr(default)
