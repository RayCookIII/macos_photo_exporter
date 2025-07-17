"""
This script is used to export Photos from the MacOS Photos application based on the
date range specified. This script was created using Python 3.13.1.
"""

import os.path
import sys

from datetime import datetime, timedelta
from dateutil.parser import parse as dateutil_parse

from pathvalidate import is_valid_filepath
import click
import osxphotos


def export(export_path: str, from_date: str, to_date: str, library_path: str) -> None:
    """Export all of the pictures in a date range from the specified library to the
    export path. The pictures will be saved to in a directory structure based on the
    date it was created. If the directory does not exist it will be created. Duplicate
    files will be overwritten.

    Args:
        export_path (String): Filesystem path where the photos should be exported to.
        from_date (String): The date to start exporting files from in YYYY-MM-DD format.
        The default is two weeks from today.
        to_date (String): The date to stop exporting files in YYYY-MM-DD format.
        library_path (String): The absolute path to the photo library containg the photos
        to be exported. Specify 'None' to use the currently active library.
    """
    # Ensure the export_path is valid
    if not is_valid_filepath(export_path, platform='auto'):
        sys.exit(f'The export path {export_path} is invalid.')

    # Parse out the parameter dates and convert to datetime objects
    photo_from_date = dateutil_parse(from_date)
    photo_to_date = dateutil_parse(to_date)

    # Create the photos database object
    if library_path is not None:
        photosdb = osxphotos.PhotosDB(library_path)
    else:
        photosdb = osxphotos.PhotosDB()

    # Retrieve information for the photos within the dates requested
    photos = photosdb.query(osxphotos.QueryOptions(from_date=photo_from_date, to_date=photo_to_date, photos=True))

    for photo in photos:
        # Make sure the photo file exists
        if not photo.ismissing:
            # Construct the target folder based on the date the photo was taken
            export_target = os.path.join(export_path, photo.date.strftime('%Y'), photo.date.strftime('%Y-%m-%d'))

            # Create the target directory if it does not exist
            if not os.path.isdir(export_target):
                os.makedirs(export_target)

            # Export the photo. Only export the uneditied versions and overwrite if it already exists.
            photo.export(export_target, overwrite=True)
            print(f'Exported photo {photo.original_filename} to {export_target}')
        else:
            print(f'Skipping missing photo {photo.filename}')


@click.command()
@click.argument('export_path', type=click.Path(exists=True))
@click.option(
    '--from-date',
    help='The date to start exporting photos from. Defaults to today.',
    default=datetime.today() - timedelta(weeks=1)
)
@click.option(
    '--to-date',
    help='The date to end exporting photos from. Defaults to today.',
    default=datetime.today()
)
@click.option(
    '--library-path',
    help='Path to Photos library, defaults to last used library',
    default=None
)
def main(export_path, from_date, to_date, library_path) -> None:
    """Script entry point

    Args:
        export_path (String): Filesystem path where the photos should be exported to.
        from_date (String): The date to start exporting files from in YYYY-MM-DD format.
        to_date (String): The date to stop exporting files in YYYY-MM-DD format.
        library_path (String): The absolute path to the photo library containg the photos
        to be exported.
    """

    # Process the CLI arguments
    export_path = os.path.expanduser(export_path)
    library_path = os.path.expanduser(library_path) if library_path else None
    from_date = os.path.expanduser(from_date)
    to_date = os.path.expanduser(to_date)
    print(f'export path: {export_path}\n'
          f'from: {from_date}\n'
          f'to: {to_date}'
          )

    # Export the photos in the specified date range
    export(export_path, from_date, to_date, library_path)


if __name__ == '__main__':
    main()  # pylint: disable=no-value-for-parameter
