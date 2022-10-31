import pymysql, csv, json
from PyQt5.QtWidgets import *
import sys
import xml.etree.ElementTree as ET

class DB_Utils:

    def queryExecutor(self, db, sql, params):
        conn = pymysql.connect(host='localhost', user='guest', password='bemyguest', db=db, charset='utf8')

        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:     # dictionary based cursor
                cursor.execute(sql, params)
                rows = cursor.fetchall()
                return rows
        except Exception as e:
            print(e)
            print(type(e))
        finally:
            conn.close()

class DB_Queries:

    def UserName(self):
        sql = "SELECT DISTINCT name FROM customers"
        params = ()

        util = DB_Utils()
        rows = util.queryExecutor(db="classicmodels", sql=sql, params=params)
        return rows

    def Country(self):
        sql = "SELECT DISTINCT country FROM customers"
        params = ()

        util = DB_Utils()
        rows = util.queryExecutor(db="classicmodels", sql=sql, params=params)
        return rows

    def City(self,country):
        if not country:
            sql = "SELECT DISTINCT city FROM customers"
            params = ()
            util = DB_Utils()
            rows = util.queryExecutor(db="classicmodels", sql=sql, params=params)
            return rows
        elif country == "ALL":
            sql = "SELECT DISTINCT city FROM customers"
            params = ()
            util = DB_Utils()
            rows = util.queryExecutor(db="classicmodels", sql=sql, params=params)
            return rows
        elif country != "ALL":
            sql = "select distinct city from customers where country = %s order by city"
            params = (country)
            util = DB_Utils()
            rows = util.queryExecutor(db="classicmodels", sql=sql, params=params)
            return rows


    def searchbykey(self, name,country,city):
        if name == 'ALL' and country =='ALL' and city == 'ALL':
            sql = "SELECT orderNo, orderDate, requiredDate, shippedDate, status, name as customer, comments FROM (SELECT orderNo, orderDate, requiredDate, shippedDate, status, name, comments from orders LEFT JOIN CUSTOMERS ON ORDERS.CUSTOMERID = CUSTOMERS.CUSTOMERID) AS TEMP"
            params = ()
        if name == 'ALL' and country != 'ALL' and city != 'ALL':
            sql = "SELECT orderNo, orderDate, requiredDate, shippedDate, status, name as customer, comments FROM (SELECT orderNo, orderDate, requiredDate, shippedDate, status, name, comments, country, city from orders LEFT JOIN CUSTOMERS ON ORDERS.CUSTOMERID = CUSTOMERS.CUSTOMERID) AS TEMP WHERE country = %s and city = %s"
            params = (country,city)
        if name != 'ALL' and country =='ALL' and city == 'ALL':
            sql = "SELECT orderNo, orderDate, requiredDate, shippedDate, status, name as customer, comments FROM (SELECT orderNo, orderDate, requiredDate, shippedDate, status, name, comments, country, city from orders LEFT JOIN CUSTOMERS ON ORDERS.CUSTOMERID = CUSTOMERS.CUSTOMERID) AS TEMP WHERE name = %s"
            params = (name)
        if name == 'ALL' and country !='ALL' and city == 'ALL':
            sql = "SELECT orderNo, orderDate, requiredDate, shippedDate, status, name as customer, comments FROM (SELECT orderNo, orderDate, requiredDate, shippedDate, status, name, comments, country, city from orders LEFT JOIN CUSTOMERS ON ORDERS.CUSTOMERID = CUSTOMERS.CUSTOMERID) AS TEMP WHERE country = %s"
            params = (country)
        if name == 'ALL' and country =='ALL' and city != 'ALL':
            sql = "SELECT orderNo, orderDate, requiredDate, shippedDate, status, name as customer, comments FROM (SELECT orderNo, orderDate, requiredDate, shippedDate, status, name, comments, country, city from orders LEFT JOIN CUSTOMERS ON ORDERS.CUSTOMERID = CUSTOMERS.CUSTOMERID) AS TEMP WHERE city = %s"
            params = (city)


        util = DB_Utils()
        rows = util.queryExecutor(db="classicmodels", sql=sql, params=params)
        return rows

    def searchbyOrderNum(self,orderNum):
        sql =" SELECT B.orderLineNo,B.productCode, C.NAME as productName, B.quantity, convert(B.priceEach,char) as priceEach, convert(B.quantity*round(B.priceEach,1),char) AS '상품주문액' FROM ORDERS AS A LEFT JOIN ORDERDETAILS AS B ON A.ORDERNO = B.ORDERNO LEFT JOIN PRODUCTS C ON B.PRODUCTCODE = C.PRODUCTCODE WHERE A.ORDERNO = %s"
        params = (orderNum)

        util = DB_Utils()
        rows = util.queryExecutor(db="classicmodels", sql=sql, params=params)
        return rows
#########################################

class SecondWindow(QDialog,QWidget):
    def __init__(self,order_num):
        super().__init__()
        self.setupUI(order_num)
        self.show()

    def setupUI(self,order_num):
        self.setWindowTitle("Second DB")
        self.setGeometry(300,300,800,600)

        self.label_order_detail = QLabel("주문 상세 내역", self)
        self.label_order_number = QLabel("주문번호: ",self)
        self.label_order_number_print = QLabel()
        self.label_order_number_print.setText(order_num)
        self.label_order_count = QLabel("상품개수: ",self)
        self.label_order_count_print = QLabel()
        self.label_order_price = QLabel("주문액: ",self)
        self.label_order_price_print = QLabel()
        self.savebutton = QPushButton("저장")
        self.label_print = QLabel("파일 출력",self)

        self.tableWidget = QTableWidget(self)
        self.tableWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        query = DB_Queries()
        results = query.searchbyOrderNum(order_num)
        ############### orderNo 로 정렬 ##############
        sorted_results = sorted(results, key=lambda x: x['orderLineNo'])
        self.savebutton.clicked.connect(lambda: self.save_button(order_num,sorted_results))
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(len(results))
        self.tableWidget.setColumnCount(len(results[0]))
        columnNames = list(results[0].keys())
        self.tableWidget.setHorizontalHeaderLabels(columnNames)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        total_price = 0
        for rowIDX, result in enumerate(sorted_results):
            total_price += float(result['상품주문액'])
            for columnIDX, (k, v) in enumerate(result.items()):
                if v == None:
                    continue
                else:
                    item = QTableWidgetItem(str(v))
                self.tableWidget.setItem(rowIDX, columnIDX, item)
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()
        self.label_order_count_print.setText("%s" % (len(sorted_results)))
        self.label_order_price_print.setText("%s" % round(total_price,2))

        ############ csv, json, xml 라디오버튼 ############
        self.radioBtn_csv = QRadioButton("CSV", self)
        self.radioBtn_csv.setChecked(True)
        self.radioBtn_json = QRadioButton("JSON", self)
        self.radioBtn_xml = QRadioButton("XML", self)

        ############레이아웃 설정##########################
        box1 = QHBoxLayout()
        box1.addWidget(self.label_order_detail)

        box2 = QHBoxLayout()
        box2.addWidget(self.label_order_number)
        box2.addWidget(self.label_order_number_print)
        box2.addWidget(self.label_order_count)
        box2.addWidget(self.label_order_count_print)
        box2.addWidget(self.label_order_price)
        box2.addWidget(self.label_order_price_print)

        box3 = QHBoxLayout()
        box3.addWidget(self.radioBtn_csv)
        box3.addWidget(self.radioBtn_json)
        box3.addWidget(self.radioBtn_xml)

        box4 = QHBoxLayout()
        box4.addWidget(self.savebutton)

        Vbox = QVBoxLayout()
        Vbox.addLayout(box1)
        Vbox.addLayout(box2)
        Vbox.addWidget(self.tableWidget)
        Vbox.addWidget(self.label_print)
        Vbox.addLayout(box3)
        Vbox.addLayout(box4)

        self.setLayout(Vbox)

    def readDB_writeCSV(self,order_num,results):
        with open('{}.csv'.format(order_num), 'w', encoding='utf-8', newline='') as f:
            wr = csv.writer(f)
            columnNames = list(results[0].keys())
            wr.writerow(columnNames)
            for row in results:
                orderlist = list(row.values())
                wr.writerow(orderlist)

    def readDB_writeJSON(self,order_num,results):
        newDict = dict(orderDetails = results)
        with open('{}.json'.format(order_num), 'w', encoding='utf-8') as f:
            json.dump(newDict, f, indent=4, ensure_ascii=False)

    def readDB_writeXML(self,order_num,results):
        newDict = dict(orderDetails=results)

        tableName = list(newDict.keys())[0]
        tableRows = list(newDict.values())[0]

        rootElement = ET.Element('TABLE')
        rootElement.attrib['name'] = tableName

        for row in tableRows:
            rowElement = ET.Element('ROW')
            rootElement.append(rowElement)

            for columnName in list(row.keys()):
                if row[columnName] == None:
                    rowElement.attrib[columnName] = ''
                elif type(row[columnName]) == int:
                    rowElement.attrib[columnName] = str(row[columnName])
                else:
                    rowElement.attrib[columnName] = row[columnName]

        ET.ElementTree(rootElement).write('{}.xml'.format(order_num), encoding='utf-8', xml_declaration=True)

    def save_button(self,order_num,results):
        if self.radioBtn_csv.isChecked():
            self.readDB_writeCSV(order_num,results)
        elif self.radioBtn_json.isChecked():
            self.readDB_writeJSON(order_num,results)
        elif self.radioBtn_xml.isChecked():
            self.readDB_writeXML(order_num,results)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        global query
        query = DB_Queries()
        self.setWindowTitle("Classic Model DB")
        self.setGeometry(30,30,1000,600)
#############################################################################################
        rows_username = query.UserName()
        self.label_main = QLabel("주문 검색", self)
        self.label_user = QLabel("고객:", self)
        columnName_user = list(rows_username[0].keys())[0]
        all = ['ALL']
        items_user = [row[columnName_user] for row in rows_username]
        items_user.sort()
        items_user = all + items_user

        self.comboBox_user = QComboBox(self)
        self.comboBox_user.addItems(items_user)
        self.comboBox_user.setCurrentIndex(0)
        self.UserValue = self.comboBox_user.currentText()
        self.comboBox_user.activated.connect(self.comboBox_Activated_User)

#############################################################################################
        rows_country = query.Country()
        self.label_country = QLabel("국가:", self)
        columnName_country = list(rows_country[0].keys())[0]
        all = ['ALL']
        items_country = [row[columnName_country] for row in rows_country]
        items_country.sort()
        items_country = all + items_country

        self.comboBox_country = QComboBox(self)
        self.comboBox_country.addItems(items_country)
        self.comboBox_country.setCurrentIndex(0)
        self.CountryValue = self.comboBox_country.currentText()
        self.comboBox_country.activated.connect(self.comboBox_Activated_Country)


#############################################################################################
        rows_city = query.City(self.CountryValue)
        self.label_city = QLabel("도시:", self)
        columnName_city = list(rows_city[0].keys())[0]
        all = ['ALL']
        items_city = [row[columnName_city] for row in rows_city]
        items_city.sort()
        items_city = all + items_city

        self.comboBox_city = QComboBox(self)
        self.comboBox_city.addItems(items_city)
        self.comboBox_city.setCurrentIndex(0)
        self.CityValue = self.comboBox_city.currentText()
        self.comboBox_city.activated.connect(self.comboBox_Activated_City)


#############################################################################################
        self.Search_pushButton = QPushButton("검색", self)
        self.Search_pushButton.clicked.connect(self.Search_pushButton_Clicked)

        self.label_count = QLabel("검색된 주문의 개수:", self)
        self.label_number = QLabel(self)

        self.Reset_pushButton = QPushButton("초기화", self)
        self.Reset_pushButton.clicked.connect(self.Reset_pushButton_Clicked)


        # 테이블위젯 설정
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)

        # 테이블 클릭시 이벤트
        self.tableWidget.cellClicked.connect(self.cellclicked_event)

        up_box = QHBoxLayout()
        up_box.addWidget(self.label_main)

        self.comboBox_user.setFixedWidth(150)
        self.comboBox_country.setFixedWidth(150)
        self.comboBox_city.setFixedWidth(150)

        up_box_1 = QHBoxLayout()
        up_box_1.addWidget(self.label_user)
        up_box_1.addWidget(self.comboBox_user)
        up_box_1.addStretch(1)
        up_box_1.addWidget(self.label_country)
        up_box_1.addWidget(self.comboBox_country)
        up_box_1.addStretch(1)
        up_box_1.addWidget(self.label_city)
        up_box_1.addWidget(self.comboBox_city)
        up_box_1.addStretch(2)
        up_box_1.addWidget(self.Search_pushButton)

        up_box_2 = QHBoxLayout()
        up_box_2.addWidget(self.label_count)
        up_box_2.addWidget(self.label_number)
        up_box_2.addStretch(2)
        up_box_2.addWidget(self.Reset_pushButton)

        up_box_3 = QHBoxLayout()
        up_box_3.addWidget(self.tableWidget)

        box = QVBoxLayout()
        box.addLayout(up_box)
        box.addLayout(up_box_1)
        box.addLayout(up_box_2)
        box.addLayout(up_box_3)


        self.setLayout(box)

    def comboBox_Activated_User(self):
        self.UserValue = self.comboBox_user.currentText()

    def comboBox_Activated_Country(self):
        self.CountryValue = self.comboBox_country.currentText()
        all = ["ALL"]
        rows_city = query.City(self.CountryValue)
        columnName_city = list(rows_city[0].keys())[0]
        items_city = [row[columnName_city] for row in rows_city]
        items_city.sort()
        if self.CountryValue == "ALL":
            items_city = all + items_city
        self.comboBox_city.clear()
        self.comboBox_city.addItems(items_city)
        self.CityValue = self.comboBox_city.currentText()
        self.comboBox_city.activated.connect(self.comboBox_Activated_City)

    def comboBox_Activated_City(self):
        self.CityValue = self.comboBox_city.currentText()

    def Search_pushButton_Clicked(self):
        query = DB_Queries()
        results = query.searchbykey(self.UserValue,self.CountryValue,self.CityValue)
        if results:
            self.tableWidget.clearContents()
            self.tableWidget.setRowCount(len(results))
            self.tableWidget.setColumnCount(len(results[0]))
            columnNames = list(results[0].keys())
            self.tableWidget.setHorizontalHeaderLabels(columnNames)
            self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
            ############### orderNo 로 정렬 ##############
            sorted_results = sorted(results,key = lambda x : x['orderNo'])
            for rowIDX, result in enumerate(sorted_results):
                for columnIDX, (k, v) in enumerate(result.items()):
                    if v == None:
                        continue
                    else:
                        item = QTableWidgetItem(str(v))

                    self.tableWidget.setItem(rowIDX, columnIDX, item)

            self.tableWidget.resizeColumnsToContents()
            self.tableWidget.resizeRowsToContents()
            self.label_number.setText("%s" % (len(results)))

        else:
            self.tableWidget.clearContents()
            self.tableWidget.setRowCount(0)
            self.tableWidget.setColumnCount(0)
            self.label_number.setText('0')

    def Reset_pushButton_Clicked(self):
        self.tableWidget.clear()
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(0)
        self.label_number.setText('0')

    def cellclicked_event(self):
        row = self.tableWidget.currentIndex().row()
        order_num = self.tableWidget.item(row,0)
        self.hide()
        SW = SecondWindow(order_num.text())
        SW.exec()
        self.show()



#########################################

def main():
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    mainWindow.Search_pushButton_Clicked()
    sys.exit(app.exec_())

main()