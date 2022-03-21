from django.db import models


# Create your models here.
class TempExtractData(models.Model):  # 保存临时提出并转换后的数据
    onlyCode = models.CharField('唯一随机ID', max_length=100, null=True)
    keys = models.CharField('key', max_length=100, null=True)
    values = models.TextField('value', null=True)
    valueType = models.CharField('值类型', max_length=50, null=True)
    createTime = models.DateTimeField('创建时间', auto_now=True)


class ApiTestReport(models.Model):  # 一级主报告列表
    pid = models.ForeignKey("ProjectManagement.ProManagement", to_field='id', on_delete=models.CASCADE)
    reportName = models.CharField("报告名称", max_length=50, null=False)
    reportType = models.CharField("报告类型(API:单接口,CASE:测试用例,TASK:定时任务,BATCH:批量任务)", max_length=10, null=False)
    taskId = models.CharField("ApiId/CaseId/TaskId/BatchId,根据任务类型来取", max_length=10, null=False)
    apiTotal = models.IntegerField("统计总需要执行的接口数量", null=False)
    reportStatus = models.CharField("测试报告状态(Pass,Fail,Error)", max_length=10, null=False)
    runningTime = models.FloatField("运行总时间", null=True)
    createTime = models.DateTimeField('创建时间', auto_now=True)
    updateTime = models.DateTimeField('修改时间', auto_now=True)
    uid = models.ForeignKey(to='login.UserTable', to_field='id', on_delete=models.CASCADE)  # 用户Id
    is_del = models.IntegerField("是否删除(1:删除,0:不删除)", null=False)


class ApiReportTaskItem(models.Model):  # 二级批量任务列表
    testReport = models.ForeignKey("ApiTestReport", to_field='id', on_delete=models.CASCADE)  # 主报告ID
    task = models.ForeignKey("Api_TimingTask.ApiTimingTask", to_field='id', on_delete=models.CASCADE)
    taskName = models.CharField("定时任务名称", max_length=50, null=True)
    runningTime = models.FloatField("运行总时间", null=True)
    successTotal = models.IntegerField("成功数", null=False)
    failTotal = models.IntegerField("失败数", null=False)
    errorTotal = models.IntegerField("错误数", null=False)
    updateTime = models.DateTimeField('修改时间', auto_now=True)
    is_del = models.IntegerField("是否删除(1:删除,0:不删除)", null=False)


class ApiReportItem(models.Model):  # 二级报告列表
    testReport = models.ForeignKey("ApiTestReport", to_field='id', on_delete=models.CASCADE)  # 主报告ID
    apiId = models.ForeignKey("Api_IntMaintenance.ApiBaseData", to_field='id', on_delete=models.CASCADE)  # 接口ID
    apiName = models.CharField("接口名称", max_length=50, null=True)
    case_id = models.IntegerField("单接口没有此ID/Case,Task,Batch类型时这里显示CaseId", null=True)  # 这个接口出自哪个用例的
    batchItem_id = models.IntegerField("Batch类型时才有此ID", null=True)
    runningTime = models.FloatField("运行总时间", null=True)
    successTotal = models.IntegerField("成功数", null=False)
    failTotal = models.IntegerField("失败数", null=False)
    errorTotal = models.IntegerField("错误数", null=False)
    updateTime = models.DateTimeField('修改时间', auto_now=True)
    is_del = models.IntegerField("是否删除(1:删除,0:不删除)", null=False)


class ApiReport(models.Model):  # 三级用例报告
    reportItem = models.ForeignKey("ApiReportItem", to_field='id', on_delete=models.CASCADE)  # 二级报告表ID
    requestUrl = models.CharField('请求地址', max_length=100, null=False)
    requestType = models.CharField("请求类型(GET/POST)", max_length=50, null=False)
    requestHeaders = models.TextField('请求头部', null=True)
    requestData = models.TextField('请求数据', null=True)
    reportStatus = models.CharField("测试报告状态(Pass,Fail,Error)", max_length=10, null=False)

    statusCode = models.IntegerField("返回代码", null=True)
    responseHeaders = models.TextField('返回头部', null=True)
    responseInfo = models.TextField('返回信息', null=True)
    requestExtract = models.TextField('请求提取信息', null=True)
    requestValidate = models.TextField('请求断言信息', null=True)
    responseValidate = models.TextField('返回断言信息', null=True)
    preOperationInfo = models.TextField('前置操作返回信息', null=True)
    rearOperationInfo = models.TextField('后置操作返回值', null=True)
    errorInfo = models.TextField('错误信息', null=True)
    runningTime = models.CharField("运行总时间", max_length=50, null=True)
    updateTime = models.DateTimeField('修改时间', auto_now=True)
    is_del = models.IntegerField("是否删除(1:删除,0:不删除)", null=False)


class WarningInfo(models.Model):  # 用于测试报告显示
    testReport = models.ForeignKey("ApiTestReport", to_field='id', on_delete=models.CASCADE)  # 主报告ID
    triggerType = models.CharField("触发类型(Warning,Error)", max_length=20, null=False)
    taskId = models.CharField("ApiId/CaseId/TaskId/BatchId,根据任务类型来取", max_length=10, null=False)
    taskName = models.CharField("接口/用例/定时任务的名称", max_length=50, null=False)
    info = models.TextField('信息', null=True)
    updateTime = models.DateTimeField('修改时间', auto_now=True)
    uid = models.ForeignKey(to='login.UserTable', to_field='id', on_delete=models.CASCADE)  # 用户Id


class ApiQueue(models.Model):  # 队列信息
    pid = models.ForeignKey("ProjectManagement.ProManagement", to_field='id', on_delete=models.CASCADE)
    page_id = models.IntegerField("所属页面", null=True)
    fun_id = models.IntegerField("所属功能", null=True)
    taskType = models.CharField('任务类型(API:单接口,Case,Task:定时任务,batch:批量任务)', max_length=50, null=False)
    taskId = models.IntegerField("任务ID,apiId,CaseId,TaskId,BatchId", null=False)
    testReport = models.ForeignKey("ApiTestReport", to_field='id', on_delete=models.CASCADE)  # 主报告id
    queueStatus = models.IntegerField("队列执行状态(0:未开始,1:执行中,2:已结束)", null=False)
    updateTime = models.DateTimeField('修改时间', auto_now=True)
    uid = models.ForeignKey(to='login.UserTable', to_field='id', on_delete=models.CASCADE)  # 用户Id
