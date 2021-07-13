import json
import argparse


class Solution():
    def __init__(self, data) -> None:
        self.data = data # hashmap  with data
        self.answer = [] # will hold combination item prices which equal target
        self.target = 0 # will hold target price for current instance
        self.priceMap = {} # will hold hashmap(price -> name) for current data

    # parse json data and create
    # hash map with price of item -> name of item
    def parse_data(self):
        try:
            self.target = float(self.data['Target Price'][1:])
            priceMap = {}
            for item in self.data['Items']:
                price = float(item['Price'][1:])
                priceMap[price] = item['Name']
            self.priceMap = priceMap
            return 1
        except KeyError as e:
            print('Cannot find', e, 'in json file')
            return 0 
        except Exception as e:
            print(e)
            return 0

    # uses backtracking algorithm to find first occurence of
    # a combination with sum of prices equal to the target price
    def combination_sum(self, prices, curSum=0, partial=[]):
        # return when solution already found
        if self.answer:
            return

        # check if target is equal to the current sum
        # if so update self.answer and return
        if self.target == curSum:
            self.answer = partial
            return
        
        # return if current sum is greater than target
        if curSum > self.target:
            return

        # loop through other possible combinations
        for idx in range(len(prices)):
            price = prices[idx]
            remaining = prices[idx+1:]
            self.combination_sum(remaining, curSum+price, partial+[price])

    # find combination with sum equal to target
    def find_combination(self):
        self.combination_sum(list(self.priceMap.keys()))
        if self.answer:
            return 'Combination of dishes that has a total equal to the target price: ' + ', '.join([self.priceMap[key] for key in self.answer])
        return 'No combination of dishes is equal to the target price'


def main():
    # argument parser for file path
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file_path', type=str, default='input.json', help='path to json file')
    args = parser.parse_args()
    inputFile = args.file_path

    try:
        # open file and load json 
        f = open(inputFile)
        data = json.load(f)
    except IOError:
        print('Please input a valid file path')
        return
    except Exception as e:
        print('Following exception occured: ', e)
        return

    # create instance of solution class
    soltn = Solution(data)
    if (not soltn.parse_data()):
        # error in parsing json data
        return 

    # print result
    print(soltn.find_combination())

    # close file
    f.close()

if __name__ == "__main__":
    main()
