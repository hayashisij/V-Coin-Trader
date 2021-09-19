from lib.public import PublicAPI
import datetime


def main():
    pub = PublicAPI()
    from_date = datetime.datetime(year=2021, month=9, day=1)

    markets = pub.get_markets()
    board = pub.get_board()
    ticker = pub.get_ticker()
    executions = pub.get_executions()
    broadest = pub.get_board_state()
    health = pub.get_health()
    leverage = pub.get_corporateleverage()
    chats = pub.get_chats(from_date)

    print("end")


if __name__ == '__main__':
    main()
