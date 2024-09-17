import array, os
import numpy as np
from PIL import Image
from .exbip.Serializable import Serializable


class Font(Serializable):

	def __init__(self):

		self.HeaderSize  = 0
		self.FileSize    = 0
		self.UnkWhatever = "\0"*6

		self.GlyphCount    = None
		self.GlyphSize1    = None
		self.GlyphSize2    = None
		self.GlyphByteSize = None

		self.UnkShort     = 0
		self.LastPosition = 0
		self.UNUSED       = 0

		self.Dims           = (0, 0, 0)
		self.PixelsPerGlyph = 0
		self.BitsPerPixel   = 0
		self.NumberOfColor  = 0

		self.Palettes       = None
		self.PaletteMap     = dict()

		self.WidthTableSize = 0
		self.WidthTable     = None

		self.FlagsSize = 0
		self.Flags     = None
		self.Reserved  = None

		self.Compressed    = None
		self.Decompressed  = None
		self.HasExtraThing = False

		self.Last = None

	def __rw_hook__(self, rw):

		rw.endianness = "<"

		self.HeaderSize  = rw.rw_uint32(self.HeaderSize)
		self.FileSize    = rw.rw_uint32(self.FileSize)
		self.UnkWhatever = rw.rw_bytestring(self.UnkWhatever, 6)

		self.GlyphCount    = rw.rw_uint16(self.GlyphCount)
		self.GlyphSize1    = rw.rw_uint16(self.GlyphSize1)
		self.GlyphSize2    = rw.rw_uint16(self.GlyphSize2)
		self.GlyphByteSize = rw.rw_uint16(self.GlyphByteSize)

		self.UnkShort     = rw.rw_uint16(self.UnkShort)
		self.LastPosition = rw.rw_uint32(self.LastPosition)
		self.UNUSED       = rw.rw_uint32(self.UNUSED)
		assert self.UNUSED == 0
		if rw.is_parselike:
			self.HeaderSize = rw.tell()
		assert rw.tell() == self.HeaderSize

		self.Dims           = (self.GlyphSize1, self.GlyphSize2, 4)
		self.PixelsPerGlyph = self.GlyphSize1*self.GlyphSize2
		self.BitsPerPixel   = (self.GlyphByteSize*8) // (self.GlyphSize1*self.GlyphSize2)
		self.NumberOfColor  = 2**self.BitsPerPixel

		self.Palettes       = rw.rw_objs(self.Palettes, Palette, self.NumberOfColor)
		for i in range(self.NumberOfColor):
			self.PaletteMap[tuple(self.Palettes[i].RGBA)] = i

		self.WidthTableSize = rw.rw_uint32(self.WidthTableSize)
		checkpoint          = rw.tell()
		self.WidthTable     = rw.rw_objs(self.WidthTable, VerticalCuts, self.WidthTableSize//2)
		assert rw.tell() - checkpoint == self.WidthTableSize

		self.FlagsSize = rw.rw_uint32(self.FlagsSize)
		self.Flags     = rw.rw_int8s(self.Flags, self.FlagsSize)
		self.Reserved  = rw.rw_uint32s(self.Reserved, self.GlyphCount)
		assert all(i == 0 for i in self.Reserved)

		self.Compressed = rw.rw_obj(self.Compressed, CompressedData)
		assert self.PixelsPerGlyph == self.Compressed.BytesPerGlyph

		if self.LastPosition != 0:
			if rw.is_parselike:
				self.LastPosition = rw.tell()
			if self.LastPosition != rw.tell():
				buffer = None
				buffer = rw.rw_uint8s(buffer, self.LastPosition-rw.tell())
				assert all(byte for byte in buffer == 0)
			self.Last = rw.rw_uint16s(self.Last, self.GlyphCount)

		if rw.is_parselike:
			self.FileSize = rw.tell()
		# assertion fails on reading P5R's FONT0 so like! okay! whatever...
		#assert rw.tell() == self.FileSize

		failed = False
		try:
			rw.assert_eof()
		except Exception:
			failed = True

		if failed:
			print("Failed to read file!")
			remainder = rw.peek_bytestream(64)
			print(len(remainder), remainder)

	def update_offsets(self):
		self.tobytes()

	def write_right(self, path):
		self.update_offsets()
		self.write(path)

	def decompress(self):
		assert self.Compressed is not None
		temp = 0
		self.Decompressed = [list()]
		for i in range(self.Compressed.CompressedBlockSize):
			byte = self.Compressed.Data[i]
			for j in range(8):
				temp = self.Compressed.Dictionary[temp][byte % 2 + 1]
				byte = byte >> 1
				if self.Compressed.Dictionary[temp][1] == 0:
					if len(self.Decompressed[-1]) == self.Compressed.BytesPerGlyph:
						self.Decompressed.append(list())
					self.Decompressed[-1].append(self.Compressed.Dictionary[temp][2])
					temp = 0
		self.HasExtraThing = (len(self.Decompressed[-1]) < self.Compressed.BytesPerGlyph)
		assert len(self.Decompressed) == self.GlyphCount + int(self.HasExtraThing)

	def compress(self):
		assert self.Decompressed is not None
		self.Compressed.compress(self.Decompressed)

	def to_single_image(self, path, width=60):
		img = list()
		addedGlyphs = 0
		while addedGlyphs < self.GlyphCount:
			row = list()
			for i in range(width):
				if addedGlyphs < self.GlyphCount and len(self.Decompressed[addedGlyphs]) == self.PixelsPerGlyph:
					elem = np.reshape(np.array([self.Palettes[j].RGBA for j in self.Decompressed[addedGlyphs]], dtype=np.uint8), self.Dims)
					if elem.sum() == 0:
						assert self.Flags[addedGlyphs] == -1
					# doesn't hold for P5R KEYTOP_FONT...
					#else:
					#	assert self.Flags[addedGlyphs] == 0
				else:
					elem = np.zeros(self.Dims, dtype=np.uint8)
				row.append(elem)
				addedGlyphs += 1
			row = np.concatenate(row, axis=1)
			img.append(row)
		img = np.concatenate(img, axis=0)
		Image.fromarray(img).save(path)

	def to_many_images(self, path):
		os.makedirs(path, exist_ok=True)
		for i in range(self.GlyphCount):
			img = np.reshape(np.array([self.Palettes[j].RGBA for j in self.Decompressed[i]], dtype=np.uint8), self.Dims)
			Image.fromarray(img).save(f"{path}/{i}.png")

	def update_from_dir(self, path):
		for filename in os.listdir(path):
			if filename.endswith(".png"):
				i = int(filename[:-4])
				img = np.reshape(np.array(Image.open(os.path.join(path, filename)), dtype=np.uint8), (self.PixelsPerGlyph, 4))
				self.Decompressed[i] = list()
				#for j in range(len(self.Decompressed[i])):
				for j in range(self.PixelsPerGlyph):
					#if img[j][0] == 0 and img[j][1] == 0 and img[j][2] == 0:
					#	palette = tuple([0, 0, 0, 0])
					#else:
					palette = tuple([int(channel) for channel in img[j]])
					#assert self.Decompressed[i][j] == self.PaletteMap[palette]
					#self.Decompressed[i][j] = self.PaletteMap[palette]
					self.Decompressed[i].append(self.PaletteMap[palette])
				if img.sum() == 0:
					self.Flags[i] = -1
				else:
					self.Flags[i] = 0


AlphaPS2ToPC = list(range(0, 129, 2)) + list(range(129, 256, 2)) + list(range(255, 0, -2))
PCToAlphaPS2 = {AlphaPS2ToPC[i]:i for i in range(len(AlphaPS2ToPC))}
class Palette(Serializable):

	def __init__(self):
		self.RGBA = None

	def __rw_hook__(self, rw):
		if rw.is_parselike:    # writer
			self.RGBA[3] = PCToAlphaPS2[self.RGBA[3]]
		self.RGBA = rw.rw_uint8s(self.RGBA, 4)
		#if rw.is_constructlike:  # reader
		self.RGBA[3] = AlphaPS2ToPC[self.RGBA[3]]


class VerticalCuts(Serializable):

	def __init__(self):
		self.Left  = None
		self.Right = None

	def __rw_hook__(self, rw):
		self.Left  = rw.rw_uint8(self.Left)
		self.Right = rw.rw_uint8(self.Right)


class CompressedData(Serializable):

	def __init__(self):
		self.HeaderSize           = None
		self.DictionarySize       = None
		self.CompressedBlockSize  = None
		self.LastGlyphPos         = None
		self.BytesPerGlyph        = None
		self.UNUSED               = None
		self.GlyphTableCount      = None
		self.GlyphPosTableSize    = None
		self.UncompressedFontSize = None

		self.Dictionary = None
		self.GlyphTable = None
		self.Data       = None

	def __rw_hook__(self, rw):
		checkpoint = rw.tell()
		self.HeaderSize           = rw.rw_uint32(self.HeaderSize)
		self.DictionarySize       = rw.rw_uint32(self.DictionarySize)
		self.CompressedBlockSize  = rw.rw_uint32(self.CompressedBlockSize)
		self.LastGlyphPos         = rw.rw_uint32(self.LastGlyphPos)
		self.BytesPerGlyph        = rw.rw_uint16(self.BytesPerGlyph)
		self.UNUSED               = rw.rw_uint16(self.UNUSED)
		assert self.UNUSED == 0
		self.GlyphTableCount      = rw.rw_uint32(self.GlyphTableCount)
		self.GlyphPosTableSize    = rw.rw_uint32(self.GlyphPosTableSize)
		self.UncompressedFontSize = rw.rw_uint32(self.UncompressedFontSize)
		if rw.is_parselike:
			self.HeaderSize = rw.tell() - checkpoint
		assert rw.tell() - checkpoint == self.HeaderSize

		checkpoint = rw.tell()
		self.Dictionary = rw.rw_uint16s(self.Dictionary, (self.DictionarySize//6, 3))
		if rw.is_parselike:
			self.DictionarySize = rw.tell() - checkpoint
		assert rw.tell() - checkpoint == self.DictionarySize

		self.GlyphTable = rw.rw_uint32s(self.GlyphTable, self.GlyphTableCount)
		if rw.is_parselike:
			self.CompressedBlockSize = len(self.Data)
			self.LastGlyphPos = self.GlyphTable[-1]
			self.GlyphPosTableSize = self.GlyphTableCount*4
		assert self.LastGlyphPos == self.GlyphTable[-1]
		assert self.GlyphPosTableSize == self.GlyphTableCount*4
		self.Data       = rw.rw_uint8s(self.Data, self.CompressedBlockSize)
		self.update_glyph_table()

	def compress(self, decompressed):
		part = 0
		for i in range(1, len(self.Dictionary)):
			if self.Dictionary[i][1] != 0:
				part = i
				break
		compressed = list()
		for i in reversed(range(len(decompressed))):
			for j in reversed(range(len(decompressed[i]))):
				s4 = decompressed[i][j]
				k = 1
				while self.Dictionary[k][2] != s4:
					k += 1
					if self.Dictionary[k][1] != 0:
						if (s4 >> 4) > ((s4 << 4) >> 4):
							s4 -= (1 << 4)
						else:
							s4 -= 1
						k = 1
				v0 = k
				while v0 != 0:
					v0 = self.find_index_add_bits(v0, part, compressed)
		byteified = list()
		for i in range(len(compressed)-1, 0, -8):
			k = 0
			for j in range(8):
				if i-j > 0 and i-j < len(compressed):
					k += compressed[i-j] << j
			byteified.append(k)
		self.CompressedBlockSize = len(byteified)
		self.Data = array.array("B", byteified)
		self.update_glyph_table()

	def find_index_add_bits(self, v0, part, compressed):
		if self.Dictionary[0][1] == v0:
			compressed.append(0)
			return 0
		elif self.Dictionary[0][2] == v0:
			compressed.append(1)
			return 0
		for l in range(part, len(self.Dictionary)):
			if self.Dictionary[l][1] == v0:
				compressed.append(0)
				return l
			elif self.Dictionary[l][2] == v0:
				compressed.append(1)
				return l
		return 255

	def update_glyph_table(self):
		temp, a, b = 0, 0, 0
		glyphTable = [0]
		for i in range(self.CompressedBlockSize):
			s4 = self.Data[i]
			a += 1
			for j in range(1, 9):
				temp = self.Dictionary[temp][s4 % 2 + 1]
				s4 = s4 >> 1
				if self.Dictionary[temp][1] == 0:
					b += 1
					if b % self.BytesPerGlyph == 0:
						glyphTable.append(((a-1) << 3) + j)
					temp = 0
		self.GlyphTable = array.array("I", glyphTable)
