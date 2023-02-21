import pandas as pd
from sheetyAPI import Destination, Subscriber
from tequilaAPI import FlightSearch

class PriceMatrix:
    def __init__(self, dest_obj:Destination, sub_obj:Subscriber):
        self.dest_obj = dest_obj
        self.sub_obj = sub_obj
        self.df = pd.read_csv('destination-origin matrix.csv', index_col="Origin/Destination")

        self.destinations = [row['iataCode'] for row in self.dest_obj.content]
        self.origins = [row['iataCode'] for row in self.sub_obj.content]

        self.routes = []

    def fill_matrix(self):
        """"""
        for destination in self.destinations:
            if destination not in self.df.columns.values:
                self.df[destination] = 500

        for origin in self.origins:
            if origin not in self.df.index.values:
                self.df.loc[origin] = [500 for item in self.df.columns.values]

        for column in self.df.columns.values:
            if column not in self.destinations:
                self.df.drop(columns=column, inplace=True)

        for row in self.df.index.values:
            if row not in self.origins:
                self.df.drop(index=row, inplace=True)

        self.df.to_csv('destination-origin matrix.csv')

    def generate_routes(self):
        for row in self.df.index.values:
            for column in self.df.columns.values:
                self.routes.append({'origin':row,
                                    'destination':column,
                                    'price':self.df.at[row, column]})

    def update_prices(self, catalog:dict):
        for key, value in catalog.items():
            lowest_price = min([item.price for item in value])
            print(f"Lowest price found for {key[0]} to {key[1]} is {lowest_price}")
            self.df.at[key[0], key[1]] = lowest_price
        for row in self.df.index.values:
            for column in self.df.columns.values:
                if (row, column) not in [(item[0], item[1]) for item in catalog.keys()]:
                    self.df.at[row, column] *= 1.05
                    self.df.at[row, column] = int(self.df.at[row, column])
        self.df.to_csv('destination-origin matrix.csv')









if __name__ == "__main__":
    my_destination = Destination()
    my_subscriptions = Subscriber()
    my_matrix = PriceMatrix(dest_obj=my_destination, sub_obj=my_subscriptions)
    my_matrix.fill_matrix()
    my_matrix.generate_routes()


    for route in my_matrix.routes:
        result = my_searcher.lookup_flights(origin=route['origin'], destination=route['destination'], lowest_price=route['price'], stopovers=1)
        print(result)
