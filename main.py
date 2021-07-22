import datetime

from lib.bitflyer import BitFlyer, BitFlyerError
import datetime

def main():
    bitflyer = BitFlyer()
    from_date = datetime.date(year=2021, month=7, day=21)
    chats = bitflyer.get_chats(from_date=from_date)
    print("end")
if __name__ == '__main__':
    main()
