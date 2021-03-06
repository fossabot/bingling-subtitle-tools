#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""initial module
"""


# Import built-in modules
import argparse
import itertools
import os


# Import third-party modules


# Any changes to the path and your own modules
from bingling_subtitle_tools import ass_v4p_prcs
from bingling_subtitle_tools import file_io
from bingling_subtitle_tools import version
# nuitka build limitation


class Bunch(object):
    def __init__(self, adict):
        self.__dict__.update(adict)


def get_cmd_args():
    __version__ = version.__version__

    parser = argparse.ArgumentParser(description="""A tool that do batch processing jobs on ASS\
(Advanced SubStation Alpha) files""",
                                     epilog="""Make sure the argument with space is in quotes.
The default value is used when the option is not present at the command line.
The \"arg_num\" in the help means if the option is input, the number of arguments is required.
The \"-xx: \" in the help means it works when \"xx\" option is input.
Reference: http://moodub.free.fr/video/ass-specs.doc
           https://github.com/sorz/asstosrt
Author: BingLingFanSub
Bug report: https://github.com/BingLingGroup/bingling-subtitle-tools""",
                                     formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument("-c", "--config",
                        help="""A config file stores the command line options and arguments.
                        Currently only support .py format.
                        If using, other options will be overridden.
                        [arg_num = 1]""")
    parser.add_argument("-i", "--input", nargs="*",
                        default=[os.getcwd(), ], dest="input_",
                        help="""Path(s) of the input .ass file(s).
                        [arg_num ≥ 0]
                        [default: Current directory]""")
    parser.add_argument("-o", "--output", nargs="*",
                        default=[os.getcwd() + "\\new", ],
                        help="""Name(s) of the output directory.
                        Functions when direction(s) exist(s)
                        and it has the same number of the input.
                        Otherwise it will try the default value.
                        [arg_num ≥ 0]
                        [default: Make a new folder named \"new\"
                        in the input directory]""")
    parser.add_argument("-es", "--exp-smp", action="store_true",
                        help="Enable a function: do a batch job on exporting .ass file(s) to txt file(s).\
                        [arg_num = 0]")
    parser.add_argument("-fn", "--field-name", nargs="?",
                        default="Style", const="Style", metavar="FIELD_NAME",
                        help="""-es: A Field name to separate .ass files into txt files.
                        Using the option without argument for default value.
                        Functions when -es is used.
                        [arg_num = 0 or 1]
                        [default: %(default)s]""")
    parser.add_argument("-msg", "--custom-msg", nargs="?",
                        default=" ", const="", metavar="STRING",
                        help="""-es: A custom message is written
                        on the first line of the output files.
                        Using the option without argument for no extra message export.
                        [arg_num = 0 or 1]
                        [default: # Exported by BingLingSubtitleTools {ver}]""".format(ver=__version__))
    parser.add_argument("-nts", "--name-tails", nargs="*",
                        default=["_CN", "_EN", ], metavar="STRING",
                        help="""-es: The output files' name tail(s).
                        Using the option without argument 
                        for each event's specific field content as their name tail.
                        Functions when name tails have the same number as
                        the ones after \"filter\".
                        The default \"..., ...\" means if not using this option,
                        it will try these 2 arguments: ..., ...
                        Same info omit below.
                        [arg_num ≥ 0]
                        [default: %(default)s]""")
    parser.add_argument("-ft", "--filter", nargs="*",
                        default=["中文字幕", "英文字幕", ], dest="filter_", metavar="FIELD_CONTENT",
                        help="""-es: Field content(s) to filter the events.
                        Using the option without argument 
                        for filter disabled and all the events will export to files 
                        separated by their field contents under the specific field name.
                        [arg_num ≥ 0]
                        [default: %(default)s]""")
    parser.add_argument("-te", "--text-excluded", action="store_true",
                        help="""-es: Enable output for text-excluded part,
                        which is separated into a file with a \"_t\" name tail
                        [arg_num = 0]""")
    parser.add_argument("-rn", "--rename-number", action="store_true",
                        help="""-es: Enable changing the export name into
                        a kind of format like \"E\" + the number already in the file name.
                        [arg_num = 0]""")
    parser.add_argument("-koc", "-es: --keep-override-code", action="store_true",
                        help="""Keep the override codes (similar words are override tags
                        by http://docs.aegisub.org/3.2/ASS_Tags/) instead of deleting them.  
                        [arg_num = 0]""")
    parser.add_argument("-nfe", "--no-forced-encoding", action="store_true",
                        help="""Disable output file encoding into utf-8 without BOM
                        equal to utf-8 with unix LF and it will use the same encoding 
                        as the input file with the windows CRLF.
                        [arg_num = 0]""")
    parser.add_argument("-lo", "--limited-output", action="store_true",
                        help="""Limit the files to one path 
                        which is the first \"-o/--output\" argument
                        [arg_num = 0]""")
    parser.add_argument("-ds", "--del-sect", action="store_true",
                        help="Enable a function: do a batch job on deleting .ass section(s) in .ass file(s).\
                        [arg_num = 0]")
    parser.add_argument("-sc", "--sect-name", nargs="+",
                        default=["[Aegisub Project Garbage]", ], metavar="SECTION_NAME",
                        help="""-ds: The section name(s) to Delete.
                        [arg_num > 0]
                        [default: %(default)s]""")
    parser.add_argument("-nt", "--name-tail", nargs="?",
                        default="_new",
                        const="", metavar="STRING",
                        help="""-ds: The output files' name tail.
                        Using the option without argument for no name tail output.
                        [arg_num = 0 or 1]
                        [default: %(default)s]""")
    parser.add_argument("-ow", "--overwrite", action="store_true",
                        help="""-ds: [WARNING] Enable overwriting files.
                        Using this option will override the \"-o/--output\" option 
                        and the \"-nt/--name-tail\" option.
                        Not using this option will prevent any attempts to overwrite the files.
                        [arg_num = 0]""")
    parser.add_argument("-v", "--version", action="version", version="{ver}".format(ver=__version__))

    return parser.parse_args(), __version__


def set_default_dict(arg_dict):
    if "input_" not in arg_dict:
        arg_dict["input_"] = [os.getcwd(), ]
    if "output" not in arg_dict:
        arg_dict["output"] = []
    if "exp_smp" not in arg_dict:
        arg_dict["exp_smp"] = False
    if "field_name" not in arg_dict:
        arg_dict["field_name"] = "Style"
    if "custom_msg" not in arg_dict:
        arg_dict["custom_msg"] = " "
    if "name_tails" not in arg_dict:
        arg_dict["name_tails"] = ["_CN", "_EN", ]
    if "filter_" not in arg_dict:
        arg_dict["filter_"] = ["中文字幕", "英文字幕", ]
    if "text_excluded" not in arg_dict:
        arg_dict["text_excluded"] = False
    if "rename_number" not in arg_dict:
        arg_dict["rename_number"] = False
    if "keep_override_code" not in arg_dict:
        arg_dict["keep_override_code"] = False
    if "no_forced_encoding" not in arg_dict:
        arg_dict["no_forced_encoding"] = False
    if "limited_output" not in arg_dict:
        arg_dict["limited_output"] = False
    if "del_sect" not in arg_dict:
        arg_dict["del_sect"] = False
    if "sect_name" not in arg_dict:
        arg_dict["sect_name"] = ["[Aegisub Project Garbage]", ]
    if "name_tail" not in arg_dict:
        arg_dict["name_tail"] = "_new"
    if "overwrite" not in arg_dict:
        arg_dict["overwrite"] = False


def main():
    args, __version__ = get_cmd_args()

    print()
    arg_dict = {}
    if args.config and len(args.config) > 0:
        if args.config.endswith(".py"):
            fail_c, in_codec, arg_str = file_io.file_to_str(args.config)
            if fail_c == 0:
                exec(arg_str, arg_dict)
                set_default_dict(arg_dict)
                args = Bunch(arg_dict)
                print(".py config file detected. Read successfully.")

            else:
                print("File's codec not supported.")
                return
        else:
            print("This format of config file currently not supported.")
            return

    if not args.del_sect and not args.exp_smp:
        print("No works done! Check your options.")
        return
    if len(args.input_) == 0:
        args.input_.append(os.getcwd())

    if args.custom_msg == " ":
        # process the "default" custom_msg
        args.custom_msg = "# Exported by BingLingSubtitleTools {ver}".format(ver=__version__)

    i = 0
    if args.limited_output:
        if len(args.output) > 0:
            args.output = list(itertools.repeat(args.output[0], len(args.input_)))
        else:
            print("At least one output must be specified. Limited-output option is invalid now.\n")
    for input_file in args.input_:
        if os.path.isdir(input_file):
            # input direction(s)
            if args.exp_smp:
                # simple ass export batch
                if i >= len(args.output):
                    args.output.append(input_file + "\\new")
                    print("""The number of output isn't enough.
                Using \"{inp}\" instead.\n""".format(inp=args.output[i]))
                    if not os.path.isdir(args.output[i]):
                        os.makedirs(args.output[i])

                elif not os.path.isdir(args.output[i]):
                    args.output[i] = input_file + "\\new"
                    print("""Output direction doesn't exist.
                Using \"{inp}\" instead.\n""".format(inp=args.output[i]))
                    if not os.path.isdir(args.output[i]):
                        os.makedirs(args.output[i])

                print("Simply exporting......")
                ass_v4p_prcs.simple_ass_export_batch(import_dir=input_file,
                                                     export_dir=args.output[i],
                                                     custom_msg=args.custom_msg,
                                                     field_name=args.field_name,
                                                     name_tail=args.name_tails,
                                                     filter_tuple=args.filter_,
                                                     export_method=(not args.no_forced_encoding,
                                                                    args.rename_number,
                                                                    args.text_excluded,
                                                                    args.keep_override_code)
                                                     )

                print("\nSimply exporting .ass in \"{inp}\" are all done.\n".format(inp=input_file))
            if args.del_sect:
                # delete ass section batch

                print("Deleting .ass sections......")
                if args.overwrite:
                    ass_v4p_prcs.delete_ass_sect_batch(import_dir=input_file,
                                                       export_dir=input_file,
                                                       name_tail="",
                                                       sect=args.sect_name,
                                                       is_forced_lf=not args.no_forced_encoding)

                elif i >= len(args.output):
                    args.output.append(input_file + "\\new")
                    print("""The number of output isn't enough.
                Using \"{inp}\" instead.\n""".format(inp=args.output[i]))
                    if not os.path.isdir(args.output[i]):
                        os.makedirs(args.output[i])

                elif not os.path.isdir(args.output[i]):
                    args.output[i] = input_file + "\\new"
                    print("""Output direction doesn't exist.
                Using \"{inp}\" instead.\n""".format(inp=args.output[i]))
                    if not os.path.isdir(args.output[i]):
                        os.makedirs(args.output[i])

                elif args.output[i] != input_file or len(args.name_tail) > 0:
                    ass_v4p_prcs.delete_ass_sect_batch(import_dir=input_file,
                                                       export_dir=args.output[i],
                                                       name_tail=args.name_tail,
                                                       sect=args.sect_name,
                                                       is_forced_lf=not args.no_forced_encoding)
                else:
                    print("""\"{elem}\":
                        ......Attempt to overwrite but failed.
                        ......Using \"-ow\" or \"--overwrite\" option to overwrite.\n""".format(elem=input_file))

                print("\nDeleting .ass section(s) in \"{inp}\" are all done.\n".format(inp=input_file))

        else:
            print("Input: \"{inp}\" does not exist.".format(inp=input_file))

        i += 1














