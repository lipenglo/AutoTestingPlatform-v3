import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# db here
from SystemParams.models import SystemParams as db_SystemParams

# Create reference here.
from ClassData.Logger import Logging
from ClassData.Common import Common

cls_Logging = Logging()
cls_Common = Common()


class Email(object):
    def send_email(self,receiver, header, msgs):  # 邮件接收者对象，信息头,信息
        """
        :param receiver: # 接收者 ['1','2'] 数据为str
        :param header:标题
        :param msgs:
        :return:
        """
        # region EmailUser
        obj_db_SystemParams = db_SystemParams.objects.filter(keyName='EmailUser')
        if obj_db_SystemParams.exists():
            sender = obj_db_SystemParams[0].value
        else:
            sender = ''
            errorMsg = f"系统参数:EmailUser,缺失"
            cls_Logging.print_log('error', 'send_email', errorMsg)
            cls_Logging.record_error_info('API', 'ClassData', 'send_email', errorMsg)
        # endregion
        # region password
        obj_db_SystemParams = db_SystemParams.objects.filter(keyName='EmailPwd')
        if obj_db_SystemParams.exists():
            password = obj_db_SystemParams[0].value
        else:
            password = ''
            errorMsg = f"系统参数:EmailPwd,缺失"
            cls_Logging.print_log('error', 'send_email', errorMsg)
            cls_Logging.record_error_info('API', 'ClassData', 'send_email', errorMsg)
        # endregion
        # region SmtpServer
        obj_db_SystemParams = db_SystemParams.objects.filter(keyName='SmtpServer')
        if obj_db_SystemParams.exists():
            smtpserver = obj_db_SystemParams[0].value
        else:
            smtpserver = ''
            errorMsg = f"系统参数:SmtpServer,缺失"
            cls_Logging.print_log('error', 'send_email', errorMsg)
            cls_Logging.record_error_info('API', 'ClassData', 'send_email', errorMsg)
        # endregion
        # smtpserver = "smtp.163.com"
        # sender = "lipenglo@163.com"
        # password = "li123123"
        receiver = receiver  # 接收者

        msg = MIMEText(msgs, "html", "utf-8")
        msgRoot = MIMEMultipart('related')
        msgRoot['Subject'] = Header(header, 'utf-8')  # 邮件标题
        msgRoot['From'] = sender  # 发送者
        msgRoot['To'] = ','.join(receiver)  # 接收者
        msgRoot.attach(msg)
        # msgRoot.attach(att)
        try:
            smtp = smtplib.SMTP_SSL(smtpserver)  # 这里要用这种方式 不然他们centos服务器不能发送邮件
            # smtp.connect(smtpserver)
            smtp.login(sender, password)
            smtp.sendmail(sender, receiver, msgRoot.as_string())
            smtp.quit()

            cls_Logging.print_log('info', 'send_email', '发送完成')
            # return True
        except BaseException as e:
            errorMsg = f'发送失败:{e}'
            cls_Logging.print_log('error', 'send_email', errorMsg)
            cls_Logging.record_error_info('API', 'ClassData', 'send_email', errorMsg)

    def email_report(self,reportData):
        reportType = reportData['reportType']
        if reportType == 'TASK':
            bodyTitle = "定时任务"
        elif reportType == 'BATCH':
            bodyTitle = "批量任务"
        else:
            bodyTitle = None

        passTotal = int(reportData['passTotal'])
        failTotal = int(reportData['failTotal'])
        errorTotal = int(reportData['errorTotal'])
        allTotal = passTotal + failTotal + errorTotal

        header = f"【{bodyTitle}】-测试报告:{reportData['reportName']}---{reportData['reportStatus']}"
        body = f"<li>耗时时长:{reportData['runningTime']} ms&nbsp;&nbsp;&nbsp;" \
               f"通过率:{reportData['passRate']}%</li>"
        body += f"<li>总计数量:{int(allTotal)}&nbsp;&nbsp;&nbsp;" \
                f"成功:{passTotal}&nbsp;&nbsp;&nbsp;" \
                f"失败:{failTotal}&nbsp;&nbsp;&nbsp;" \
                f"错误:{errorTotal}</li>"
        body += f"<li>测试结果:{reportData['reportStatus']}</li>"
        return header, body