#-------------------------------------------------------------------------------
# Name:        printers
# Purpose:      Сканирование имеющихся принтеров с целью определения
#                наличия тонера
#
# Author:      pavel
#
# Created:     29.11.2023
# Copyright:   (c) pavel 2023
# Licence:     MIT
#-------------------------------------------------------------------------------

from pysnmp.entity.rfc3413.oneliner import cmdgen
#from pysnmp.hlapi import *
IOD_Counter = (1,3,6,1,2,1,43,10,2,1,4,1)
IOD_Current = (1,3,6,1,2,1,43,11,1,1,9,1)
IOD_Current_ = ['43.11.1.1.9.1.1', '43.11.1.1.9.1.2', '43.11.1.1.9.1.3', '43.11.1.1.9.1.4', '43.11.1.1.9.1.5']

IOD_Full    = (1,3,6,1,2,1,43,11,1,1,8,1)
IOD_Full_   = ['43.11.1.1.8.1.1', '43.11.1.1.8.1.2', '43.11.1.1.8.1.3', '43.11.1.1.8.1.4', '43.11.1.1.8.1.5']


IOD_Full2   = (1,3,6,1,2,1,43,11,1,1,8,1,1)
IOD_Full2_  = '43.11.1.1.8.1.1'


class printer_:
    name = 'noname'
    ip = 'localhost'
    def get_count(self):
        errorIndication, errorStatus, errorIndex, \
        varBindTable = cmdgen.CommandGenerator().nextCmd(
                        cmdgen.CommunityData('public', mpModel=0),
                        cmdgen.UdpTransportTarget((self.ip, 161)),
                        #(1,3,6,1,2,1,1)
                        IOD_Counter
                        )
        #print(varBindTable)
        for varBindTableRow in varBindTable:
                for name, val in varBindTableRow:
                    #print(name.prettyPrint())
                    #print(val.prettyPrint())
                    return val.prettyPrint()

    def get_cartridge_status(self, catrid_N = 0):
        full = 0
        current = 0
        errorIndication, errorStatus, errorIndex, \
        varBindTable = cmdgen.CommandGenerator().nextCmd(
                        cmdgen.CommunityData('public', mpModel=0),
                        cmdgen.UdpTransportTarget((self.ip, 161)),
                        IOD_Full
                        )
        #print(varBindTable)
        for varBindTableRow in varBindTable:
                for name, val in varBindTableRow:
                    #print(name.prettyPrint())
                    #print(val.prettyPrint())
                    if IOD_Full_[catrid_N] in name.prettyPrint():
                        full = val.prettyPrint()

        errorIndication, errorStatus, errorIndex, \
        varBindTable = cmdgen.CommandGenerator().nextCmd(
                        cmdgen.CommunityData('public', mpModel=0),
                        cmdgen.UdpTransportTarget((self.ip, 161)),
                        IOD_Current
                        )
        #print(varBindTable)
        for varBindTableRow in varBindTable:
                for name, val in varBindTableRow:
                    #print(name.prettyPrint())
                    #print(val.prettyPrint())
                    if IOD_Current_[catrid_N] in name.prettyPrint():
                        current = val.prettyPrint()
                        #print(val.prettyPrint())
        return float(current) / float(full);

    def status(self):
        print("Принтер ", self.name, " по адресу ", self.ip)
        print("Катридж заполнен: ", self.get_cartridge_status())
        print("Всего распечатано страниц: ", self.get_count())


class printer_color(printer_):

    def status(self):
        print("Принтер ", self.name, " по адресу ", self.ip)
        print("Катридж 1 заполнен: ", self.get_cartridge_status(0))
        print("Катридж 2 заполнен: ", self.get_cartridge_status(1))
        print("Катридж 3 заполнен: ", self.get_cartridge_status(2))
        print("Катридж 4 заполнен: ", self.get_cartridge_status(3))
        print("Катридж 5 заполнен: ", self.get_cartridge_status(4))
        print("Всего распечатано страниц: ", self.get_count())

class printer_BR(printer_):
    # look https://github.com/saper-2/BRN-Printer-sCounters-Info/blob/master/MFC-L2720DW.md
    IOD_brInfoMaintenance = (1,3,6,1,4,1,2435,2,3,9,4,2,1,5,5,8)
    IOD_brInfoMaintenance_ = '2435.2.3.9.4.2.1.5.5.8.0'
    def get_cartridge_status(self, catrid_N = 0):
        full = ''
        errorIndication, errorStatus, errorIndex, \
        varBindTable = cmdgen.CommandGenerator().nextCmd(
                        cmdgen.CommunityData('public', mpModel=0),
                        cmdgen.UdpTransportTarget((self.ip, 161)),
                        self.IOD_brInfoMaintenance
                        )
        #print(varBindTable)
        for varBindTableRow in varBindTable:
                for name, val in varBindTableRow:
                    #print(name.prettyPrint())
                    #print(val.prettyPrint())
                    if self.IOD_brInfoMaintenance_ in name.prettyPrint():
                        full = val.prettyPrint()
        if full != '':
            cartridge = full[80:86]
            cartridge_count = int(cartridge,16)
            return cartridge_count / 100

def main():
    printer_1 = printer_()
    printer_1.name = 'FS6530'
    printer_1.ip ='192.168.3.243'
    printer_1.status()

    print('')

    printer_2 = printer_()
    printer_2.name = 'MF4780w'
    printer_2.ip ='192.168.3.21'
    printer_2.status()
    #print (printer_2.get_count())

    print('')

    printer_3 = printer_color()
    printer_3.name = 'LaserJet500'
    printer_3.ip ='192.168.3.20'
    printer_3.status()
    # print (printer_3.get_count())

    print('')

    printer_4 = printer_BR()
    printer_4.name = 'L2720DW'
    printer_4.ip ='192.168.3.23'
    printer_4.status()

    print('')

    printer_5 = printer_()
    printer_5.name = 'MF4780w'
    printer_5.ip ='192.168.3.51'
    printer_5.status()
    pass

if __name__ == '__main__':
    main()
