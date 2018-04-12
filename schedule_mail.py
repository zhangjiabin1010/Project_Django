import schedule,time
import smtplib
from email.mime.text import MIMEText
import cx_Oracle
import datetime


def select_sql():
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    ntime = ("'" + yesterday.strftime('%Y-%m-%d 18:00:00') + "'")
    btime = ("'"+today.strftime('%Y-%m-%d 18:00:00')+"'")
    try:
    #链接数据库
        conn = cx_Oracle.connect('用户名/密码@ip:1521/服务')
        curs = conn.cursor()
        #慧择
        sql = "select nvl(sum(n_prm),0),count(1) from zyccard.t_ply_base where c_prod_no in ('0676', '0677', '0615')/*   and c_b2b_udr_mrk in ('H','2','0')*/and t_udr_date >= to_date({0}, 'yyyy-mm-dd hh24:mi:ss') and t_udr_date <= to_date({1},'yyyy-mm-dd hh24:mi:ss')".format(ntime,btime)
        # #未进核心
        sql1 = "select  nvl(sum(n_prm),0),count(1) from zyccard.t_ply_base where  /*c_prod_no not in ('0676', '0677', '0615') and*/c_b2b_udr_mrk in ('2','0','H') and t_udr_date >= to_date({0}, 'yyyy-mm-dd hh24:mi:ss') and t_udr_date <= to_date({1}, 'yyyy-mm-dd hh24:mi:ss')".format(ntime,btime)
        # #已进核心
        sql2 = "select  nvl(sum(n_prm),0),count(1) from t_ply_base where t_udr_date >= to_date({0}, 'yyyy-mm-dd hh24:mi:ss') and t_udr_date <= to_date({1}, 'yyyy-mm-dd hh24:mi:ss')/*and c_prod_no not  in ('0676', '0677', '0615') */and c_b2b_udr_mrk in ('9')".format(ntime,btime)

        #查询  慧择
        rr = curs.execute(sql)
        huize = curs.fetchone()
        # 查询 未进核心
        rr = curs.execute(sql1)
        weijinhexin = curs.fetchone()
        # 查询 已进核心
        rr = curs.execute(sql2)
        yijinhexin = curs.fetchone()
        curs.close()
        conn.close()
    except Exception as e:
        print(str(e))

    return huize, weijinhexin, yijinhexin



def send_mail():
    data = list(select_sql())
    huize = data[0]
    weijinhexin = data[1]
    yijinhexin = data[2]
    #以下三行是把 字符串类型的数字 转为 2位小数点的浮点型
    huize0 = float('%.2f' % huize[0])
    weijinhexin0 = float('%.2f' % weijinhexin[0])
    yijinhexin0 = float('%.2f' % yijinhexin[0])

    #总数量
    count = huize[1] + weijinhexin[1] + yijinhexin[1]
    #总价格
    price = float(huize0 + weijinhexin0 + yijinhexin0)
    price0 = ('%.2f' % price)



    #邮箱服务器地址,163邮箱为smtp.163.com'、qq邮箱为smtp.qq.com
    mail_host = 'smtp.163.com'
    #用户名
    mail_user = 'xxxxxxx'
    #密码(授权码口令)
    mail_pass = 'xxxxxx'
    #邮件发送方邮箱地址
    sender = 'xxxxxx@163.com'
    #邮件接受方邮箱地址,可群发。
    receivers = ['xxxxx@qq.com']

    #邮件内容
    message = MIMEText("""

                    <table color="CCCC33" width="500" border="1" cellspacing="0" cellpadding="5" text-align="center">
                            <tr style="text-align:center;color: red">
                                    <th>类别</th>
                                    <th>保费</th>
                                    <th>单量</th>
                            </tr>
                            <tr style="text-align:center;">
                                    <td>慧择总量</td>
                                    <td>%s</td>
                                    <td>%s</td>
                            </tr>
                            <tr style="text-align:center;">
                                    <td>电商总量</td>
                                    <td>%s</td>
                                    <td>%s</td>
                            </tr>
                            <tr style="text-align:center;">
                                    <td>未进核心</td>
                                    <td>%s</td>
                                    <td>%s</td>
                            </tr>
                            <tr style="text-align:center;">
                                    <td>已进核心</td>
                                    <td>%s</td>
                                    <td>%s</td>
                            </tr>
                    </table>""" % (huize0,huize[1],price0,count,weijinhexin0,weijinhexin[1],yijinhexin0,yijinhexin[1]),'HTML','utf-8')
    #邮件主题
    message['Subject'] = '数据库查询报表'

    message['From'] = sender
    message['To'] = receivers[0]

    #登录并发送邮件
    try:
        smtpObj = smtplib.SMTP()
        #连接到服务器，默认25端口
        smtpObj.connect(mail_host,25)
        smtpObj.login(mail_user,mail_pass)
        smtpObj.sendmail(
            sender,receivers,message.as_string())
        #退出
        smtpObj.quit()
        print('发送成功')
    except smtplib.SMTPException as e:
        print('发送邮件失败',e)


schedule.every(10).seconds.do(send_mail)
#定时发送邮件
# schedule.every().day.at("20:20").do(send_mail)

while True:
    schedule.run_pending() #执行任务


