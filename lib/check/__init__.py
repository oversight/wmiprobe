# import sys
# sys.path.append('../oswmicprobe')
# from core.wmicCheckFactory import constructors
# CHECKS = {
#     k: v() for k, v in constructors.items()
# }

class Base:
    interval = 300
    namespace = 'root/cimv2'
    required_services = []


class CheckTest(Base):
    interval = 1

    async def get_data(*args):
        return {'type': {'i0': {'name': 'i0', 'metric': 1}}}


CHECKS = {
    'check': CheckTest
}
