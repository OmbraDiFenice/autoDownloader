import sys
from io import StringIO
import socket
from xmlrpc.client import dumps, loads, Fault
from urllib.parse import uses_netloc, urlsplit, splitport

uses_netloc.append('scgi')


def do_scgi_xmlrpc_request(host, method_name, params=()):
	xml_req = dumps(params, method_name)
	xml_resp = SCGIRequest(host).send(xml_req)
	return xml_resp


def do_scgi_xmlrpc_request_py(host, method_name, params=()):
	xml_resp = do_scgi_xmlrpc_request(host, method_name, params)
	return loads(xml_resp)[0][0]


class SCGIRequest(object):

	def __init__(self, url):
		self.url = url
		self.resp_headers = []

	def __send(self, scgi_req):
		scheme, netloc, path, query, frag = urlsplit(self.url)
		host, port = splitport(netloc)

		if netloc:
			# sys.stderr.write("host:%s port:%s\n" % (host, port))

			inet6_host = ''  # re.search( r'^\[(.*)\]$', host, re.M).group(1)

			if len(inet6_host) > 0:
				# sys.stderr.write("inet6_host:%s\n" % (inet6_host))
				addr_info = socket.getaddrinfo(inet6_host, port, socket.AF_INET6, socket.SOCK_STREAM)
			else:
				# sys.stderr.write("inet_host:%s\n" % (host))
				addr_info = socket.getaddrinfo(host, port, socket.AF_INET, socket.SOCK_STREAM)

			assert len(addr_info) == 1, "There's more than one? %r" % addr_info

			sock = socket.socket(*addr_info[0][:3])
			sock.connect(addr_info[0][4])
		else:
			sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
			sock.connect(path)

		sock.send(scgi_req)
		recv_data = resp = sock.recv(1024)

		while recv_data != '':
			recv_data = sock.recv(1024)
			resp += recv_data
		sock.close()
		return resp

	def send(self, data):
		"""Send data over scgi to url and get response"""
		scgiresp = self.__send(self.add_required_scgi_headers(data))
		resp, self.resp_headers = self.get_scgi_resp(scgiresp)
		return resp

	@staticmethod
	def encode_netstring(string):
		"""Encode string as netstring"""
		return '%d:%s,' % (len(string), string)

	@staticmethod
	def make_headers(headers):
		"""Make scgi header list"""
		return '\x00'.join(['%s\x00%s' % t for t in headers]) + '\x00'

	@staticmethod
	def add_required_scgi_headers(data, headers=None):
		"""Wrap data in an scgi request,\nsee spec at: http://python.ca/scgi/protocol.txt"""
		if headers is None:
			headers = []
		headers = SCGIRequest.make_headers([('CONTENT_LENGTH', str(len(data))), ('SCGI', '1'), ] + headers)
		enc_headers = SCGIRequest.encode_netstring(headers)
		return enc_headers + data

	@staticmethod
	def gen_headers(file):
		"""Get header lines from scgi response"""
		line = file.readline().rstrip()

		while line.strip():
			yield line
			line = file.readline().rstrip()

	@staticmethod
	def get_scgi_resp(resp):
		"""Get xmlrpc response from scgi response"""
		f_resp = StringIO(resp)
		headers = []

		for line in SCGIRequest.gen_headers(f_resp):
			headers.append(line.split(': ', 1))

		xml_resp = f_resp.read()
		return xml_resp, headers


class RTorrentXMLRPCClient(object):

	def __init__(self, url, method_name=''):
		self.url = url
		self.method_name = method_name

	def __call__(self, *args):
		scheme, netloc, path, query, frag = urlsplit(self.url)
		xml_req = dumps(args, self.method_name)

		if scheme == 'scgi':
			xml_resp = SCGIRequest(self.url).send(xml_req)
			return loads(xml_resp)[0][0]
		elif scheme == 'http':
			raise Exception('Unsupported protocol')
		elif scheme == '':
			raise Exception('Unsupported protocol')
		else:
			raise Exception('Unsupported protocol')

	def __getattr__(self, attr):
		method_name = self.method_name and '.'.join([self.method_name, attr]) or attr
		return RTorrentXMLRPCClient(self.url, method_name)


def convert_params_to_native(params):
	"""Parse xmlrpc-c command line arg syntax"""
	c_params = []

	for param in params:
		if len(param) < 2 or param[1] != '/':
			c_params.append(param)
			continue
		if param[0] == 'i':
			p_type = int
		elif param[0] == 'b':
			p_type = bool
		elif param[0] == 's':
			p_type = str
		else:
			c_params.append(param)
			continue
		c_params.append(p_type(param[2:]))

	return tuple(c_params)


def print_script(response):
	if type(response) is int:
		print(response)
	elif type(response) is str:
		print(response)
	else:
		for line in response:
			print(" ".join(line))


def main(argv):
	if len(argv) < 1:
		print("No arguments.")
		raise SystemExit(-1)

	output_arg = None
	if len(argv[0]) and argv[0][0] == '-':
		output_arg = argv[0]
		argv.pop(0)

	if len(argv) < 2:
		print("Too few arguments.")
		raise SystemExit(-1)

	host, method_name = argv[:2]
	resp_xml = do_scgi_xmlrpc_request(host, method_name, convert_params_to_native(argv[2:]))

	if output_arg == '-p':
		print(loads(resp_xml)[0][0])
	elif output_arg == '-s':
		print_script(loads(resp_xml)[0][0])
	else:
		print(resp_xml)


if __name__ == "__main__":
	try:
		main(sys.argv[1:])
	except Fault as e:
		print("xmlrpclib.Fault({0}): {1}".format(e.faultCode, e.faultString))
