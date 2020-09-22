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

class HuffmanTable:
    def __init__(self):
        self.root=[]
        self.elements = []
    
    def bits_from_lengths(self, root, element, pos):
        if isinstance(root,list):
            if pos==0:
                if len(root)<2:
                    root.append(element)
                    return True                
                return False
            for i in [0,1]:
                if len(root) == i:
                    root.append([])
                if self.bits_from_lengths(root[i], element, pos-1) == True:
                    return True
        return False
    
    def get_huffman_bits(self,  lengths, elements):
        self.elements = elements
        ii = 0
        for i in range(len(lengths)):
            for j in range(lengths[i]):
                self.bits_from_lengths(self.root, elements[ii], i)
                ii+=1
    def find(self,st):
        r = self.root
        while isinstance(r, list):
            r=r[st.GetBit()]
        return  r 
    def get_code(self, st):
        while(True):
            res = self.find(st)
            if res == 0:
                return 0
            elif ( res != -1):
                return res
                
class JPEG:
    # -----
    def decode_huffman(self, data):
        # ----
        hf = HuffmanTable()
        hf.get_huffman_bits(lengths, elements)
        data = data[offset:]
