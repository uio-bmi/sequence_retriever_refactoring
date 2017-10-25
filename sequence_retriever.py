from urllib.request import urlopen
from os import linesep
import encodings
import urllib
from xml.etree import ElementTree

SEQUENCE = "SEQUENCE"
DNA = "DNA"


def fetch_sequence_from_web_service(source, chromosome, start_position, end_position):
    assert start_position >= 0
    assert end_position >= 0 and end_position > start_position

    # Convert 0-indexed with exclusive end to to 1-indexed inclusive end
    # (which is required by uscs and togows)
    start_position += 1

    if source != "UCSC" and source != "TOGOWS":
        raise NotImplementedError("Cannot fetch sequences from %s" % source)

    return _fetch_sequence_from_togows(chromosome, start_position, end_position) \
        if source == "TOGOWS" \
        else _fetch_sequence_from_ucsc(chromosome, start_position, end_position)


def _fetch_sequence(url):
    try:
        sequence = urlopen(url).read()
    except urllib.error.HTTPError:
        raise Exception("Invalid URL" + url)

    return sequence


def _fetch_sequence_from_togows(chromosome, start_position, end_position):
    sequence = _fetch_sequence(
        "http://togows.org/api/ucsc/hg38/%s:%d-%d.fasta" % (chromosome, start_position, end_position))

    # TOGOWS returns sequence with line breaks
    # Remove first line (header) and line breaks
    sequence = "".join(sequence.decode(encodings.utf_8.getregentry().name).split(linesep)[1:])
    return sequence.lower()


def _fetch_sequence_from_ucsc(chromosome, start_position, end_position):
    sequence = _fetch_sequence(
        "http://genome.ucsc.edu/cgi-bin/das/hg38/dna?segment=%s:%d,%d" % (chromosome, start_position, end_position))

    # UCSC the sequence wrapped in specially formatted xml
    xml_object = ElementTree.fromstring(sequence)
    sequence_element = xml_object.find(SEQUENCE).find(DNA)
    return "".join(sequence_element.text.split()).lower()
