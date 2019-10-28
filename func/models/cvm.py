class CVM:
    stock: str = ""
    cvm_code: str = ""

    def __init__(self, stock: str, cvm_code: str):
        self.cvm_code = cvm_code
        self.stock = stock
        pass
    pass