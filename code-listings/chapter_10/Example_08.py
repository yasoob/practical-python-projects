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
