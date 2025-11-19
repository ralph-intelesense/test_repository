import xml.etree.ElementTree as ET
import os
def organize_elements(root: ET.Element) -> dict:
	elements = {}
	elements['event'] = root.attrib

	for child in root:
		if child.tag == 'point':
			elements['point'] = child.attrib

		if child.tag == 'detail':
			for g_child in child:

				if g_child.tag == '_flow-tags_':
					continue

				elements[str(g_child.tag)] = g_child.attrib

				'''adds remarks as a key,val pair in elements dict'''
				if g_child.tag == 'remarks':
					# print(g_child.text)
					remarks_list = [word.strip() for word in g_child.text.split(",")]
					remarks_list = remarks_list[1:]

					for group in remarks_list:
						curr_group = [word.strip() for word in group.split("=")]
						elements[str(g_child.tag)][curr_group[0]] = curr_group[1]

				if g_child.text and g_child.tag != 'remarks':
					elements[str(g_child.tag)]['text'] = g_child.text

	return elements

def make_mesg(elements: dict) -> str:
	identifer: str = None
	temp_dict: dict = None
	result: str = ''

	if "remarks" in elements:
		result += 'sta,'
		temp_dict = elements.pop("remarks")
	else:
		identifer = next((key for key in elements.keys() if len(key) == 2), None)
		if identifer is None:
			print("ERROR MISSING TAGS")
			os._exit(0)
		result += f'S{identifer},'
		temp_dict = elements.pop(identifer)

	event_dict: dict = elements.pop('event')
	for key in event_dict:
		if key == 'uid' or key == 'time':
			result += f'{event_dict.get(key)},'
		if key == 'stale': # perhaps reduce to just add difference in time
			result += f'{event_dict.get(key)},'

	gps_dict: dict = elements.pop('point')
	# result += 'gps,'
	for key in gps_dict:
		if key == 'lat' or key == 'lon' or key == 'sat':
			result += f'{gps_dict.get(key)},'
	# if not gps_dict.get('sat'):
	#     result += '0,'

	if temp_dict is not None:
		for key in temp_dict:
			result += f'{temp_dict.get(key)},'
		if len(temp_dict) == 0:
			result += ','

	result = result[:-1]
	result += '</event>'

	return result

def status_reform(xml_string: str) -> str:	
	root = ET.fromstring(xml_string)
	elements: dict = organize_elements(root)

	reformed_mesg: str = make_mesg(elements)
	print(reformed_mesg)
	return reformed_mesg

def main() -> None:
    # xml_str: str = '<?xml version="1.0" encoding="UTF-8"?><event version="2.0" uid="IOTAI_SB02_RDY" type="a-f-G-U-C" time="2025-06-24T23:26:14.621Z" start="2025-06-24T23:26:14.621Z" stale="2025-06-24T23:27:54.621Z" how="m-g"><point lat="37.470318" lon="-121.940350" hae="0" ce="0" le="0" sat="0"/><detail><EV></EV></detail></event>'
	# xml_str: str = '<?xml version="1.0" encoding="UTF-8"?><event version="2.0" uid="IOTAI_SB05F" type="a-f-G-U-C" time="2024-11-20T00:50:03Z" start="2024-11-20T00:37:46.843Z" stale="2024-11-20T00:39:26.843Z" how="m-g"><point lat="37.470368" lon="-121.940193" hae="0.0" ce="32" le="32" sat="0"/><detail><RF freq_start="472.2" freq_end="473.1" freq_inc="0.1">H4sIAFovPWcC/wsJDQ/xCg8LDgEAJdokdAkAAAA=</RF><_flow-tags_ TAK-Server-6a9a383d62234470a7a948917b0b3643="2024-11-20T00:50:03Z"/></detail></event>'
	# xml_str: str = '<?xml version="1.0" encoding="UTF-8"?><event version="2.0" uid="IOTAI_SB07" type="a-f-G-U-C-I" time="2024-11-20T22:35:51Z" start="2024-11-20T22:23:26.00Z" stale="2025-11-20T22:23:26.00Z" how="m-g"><point lat="37.470365" lon="-121.940232" hae="0.000000" ce="32" le="32" sat="9"/><detail><_flow-tags_ IOTAI_SB07="2024-11-20T22:23:26.00Z" TAK-Server-6a9a383d62234470a7a948917b0b3643="2024-11-20T22:35:51Z"/><remarks>2024/11/20 22:23:26, stype=system,XLR_ORI=0013a200416e1375,XLR_PRNT=0013a200416e1395,XLR_GW=ffffffffffffffff,XLR_NET=7FFA,fw_version=375d,TXRETRY=1,XLRTX=2,XLRRX=1,P_RSSI=-14,XLRTX_kBps=0.0507,XLRRX_kBps=0.0035,XLRTX_PPS=0.1333,XLRRX_PPS=0.0667,SEQ=1128,QLEN=0,LVL=1,P_POW=4,TEMP=58,IP=15.240.15.240</remarks></detail></event>'
	# xml_str: str = '<event version="2.0" uid="IOTAI_SB07B" type="a-f-G-U-C" time="2024-11-14T21:44:52Z" start="2024-11-14T21:33:17.879Z" stale="2024-11-14T21:34:57.879Z" how="m-g"><point lat="37.471118" lon="-121.940293" hae="0" ce="0" le="0" sat="3"/><detail><BT>crIKSR72fDY0fEFwcGxlLEluYy5EZXZpY2V8O2j8ytnNfXw3MHxTYW1zdW5nRWxlY3Ryb25pY3NDby5MdGQuRGV2aWNlfDtbIrrRxqx8NzR8QXBwbGUsSW5jLkRldmljZXw7d33ragKCfDY0fE1pY3Jvc29mdERldmljZXw7I92As/tZfDcwfE1pY3Jvc29mdERldmljZXw7UJqau9rVfDY4fE1pY3Jvc29mdERldmljZXw7LVnKQnNhfDc2fE1pY3Jvc29mdERldmljZXw7A2RPqmIefDU4fEdvb2dsZUxMQ0RldmljZXw7azYicltMfDYyfEFwcGxlLEluYy5EZXZpY2V8O2vz2tKDZHw3MnxBcHBsZSxJbmMuRGV2aWNlfDslTuiohi58Njh8R29vZ2xlTExDRGV2aWNlfDtMShRJC718NjR8QXBwbGUsSW5jLkRldmljZXw7audkOAmXfDY4fEFwcGxlLEluYy5EZXZpY2V8O31SxC9OeHw2OHxBcHBsZSxJbmMuRGV2aWNlfDtuXFXie458NTh8QXBwbGUsSW5jLkRldmljZXw768+bUancfDYwfE1SNzkwMVB8OxGF7cXhpXw2NnxNaWNyb3NvZnREZXZpY2V8O/WuxbuO5Hw2NHxBcHBsZSxJbmMuRGV2aWNlfDtMrJVaz3p8NjR8QXBwbGUsSW5jLkRldmljZXw7bXJCAOrkfDY0fEFwcGxlLEluYy5EZXZpY2V8O3/HbcSHa3w4MHxNaWNyb3NvZnREZXZpY2V8O8ObNnmU23w3OHxBcHBsZSxJbmMuRGV2aWNlfDsYmcgyXQh8NjB8TWljcm9zb2Z0RGV2aWNlfDsG0Lhqp3B8NjB8R29vZ2xlTExDRGV2aWNlfDsi+Yr6PaZ8NjZ8TWljcm9zb2Z0RGV2aWNlfDtWAcDVoYd8NzR8QXBwbGUsSW5jLkRldmljZXw7EvWN8P0LfDY4fE1pY3Jvc29mdERldmljZXw7XVVA+p4SfDcyfE1pY3Jvc29mdERldmljZXw7X32yrRH8fDc4fEFwcGxlLEluYy5EZXZpY2V8O83+exPlpHw2NHxBcHBsZSxJbmMuRGV2aWNlfDtk2UQjaGt8NzB8R29vZ2xlTExDRGV2aWNlfDtY/3Uw0k98NjB8QXBwbGUsSW5jLkRldmljZXw75AncvLYIfDY2fEFwcGxlLEluYy5EZXZpY2V8O/xCv5laLHw2OHxBcHBsZSxJbmMuRGV2aWNlfDst5Yxnyl98NTZ8TWljcm9zb2Z0RGV2aWNlfDvMaXqRHL58NjJ8QXBwbGUsSW5jLkRldmljZXw7</BT><_flow-tags_ TAK-Server-6a9a383d62234470a7a948917b0b3643="2024-11-14T21:44:52Z"/></detail></event>'
	# status_reform(xml_str
	# xml_str: str = '<?xml version="1.0" encoding="UTF-8"?><event version="2.0" uid="IOTAI_SB02B" type="a-f-G-U-C" time="2025-03-20T17:34:02Z" start="2025-03-19T01:31:06.433Z" stale="2025-03-19T01:32:46.433Z" how="m-g"><point lat="37.470142" lon="-121.939835" hae="0" ce="0" le="0" sat="0"/><detail><BT>R0+fZuepfDQ4fEFwcGxlLEluYy5EZXZpY2V8Ozb+We4fKnw3MHxNaWNyb3NvZnREZXZpY2V8O/hG1S60c3w2MHxBcHBsZSxJbmMuRGV2aWNlfDt/sXwZVUB8NTJ8QXBwbGUsSW5jLkRldmljZXw7cdI3FznffDc0fEFwcGxlLEluYy5EZXZpY2V8O7xXKQXwhHw3MnxLQlByb180NzI2MTZ8O1tcFGsOuHw3MHxBcHBsZSxJbmMuRGV2aWNlfDvZyKqwiaN8Njh8TVI3OTAxUHw7CRj1HB7MfDUyfE1pY3Jvc29mdERldmljZXw71T6D6pbKfDYyfEFwcGxlLEluYy5EZXZpY2V8Ow==</BT><_flow-tags_ TAK-Server-6a9a383d62234470a7a948917b0b3643="2025-03-20T17:34:02Z"/></detail></event><?xml version="1.0" encoding="UTF-8"?>'
	# xml_str: str = '<event version="2.0" uid="IOTAI_SB00W" type="a-f-G-U-C" time="2025-11-18T17:37:39Z" start="2025-11-17T01:34:14.429Z" stale="2025-11-17T01:35:54.429Z" how="m-g"><point lat="0" lon="0" hae="0.0" ce="32" le="32" sat="0"/><detail><WF>RTg5QzI1QkNDMUM0fElOVEVMRVNFTlNFLUNPTkYgUk18OXwyNDUyfDQwfFdQQTJ8O0U4OUMyNUJDQzEzNnxJTlRFTEVTRU5TRS1DVUJJQ0xFU3wxMHwyNDU3fDQ2fFdQQTJ8Ozk0ODNDNDI0QTU1M3xHTC1TRlQxMjAwLTU1MC01R3w0NHw1MjIwfDQ2fFdQQTJ8O0VBOUMyNUJDQzFDNHxJTlRFTEVTRU5TRS1DT05GIFJNfDExNnw1NTgwfDUyfFdQQTJ8OzEyQTc5MzhEQzYwRnxFWFRFUk5BTC1DT01DQVNUIDIuNEdIenw2fDI0Mzd8NTl8V1BBMnw7OTQ4M0M0MjRBNTUyfE9QQUwtSU9UQUkyfDl8MjQ1Mnw2MHxXUEEyfDsyMEU1MkE3QTIxMTl8bmdIdWJfMzE5MzMxTjYwMDI3Qnw2fDI0Mzd8NjJ8V1BBMnw7MzgyQzRBNkM3RDUwfEF5YW50cmF8N3wyNDQyfDYyfFdQQTJ8O0VBOUMyNUJDQzEzNnxJTlRFTEVTRU5TRS1DVUJJQ0xFU3wxMTZ8NTU4MHw2MnxXUEEyfDsxMkE3OTM5NEM2MDh8RVhURVJOQUwtQ09NQ0FTVCA1R0h6fDE0OXw1NzQ1fDYwfFdQQTJ8OzEyQTc5Mzk0QzYwQXx4ZmluaXR5d2lmaXwxNDl8NTc0NXw2MHxOb25lfDs4QzNCQURBOUNGMzZ8bmdIdWJfMzE5NDdBTkEwMTA3OXwxMXwyNDYyfDYzfFdQQTJ8Ow==</WF><_flow-tags_ TAK-Server-cf51cb8f5cab4e85a0385d87678ea413="2025-11-18T17:37:39Z"/></detail></event>'
	# xml_str: str = '<?xml version="1.0" encoding="UTF-8"?><event version="2.0" uid="IOTAI_SB00B" type="a-f-G-U-C" time="2025-11-18T17:42:29Z" start="2025-11-17T01:39:04.886Z" stale="2025-11-17T01:40:44.886Z" how="m-g"><point lat="0" lon="0" hae="0.0" ce="32" le="32" sat="0"/><detail><BT>AAYoxqsKgNIuOwBMUEGOPmHhNDsABm3fSK7FRj47AAYmMcf23UZEOwB1aPzK2c19ODsATF/A6znkiEo7AExDJ8fxgo1IOw==</BT><_flow-tags_ TAK-Server-cf51cb8f5cab4e85a0385d87678ea413="2025-11-18T17:42:29Z"/></detail></event>'
	
	# xml_str: str ='<?xml version="1.0" encoding="UTF-8"?><event version="2.0" uid="IOTAI_SB00" type="a-f-G-E-S-E" time="2025-11-18T17:47:51Z" start="2025-11-17T01:44:27.00Z" stale="2026-11-17T01:44:27.00Z" how="m-g"><point lat="0" lon="0" hae="0.0" ce="32" le="32" sat="0"/><detail><remarks>2025-11-17 01:44:27, stype=system,XLR_ORI=0013a2004242ffe5,XLR_PRNT=0013a200426be23f,XLR_GW=ffffffffffffffff,XLR_NET=7EEA,fw_version=387c,TXRETRY=2,XLRTX=77,XLRRX=4,P_RSSI=-40,XLRTX_kBps=0.2016,XLRRX_kBps=0.0103,XLRTX_PPS=1.2833,XLRRX_PPS=0.0667,SEQ=20,TxQ=0,RxQ=0,LVL=1,P_POW=2,vC=0.00,vB=0.00,IP=10.1.10.206,TEMP=43.00,PRES=0.00,HUMID=0.00</remarks><_flow-tags_ TAK-Server-cf51cb8f5cab4e85a0385d87678ea413="2025-11-18T17:47:51Z"/></detail></event>'
	xml_str: str = '<?xml version="1.0" encoding="UTF-8"?><event version="2.0" uid="IOTAI_SB00F" type="a-f-G-U-C" time="2025-11-18T17:50:50Z" start="2025-11-17T01:47:26.373Z" stale="2025-11-17T01:49:06.373Z" how="m-g"><point lat="0" lon="0" hae="0.0" ce="32" le="32" sat="0"/><detail><EV>AAAAAADQfUA/</EV><_flow-tags_ TAK-Server-cf51cb8f5cab4e85a0385d87678ea413="2025-11-18T17:50:50Z"/></detail></event>'
	status_reform(xml_str)

if __name__ == "__main__":
	main()