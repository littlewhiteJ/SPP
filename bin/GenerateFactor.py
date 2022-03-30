from utils import *

class GenerateFactor():
    def __init__(self, config):
        self.config = config
        with open(self.config.stock_list_file, 'r') as f:
            self.stock_list = json.load(f)

    def filter_data_by_periods(self, lines, periods):
        lines = [[''.join(line[0].split('-'))] + line[1:] for line in lines]
        lines = [line for line in lines if any(1 for period in periods if line[0] >= period[0] and line[0] <= period[1])]
        return lines

    def generate_baostock(self, stock_list, train_period_list, test_period_list):
        train_period_list = [period.split('-') for period in train_period_list]
        test_period_list = [period.split('-') for period in test_period_list]

        # get years
        years = set()
        for timestamp in sum(train_period_list + test_period_list, []):
            years.add(timestamp[:4])
        
        # load data and normalize
        for stock in stock_list:
            train_data = []
            test_data = []

            for year in years:
                df = pd.read_csv(os.path.join(config.rawdata_home, stock + '_' + year + '.csv'), dtype=str)
                lines = df.values.tolist()
                train_lines = self.filter_data_by_periods(lines, train_period_list)
                test_lines = self.filter_data_by_periods(lines, test_period_list)
                train_data += train_lines
                test_data += test_lines

            # sort the data by the date
            train_data.sort(key=lambda x:x[0])
            test_data.sort(key=lambda x:x[0])

            # normalize fit train data and translate both
            train_data_date = [line[0] for line in train_data]
            train_data_body = np.array([line[1:] for line in train_data])
            test_data_date = [line[0] for line in test_data]
            test_data_body = np.array([line[1:] for line in test_data])

            scaler = MinMaxScaler()
            train_data_body = scaler.fit_transform(train_data_body).tolist()
            test_data_body = scaler.transform(test_data_body).tolist()

            train_data = [[date] + body for date, body in zip(train_data_date, train_data_body)]
            test_data = [[date] + body for date, body in zip(test_data_date, test_data_body)]

            '''
            print(stock)
            print(train_data[-3:])
            print(test_data[-3:])
            '''
            # store to factor_home
            with open(os.path.join(config.factor_home, stock + '_baostock_train.npy'), 'wb') as f:
                np.save(f, np.array(train_data))
            with open(os.path.join(config.factor_home, stock + '_baostock_test.npy'), 'wb') as f:
                np.save(f, np.array(test_data))
            
    def run(self):
        logging.info('start all factor generation')

        # check use_factor
        for u_factor in self.config.use_factor:
            if u_factor == 'baostock':
                self.generate_baostock(self.stock_list, self.config.train_period, self.config.test_period)
            else:
                # other data source
                pass
    
        logging.info('finish all factor generation')
        
if __name__ == '__main__':
    config = Config('/home/mokou/SPP/config/base_config.json')
    config.run()
    
    generate_factor = GenerateFactor(config)
    generate_factor.run()
