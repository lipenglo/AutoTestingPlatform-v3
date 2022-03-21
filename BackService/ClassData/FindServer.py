from ClassData.Logger import Logging as cls_Logging
from ClassData.Common import Common

import psutil

cls_Common = Common()


class FindLocalServer(cls_Logging):
    def get_cpu_state(self):
        try:
            cpu = psutil.cpu_percent(interval=2)
        except BaseException as e:
            cls_Logging.print_log(self, 'error', 'get_cpu_target', e)
            return 0
        else:
            return cpu

    def get_mem_state(self):
        try:
            mem = psutil.virtual_memory()[2]
        except BaseException as e:
            cls_Logging.print_log(self, 'error', 'get_mem_target', e)
            return 0
        else:
            return mem

    def get_celery_state(self):
        celeryState = False
        debug_worker = []  # 在Debug模式下有点奇葩所以要计数下
        try:
            perform = cls_Common.run_command("ps -ef |grep worker", False)
            for i in perform:
                if "celery -A BackService worker -l info" in i:
                    celeryState = True
                    break
                elif "celery worker -A BackService -E --loglevel=INFO" in i:  # Debug模式
                    debug_worker.append(i)
                    if len(debug_worker) >= 3:
                        celeryState = True
                        break
        except BaseException as e:
            cls_Logging.print_log(self, 'error', 'get_celery_state', e)
            return celeryState
        else:
            return celeryState

    def get_celery_beat_state(self):
        celeryState = False
        try:
            perform = cls_Common.run_command("ps -ef |grep beat", False)
            for i in perform:
                if "celery -A BackService beat -l info" in i:
                    celeryState = True
                    break
                elif "celery beat -A BackService --loglevel=INFO" in i:  # Debug模式
                    celeryState = True
                    break
        except BaseException as e:
            cls_Logging.print_log(self, 'error', 'get_celery_beat_state', e)
            return celeryState
        else:
            return celeryState
