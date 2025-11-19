from lib.reformstatus import status_reform

# pytest tests/test_reformstatus.py

def test_ready_packet_reform():
    cot_packet = '<?xml version="1.0" encoding="UTF-8"?><event version="2.0" uid="IOTAI_SB02_RDY" type="a-f-G-U-C" time="2025-06-24T23:26:14.621Z" start="2025-06-24T23:26:14.621Z" stale="2025-06-24T23:27:54.621Z" how="m-g"><point lat="37.470318" lon="-121.940350" hae="0" ce="0" le="0" sat="0"/><detail><EV></EV></detail></event>'
    cotless_packet = status_reform(cot_packet)
    verified_ans = 'SEV,IOTAI_SB02_RDY,2025-06-24T23:26:14.621Z,2025-06-24T23:27:54.621Z,37.470318,-121.940350,0,</event>'
    assert cotless_packet == verified_ans, "RDY cot packet reformed failed."
    
def test_min_mode_reform():
    min_cot_packet = '<?xml version="1.0" encoding="UTF-8"?><event version="2.0" uid="IOTAI_SB00F" type="a-f-G-U-C" time="2025-11-18T17:50:50Z" start="2025-11-17T01:47:26.373Z" stale="2025-11-17T01:49:06.373Z" how="m-g"><point lat="0" lon="0" hae="0.0" ce="32" le="32" sat="0"/><detail><EV>AAAAAADQfUA/</EV><_flow-tags_ TAK-Server-cf51cb8f5cab4e85a0385d87678ea413="2025-11-18T17:50:50Z"/></detail></event>'
    min_cotless_reform = status_reform(min_cot_packet)
    verified_ans ='SEV,IOTAI_SB00F,2025-11-18T17:50:50Z,2025-11-17T01:49:06.373Z,0,0,0,AAAAAADQfUA/</event>'
    assert min_cotless_reform == verified_ans, "Minimal mode cot packet reformed failed."

def test_status_reform():
    status_cot_packet = '<?xml version="1.0" encoding="UTF-8"?><event version="2.0" uid="IOTAI_SB00" type="a-f-G-E-S-E" time="2025-11-18T17:47:51Z" start="2025-11-17T01:44:27.00Z" stale="2026-11-17T01:44:27.00Z" how="m-g"><point lat="0" lon="0" hae="0.0" ce="32" le="32" sat="0"/><detail><remarks>2025-11-17 01:44:27, stype=system,XLR_ORI=0013a2004242ffe5,XLR_PRNT=0013a200426be23f,XLR_GW=ffffffffffffffff,XLR_NET=7EEA,fw_version=387c,TXRETRY=2,XLRTX=77,XLRRX=4,P_RSSI=-40,XLRTX_kBps=0.2016,XLRRX_kBps=0.0103,XLRTX_PPS=1.2833,XLRRX_PPS=0.0667,SEQ=20,TxQ=0,RxQ=0,LVL=1,P_POW=2,vC=0.00,vB=0.00,IP=10.1.10.206,TEMP=43.00,PRES=0.00,HUMID=0.00</remarks><_flow-tags_ TAK-Server-cf51cb8f5cab4e85a0385d87678ea413="2025-11-18T17:47:51Z"/></detail></event>'
    status_cotless_reform = status_reform(status_cot_packet)
    verified_ans = 'sta,IOTAI_SB00,2025-11-18T17:47:51Z,2026-11-17T01:44:27.00Z,0,0,0,system,0013a2004242ffe5,0013a200426be23f,ffffffffffffffff,7EEA,387c,2,77,4,-40,0.2016,0.0103,1.2833,0.0667,20,0,0,1,2,0.00,0.00,10.1.10.206,43.00,0.00,0.00</event>'
    assert status_cotless_reform == verified_ans, "Status cot packet reformed failed."
    
def test_anom_mode_reform():
    anom_cot_packet = '<?xml version="1.0" encoding="UTF-8"?><event version="2.0" uid="IOTAI_SB05F" type="a-f-G-U-C" time="2024-11-20T00:50:03Z" start="2024-11-20T00:37:46.843Z" stale="2024-11-20T00:39:26.843Z" how="m-g"><point lat="37.470368" lon="-121.940193" hae="0.0" ce="32" le="32" sat="0"/><detail><RF freq_start="472.2" freq_end="473.1" freq_inc="0.1">H4sIAFovPWcC/wsJDQ/xCg8LDgEAJdokdAkAAAA=</RF><_flow-tags_ TAK-Server-6a9a383d62234470a7a948917b0b3643="2024-11-20T00:50:03Z"/></detail></event>'
    anom_cotless_reform = status_reform(anom_cot_packet)    
    verified_ans = 'SRF,IOTAI_SB05F,2024-11-20T00:50:03Z,2024-11-20T00:39:26.843Z,37.470368,-121.940193,0,472.2,473.1,0.1,H4sIAFovPWcC/wsJDQ/xCg8LDgEAJdokdAkAAAA=</event>'
    assert anom_cotless_reform == verified_ans, "Anomaly mode cot packet reformed failed."
    
def test_wifi_mode_reform():
    wifi_cot_packet = '<event version="2.0" uid="IOTAI_SB00W" type="a-f-G-U-C" time="2025-11-18T17:37:39Z" start="2025-11-17T01:34:14.429Z" stale="2025-11-17T01:35:54.429Z" how="m-g"><point lat="0" lon="0" hae="0.0" ce="32" le="32" sat="0"/><detail><WF>RTg5QzI1QkNDMUM0fElOVEVMRVNFTlNFLUNPTkYgUk18OXwyNDUyfDQwfFdQQTJ8O0U4OUMyNUJDQzEzNnxJTlRFTEVTRU5TRS1DVUJJQ0xFU3wxMHwyNDU3fDQ2fFdQQTJ8Ozk0ODNDNDI0QTU1M3xHTC1TRlQxMjAwLTU1MC01R3w0NHw1MjIwfDQ2fFdQQTJ8O0VBOUMyNUJDQzFDNHxJTlRFTEVTRU5TRS1DT05GIFJNfDExNnw1NTgwfDUyfFdQQTJ8OzEyQTc5MzhEQzYwRnxFWFRFUk5BTC1DT01DQVNUIDIuNEdIenw2fDI0Mzd8NTl8V1BBMnw7OTQ4M0M0MjRBNTUyfE9QQUwtSU9UQUkyfDl8MjQ1Mnw2MHxXUEEyfDsyMEU1MkE3QTIxMTl8bmdIdWJfMzE5MzMxTjYwMDI3Qnw2fDI0Mzd8NjJ8V1BBMnw7MzgyQzRBNkM3RDUwfEF5YW50cmF8N3wyNDQyfDYyfFdQQTJ8O0VBOUMyNUJDQzEzNnxJTlRFTEVTRU5TRS1DVUJJQ0xFU3wxMTZ8NTU4MHw2MnxXUEEyfDsxMkE3OTM5NEM2MDh8RVhURVJOQUwtQ09NQ0FTVCA1R0h6fDE0OXw1NzQ1fDYwfFdQQTJ8OzEyQTc5Mzk0QzYwQXx4ZmluaXR5d2lmaXwxNDl8NTc0NXw2MHxOb25lfDs4QzNCQURBOUNGMzZ8bmdIdWJfMzE5NDdBTkEwMTA3OXwxMXwyNDYyfDYzfFdQQTJ8Ow==</WF><_flow-tags_ TAK-Server-cf51cb8f5cab4e85a0385d87678ea413="2025-11-18T17:37:39Z"/></detail></event>'
    wifi_cotless_reform = status_reform(wifi_cot_packet)
    verified_ans = 'SWF,IOTAI_SB00W,2025-11-18T17:37:39Z,2025-11-17T01:35:54.429Z,0,0,0,RTg5QzI1QkNDMUM0fElOVEVMRVNFTlNFLUNPTkYgUk18OXwyNDUyfDQwfFdQQTJ8O0U4OUMyNUJDQzEzNnxJTlRFTEVTRU5TRS1DVUJJQ0xFU3wxMHwyNDU3fDQ2fFdQQTJ8Ozk0ODNDNDI0QTU1M3xHTC1TRlQxMjAwLTU1MC01R3w0NHw1MjIwfDQ2fFdQQTJ8O0VBOUMyNUJDQzFDNHxJTlRFTEVTRU5TRS1DT05GIFJNfDExNnw1NTgwfDUyfFdQQTJ8OzEyQTc5MzhEQzYwRnxFWFRFUk5BTC1DT01DQVNUIDIuNEdIenw2fDI0Mzd8NTl8V1BBMnw7OTQ4M0M0MjRBNTUyfE9QQUwtSU9UQUkyfDl8MjQ1Mnw2MHxXUEEyfDsyMEU1MkE3QTIxMTl8bmdIdWJfMzE5MzMxTjYwMDI3Qnw2fDI0Mzd8NjJ8V1BBMnw7MzgyQzRBNkM3RDUwfEF5YW50cmF8N3wyNDQyfDYyfFdQQTJ8O0VBOUMyNUJDQzEzNnxJTlRFTEVTRU5TRS1DVUJJQ0xFU3wxMTZ8NTU4MHw2MnxXUEEyfDsxMkE3OTM5NEM2MDh8RVhURVJOQUwtQ09NQ0FTVCA1R0h6fDE0OXw1NzQ1fDYwfFdQQTJ8OzEyQTc5Mzk0QzYwQXx4ZmluaXR5d2lmaXwxNDl8NTc0NXw2MHxOb25lfDs4QzNCQURBOUNGMzZ8bmdIdWJfMzE5NDdBTkEwMTA3OXwxMXwyNDYyfDYzfFdQQTJ8Ow==</event>'
    assert wifi_cotless_reform == verified_ans, "Wifi mode cot packet reformed failed."    
    
def test_bluetooth_mode_reform():
    bt_cot_packet = '<?xml version="1.0" encoding="UTF-8"?><event version="2.0" uid="IOTAI_SB00B" type="a-f-G-U-C" time="2025-11-18T17:42:29Z" start="2025-11-17T01:39:04.886Z" stale="2025-11-17T01:40:44.886Z" how="m-g"><point lat="0" lon="0" hae="0.0" ce="32" le="32" sat="0"/><detail><BT>AAYoxqsKgNIuOwBMUEGOPmHhNDsABm3fSK7FRj47AAYmMcf23UZEOwB1aPzK2c19ODsATF/A6znkiEo7AExDJ8fxgo1IOw==</BT><_flow-tags_ TAK-Server-cf51cb8f5cab4e85a0385d87678ea413="2025-11-18T17:42:29Z"/></detail></event>'
    bt_cotless_reform = status_reform(bt_cot_packet)
    verified_ans = 'SBT,IOTAI_SB00B,2025-11-18T17:42:29Z,2025-11-17T01:40:44.886Z,0,0,0,AAYoxqsKgNIuOwBMUEGOPmHhNDsABm3fSK7FRj47AAYmMcf23UZEOwB1aPzK2c19ODsATF/A6znkiEo7AExDJ8fxgo1IOw==</event>'
    assert bt_cotless_reform == verified_ans, "Bluetooth mode cot packet reformed failed."
    
    