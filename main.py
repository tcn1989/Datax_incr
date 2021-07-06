import pymysql
import os


def get(table_name_input):
    conn = pymysql.connect(
        host='47.98.245.217',
        port=3306,
        # 数据库登录账户
        user='root',
        # 数据库登录密码
        passwd='TmsTest!1234',
        # 要连接的数据库
        db=''
    )
    cur = conn.cursor()
    DB = cur.execute(
        """select concat("{'name':'",COLUMN_NAME,"',","'type':'STRING'},")
    from information_schema.columns
    where TABLE_SCHEMA ='tms' and table_name=""" + "'" + table_name_input + "'"
    )
    DBS = cur.fetchmany(DB)
    DB2 = cur.execute("""select
        concat('REPLACE(REPLACE(',
        COLUMN_NAME,
        ", CHAR(10), ''), CHAR(13), '') as ",
        COLUMN_NAME,
        ','

        )

        from information_schema.columns 
    where TABLE_SCHEMA ='tms' and table_name=""" + "'" + table_name_input + "'")

    DBS2 = cur.fetchmany(DB2)

    fd = os.open('ods_tms_' + table_name_input + '_incr' + ".json", os.O_RDWR | os.O_CREAT)
    ret = os.write(fd, """{
      "job":{
        "content":[
          {
            "reader":{
              "name":"mysqlreader",
              "parameter":{
                "connection":[
                  {
                    "jdbcUrl":[
                      "jdbc:mysql://47.98.245.217"
                    ],
                    "querySql":[
                        "select """.encode())
    word1 = []
    for s in DBS2:
        o = str('\n' + "      " + s[0])
        word1.append(o)
    word1_result = ''.join(word1)

    word1_strip = word1_result.rstrip(',')

    ret = os.write(fd, word1_strip.encode())

    ret = os.write(fd, ("\n\t\t from tms." + table_name_input + """ where modify_time > date_sub(now(), interval 1 hour);" """
                                                                """                ]
                                                                }
                                                              ],
                                                              "password":"TmsTest!1234",
                                                              "username":"root"
                                                            }
                                                          },
                                                          "writer":{
                                                            "name":"hdfswriter",
                                                            "parameter":{
                                                              "column":[ """).encode())
    word2 = []
    for s1 in DBS:
        o1 = str('\n' + "      " + s1[0])
        word2.append(o1)
    word2_result = ''.join(word2)

    word2_strip = word2_result.rstrip(',')

    ret = os.write(fd, word2_strip.encode())

    ret = os.write(fd, ("""\n           ],
                "compress":"bzip2",
                "defaultFS":"hdfs://172.16.182.178:8020",
                "fieldDelimiter":"\1",
                "fileName":"ods_tms_""" + table_name_input + """_incr",
                "fileType":"text",
                "path":"/data/datax/tms_ods_incr",
                "writeMode":"append"
              }
            }
          }
        ],
        "setting":{
          "errorLimit":{
            "percentage":0.02,
            "record":0
          },
          "speed":{
            "channel":1
          }
        }
      }
    }""").encode())
