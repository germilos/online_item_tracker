import mongoengine as me


class Price(me.EmbeddedDocument):
    amount = me.DecimalField(required=True)
    currency = me.StringField(required=True)

    def __repr__(self):
        return f"{self.price!r} {self.currency!r})"

    def __str__(self):
        return f"{self.amount} {self.currency}"


class CurrentPrice:
    def __init__(self, amount, currency):
        self.amount = amount
        self.currency = currency

    def __repr__(self):
        return f"{self.price!r} {self.currency!r})"

    def __str__(self):
        return f"{self.amount} {self.currency}"