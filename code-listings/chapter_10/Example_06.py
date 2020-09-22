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

class JPEG:
    def __init__(self, image_file):
        self.huffman_tables = {}
        self.quant = {}
        self.quant_mapping = []
        with open(image_file, 'rb') as f:
            self.img_data = f.read()
    # ----
    def BaselineDCT(self, data):
        hdr, self.height, self.width, components = unpack(">BHHB",data[0:6])
        print("size %ix%i" % (self.width,  self.height))
        for i in range(components):
            id, samp, QtbId = unpack("BBB",data[6+i*3:9+i*3])
            self.quant_mapping.append(QtbId)
    
    def decode(self):
        # ----
        while(True):
                # -----
                elif marker == 0xffdb:
                    self.define_quantization_tables(chunk)
                elif marker == 0xffc0:
                    self.BaselineDCT(chunk)
                data = data[len_chunk:]            
            if len(data)==0:
                break        
