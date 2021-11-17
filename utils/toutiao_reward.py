import requests
from uuid import uuid4
from urllib.parse import quote
from utils.common import Common
from random import randint, random
from utils.toutiao_sdk import cbc_encrypt, cbc_decrypt, create_key_iv, md5


class TouTiao(Common):

    def __init__(self, mobile):
        super(TouTiao, self).__init__()
        self.mobile = mobile
        self.session = requests.Session()
        self.session.headers = requests.structures.CaseInsensitiveDict({
            "content-type": "application/json; charset=utf-8",
            "accept-encoding": "gzip",
            "user-agent": "okhttp/3.9.1",
        })

    def reward(self, options, retry=2):
        # 避免出现orderId相同
        orderId = md5(str(self.timestamp) + self.mobile + uuid4().hex)
        print(orderId)
        media_extra = [
            options.get('ecs_token', ''),
            self.mobile,
            'android',
            options.get('arguments1', ''),
            options.get('arguments2', ''),
            orderId,
            str(options.get('codeId', '')),
            options['remark'],
            'Wifi'  # 4G / Wifi
        ]
        duration = randint(28000, 30000) / 1000
        uuid_ = self.getDeviceId
        message = {
            "oversea_version_type": 0,
            "reward_name": options['channelName'],
            "reward_amount": 1,
            "network": 4,  # 4 / 5 (Wifi / 4G)
            "sdk_version": "4.0.1.9",
            "user_agent": "Mozilla/5.0 (Linux; Android 8.1.0; MI 8 SE Build/OPM1.171019.019; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.91 Mobile Safari/537.36",
            "extra": {
                "ad_slot_type": 7,
                "oaid": "",
                "language": "golang",
                "ug_creative_id": "",
                "ad_id": None,
                "creative_id": None,
                "convert_id": None,
                "uid": None,
                "ad_type": None,
                "pricing": None,
                "ut": 12,
                "version_code": "8.8.5",
                "device_id": None,
                "width": 360,
                "height": 705,
                "mac": self.getMac,
                "uuid": uuid_,
                "uuid_md5": md5(uuid_),
                "os": "android",
                "client_ip": "",
                "open_udid": "",
                "os_type": None,
                "app_name": "中国联通APP",
                "device_type": "MI 8 SE",
                "os_version": "8.1.0",
                "app_id": "5049584",
                "template_id": 0,
                "template_rate": 0,
                "promotion_type": 0,
                "img_gen_type": 0,
                "img_md5": "",
                "source_type": None,
                "pack_time": round(self.timestamp / 1000 + random(), 6),
                "cid": None,
                "interaction_type": 4,
                "src_type": "app",
                "package_name": "com.sinovatech.unicom.ui",
                "pos": 5,
                "landing_type": None,
                "is_sdk": True,
                "is_dsp_ad": None,
                "imei": "",
                "req_id": "",
                "rit": int(options.get('codeId', 0)),
                "vid": "",
                "orit": 900000000,
                "ad_price": "",
                "shadow_ad_id": None,
                "shadow_creative_id": None,
                "shadow_advertiser_id": None,
                "shadow_campaign_id": None,
                "dynamic_ptpl_id": None,
                "engine_external_url": "",
                "engine_web_url": "",
                "variation_id": "",
                "app_bundle_id": "com.sinovatech.unicom.ui",
                "applog_did": "",
                "ad_site_id": "",
                "ad_site_type": 1,
                "clickid": "",
                "global_did": None,
                "ip": "",
                "ua": "Mozilla/5.0 (Linux; Android 8.1.0; MI 8 SE Build/OPM1.171019.019; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.91 Mobile Safari/537.36",
                "sys_language": "zh-CN",
                "playable_var_ids": "",
                "playable_template_var_id": 0,
                "country_id": None,
                "province_id": None,
                "city_id": None,
                "dma_id": None,
                "playable_url": None,
                "dco_pl_strategy": None,
                "dy_pl_type": None
            },
            "media_extra": quote('|'.join(media_extra)),
            "video_duration": duration,
            "play_start_ts": int(self.timestamp / 1000) - randint(30, 35),
            "play_end_ts": 0,
            "duration": int(duration * 1000),
            "user_id": "5049584",
            "trans_id": uuid4().hex,
            "latitude": 0,
            "longitude": 0
        }
        key, iv = create_key_iv()
        message = cbc_encrypt(message, key, iv)
        data = {
            'message': message,
            'cypher': 3
        }
        self.flushTime(randint(1, 5))
        url='https://is.snssdk.com/api/ad/union/sdk/reward_video/reward/'
        url='https://is.snssdk.com/api/ad/union/sdk/get_ads/'
        url = 'https://api-access.pangolin-sdk-toutiao.com/api/ad/union/sdk/reward_video/reward/'
        resp = self.session.post(url=url, json=data)
        resp.encoding = 'utf8'
        data = resp.json()
        message = {}
        if data.get('message', False):
            try:
                message = cbc_decrypt(data['message'])
                print(message)
            except:
                pass
        print(data)
        if not message.get('verify', False) and retry > 0:
            self.flushTime(randint(1, 5))
            return self.reward(options, retry - 1)
        return orderId


if __name__ == '__main__':
    pass
    data={"message":"3fPOJmhexAy30gIaMuyHWniOIkYvZwRkj25QsLRkV0aa4Y3cmpDaHF6+NVAlM3e6RoPy8YMwU7q0mRmn+2PybY8D2Wd3im+WJ3fdJL+n2WC02E2fqYV2XN0PDN2TQW4cpPFQoxF5v96S5WttV3Z+vKbnQGjKSzapxni/2fudXHCDD4AUJ4Mjk+QYGxQ2M4lCPnNBwVGa/B03T8giY8Bd6tLzAN4Tt+JeZ/CnKpNizoxIKDXJqO21s39DQ0kCv5g5LsmCrjw==","cipher":2,"ad_sdk_version":"2.7.5.2"}

    #data={"message":"22161e0f81dc1b0dc1e57Cy+Oc6zK3gZ7UkOkD9w4U3gxeGG\/EG4\/R7JdncgkAqlcz+NL1O2tNOLOMr13AH3mzk6Ctxn0\n94P6k6Sc9qDCVmsH3Oj\/8+khGhgj0RQppzg7yTyHoaAPD\/\/flRRLmw2UOTp6Iw7sAkNlWeM1bnLb\n7x7gP4pOymYoYxlRqq47ukXHitF1ihj7LvujzusfDo1ZjpAvK1XlOYsbBmW6x6t\/6z61sWVfU+CL\nZfelYg52q1c+Ff3fkHHHz1I8duC\/c7+\/nMav4Vy\/uB\/gyYVJXkxW59EksrtRhHpbrmVw0aK1jkZ9\npcozJIQsoQOI5YrVyXqb65f8BxvfKhAYrnX3IdDadF6caYX\/Bd+aeHYa1Cydi3LQBxlwVUrSyUxX\nQ1nFcaZsURpRCFcfjQm30wSk0A+50exUvXCNd7g0S7WW\/z3xiW3NE3PeFBHaD+UDeYU8t0Rr2\/vl\nZS09QdKQJnTv8HX6jFT\/Bm4AW52zqxGF\/Uw=\n","cypher":2}
    #data={"cipher":1,"message":"jsR9IDqJc8QkY4cY8fPDqJKuWC+Mxth1ups8LnV15NTFKcnliT8si194fBdOvne9H9aqV+\/RznqR\nR6hDN\/cWejdwQGgql5jpt4jhlo1xrJYfZt7U2qlIvPwrrMoItlvTauI4ncLZoUromLDI8k3W\/vVe\nbrnS1J+YgIvncYNp9e49lbK4NaLb8qJb9RIY2Ob9PAYIoKbDa4pmo9OTZE9yYWmphKEP2yznghIn\nVQIJtwBw9iPV0oRcGR98S1Au9Eqm0J6yM6ZMK0gJ52uGE1hYfvGP4IMYowCI5wZKAj0v2rqG\/ApB\nuIhJud\/C0DQLmsV3EeElk\/SdeRIh1s3SF3l2St\/Xp549iWSQ72QQRhttulp+KxD3gtUiBVBPiqRo\nHu4UvS\/MNsSO26Rpxf8Yt7r1XgF99GLpWFrhKMnTjF6prLJ\/h99Gg5CTgJgicgdU19E2IyJBRXBb\nyydsXayoN62Hjt67Ar8iajR\/9nrjfYEKpR68e4iNvOZCOP2qYVyH6lA5Dgrhgt7IYFdqhQKqhD1Z\nzjKwzt08wtB9YW2zLNGM2M\/lgx6tJxE9aWR4zhAVTZJXyZocPot6L2zUBk0PUYDUouAcvtrjDcze\neP1DN3Apw+TpA+VMVQlw1jdGoQVYiwYuejZ7+Nq1xLL6gRQWqULP09CHUAje0+FGfgXAUcJY4BBZ\npREuol0Ul4tGHphz1jxy2QaZvL3izYhRERo1qSFJmQE4QCk\/2mR7WP17a7+frHF6HQomIUwvsiZf\nZYdGnqU8k4TL1F51AhnQcRjhd6RxRpUHDvlLpBRWwGKn+LVmSzkk5SWSVgMHJ3r9LCG\/Uu4x1u5Y\nVrhbaMtpIopVpR1OyuOAmFg3D9mVCJ3VxHx9ZMou7nJQ\/qUtXBNX7UFo0ib1+jzo\/gd4V\/Ljthtz\nVOrq1QxAPWYE3J2PsZ7B+wGZlBDDcL0S0mMMjgn5HtAxU28k14Py4vIReXEz2Dr7CrkjhKyj32OT\n9Rl+rriUg7ruvG60v1VznW7rr2c0SdnR4GCwT9CUMPOG3eUf6FIRGjKQyG0Wc9FrtbBC2UGOmcOS\npCdDo76FTmiP7LPSuubC9gVO1m1eOFIJEZEgpd0LAvyUX\/VEBxby2f80xARCEbNnu92DqyQ1pyd3\nwK3EmxzidB3ef4ffRoOQk4CYInIHVNfRNi5Ex4mbPw6xQF1J2Yk6oe+nA28v3tc1KnJfGgBqw\/qi\nsTB0zuAVF4113EQMStoygbi89pVvcIikRcGaGZO8JZFEJKFtKptOAl5HXTHKB3pGuVmFDYh0PftT\n3ZYhp\/+9cRhEqVbyhvsa\/mANBV\/iJMHGJA7QX0Ei\/PilSPjWfMcQ5HD1PJ2qKMScUQ14zFb0zmKI\nXIIQuBetI8Sxwn2brEq5wJTdIJzfrzXeoWzmSxwmEGzCudvicMgb7CJ1c5PE6GGgoNJNDL4W5O2x\nwgihL4EVwHeXuBHbpHY4n8OiPcmSkpCi1salA+rTc8OoUqFDclZJ2gb0Z1iUxp5hRvtc5leb3EOD\nQTcc9QGLXUubjZsyS+Gcc2RzyW9olYhyTqWvODyCB5uBoEQnU+UicDfqVvzogVYKylpaa\/mUcq4Z\nyNBFV2XCYQd9k9NU8MZhcFXWG3qY5LoEX6tafFAEAcl7NdLofgWTz+cI7r22w0CxbepUSj\/E6iV9\nGy3mYC0a+LLyFaaxecV29WvYGQzfbs6CTwL9JP9fqfr9yO5lZRryk1cCV++KvEmLjOdl+DTS4AfI\nO74yhqAyLMoOYrlUYgENBwkOqv18AwujzW3VYweEcOO7vJle+BeNDS\/jaGZ6ag655qeswtkwBi\/t\narPIm8+Z1iepgQ0nSmSXBWGLcUVI1c8OPlPqP5fJDWAAabVYk1Hldh155qkoZQWLDtYIkVHnxKJX\nvuax\/wvA1q5sBlW1EW0E5RmLR\/+dPt59Fe05ydyjelmaqKlz3O0ts3QJ9a+KqLmOCgAwDKrT6TUV\nW+lSWgjJxEw0j9GmWsorGG1ZsamJ0kjifWZxpAbvO1nCuM1Lbm3QMOOUOY8dxolaI4H87vxjYDWe\n9qAk3AV7CPmBdbY0UDdLZiLQ118MZuONa7pGbUVCBInJNd4EHW\/tcDYhMwfFfkaF+ZyhIRo9dDmF\n20wC3ckwTwtDKK8BM+vZikS1ik4scuH8iqP59DSbjdmz3CySB116XB3PBylPjMjxbvsW\/+GDs0is\nUjPqJfWbgdQckSC+svht745+ldgKh65ihr+HbIOe5huVptM0ln19VBGXISUzuLyf3XkfBtj4aSG2\n0zEzGDyV0\/CrQzhKAe8rlZGdxzKyCf0zHC0EQkgqSMslCX3Xhtcltfj+N7zlXSQUs5ob6Yg0pDIO\n8+rIfOkIrOmGZherdDW2D6U46YT9eoIhCgq\/TMiH6ODGOV8OkDXWdoj+J5p0by83Z43B35LKML3a\n6cdDcXR7EErlLvkQ5S9fIPY9Y4BsA77fxOJnPe\/sftA\/0iOiQyoRMBcmUFj2VCkGNFWwrnZ0HhRu\ngj8c4rUrNFVfhKqwYJlbSzCaDRMZ7JYTEFrag2ILDrsJ55lAMRcaJOwERiIwd2VrnaQatrhjp16X\nJIL6gAuQ\/E6XdAYuMlormmMEvNy1XqqmD98gKhDWdnrZ6I+reGKT+fXAQ11DnA4mlxe3eajF0EP7\nvv\/7dj6NeY7wOEL\/w0PGoSBPLeyRp54jt38jZoGKsrf4sKN0LtvhzMSofwP+zW9kK22U096Lh19J\n3INL6ccHzHSUMMcJrkqYBa+tnNfyzT9Wpe+36z17ZDQ+0OvyQ\/3YSsdQAX+Ywcf4Y1htXS7QUHOS\nNHYu2JOUKjCoVPyXvPXeUPjir9KMDx1TbNqYLATRfqWgKnqKsd3kQSeLz1m55\/JHUUWF1b6I5WaU\nXmQelmXtIKLVgn1ViSBjXhCRF4QCvswic89vAULiPUIj3BGXpCRfGQSPP3KdWANM\/ShdLv599AvR\nGol65Cg37rFvk20etaewBAX1f5YUfH2M3Yr6T5VRHqp\/UMowMjjomvh2B5cyB0Rlk81c8ePSo\/qq\nZAURlBzzJdFFIusCAeX99g+SPqFq0Z52sQI8\/iqG4oKxxBSJXaffHy4k6SkVxIGdCVVgdww9BF9u\nPRQW2qyjaaJqPXRfdEOjk5C1DemD24HuSRcSxtUZbCMiCCm9PNifjfea7674juR3HnRnlLuYipjp\n8TP7NqFI8ELLNfqeoK426NXIi1gNrGHuApL31Y79YwQGrwdp3bm57fmDrCLZK2mcKM1EIIHHXOEv\nKX5E7NZofi0GM24zsuygbDO8RJb8n\/AyfLIlpphElTIH6+BKdiJ1v4GEi2BfxIASrVlxj7Y+EnRg\nPVKTSRL+TIP7XkORUhiHg1sLdjlKmvmlIW8x+Tt2Kk50UDFFp1fhmP0WluKpLaBqXLuGxEUqaiuf\nxQO1LRewzs\/drCmbWfnEub0FCXjNHh8RjmXWdkYlVCnaoAVSVoPh2VnhH2ugi6aCj1\/uzqLX4jT9\n0UY+MJawg4xtnmeIX0Im1P3Rl7j+6AuQOinX7ERHznUS3ElLkSrt3vfcSiNs6Uk1r+Jg2WLee+Nk\nmeiUPFh2MdD9xTZY5yurVbfVHBT83IjJsuwesx1OVAg1YR3Q\/QJ6U2cmM9ndyFuuT+dR8W4boUoy\nm+z45w0dZUbXnTw907gj4KHhe8JkkxN59NLCH\/4dILTZfVNlzYfNMZs1Tk6ewQGN2x5ByeiLgFtE\n\/1NCVLUiA6oH60POYwf9rDV65YlJ9uSMSnW+3OECL9JEHFhxjfy2lItIQzVFMA+z8DgrSnNOPlKD\nNWVx0gjxMDLQRBAwyJoXF6FVF8C5nca4wXz55igAUUK+PBj2TE0ovz4H4JPoYyeEnsX7hOf\/aiCC\nWkZmAmG6bGrapDS96S0gGlqEJo1st\/KEBbhm9reIRuITbKOaB9M+0kR2y8V0CkAJesw0y46AzLR9\nVelXP48Ap2RNw5IMsdLoVOUYo4484rMXqLTdxicScOp0ikgMKAXtCuyKk4aYAYaihlqZ71CjT40V\nCUugO78nBmx2+x9YHVM1GkE\/JOKX8a\/qkqlpaAdyG4gFqWkcQsR3GQ8wKRijw5x3db9l2P3MRo+K\nH0JWPs73PWa6TfCTEEDZKsGbHTMJHfLS\/oadIB3mBsQVBxwwqjMoHazAkIJ7UftTD1yQQ6oo6bXU\nAgOjEfXCOtU\/YNgJZdxX\/BIqwDumibQudK90NKeATjucDMzFuKr8Zf93CrnGCLF11a9SOTZ3IPZ0\nqm22rZ\/PoXNlS8hCyWimezBGJ+1bYRdxSUisPM35Hm\/NHFnAKUbuWeQ8kKrYffSs0hKJr0Jf+F\/n\nqrh3Xz6qxuDTH7NEikEPqbVjch4CoFJahd0DFAZOyvC6phUHjdC1djQ3iZ8ECDUuYe8GErcqKRL+\nifnJOAQ9sykwXY0XZ\/Djm5GKORKgj6M3\/mraUrUIZjCzEGDcwQbK7uKEYGa\/PXTNdYLQesqCrL8f\no0A8vni1LT8FUHm3Glm6SheZ67M+3qt4t16J3sMMx25vN\/jsAdMnIPeldXixeRtkn6f4IWqVuc5A\n2Nhs7poPmkzQv\/e6XnC2WT5qKxCa8SecESzIRT7hzGpGqEj\/qG5rTa8bebgMoah38bxRIokcyhS\/\neZZ0CsT2YZZKNTbBwdQSxZzACUGwgw+1EvwkR8lzREFR7IJ4q2Sy2yYy\/J+M6nJ0eGRqiAqiflKC\n64Bro30ksa4w4QgJ79Kzo\/+4hQafszjaKOH0Ls1yLw2SEscNhuImKJJ7d+O2MJLCxLb5AMPcBgOL\nM0PsKluZEPR2FhuILZzL1xr1FBJvyLpo0s3+RAGgpW\/oUPHXju25e4Y=\n"}
    data={"message":"382d27b2441c9f125271edf9c1ffe3152314cc6541a290c1a\/acXptRJ1WQO3rgnzx2YI5D4lUAlCEBlM8DLOb212HKqUAq4iVqerLFHVNucjE1ZfwHfIe9zOXIV\np6cJaqarydvURBiwjZQILBLQmkNwi0CXvijtyEwQ3zJfrGJWAg1M7B0kpX+dEa+XIHP5D55AfbND\ngAC74cvK8blrB2XF84kR9FRgdL4QMJgcik4HlcGHUTOKuhK0Fp5mom6OMSvGUmmCIFTRBRFuGO\/D\nUQ2JB0OCj9pjdGjqFdmEQ2+6l6VXOAP7XUk0zLEnl4L6M7p6ORp1lVYlsb\/3+qg5u4dp8oVdjJK9\nBEiTJN4nCTZRb3LlpM8Cm\/33n\/swGSFdawc4ZjlBHFy39d4wdcJUuR26YDFzfwgF7L2Y3DRV9FKU\nhU328kbyQogo+Igb+voq2iGd5AMRVaXcn8XSY2GWySFlHMQdOvwbqAzWZ0n3FpulCcBzeL7Lb00m\nD6HOjri74SGLlhFdE35O+MH3Cl94PJjPmHYDfCnteFKRR+ZcnMuSNA2OpyVBo7OQKOftc0ixV\/4m\njyflsycLkhA12JrSOssz9E4GpQYEaYxyzWqZ8lYEfdaLA1SGPsXOVKxoGdnr9Eu9H7FI85jD7LDx\ndzfPjaazPb5VJPCkyCrHnLu5A8RwJ4RujZqHtnCZkpmMx6LJLne9FYMShJVXIXlRC6XgkNmkQ8ys\nJ1Ot9ImY8W1oU95s+lBG6kDkzI3uCPcgK6Dv5WTkxs6OL635Hk3TJrFbBehT3YVU8\/L4rAzqIxND\nhxL4TKbvFosF3Ey1JAf2ttRdvNOjI6TZFZsyglUWJmVi4yNQjJcwyLMqRgJIQ19zKJV30kmUlo6B\nuSulA8iWIbpePffuQo1ItNNVg+MdY7ZgEkIUpNhzukP2Et6FmQCg9bxCixzCyucjNNSMqcw1Q7Lz\ntkKVVvE1ZpPdgiPt245SsYH6VKdlDXjUZFS1weqOtjc79mYVpZZZNWoC0KmyLhlxCiSSqb\/KWZpu\nrJG6cMZrFes9C0kLadAbRPpYTYxnBhTDlI4a+vEr44B3sr+MIq4yAqMyiFoxdiI4g8dJyb5SgYdk\nGTqO6ErDpIGOY1m2\/LJqrMvzfMZVPt8N4p6bmHh4tboz1DvljGUBeQa3RbjbWnLRnWoEk09Qfk2X\nLvdDvCbHnt7WZ90EY2um34bNTAbp8vN11pQnRJerjIV80Bzj9z1Ah0KDMNS9dlH9zEkTDHm+O5gL\nrRu8kVYdnqMJ+fhitT4Ghtr8V4FxOixk5sqXOv3ahX95kpI24tedSpforH1lFi9+1kZvSYwKMez4\n+l4jgDvIJSVm88RIVWMtEnrL44TtxeVIeZ+jNsKvC8XZ\/PlSEpzO33VZSOiJCos5VaPSPkSBVeG9\niTgo+0YMKKqltH3ik6lgiLl0VJhCFTTP\/P+qQpnCHhClWot0keNkIINRSy9sGVhzy67z5KpMS2Hs\ncgm5zo1941oVLnxTaAAvRgukNfye2yDDOtW6Psg59cSl7fb532BNkcv0O7NNIGJ4WmbMl4x2x8wq\nsuZLcNj2B8+hgnR+SPGhOcPxhZCxlIUAhYeGafO36hG8mWo5lQqCRK0HLBR2HNcuSPIbrkQcRgVE\nKZjN\/X+XDnez2hz9CP2ddFboJ\/Oxr4Zp8Eknd3pPhvCCggwXRiv694BN1TaByXZEEsZuA8g4Do30\nDObTrrsahyfcETiHYtHJuHAlKi51yqHn+0RclrDWPVg1MkE74D0ODw23yCCKPd\/YpJrXme1JViRm\n0LFBzrPD1\/T2xEMB\/kN6A4N3EoBSVgL8yW7Y6MJlg8hKKCn82KB\/QLJj\/5TREkIvMR8Xxg4ieKYS\nXW9JZNRT4Pdz7Ydpncjhokso7zEin+aBY8wzKwGvzeVRKI9PHIx68PgrYXud444KExPIYh1JMZ20\n1\/EmcKwfwZ6L+SR0eDBNoJE0\/oshVXFFITMWFxGRdmFz+9xJTEYKO+5hRqg8vvSKeeCLRspoieo1\nMgm0YyOnvl41zNEr1npG9nnkUTkCet0ceDTpHMeHPgDO9u2cvPhb3srdk69gOR99YXNVvVUyeoz9\nzL1hzspajIF+SapOtz3UAmTHl9e2uqSiePux8\/i6ZN1PKB1aOSBDX1xDZCXGJg7\/71TQC8SW7rl+\nYRbIEootd8Y18\/R8UX0FwzR1z+LWFwz4JpHTUKG6rqN7t246KbloiA4grobEL4IR2sVAGDp9Z2bs\ncO7AJFNWT2t\/9FplKCImqM\/BEMRoH7nfDmm5ZIVtiqYpPgnXtQulub80DBa42XarnQc7PtWPNUwC\nI3r8K89SHG5mDej+xDeNi9bOF6B+D9gGNMXgp1LeHaeOr9Owv5DcNBPuJsEj\/B0Dw1ia6\/lIrDyR\nIhikSXyKPbd8JwQC+AwyUEv\/6f8Z9v+7nqol7xYRA5iXBHjevnQoHCvtAto7baM7djuZbz8EFzgp\n4fRKfuIz7eg64zgDl4OofAEzRwLuSzTIcOR\/Jhtlg80WWiXzxs+vADVGpPHhCSuOxCcaI45LH\/US\nemPUAnGRDbsfe1iWLmtRurvsgAxHHfqmGBiRmfvvLJp50nixgrv8z2FLyjyZBvpunP2FtBoiLUhZ\nYKCHGwyOoYP0WVosayZ3Ah12ylwUmXMrA7vJfoPmvL+tUXjm\/zXoCmyIZudRtvyG8uy82pmwWcYG\nYg2Xeh\/p8ZuLQxz15FXq5xi1qZIx1MIIW4jVWTt8eF8+9deP22aMMlVbCfts\/eDAeCSGTjLHBwSF\npQzhQJZCSRDtvSXzbCZeEe5AuMVawvN2J9ZsxCu1ueX5VCShEgMtcOmdmAKcAXCuNOZzdr29fw8D\nD9zs\/Sh7ifORznd5agJ4SOY5mrD6ljD+OcgS20TVbrxcjHBLIeBWtM5qsbEVv81z4H\/9dvrVGgYC\nNA+PlrYKqZX9\/QYzCp9rnoTRZYvrTKfAnJY0aSSQ\/hEqRlirhptX0SvXy+ImuizQZrGk+6gp7fdG\nRPUqpBvtv6cbYTyzwEJxbGJvpASwSUrzqfAzokmzgtDW67QE8GAsThNE9A3SOoTqUYb0PmMkHrMi\nZrJtKHNlKcaSkjh\/Orz1qpgmTUyRssCLyKmgO8wJ7ZgZrnHK+Gnuv+fSt7XpJW8oauEx7RC8AYWJ\nlLfN8ZkNI1MObxvwqwBRfRHHPDt0N935a7PPLtNmwDQlspGMca2Y+HJZRmuItVAlV9d9qprdOJ7P\nVeX2F85Zu2+4u2UVzAV13pnLn2i+JBpK+V71QIgoMlFyz7Q8yPsu+4cKp+BmH9vCLG86mmK5MSY9\noJLtcVuq3SITHbCHJtviM+PTghA\/xSriZ4hPYU66jA2W24DOzL1uOIsXrmY9UT34eZlYckcsfPpt\nvIBgAwicei0YjKRs10cwkLpF36gCkoewCeAauaOyoxKHuh8nq3T8+qkGBTX4XdTi3p+Xf\/kI72MA\nhxZX4pu0qmFGphsMdPfEa1gWb6A41VyKIV6XCP5l5XnXLa3tfgpZ50YtmwZsIFzjpFoWlUTPo3YV\n9fp85aVhN4rzD9PvkZ0vRvwVS6aAyJoXxsaH0PRY7WBgFJxi244tnM\/cDLhu9U1oGAFG7YyNytyG\n7vwEsleTrFvIyWBGQmmKP41at97n9vT4JAlk6XDRIhFYbOn17l1WeTw98wpma+RA\/Y+YdhSaMZaI\ndBU46Sok9H3Fz1HSV026wvE7rbbfQcUpBXakM0udJwjbsDpygQN6xjYiAUbi3pXb1IQymD8AJ2fL\nBz8pybSJexIqKEvnvCdqIo5td8hcRTVUSCFK3nLyhSbSUf47AMppUKkvnKGOAeauvg99TH\/NcuXB\nhlB9iT+2km73beu7XCYfcAXLzkJTUD3LWB13Eox1bzVrhTCa8U2fJiuSCcau2yuwMhhbZA7Jo97d\nHRHAYROy2ucnKbhK5qiYOfYK0XBZ9EQHWIU7EL0lfI+I6KVd4oqSKAITONfmbcRE2wrdbSIAR0pO\njc0pgzs9D4UZr4ffz9RrSgD2zagEtgdXatJSlFUE9YNX7NVNHWxBWJmmErcyZ5Apr3uqXHpA6vDj\n3y1K1HnJ3O+vl4ts6jgqAtbjZXGxQZkuCFlKPt5yN2DFXDOkYXyJ47BAILA8bWTHE7xBKjomfREh\nXDU3h7w1pIv2pk0naCqKot0FEJIRXUHPj69DIIWf\/nAR3IONdx2HUPm4ubSCGSXUTibrrEyGIUIn\n2c\/SWcAirX9\/jUx3eq3TcTVj1jT66InPd4JCMPIej\/7Y5d\/WsAYpKwJb9mL1F+LrkUI9EyWgsLqM\ntuUQQLgno8aJxRA4m7QKG6r8552C91lvCyQIyBLm9Ajhpou0Zdwits3qfdFudoSOcpH5hnySgi2Y\nsmJvUGIcB2mTZ0UmUUif7ItfY8zS47yd8\/R8m6jFk5bU5nIeUY3Dgu32Z53x6lUbc3ZUYE4SmZsd\nytPILSJ8NkRXOLP7fQ5vGsNzCPgwptg80HL25ROP8V6C8zAAZ694eO4WIOJqQQOutO+EgPBJ1BJY\nb6aEOfR17vqj5ukP5LRCOJMKdQKOMJkc6QN0iAuAiLKMZknynvdWKeUbjfOLWizmab+++Lm6Jy3Y\nfCJrWLTq21bNQq4qEREB7MgIdJQNI0IUt8ea7KA8W4kj8rh8wf\/TqH4WE4GieSh\/SeXqvBGjNI+n\n9SdxUicY8YnJruSGOmUMgW6MjcjoaOpT0uFWGkYFrxzUnoF+F5EP9ib1HaCaxxxHxEzslJuM2i2N\nfmhqvQ\/elFMcazytSN57cq5xRSLLTdVTFguAYq4NCqRb+0KFiBE8HIiwEq\/HeQRvpEUiOZSD\/ntz\niIOUHjAyrD1hL4+n93V3vLSaay55O6AUILATe77rwbPpb4i0RZ6txNKeLOIWwcVe1jt\/DSpnStQ0\nPQbbZNyCBtQNvmMleg8rPSLl+414vYB2dJi4vnw5+Jea18Qr1Z4\/wFOmFXVuOLSQRrmr1TBHW34m\n5RG\/ssLBmmF6g\/jvCNFf5G1l4V5iRSK2Di1XpgNZbwvprw+ci\/qgE6C\/dQl525VN2P6gW3YWWzY8\nJ+7vYNgddCStv4bvhce6J\/OAXf20GSzZPJiXxDlPnZVQxz6dEQHg7OY\/q4w\/KRb\/YcsCrID774Th\nHNivZNvpcHMuZzHPRNwFPlWBkcTO2ryYJo0L\/OqxvRuj8bwMMolbf60fZYVMQY6W4uXlidn2xIko\n1mRkKEoHI5aguwc4K0SftnqILy00GzgGa8nTuD+hO8tdOInZS84Y4y3\/NAwRcmIjfPTk2J7udY0u\ns6f+dX+lBeNW1kLLJZYa32BlDs3WSGyi0ZqoFpzQf782hXodHSQy6\/Su8fSpXohSNh5+eVMnIhIt\nUGUTpg3gi+9\/uFKtPByLhGhPEFQWwqEnN1Ur2UnqCkWL7ItBs56jxI2Lt6SE9G+5CK3XgpjuI6EW\nnCRhQog2s7f\/uF1zVygAqhy4TGaN7Z9E7\/PVhMUzdzdGiog3hbOKFhnkYdLT3LWRDWIP0Bu9Ch0x\nGLVkKMnsPzk+F6HBFgJDmvRc+tIgje4A3\/iUNFw1HP6ah4efKQygDKlNMaIi4aBFXoexspbtU45s\nnLTz2DmnVaGjx1Aj2PJlLb7kZ2e+ZcppaAnYoa9YJB+TMLgnSc5nQh99zCAnsQiy9kqD7JaUIGn7\nuhwH8JsBoEv7tCGbPoaOAcxmhJMsJpoiKLoyuQKkkE59Wujabu\/BJ43jXq+YAIE6WesBE2OWzWcO\njfGNujPfhH4SJ3uZ7fzt7y8Sl8ttnkBZ+jsDZWuVrQ4EMbpcldFnccrrdyVP1mPthx30GBUozmbe\nqclFFA==\n","cypher":3}

    #data={"message":"27182c5dff4692db16v7+o6UEWArvij+JPZL5ZtDbZ6+WPQSCSijI3WR7ZzSiU3h8mRLPfY3iKoYaFknEEvI62hw+AuNk\n0PDhSWvjKl0WvuC7IzbP6lGc\/My\/M3aeVi9J2G3KGGr1wE5R7oME1gTNTYQyd9bMDYQbJ8fF\/iFV\ntDWEO0i46541DSEC8ZFnQ2KnpoCPOINRZLWgFzdMtePndb6MFULlqPSu8OjxF76m8orWwjxhRdB3\n3klCLTg\/Z9PVKomoTEGFS1MNYZzAAZ+osCfAfqwl3B8jYIoayFh2kLZkKdezB2l6x40WtYvos3qr\nrKrT1PK8rMchcUnLf0eRZ0bAV6DrRIt3Yu\/CBRuvoFnX+5qfTJzIUFChpwCaqBOmQbd4p08KlbY3\nUyw+iUAyoQ6h\/YtFhBUtFGDR3IgUtS0eApdJaZ+vn4wK503gPDpA8ocF1F7YhjljKe14Tkl7SUDe\nWlqzRY0etN4176iGd\/O9Hi2OwghU6cYdKjHLFKfeap63D2sihcnDSP4rnZDH8yQ5F1mMqR5rbds6\nmkfaXIcRFDy\/MtErRsbamNsBRExUz8pK6\/yX+ADX+TU7zJX1lCpTQnYOH\/sV\/ZyNFoE8ePcB3ipx\nCv6wITMDiOyt\/gVZKkSgFBmeUfWjbPFbxBTuBU4zkgYcR9CJz4WkGGg9\/h43tmjMZ0CnI+1MKi45\ngnSLfOQAbQSWPKwKKGtkPLDo\/GL66SeYKnhjxrX5y0WgHj7IcMowTO1p53Qvsbo2OYBPNAwtm19d\n8wNM7Xh4i2TxzJsB8ZKsTzLjq5BUfdaRiseB\/QdscV1fUDLeqH1jWRXkKz87VZ+0+bhISp5cBHpp\nDeN3\/v0oRtCXJJYUvrVM+0Ky9evaGGCoeWHPtFEi1WxWeyw+6uLslmEYfjrX41qzZi4jcr1zRH+5\nS8aZQHT4b4Nj\/7dIHbosi3eAe4aQbSNYmD7xYFyIqGPSFanE7EsNn7FV4GSzngW1crblxtdPdYMI\nTPvXv2I1fwOVQfVtJaGfrrT7hYLCBb4sThA725wro5S9KMCT\/uRULF1UryqWMr8s0OqpCuZXXd\/P\nkLv2K1mBUuKLbj8m0A+hc5iD9OCR44IL93tb9nHsNf9P518JlCkrmLxJzvjqbsMihVcBjLzrJgGr\ngOCWuSUJrW6ZjXwQHQJR7ZBKIF9RUn64iucGvmdCQYM8ZBOvB0p+mxETGwd1LEe14SK6vsRp5yY+\nygk1aDp7nu\/\/bX4J+HAi2OQrCuy3cZoD5z2sK\/3m9sJ+2qulj2e8Nv3pqlSYT33pIvDU+DHmn2zZ\nUOiYST3gcSxVFUp3l5iCGqR0fxhQRIGFiyViVlTOB6Kl4OnNVD90AXbgPjIn2dSriEClvVOVGPh7\nyEmF0zxYpg70n1Jimsz8X7YWMcRd2liJ4WKCFFwyMW68Xpl4Yzzy8K3vrmvZRzHIdta8QPZIUWvX\nfFdmanr2ECH+B3BMg8MHq9Evjn1qg8KJtbcPywl8OD6AL+bxnFWRuJSEsgo\/gd\/BpW8N\/DlJ8ajD\nxbIV8MsDXv3ujNtP\/s2FadktS0Gw\/YsInWqHavn+GSUy8SCyqGYXL+F4mfkGgy1aTk5SUhLkiJKj\nKqbjFSFnmd4HfeAW8ABfwI41EDjDNEcdHMPo5OVkA8axrVFoNxAu2OkkP1rajcXMvvPyBiOFGNEq\n+vENAp08yQ3\/6O+097MNjzAj73RzgqJMu+CFRitX5BmxWUxrhSAjM5grOtPZYerYrq9LkjdUdH4R\nb8C\/5V6zUYjX9ER+uMbXFbU8jErk+T4iXUbrnV8CbIMnN68bdB4BiDOb0biCDBQcInDk6+o63Inc\nJXC19DTY9T7pTyhAI7mrLFASPAWbZcYSngERlCiESZDKrpIvspphgZ69mUfuHcJO7y0RmaJfKo1K\npg7SuWkk7yuq28ghS0Gu3rjiTSf\/cGAjMSok0Py0xVxz3WPcajElipgiAXpmYyU82ygukdaGkb3i\nMUUokyI9t11pzAymIGcqjvDSiRUrRGFI2voUD3jzCpO8WQ5wbmeke1WT\/x3n0mKdGFZ1t6qJt69Z\nlbQJqiADSAssdoO\/2uhcIM3ABobM4NwhAv19tAOhHhkfq3MUNk8xFl2t0VyQ\n","cipher":2,"ad_sdk_version":"2.7.5.2"}
    data={"message":"2599fda2fd7880f83WLLX6eT3kXXsE5sramZlOxxAxxE2BUpecmbHp8tfpMhMoJqKUaHdppiXJHWDVE9o5JWPDWnkQp5P\nhkHQEUfHLQyGgGoIU5gHErh3+2tuheHXhQEn09Pw3NBQwVCcEu3HIdGWCF1tZfND+\/4rUPCtnWLn\nPOqfQWmZHJMFJ0xgtCL\/4gsMFJtkSbb+9Ipl57\/LqNmmvMODElo6iMhoZVhe8LH3L7L78XueyUpi\nnZxcF9\/BG5CcYauUoEyqktfhTSx1c81wuo9OxWaNie39FQwWoxZ3STMMcjjM5zOAOWXOHVTid4DO\nd9avqJ1GbW0frTqoYBo3JtnfFKRx1Uxd00WV+KVfj5hAJ+Z0HJIg+i6LBsK6Wy9cUMnBD42n0Cvj\ne3kpwye0rd5GGF3UjPmWn5wPNzjvT4mRRdRga8j2HL5jWUo2zjtfAUyiaPdBLUoUIeux\n","cypher":2}

    data={"cipher":1,"message":"jsR9IDqJc8QkY4cY8fPDqJKuWC+Mxth1ups8LnV15NTFKcnliT8si194fBdOvne9H9aqV+\/RznqR\nR6hDN\/cWejdwQGgql5jpt4jhlo1xrJYfZt7U2qlIvPwrrMoItlvTauI4ncLZoUromLDI8k3W\/vVe\nbrnS1J+YgIvncYNp9e49lbK4NaLb8qJb9RIY2Ob9PAYIoKbDa4pmo9OTZE9yYWmphKEP2yznghIn\nVQIJtwBw9iPV0oRcGR98S1Au9Eqm0J6yM6ZMK0gJ52uGE1hYfvGP4IMYowCI5wZKAj0v2rqG\/ApB\nuIhJud\/C0DQLmsV3EeElk\/SdeRIh1s3SF3l2St\/Xp549iWSQ72QQRhttulp+KxD3gtUiBVBPiqRo\nHu4UkLp1VDuFqWHq3tKA0qYTJMl09NKozijpaXWawMSucPuhTCp1fags9ydpqN7dhnFX\/H7J+y1L\n64Onu4GnO3vryq+EqYihMuKL5oKCoeGtrL+PP33V4M1fIwT11XwQqMOKy9HtQdRlj\/PGLFDaMe99\nTS3+xd0N6brkCkFp7ztNsOkgn4LE\/bNwVK8xcYA52vYZnEJnSkqB8E1whMZXU77EQPvnTGGdmXgO\n+3wgVIuEVntOC1NUKUohYnB7+JdHCevlap9aQXVBhRNG7v2w0qYYLu6JAOFdxweP808Scq8sjM4M\nXYOst6QwTbDC\/qMFEcR\/o06BvITlsN0hfv9tvzfimdo1VbLJW0RvKmL9nmi4RrWjd+Vg8k7s6\/wC\nn3jnrPJ6e1+4kOUF41IaAZCT9KzKuUO4W\/phIe3PTHxyAV34nM7bP34wZRqoRQKfQX8DsV11wMxX\n9fPd8Vcey0FUwQi4mn3Djt9rInL\/3KF1\/3tW6h9uWjy0x0T9CNStn2hqJcWqaQa+KM7zzW\/FDcSN\noDK4XAsdkriDzk949ddLMYcx9jxtlQJNuXgAmTi2SrJHeRKbWYtEc9RLyEan0jLLENaT3N1ccmOL\npPbtpDzG+zuEDkj7yTO6pY0TjC4jodj7HHw0Lm4JrDddHIbs+DMtmG\/xDAopTiJB9\/XbP7FH+nAc\n8OpXUtzEWIdw61gRz+d\/uE6U6MDYG1edpul5FsHUeTyEbVkL87\/foeTVhGXDJMewO9kTXU4q6HfF\nBWe7Tr8eM+2M5U6WlyUFsCQG+HHIV3b5drAvs0uFmNuRo96+J\/Y+F6ZeBT84xrT61U6VrgaEpyf0\n1Oa1Q6A51I79nXI615k1FoHHUgpwKy7RsSRsENS6RKznqQMkOmlM30RczkS64VP4p0mMdeRgY5g7\nZL62lKAAlbX4rgsdiflOVoUhPQ19NxT7Ioehz\/68VH5WDCXhti3yaUs\/\/\/6UB7S2P0A\/3lCp3dDx\n2ZX2bLBUg2CEIPGpWhc4nmy5zYDE+5etb6xQR4EubZLOqdDiyDIYWLXHjSOuP6QrQeOozTrwQixY\nlC\/f1zKANxBeT\/7L3mHqMH5uez9hrusXZac7VobjM1yKGQg+Dreq6ngxEwPTNczO\/oH4A0TBW5fo\nwVhICr85+pzhz8GzFu0Cny19\/6SZKPE\/i\/y2dFZhWOmlgWTK5S6GZ8PF\/UONMJMcRV6sTnmIsGMQ\np37wDnaA4qiUad6q4\/9Gx4V6hw0Oi7DxOGm8fQGMvwZZyBVV2oXRh8sI0\/cvRqPa7TnBrQDAQ\/Uj\nbitaB0tn\/oTyFG873G2WoAYkr\/SRAfedpFvZ\/zPqfM\/8aZCAKtuKOKHO5oLOtuS\/BmfuvArxF+cz\nzxAE5NStMpij+Osl61g+LWTdpnFp5J41hW8uQnUlUM0NB7g\/dZd1XkPQz9v8Opz4ezJreSVT1L9K\n1QBGB8o8OTyWT+QuWjZX8tioTzX7Ni+nbphO1LuYX6vanI9dG01WL\/sH7pZiX3LaRRAEDu6i+Sbu\nv8hlngXiA8bH41AtyHWLEHCLlnmFlNmtcTZkwsgiYdn2qoCE0Id77DXKT+8Y51KS+xWrvSPMsIWX\nDhrRqets99PutcerAbrWkoNBJmo51kD7A08l94CwNvYHRadyGUjoNUY7UklYURaZAXK3mGizWOLc\nNKaeNPQ9Deaq50kTLINrJtrTQRuUbvohpx6T1NipsBk9v5qCBMG4yDr4WjhU\/0x22hEnd8ts\/K2S\nbDFxSRzz9sU2o6HnxxAOmp46mGU2fF8Qaiwm\/gGfCp0G0e9fWMORBs6aamYgYCk6wbl+ymI\/Y2r6\n7iMTJtRYmWX0IhGn1XO6v88ww724fWHn0p72Da4QszgqHIIahO9knZ0qoxWpJhPXDxno4ItZRp1y\nwvkzFduqDAzCcySt0mmL2tpPswv7OOK1wveIOW5YJEjDrBwuM16ULDFohzaj2WA2uQsd9CD8K02p\nFYnzxO\/Rhk2KXJd2UOrPWVaDteQu5gt\/hfZUNMexyn+rbMBqh0GDZGDbb3qMIv9+jgfulzpHCOjM\nDh0eFdxoSG3m2SAPelV+AzbVEeF\/0qUeFJmr1vBp0EfYOhSdT03vPGPZs2IAM0RETPLpfhnOSw5l\noJUGNFogduDY52peuHinBRv2KM\/D70jnqwBP6BjY\/s8\/v5IMXXKX+crCqzqdwGejOBk8vS\/+ES0D\n1QRsHWLjMKQo\/RxY+6XPQALo4ToNv7odzbV3SE+huzhpaDXLPIfscRN\/NP23JLQQTcwhSRUz01ep\nrIz3SbKdnTnpP\/lgPkY\/yQir1KMTvMO7BGbPeTsU+HWgPe2JoH1ESHcJv+dHqxLWSL7Tsr252meu\nfui\/JovLl6MW8GFPmJnUWQmvajbQC6dIhPI0anXLpdkU5RuBxS\/uYW7ua1Zi1Szm6y1inaC0I\/5S\n3Xqkg65jCKVDLr0prGoabdaSjZfmKiq09HEom6QLjmdfRJXPzh3Qck52E+ufV\/c69tq0dRRNHvNP\nSfpdqcHn7veKdhIgoK5932Yp9vP+xPHLmY7Wn5Yuh1wi0Tkl9TyuD6y7T9WiMHb3anjnU7Ekf2mU\nLT6L0sW8doo2\/am5r4tsAZXdl3zpTy\/iPGSBb3na24FtsP61QkysK4yUfHeviOwPIOOPXKU46MXa\nVAxVgTHrbzfV\/n5mbhScNm3oKlZCUhbExsMVPdXbiZw7GcB09x12Brc8P5a\/8ojVhrM80uNnpEXn\nRDkmdIEuYtcKHU3m1EzNVPXYS6qF+mEAOtqC9THz4Ef+mYyZF\/b9nQkHXrh8+Cf2ip9EyE+GaDUM\nkwKnugSiw0cR+vgI+KUqLveWO8sD+vnQFeSNYyvpwhPtbNZo0iXPE7hMA2MGo8SldQvFTTgcaINE\nbyJvD7NXFZ3c1fFMbeE8NiI530exkhMrdeJXuWrOEAiy5R3MvKQqUdRzS1jE+ZY+yGqmhSoZ17Pw\n8TmyyusVYPhs3g7SeQH5B2f0p9aiX4nuaQ6Dd0SZVLhiuPTDda0ihzOvXhjuWL2e7hRCTFoiMrR8\nabXqZ2Pq2lBLN88MoHxoDPkiypJmyWHIVUfneMdKkONxuoUC0OCiLOFUQoRO82Zkl6XsFhTr7nFR\nPjMoZyEJhNH6HsVAzFykmUIgV9rkrXdtrGYHXc+OEYsSdu\/k6FCdlfEOCaF0i7O99f6V7VYDKgyl\nYPCKuwoOZt5AgcdSCnArLtGxJGwQ1LpErDrFIC1CrK+PHZr\/z82ZXl+3qOja2A4PFpql7jlbATP8\nRzs0R5zrka2yHnNw1t022eaFeGR4wg\/Q0H05X6BsmrhPGwEI2hvHxzt23XsxAlURoQmJoQvpxG7E\nGpNcyhFCQd15RrHHgcCrwypAXPOa+7YEQAnBBUcBYi7f2aLX\/aw6Xc8Ob9WP2vrn1U1bcgzY6R6O\n4Jsyp9yI6OLE1jg3h7ElWYJLYO3FC6y4g6lDcXuuP+F1ROSbuQ\/o9R1FKP0TUnZBIe92xvFI6aqC\n+UPjwreETDF\/sigl4DPxr9xMTRcLU4Q9H8hmnb7mwpcKHY3Y9rCasqFbypBLcBh76Q2GCfnyq734\nKllg7AlnfEWza2JDgULg4afnoWLGZJwrR\/TxbWh3V2tMSvPPaiyeVTJT4Np7dSpARhUI0stbz14h\n1TTqMl8+P3ZdvlWHQlHXtXeHFA6HnmlSdVsZrpMhtR8TrBt6NRb\/W6djLNvFKphO5WBOI5gIMpte\n4Q15FMQj+5AEWx\/+QH2oFNK14SxjUpXclp9d\/T+HKoTn75dLolqELREPmbITOMtmHwJ7tOxXd6RB\nvvtS45WGrtf32YKEKja9o\/M\/MyKDdT4U9c4auzbFHgiFR2f90tXBOvC8Xn0jElZRmErLgV4cGnoP\nmzry71nGxxmQcVmc6dpavUpw3dFrZDARf3nI6kvvNmKOStvInvv3tJn\/fiC4WhRdtPE14p9imcFu\nLL56uT1w4QX8OoMehdX7wvP8dn2y\/sB8EKj7DMSJkCSryZq1K43GQ5UI7sXwcvqhzEzz6+ChII19\nfEeF6h3hK60MU7OB9scFjVPxZ+qnj1DJ8ARQzTObeWok1MRTQmC2N+jX0BMBnGRW890kLPPo9PSJ\nwht2zGNE+XZgAXMxQVBfuCKxFGfW5Dbjd2Ksbgt6EgoX3tZYtomDafoG\/x6I\n"}





    import urllib.parse
    message = cbc_decrypt(data['message'])
    print(message)
    bytes='%7B%22identify%22%3A%22475571%22%2C%22index%22%3A%22game_analysis-423vljh2v6e4eh9j%22%2C%22properties%22%3A%7B%22identifyType%22%3A%22user%22%2C%22device%22%3A%22Android%22%2C%22channel%22%3A%22TapTap%22%2C%22width%22%3A2499%2C%22height%22%3A1200%2C%22device_name%22%3A%22HUAWEI%20ELS-AN00%22%2C%22system_version%22%3A%22Android%2010%22%2C%22provider%22%3A%22%E4%B8%AD%E5%9B%BD%E8%81%94%E9%80%9A%22%2C%22network%22%3A%22-2%22%2C%22ver%22%3A%22ver%3A1.39.4%22%2C%22ga_ver%22%3A%222.1.6%22%2C%22device_id2%22%3A%22e4962bd0-33aa-4202-8c10-5a90b99154a6%22%2C%22device_id3%22%3A%22bf8cad83ebac47b9%22%2C%22install_uuid%22%3A%2299507326-c265-43ca-b2fb-7127ed47eb0f%22%2C%22persist_uuid%22%3A%2299507326-c265-43ca-b2fb-7127ed47eb0f%22%2C%22mobile_identify%22%3A%22bf8cad83ebac47b9%22%7D%2C%22module%22%3A%22GameAnalysis%22%7D'
    print(urllib.parse.unquote(bytes))
