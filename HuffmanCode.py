import heapq
import os


class HuffmanCode:

    class HeapNode:

        # constructor for heap node
        def __init__(self, char, freq):
            self.char = char
            self.freq = freq
            self.left = None
            self.right = None

        def __lt__(self, other):
            return self.freq < other.freq

        def __eq__(self, other):
            if other is None:
                return False
            if not isinstance(other, HeapNode):
                return False
            return self.freq == other.freq

    # constructor for Huffman class
    def __init__(self, path):
        self.path = path           # This is the file path for the text file that is to be compressed
        self.heap = []             # creates list for a heap for the Huffman's tree
        self.character_codes = {}  # dict where the key is the character and the value is the code of the character
        self.undo_code = {}

    # compression:
    def character_frequency(self, text):
        # this method creates a frequency dictionary of the different characters
        frequency = {}
        for character in text:
            if character not in frequency:
                frequency[character] = 0
            frequency[character] += 1
        # print(frequency)
        return frequency

    def add_characters(self, text, freq):
        # adds special characters, that are present in the different languages, to the character frequency dictionary
        for character in text:
            if character not in freq:
                freq[character] = 0
            # freq[character] += 1
        # print(freq)
        return freq

    def make_heap(self, frequency):
        # make heap to represent the priority queue
        for key in frequency:
            node = self.HeapNode(key, frequency[key])
            heapq.heappush(self.heap, node)
        while len(self.heap) > 1:
            node1 = heapq.heappop(self.heap)
            node2 = heapq.heappop(self.heap)
            merged = self.HeapNode(None, node1.freq + node2.freq)
            merged.left = node1
            merged.right = node2
            heapq.heappush(self.heap, merged)

    def add_codes(self, root, code):
        # This function uses recursion, therefore it is outside of the character_code function
        if root.char is not None:
            self.character_codes[root.char] = code
            self.undo_code[code] = root.char
            return
        # The left edges are assigned the value 0 while right nodes, 1
        self.add_codes(root.left, code + "0")
        self.add_codes(root.right, code + "1")

    def character_code(self):
        # creates the unique code for each character present in the text file
        root = heapq.heappop(self.heap)
        current_code = ""
        self.add_codes(root, current_code)

    def encode(self, text):
        encoded_text = ""
        for character in text:
            encoded_text += self.character_codes[character]

        add_padding = 8 - len(encoded_text) % 8
        for i in range(add_padding):
            encoded_text += "0"

        padded_info = "{0:08b}".format(add_padding)
        encoded_text = padded_info + encoded_text
        return encoded_text

    def bits2byte(self, encoded_text):
        bits_2_byte = bytearray()
        for i in range(0, len(encoded_text), 8):
            byte = encoded_text[i:i + 8]
            bits_2_byte.append(int(byte, 2))
        return bits_2_byte

    def compress(self):
        name, extension = os.path.splitext(self.path)   # separated the path of the file and the extension
        compressed_file = name + ".bin"    # so that the compressed binary file is stored in the same directory

        file = open(self.path, 'r')          # open file to be compressed as read only.
        text = file.read().rstrip()

        # make frequency dictionary and encode the text file
        freq = self.character_frequency(text)
        self.make_heap(freq)
        self.character_code()
        encoded_text = self.encode(text)

        output = open(compressed_file, 'wb')       # open empty output file as write in binary
        to_write = self.bits2byte(encoded_text)
        output.write(bytes(to_write))

        print("Compression complete!")
        return compressed_file

    # same tree on different language
    def language_compress(self, x):
        name1, name2 = os.path.splitext(x)
        print(f' Input file size in bytes is {os.stat(x).st_size}')
        compressed_file = name1 + ".bin"
        file = open(x, 'r')                 # open file to be compressed as read only.
        text = file.read().rstrip()

        file2 = open(self.path, 'r')        # open file to as read only. This is to create the encoding
        text2 = file2.read().rstrip()

        # make frequency dictionary and encode the text file
        freq = self.character_frequency(text2)
        freq = self.add_characters(text, freq)
        self.make_heap(freq)
        self.character_code()
        encoded_text = self.encode(text)

        output = open(compressed_file, 'wb')      # open empty output file as write in binary
        x = self.bits2byte(encoded_text)
        output.write(bytes(x))

        print("Compression complete!")
        return compressed_file

    # decompression:
    def decode_text(self, encoded_text):
        current_code = ""
        decoded_text = ""

        for bit in encoded_text:
            current_code += bit
            if current_code in self.undo_code:
                character = self.undo_code[current_code]
                decoded_text += character
                current_code = ""

        return decoded_text

    def decompress(self, compressed_file):
        name, extension = os.path.splitext(self.path)
        decompressed_file = name + "_decompressed" + ".txt"

        file = open(compressed_file, 'rb')
        bit_string = ""
        byte = file.read(1)
        while len(byte) > 0:
            byte = ord(byte)
            bits = bin(byte)[2:].rjust(8, '0')
            bit_string += bits
            byte = file.read(1)

        # remove the padding
        padded_info = bit_string[:8]
        extra_padding = int(padded_info, 2)
        padded_encoded_text = bit_string[8:]
        encoded_text = padded_encoded_text[:-1 * extra_padding]

        decompressed_text = self.decode_text(encoded_text)

        output = open(decompressed_file, 'w')
        output.write(decompressed_text)

        print("Decompression complete!")
        return decompressed_file

    def decompress_language(self, compressed_file, file_path):
        name, extension = os.path.splitext(file_path)
        decompressed_file = name + "_decompressed" + ".txt"

        file = open(compressed_file, 'rb')
        bit_string = ""
        byte = file.read(1)
        while len(byte) > 0:
            byte = ord(byte)
            bits = bin(byte)[2:].rjust(8, '0')
            bit_string += bits
            byte = file.read(1)

        # remove the padding
        padded_info = bit_string[:8]
        extra_padding = int(padded_info, 2)
        padded_encoded_text = bit_string[8:]
        encoded_text = padded_encoded_text[:-1 * extra_padding]

        decompressed_text = self.decode_text(encoded_text)

        output = open(decompressed_file, 'w')
        output.write(decompressed_text)

        print("Decompression complete!")
        return decompressed_file


print('Select one of the following:\n ' +
      '1. Regular compression of txt file\n' +
      ' 2. Compression of a txt file using the frequency dictionary of another file')

selection = input("")

if selection == '1':
    print("Input filepath of text file in directory: ")
    filepath = input("")
    HuffmanCoding = HuffmanCode(filepath)
    print(f'Input file size: {os.stat(filepath).st_size} bytes')
    compressed = HuffmanCoding.compress()
    print(f'Compressed file size: {os.stat(compressed).st_size} bytes')
    decompressed = HuffmanCoding.decompress(compressed)
    print(f'Decompressed file size {os.stat(decompressed).st_size} bytes')
    print("")

elif selection == '2':
    filepath = input("Input filepath of text file for frequency dictionary: \n")
    HuffmanCoding = HuffmanCode(filepath)
    filepath2 = input('Input different language file path: \n')
    compressed_lan = HuffmanCoding.language_compress(filepath2)
    print(f'Compressed file size: {os.stat(compressed_lan).st_size} bytes')
    decompressed2 = HuffmanCoding.decompress_language(compressed_lan, filepath2)
    print(f'decompressed file size: {os.stat(decompressed2).st_size} bytes')

else:
    print('invalid user input, input must be 1 or 2')
