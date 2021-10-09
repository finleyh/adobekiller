import re
import zlib
import os
import yara



class killer:
    def __init__(self, bytestream):
        self.bytestream = bytestream
        self.decoded_content = []
        self.text = ''
        self.yara_hits = []
        self.urls = []

    def get_text(self):
        return self.text

    def get_urls(self):
        return self.urls

    def get_decoded_content(self):
        return self.decoded_content

    def get_raw(self):
        return self.bytestream

    def get_yara_hits(self):
        return yara_hits

    def decode_content(self):
        self.decoded_content = decode_flate_streams(self.bytestream)

    def parse_text(self):
        self.text = parse_pdf_text(self.decoded_content)

    def parse_urls(self):
        self.urls = parse_pdf_urls(self.decoded_content)

    def apply_yara(self, rules=None):
        self.yara_hits = run_yara(rules)

def decode_flate_streams(bytestream):
        regex_stream = re.compile(b'.*?FlateDecode.*?stream(.*?)endstream', re.S)
        decoded_streams = []
        for s in regex_stream.findall(bytestream):
            s = s.strip(b'\r\n')
            try:
                stream = zlib.decompress(s)
                decoded_streams.append(stream)
            except Exception as e:
                print('could not decode this stream: ',e)
                pass
        return decoded_streams



def parse_pdf_text(decoded_list):
    regex_text = re.compile(b'\(([\w\s\,\.\-]+?)\)',re.S)
    return b''.join(regex_text.findall(b''.join(decoded_list))).decode("utf-8")
        

def parse_pdf_urls(decoded_list):
    regex_text = re.compile(b'((?:https?|ftp)[^\s]+)',re.S)
    return regex_text.findall(b''.join(decoded_list)).decode("utf-8")
