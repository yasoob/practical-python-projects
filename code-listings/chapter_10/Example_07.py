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

def remove_FF00(data):
    datapro = []
    i = 0
    while(True):
        b,bnext = unpack("BB",data[i:i+2])        
        if (b == 0xff):
            if (bnext != 0):
                break
            datapro.append(data[i])
            i+=2
        else:
            datapro.append(data[i])
            i+=1
    return datapro,i
class JPEG:
    # ----
    def start_of_scan(self, data, hdrlen):
        data,lenchunk = remove_FF00(data[hdrlen:])
        return lenchunk+hdrlen
      
    def decode(self):
        data = self.img_data
        while(True):
            marker, = unpack(">H", data[0:2])
            print(marker_mapping.get(marker))
            if marker == 0xffd8:
                data = data[2:]
            elif marker == 0xffd9:
                return
            else:
                len_chunk, = unpack(">H", data[2:4])
                len_chunk += 2
                chunk = data[4:len_chunk]
                if marker == 0xffc4:
                    self.decode_huffman(chunk)
                elif marker == 0xffdb:
                    self.define_quantization_tables(chunk)
                elif marker == 0xffc0:
                    self.BaselineDCT(chunk)
                elif marker == 0xffda:
                    len_chunk = self.start_of_scan(data, len_chunk)
                data = data[len_chunk:]            
            if len(data)==0:
                break        
