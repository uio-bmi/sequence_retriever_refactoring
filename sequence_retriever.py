from urllib.request import urlopen
import urllib
from xml.etree import ElementTree


def fetch_sequence_from_web_service(source, chromosome, start_position, end_position):

    assert start_position >= 0
    assert end_position >= 0 and end_position > start_position

    # Convert 0-indexed with exclusive end to to 1-indexed inclusive end
    # (which is required by uscs and togows)
    start_position += 1

    if source != "UCSC" and source != "TOGOWS":
        raise NotImplementedError("Cannot fetch sequences from %s" % source)

    if source == "TOGOWS":
        return _fetch_sequence_from_togows(source, chromosome, start_position, end_position)
    elif source == "UCSC":
        return _fetch_sequence_from_ucsc(source, chromosome, start_position, end_position)


def _fetch_sequence_from_togows(source, chromosome, start_position, end_position):

    url = "http://togows.org/api/ucsc/hg38/%s:%d-%d.fasta" % (chromosome, start_position, end_position)

    try:
        sequence = urlopen(url).read()
    except urllib.error.HTTPError:
        raise Exception("Invalid query %s:%d:%d" % chromosome, start_position, end_position)

    # TOGOWS returns sequence with line breaks
    # Remove first line (header) and line breaks
    sequence = ''.join(sequence.decode('utf8').split("\n")[1:])
    return sequence.lower()


def _fetch_sequence_from_ucsc(source, chromosome, start_position, end_position):

    url = "http://genome.ucsc.edu/cgi-bin/das/hg38/dna?segment=%s:%d,%d" % (chromosome, start_position, end_position)

    try:
        sequence = urlopen(url).read()
    except urllib.error.HTTPError:
        raise Exception("Invalid query %s:%d:%d" % chromosome, start_position, end_position)

    # UCSC the sequence wrapped in specially formatted xml
    xml_object = ElementTree.fromstring(sequence)
    sequence_element = xml_object.find("SEQUENCE").find("DNA")
    return "".join(sequence_element.text.split()).lower()
