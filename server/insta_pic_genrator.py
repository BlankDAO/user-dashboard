from time import time as now
from uuid import uuid4
from io import BytesIO
from PIL import Image
import random, string
from flask import g
import pyqrcode
import base64
import os



class InstagramQrCode(object):
	"""docstring for InstagramQrCode"""
	def __init__(self):
		self.id = ''
		self.url = ''


	def url_genrator(self):
		url = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
		res = g.db.instagram_image.find_one( {'url': url} )
		if res:
			return self.url_genrator()
		return url


	def create_qr(self):
		self.id = str(uuid4())
		url = pyqrcode.QRCode(self.id, error = 'H')
		data = url.png_as_base64_str(scale=13)
		im = Image.open(BytesIO(base64.b64decode(data)))
		im = im.convert("RGBA")
		return im


	def create_image(self, publicKey):
		qr = self.create_qr()
		photo = Image.open('../ui/assets/image/insta_temp.png')
		img_w, img_h = photo.size
		qr_w, qr_h = qr.size

		photo.paste(qr, ((img_w // 2) - (qr_w // 2)  , int(img_h - (img_h * 65 / 100))), qr)

		# Create target Directory if don't exist
		path = '../insta-images'
		if not os.path.exists(path):
		    os.mkdir(path)

		self.url = self.url_genrator()
		photo.save('../insta-images/{}.png'.format(self.url))
		g.db.instagram_image.insert_one({
			'url': self.url,
			'publicKey': publicKey,
			'id': self.id,
			'uploaded': True,
			'c_time': now()
		})
		return self.url


	def get_file(self, publicKey):
		res = g.db.instagram_image.find_one( {'publicKey': publicKey} )
		if res:
			return res['url']
		return self.create_image(publicKey)
