class film:
    def __init__(self, name='', company='', wk_money='', all_money='', cinema_count=0):
        self.name = name
        self.company = company
        self.wk_money = wk_money
        self.all_money = all_money
        self.cinema_count = cinema_count

    def __str__(self) -> str:
        return "<film>[name: {}, company: {}, wk_money: {}, all_money: {}, cinema_count: {}]".format(self.name,
                                                                                                     self.company,
                                                                                                     self.wk_money,
                                                                                                     self.all_money,
                                                                                                     self.cinema_count)

