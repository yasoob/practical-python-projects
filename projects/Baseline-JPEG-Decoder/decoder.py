from struct import unpack
import math

marker_mapping = {
    0xFFD8: "Start of Image",
    0xFFE0: "Application Default Header",
    0xFFDB: "Quantization Table",
    0xFFC0: "Start of Frame",
    0xFFC4: "Huffman Table",
    0xFFDA: "Start of Scan",
    0xFFD9: "End of Image",
}


def PrintMatrix(m):
    """
    A convenience function for printing matrices
    """
    for j in range(8):
        print("|", end="")
        for i in range(8):
            print("%d  |" % m[i + j * 8], end="\t")
        print()
    print()


def Clamp(col):
    """
    Makes sure col is between 0 and 255.
    """
    col = 255 if col > 255 else col
    col = 0 if col < 0 else col
    return int(col)


def ColorConversion(Y, Cr, Cb):
    """
    Converts Y, Cr and Cb to RGB color space
    """
    R = Cr * (2 - 2 * 0.299) + Y
    B = Cb * (2 - 2 * 0.114) + Y
    G = (Y - 0.114 * B - 0.299 * R) / 0.587
    return (Clamp(R + 128), Clamp(G + 128), Clamp(B + 128))


def DrawMatrix(x, y, matL, matCb, matCr):
    """
    Loops over a single 8x8 MCU and draws it on Tkinter canvas
    """
    for yy in range(8):
        for xx in range(8):
            c = "#%02x%02x%02x" % ColorConversion(
                matL[yy][xx], matCb[yy][xx], matCr[yy][xx]
            )
            x1, y1 = (x * 8 + xx) * 2, (y * 8 + yy) * 2
            x2, y2 = (x * 8 + (xx + 1)) * 2, (y * 8 + (yy + 1)) * 2
            w.create_rectangle(x1, y1, x2, y2, fill=c, outline=c)


def RemoveFF00(data):
    """
    Removes 0x00 after 0xff in the image scan section of JPEG
    """
    datapro = []
    i = 0
    while True:
        b, bnext = unpack("BB", data[i : i + 2])
        if b == 0xFF:
            if bnext != 0:
                break
            datapro.append(data[i])
            i += 2
        else:
            datapro.append(data[i])
            i += 1
    return datapro, i


def GetArray(type, l, length):
    """
    A convenience function for unpacking an array from bitstream
    """
    s = ""
    for i in range(length):
        s = s + type
    return list(unpack(s, l[:length]))


def DecodeNumber(code, bits):
    l = 2 ** (code - 1)
    if bits >= l:
        return bits
    else:
        return bits - (2 * l - 1)


class IDCT:
    """
    An inverse Discrete Cosine Transformation Class
    """

    def __init__(self):
        self.base = [0] * 64
        self.zigzag = [
            [0, 1, 5, 6, 14, 15, 27, 28],
            [2, 4, 7, 13, 16, 26, 29, 42],
            [3, 8, 12, 17, 25, 30, 41, 43],
            [9, 11, 18, 24, 31, 40, 44, 53],
            [10, 19, 23, 32, 39, 45, 52, 54],
            [20, 22, 33, 38, 46, 51, 55, 60],
            [21, 34, 37, 47, 50, 56, 59, 61],
            [35, 36, 48, 49, 57, 58, 62, 63],
        ]
        self.idct_precision = 8
        self.idct_table = [
            [
                (self.NormCoeff(u) * math.cos(((2.0 * x + 1.0) * u * math.pi) / 16.0))
                for x in range(self.idct_precision)
            ]
            for u in range(self.idct_precision)
        ]

    def NormCoeff(self, n):
        if n == 0:
            return 1.0 / math.sqrt(2.0)
        else:
            return 1.0

    def rearrange_using_zigzag(self):
        for x in range(8):
            for y in range(8):
                self.zigzag[x][y] = self.base[self.zigzag[x][y]]
        return self.zigzag

    def perform_IDCT(self):
        out = [list(range(8)) for i in range(8)]

        for x in range(8):
            for y in range(8):
                local_sum = 0
                for u in range(self.idct_precision):
                    for v in range(self.idct_precision):
                        local_sum += (
                            self.zigzag[v][u]
                            * self.idct_table[u][x]
                            * self.idct_table[v][y]
                        )
                out[y][x] = local_sum // 4
        self.base = out


class HuffmanTable:
    """
    A Huffman Table class
    """

    def __init__(self):
        self.root = []
        self.elements = []

    def BitsFromLengths(self, root, element, pos):
        if isinstance(root, list):
            if pos == 0:
                if len(root) < 2:
                    root.append(element)
                    return True
                return False
            for i in [0, 1]:
                if len(root) == i:
                    root.append([])
                if self.BitsFromLengths(root[i], element, pos - 1) == True:
                    return True
        return False

    def GetHuffmanBits(self, lengths, elements):
        self.elements = elements
        ii = 0
        for i in range(len(lengths)):
            for j in range(lengths[i]):
                self.BitsFromLengths(self.root, elements[ii], i)
                ii += 1

    def Find(self, st):
        r = self.root
        while isinstance(r, list):
            r = r[st.GetBit()]
        return r

    def GetCode(self, st):
        while True:
            res = self.Find(st)
            if res == 0:
                return 0
            elif res != -1:
                return res


class Stream:
    """
    A bit stream class with convenience methods
    """

    def __init__(self, data):
        self.data = data
        self.pos = 0

    def GetBit(self):
        b = self.data[self.pos >> 3]
        s = 7 - (self.pos & 0x7)
        self.pos += 1
        return (b >> s) & 1

    def GetBitN(self, l):
        val = 0
        for _ in range(l):
            val = val * 2 + self.GetBit()
        return val

    def len(self):
        return len(self.data)


class JPEG:
    """
    JPEG class for decoding a baseline encoded JPEG image
    """

    def __init__(self, image_file):
        self.huffman_tables = {}
        self.quant = {}
        self.quantMapping = []
        with open(image_file, "rb") as f:
            self.img_data = f.read()

    def DefineQuantizationTables(self, data):
        (hdr,) = unpack("B", data[0:1])
        self.quant[hdr] = GetArray("B", data[1 : 1 + 64], 64)
        data = data[65:]

    def BuildMatrix(self, st, idx, quant, olddccoeff):
        i = IDCT()

        code = self.huffman_tables[0 + idx].GetCode(st)
        bits = st.GetBitN(code)
        dccoeff = DecodeNumber(code, bits) + olddccoeff

        i.base[0] = (dccoeff) * quant[0]
        l = 1
        while l < 64:
            code = self.huffman_tables[16 + idx].GetCode(st)
            if code == 0:
                break

            # The first part of the AC key_len
            # is the number of leading zeros
            if code > 15:
                l += code >> 4
                code = code & 0x0F

            bits = st.GetBitN(code)

            if l < 64:
                coeff = DecodeNumber(code, bits)
                i.base[l] = coeff * quant[l]
                l += 1

        i.rearrange_using_zigzag()
        i.perform_IDCT()

        return i, dccoeff

    def StartOfScan(self, data, hdrlen):
        data, lenchunk = RemoveFF00(data[hdrlen:])

        st = Stream(data)
        oldlumdccoeff, oldCbdccoeff, oldCrdccoeff = 0, 0, 0
        for y in range(self.height // 8):
            for x in range(self.width // 8):
                matL, oldlumdccoeff = self.BuildMatrix(
                    st, 0, self.quant[self.quantMapping[0]], oldlumdccoeff
                )
                matCr, oldCrdccoeff = self.BuildMatrix(
                    st, 1, self.quant[self.quantMapping[1]], oldCrdccoeff
                )
                matCb, oldCbdccoeff = self.BuildMatrix(
                    st, 1, self.quant[self.quantMapping[2]], oldCbdccoeff
                )
                DrawMatrix(x, y, matL.base, matCb.base, matCr.base)

        return lenchunk + hdrlen

    def BaselineDCT(self, data):
        hdr, self.height, self.width, components = unpack(">BHHB", data[0:6])
        print("size %ix%i" % (self.width,  self.height))

        for i in range(components):
            id, samp, QtbId = unpack("BBB", data[6 + i * 3 : 9 + i * 3])
            self.quantMapping.append(QtbId)

    def decodeHuffman(self, data):
        offset = 0
        (header,) = unpack("B", data[offset : offset + 1])
        print(header, header & 0x0F, (header >> 4) & 0x0F)
        offset += 1

        lengths = GetArray("B", data[offset : offset + 16], 16)
        offset += 16

        elements = []
        for i in lengths:
            elements += GetArray("B", data[offset : offset + i], i)
            offset += i

        hf = HuffmanTable()
        hf.GetHuffmanBits(lengths, elements)
        self.huffman_tables[header] = hf
        data = data[offset:]

    def decode(self):
        data = self.img_data
        while True:
            (marker,) = unpack(">H", data[0:2])
            print(marker_mapping.get(marker))
            if marker == 0xFFD8:
                data = data[2:]
            elif marker == 0xFFD9:
                return
            else:
                (len_chunk,) = unpack(">H", data[2:4])
                len_chunk += 2
                chunk = data[4:len_chunk]
                if marker == 0xFFC4:
                    self.decodeHuffman(chunk)
                elif marker == 0xFFDB:
                    self.DefineQuantizationTables(chunk)
                elif marker == 0xFFC0:
                    self.BaselineDCT(chunk)
                elif marker == 0xFFDA:
                    len_chunk = self.StartOfScan(data, len_chunk)
                data = data[len_chunk:]
            if len(data) == 0:
                break


if __name__ == "__main__":
    from tkinter import Tk, Canvas, mainloop

    master = Tk()
    w = Canvas(master, width=1600, height=600)
    w.pack()
    img = JPEG("profile.jpg")
    img.decode()
    mainloop()
