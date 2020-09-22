"""
Using This Code Example
=========================
The code examples are provided by Yasoob Khalid to help you 
reference Practical Python Projects book. Code samples follow
PEP-0008, with exceptions made for the purposes of improving book
formatting. Example code is provided "as is".
Permissions
============
In general, you may use the code we've provided with this book in your
programs . You do not need to contact us for permission unless you're
reproducing a significant portion of the code and using it in educational
distributions. Examples:
* Writing an education program or book that uses several chunks of code from
    this course requires permission. 
* Selling or distributing a digital package from material taken from this
    book does require permission.
* Answering a question by citing this book and quoting example code does not
    require permission.
Attributions usually include the title, author, publisher and an ISBN. For
example, "Practical Python Projects, by Yasoob Khalid. Copyright 2020 Yasoob."
If you feel your use of code examples falls outside fair use of the permission
given here, please contact me at hi@yasoob.me.
"""

def get_array(type,l, length):
    s = ""
    for i in range(length):
        s =s+type
    return list(unpack(s,l[:length]))
  
class JPEG:
    # ...
    def __init__(self, image_file):
        self.huffman_tables = {}
        self.quant = {}
        with open(image_file, 'rb') as f:
            self.img_data = f.read()
    def define_quantization_tables(self, data):
        hdr, = unpack("B",data[0:1])
        self.quant[hdr] =  get_array("B", data[1:1+64],64)
        data = data[65:]
    def decode_huffman(self, data):
        # ... 
        for i in lengths:
            elements += (get_array("B", data[off:off+i], i))
            offset += i 
            # ...
    def decode(self):
        # ...
        while(True):
            # ...
            else:
                # ...
                if marker == 0xffc4:
                    self.decode_huffman(chunk)
                elif marker == 0xffdb:
                    self.define_quantization_tables(chunk)
                data = data[len_chunk:]            
            if len(data)==0:
                break        
