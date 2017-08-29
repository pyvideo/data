import openpyxl as op
from textwrap import wrap
import json
import os
#from os.path import join as slash

# Process lightning talk from an excel file with these columns:
# Event, Pathname, Video, Time, Speakers, Name, Description
# run like "cd <mypydatadir>; python tools/parse_lightning_spreadsheet.py"
XLS_FILENAME = 'tools/lightning.xlsx'


class Talk:
    """ A talk.  Does not know its own conference. """

    def __init__(self, start, speakers, title, description):
        self.start = start if start else ""
        self.speakers = speakers if speakers else ""
        self.title = title if title else ""
        self.description = description if description else ""


def read_xls_file(filename):
    """ return two dictionaries indexed by filename:  talks and session_names """

    def c(rw, col):
        return worksheet.cell(row=rw, column=col).value

    workbook = op.load_workbook(filename)
    worksheet = workbook.active
    talks = {}
    session_names = {}
    row = 2
    while c(row, 2):
        pathname = c(row, 2)
        talk = Talk(c(row, 4), c(row, 5), c(row, 6), c(row, 7))
        if pathname not in talks:
            talks[pathname] = []
            session_names[pathname] = c(row, 3)
        talks[pathname].append(talk)
        row += 1
    return talks, session_names




def table(topic_name, talks):
    def table_header_part(topic_name):
        column_titles = ['Start', 'Speakers', 'Subject']
        lines = []
        lines.append(topic_name)
        lines.append("")
        lines.append(sep_line)
        lines.append(basic_line_format.format(*column_titles))
        lines.append(big_sep_line)
        return lines

    def table_part_for_talk(talk):
        # format one talk, with as many lines necessary for longer of speakers or combination of title and description

        start = wrap(talk.start, width[0])
        speakers = wrap(talk.speakers, width[1])
        title1 = wrap(talk.title, width[2] - 4)
        titles = ['**' + aline + '**' for aline in title1]
        desc = wrap('- ' + talk.description, width[2])
        big_col = titles + desc

        num_lines = max(len(start), len(speakers), len(big_col))
        part = []
        for i in range(num_lines):
            st = "" if i >= len(start) else start[i]
            sp = "" if i >= len(speakers) else speakers[i]
            bi = "" if i >= len(big_col) else big_col[i]
            part.append(basic_line_format.format(st, sp, bi))
        return part

    # set constants
    width = [8, 18, 54]
    sep_line = '+{}+{}+{}+'.format('-' * (width[0] + 2), '-' * (width[1] + 2), '-' * (width[2] + 2))
    big_sep_line = '+{}+{}+{}+'.format('=' * (width[0] + 2), '=' * (width[1] + 2), '=' * (width[2] + 2))
    basic_line_format = '+ {:' + str(width[0]) + '} | {:' + str(width[1]) + '} | {:' + str(width[2]) + '} +'

    lines = table_header_part(topic_name)
    for talk in talks:
        talk_lines = table_part_for_talk(talk)
        lines.extend(talk_lines)
        lines.append(sep_line)
    return "\n".join(lines)

def quote_for_json(unquoted_new_contents):
    b = '\\'  # a single character.  Raw strings mess up my JetBrain's IDE.
    contents = unquoted_new_contents.replace(b, b + b).replace('\n', b + 'n')
    return contents

def replace_string_field_in_json_file(filename, field_name, unquoted_new_contents):
    contents = quote_for_json(unquoted_new_contents)

    # set up filenames
    new_filename = filename + '.new'
    backup_filename = filename + '.bak'

    # read current contents to dict
    with open(filename) as f:
        json_dict = json.load(f)
        print(json_dict)

    # update new field in dict
    json_dict[field_name] = contents

    # write dict to new file
    try:
        os.unlink(new_filename)
    except OSError:
        pass

    with open(new_filename, 'w') as f:
        json.dump(json_dict, f, sort_keys=True, indent=4)

    # swap current file and backup
    try:
        os.unlink(backup_filename)
    except OSError:
        pass
    os.rename(filename, backup_filename)
    os.rename(new_filename, filename)


def process_lightning_talk_excel_file(filename=XLS_FILENAME):
    all_talks, all_session_names = read_xls_file(filename)

    for key in sorted(all_talks.keys()):
        # print("{} has {} talks".format(key, len(all_talks[key])))
        rst_block = table(all_session_names[key], all_talks[key])
        print(rst_block)

        filename = key
        replace_string_field_in_json_file(filename=filename, field_name="description",
                                          unquoted_new_contents=rst_block)

process_lightning_talk_excel_file()
