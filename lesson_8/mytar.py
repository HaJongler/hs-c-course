import argparse

from archive import Archive


def validate_args(args):
    if (not args.c) and (args.file != []):
        raise SyntaxError("Files should not be passed without the -c flag")
    if args.c and (args.file == []):
        raise SyntaxError("Files must be passed when creating a new archive")


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-c", action="store_true")
    group.add_argument("-x", action="store_true")
    group.add_argument("-l", action="store_true")
    parser.add_argument("archive_name")
    parser.add_argument("file", nargs='*')
    args = parser.parse_args()

    validate_args(args)
    if args.c:
        archive = Archive.create_from_list(*args.file)
        archive.save(args.archive_name)
    else:
        archive = Archive.load_from_file(args.archive_name)
        if args.x:
            archive.extract()
        else:
            archive.list_contents()


if __name__ == '__main__':
    main()
