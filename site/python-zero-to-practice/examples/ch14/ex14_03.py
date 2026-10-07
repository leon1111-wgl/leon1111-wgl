# 方法中的校验
class Wallet:
    def __init__(self):
        self.balance_fen = 0

    def deposit(self, amount_fen):
        if amount_fen < 0:
            raise ValueError("存入金额不能为负")
        self.balance_fen += amount_fen

wallet = Wallet()
wallet.deposit(1500)
print(wallet.balance_fen)
