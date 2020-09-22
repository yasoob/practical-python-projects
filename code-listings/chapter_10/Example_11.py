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

def clamp(col):
    col = 255 if col>255 else col
    col = 0 if col<0 else col
    return  int(col)
def color_conversion(Y, Cr, Cb):
    R = Cr*(2-2*.299) + Y
    B = Cb*(2-2*.114) + Y
    G = (Y - .114*B - .299*R)/.587
    return (clamp(R+128),clamp(G+128),clamp(B+128) )
  
def draw_matrix(x, y, matL, matCb, matCr):
    for yy in range(8):
        for xx in range(8):
            c = "#%02x%02x%02x" % color_conversion(
                matL[yy][xx], matCb[yy][xx], matCr[yy][xx]
            )
            x1, y1 = (x * 8 + xx) * 2, (y * 8 + yy) * 2
            x2, y2 = (x * 8 + (xx + 1)) * 2, (y * 8 + (yy + 1)) * 2
            w.create_rectangle(x1, y1, x2, y2, fill=c, outline=c)
class JPEG:
    # -----
    def start_of_scan(self, data, hdrlen):
        data,lenchunk = remove_FF00(data[hdrlen:])
        st = Stream(data)
        old_lum_dc_coeff, old_cb_dc_coeff, old_cr_dc_coeff = 0, 0, 0
        for y in range(self.height//8):
            for x in range(self.width//8):
                matL, old_lum_dc_coeff = self.build_matrix(st,0,
                    self.quant[self.quant_mapping[0]], old_lum_dc_coeff)
                matCr, old_cr_dc_coeff = self.build_matrix(st,1,
                    self.quant[self.quant_mapping[1]], old_cr_dc_coeff)
                matCb, old_cb_dc_coeff = self.build_matrix(st,1,
                    self.quant[self.quant_mapping[2]], old_cb_dc_coeff)
                draw_matrix(x, y, matL.base, matCb.base, matCr.base)
        
        return lenchunk+hdrlen
      
if __name__ == "__main__":
    from tkinter import *
    master = Tk()
    w = Canvas(master, width=1600, height=600)
    w.pack()
    img = JPEG('profile.jpg')
    img.decode()    
    mainloop()
